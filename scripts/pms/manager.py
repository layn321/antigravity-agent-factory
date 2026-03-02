import os
import sys
import subprocess
import argparse
import json
from datetime import datetime

# Correct environment path as per user rules
CONDA_EXEC = r"conda run -p D:\Anaconda\envs\cursor-factory"

import base64


def safe_django_repr(val):
    """Safe representation for Django ORM strings to prevent escaping hell."""
    if val is None:
        return "None"
    # Use json.dumps to get a clean string, then escape for use in f-strings if needed
    return json.dumps(val)


def run_django_command(command: str):
    """Execute a command in the plane-api container using manage.py shell."""
    # Base64 encode the command to avoid shell character issues (<, >, quotes, etc.)
    encoded_cmd = base64.b64encode(command.encode()).decode()
    # Use a raw string or careful wrapping for the docker command
    docker_cmd = f"docker exec plane-api python manage.py shell -c \"import base64; exec(base64.b64decode('{encoded_cmd}').decode())\""

    try:
        result = subprocess.run(docker_cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            stderr = result.stderr.strip()
            stdout = result.stdout.strip()
            raise Exception(
                f"Plane API (Django) error:\nSTDOUT: {stdout}\nSTDERR: {stderr}"
            )
        return result.stdout.strip()
    except Exception as e:
        print(f"Error executing Django command: {e}")
        return f"ERROR: {str(e)}"


def list_issues(
    project_id: str = None,
    state_name: str = None,
    cycle_name: str = None,
    module_name: str = None,
    assignee_email: str = None,
    label_name: str = None,
    search_query: str = None,
    as_json: bool = False,
):
    logic = [
        "from plane.db.models import Issue, Project",
        "p = Project.objects.get(identifier='AGENT')",
        "filters = {'project': p}",
    ]
    if state_name:
        logic.append(f"filters['state__name'] = '{state_name}'")
    if cycle_name:
        logic.append(f"filters['issue_cycle__cycle__name'] = '{cycle_name}'")
    if module_name:
        logic.append(f"filters['issue_module__module__name'] = '{module_name}'")
    if assignee_email:
        logic.append(f"filters['issue_assignee__assignee__email'] = '{assignee_email}'")
    if label_name:
        logic.append(f"filters['label_issue__label__name__iexact'] = '{label_name}'")
    if search_query:
        logic.append("from django.db.models import Q")
        logic.append(
            f"qs = Issue.objects.filter(Q(name__icontains='{search_query}') | Q(description_html__icontains='{search_query}'), **filters)"
        )
    else:
        logic.append("qs = Issue.objects.filter(**filters)")

    logic.append(
        "qs = qs.values('sequence_id', 'name', 'priority', 'state__name').distinct().order_by('-sequence_id')"
    )
    logic.append("print(list(qs))")
    cmd = "\n".join(logic)
    output = run_django_command(cmd)
    if as_json:
        print(output)
    else:
        print(f"Project Issues: \n{output}")


def fast_list_issues(state_name: str = None):
    """Retrieves projects, cycles, modules, and issues in a single batch, optionally filtering by state."""
    logic = [
        "from plane.db.models import Issue, Project, State, Cycle, Module",
        "import json",
        "p = Project.objects.get(identifier='AGENT')",
        "filters = {'project': p}",
    ]
    if state_name:
        logic.append(f"filters['state__name'] = '{state_name}'")
    else:
        # Default to unstarted issues if no specific state provided
        logic.append("filters['state__group'] = 'unstarted'")

    logic.extend(
        [
            "data = {",
            "  'project': {'name': p.name, 'identifier': p.identifier},",
            "  'states': list(State.objects.filter(project=p).values('name', 'group')),",
            "  'cycles': list(Cycle.objects.filter(project=p).values('name', 'id')),",
            "  'modules': list(Module.objects.filter(project=p).values('name', 'id')),",
            "  'filtered_issues': list(Issue.objects.filter(**filters).values('sequence_id', 'name', 'priority', 'state__name'))",
            "}",
            "print('START_JSON')",
            "print(json.dumps(data, default=str))",
            "print('END_JSON')",
        ]
    )
    cmd = "\n".join(logic)
    output = run_django_command(cmd)
    if "START_JSON" in output and "END_JSON" in output:
        json_part = output.split("START_JSON\n")[-1].split("\nEND_JSON")[0]
        parsed = json.loads(json_part)
        print(json.dumps(parsed, indent=2))
    else:
        print(output)


def list_modules(as_json: bool = False):
    cmd = "from plane.db.models import Module, Project; p = Project.objects.get(identifier='AGENT'); print(list(Module.objects.filter(project=p).values('name', 'id')))"
    output = run_django_command(cmd)
    if as_json:
        print(output)
    else:
        print(f"Modules: \n{output}")


def list_projects(as_json: bool = False):
    cmd = "from plane.db.models import Project; print(list(Project.objects.values('name', 'identifier')))"
    output = run_django_command(cmd)
    if as_json:
        print(output)
    else:
        print(f"Projects: \n{output}")


def get_issue_details(sequence_id: str, as_json: bool = False):
    seq_num = sequence_id.split("-")[-1]
    logic = [
        "from plane.db.models import Issue, Project",
        "from django.apps import apps",
        "import json",
        "p = Project.objects.get(identifier='AGENT')",
        f"issue = Issue.objects.get(project=p, sequence_id={seq_num})",
        "CI = apps.get_model('db', 'CycleIssue')",
        "MI = apps.get_model('db', 'ModuleIssue')",
        "ci = CI.objects.filter(issue=issue).first()",
        "mi = MI.objects.filter(issue=issue).first()",
        "data = {",
        "    'id': str(issue.id),",
        "    'sequence_id': issue.sequence_id,",
        "    'name': issue.name,",
        "    'desc': issue.description_html,",
        "    'priority': issue.priority,",
        "    'state': issue.state.name,",
        "    'assignees': list(issue.issue_assignee.values_list('assignee__email', flat=True)),",
        "    'labels': list(issue.label_issue.values_list('label__name', flat=True)),",
        "    'cycle': ci.cycle.name if ci else None,",
        "    'module': mi.module.name if mi else None,",
        "    'start_date': str(issue.start_date) if issue.start_date else None,",
        "    'target_date': str(issue.target_date) if issue.target_date else None,",
        "    'estimate': issue.estimate_point.value if issue.estimate_point else None,",
        "    'comments': list(issue.issue_comments.values('comment_html', 'created_at', 'actor__email'))",
        "}",
        "print('START_JSON')",
        "print(json.dumps(data, default=str))",
        "print('END_JSON')",
    ]
    cmd = "\n".join(logic)
    output = run_django_command(cmd)
    if "START_JSON" in output and "END_JSON" in output:
        json_part = output.split("START_JSON\n")[-1].split("\nEND_JSON")[0]
        if as_json:
            print(json_part)
        else:
            try:
                data = json.loads(json_part)
                print(
                    f"================ AGENT-{data.get('sequence_id')} ================"
                )
                print(f"Title:    {data.get('name')}")
                print(f"Priority: {data.get('priority')}")
                print(f"State:    {data.get('state')}")
                print(f"Assignee: {', '.join(data.get('assignees', [])) or 'None'}")
                print(f"Labels:   {', '.join(data.get('labels', [])) or 'None'}")
                print(f"Cycle:    {data.get('cycle') or 'None'}")
                print(f"Module:   {data.get('module') or 'None'}")
                print(
                    f"Dates:    {data.get('start_date') or 'N/A'} -> {data.get('target_date') or 'N/A'}"
                )
                print(f"Estimate: {data.get('estimate') or 'None'}")
                print(f"\nDescription:\n{data.get('desc', '')}")
                print("\nComments:")
                for c in data.get("comments", []):
                    # Clean up HTML for display if possible, or just print
                    print(
                        f"- [{c.get('created_at')}] {c.get('actor__email')}: {c.get('comment_html')}"
                    )
                print("==============================================")
            except Exception as e:
                print(f"Failed to parse details: {e}")
                print(output)
    else:
        print(output)


def list_cycles():
    cmd = (
        "from plane.db.models import Cycle, Project; "
        "p = Project.objects.get(identifier='AGENT'); "
        "qs = Cycle.objects.filter(project=p).values('name', 'id', 'start_date', 'end_date', 'description'); "
        "print(list(qs))"
    )
    output = run_django_command(cmd)
    print(f"Project Cycles: \n{output}")


def list_states():
    cmd = (
        "from plane.db.models import State, Project; "
        "p = Project.objects.get(identifier='AGENT'); "
        "qs = State.objects.filter(project=p).values('name', 'group'); "
        "print(list(qs))"
    )
    output = run_django_command(cmd)
    print(f"Project States: \n{output}")


def create_label(name: str, color: str = "#3498db"):
    """Create a new label in the project."""
    logic = [
        "from plane.db.models import Label, Project",
        "p = Project.objects.get(identifier='AGENT')",
        f"Label.objects.create(name='{name}', color='{color}', project=p, workspace=p.workspace)",
        f"print(f'Created Label: {name}')",
    ]
    cmd = "\n".join(logic)
    output = run_django_command(cmd)
    print(output)


# Governance: Restricted Label Set
ALLOWED_LABELS = {
    "FEATURE",
    "BUG",
    "DOCU",
    "CORE",
    "TEST",
    "UI",
    "DATA",
    "ORCHESTRATION",
    "GROUNDING",
    "INTEGRATION",
    "INFRA",
    "SKILL",
}


def validate_labels(labels, force=False):
    """Normalize labels to uppercase and validate against whitelist."""
    if not labels:
        return []
    normalized = [l.upper() for l in labels]
    if not force:
        invalid = [l for l in normalized if l not in ALLOWED_LABELS]
        if invalid:
            raise ValueError(
                f"Invalid labels: {invalid}. Allowed set: {sorted(list(ALLOWED_LABELS))}. Use --force to override."
            )
    return normalized


def create_issue(
    name: str,
    description: str = "",
    priority: str = "medium",
    state_name: str = "Todo",
    cycle_name: str = None,
    module_name: str = None,
    assignee_email: str = None,
    start_date: str = None,
    target_date: str = None,
    estimate: int = None,
    labels: list = None,
    force: bool = False,
    issue_type: str = None,
    use_template: bool = False,
    description_file: str = None,
):
    """Create a new issue in Plane with a check for duplicates and standardization."""
    # Load description from file if provided
    if description_file:
        try:
            with open(description_file, "r", encoding="utf-8") as f:
                description = f.read()
        except Exception as e:
            print(f"Error reading description file: {e}")
            return

    # Apply standard prefixes if type is provided
    if issue_type:
        issue_type = issue_type.upper()
        if not name.startswith(issue_type + ":"):
            name = f"{issue_type}: {name}"

    # Apply template if requested and no description provided
    if use_template and not description:
        description = (
            "# Goal\n"
            "Provide a concise summary of the problem and desired outcome.\n\n"
            "# Acceptance Criteria\n"
            "- [ ] Criterion 1 (Functional requirement)\n"
            "- [ ] Criterion 2 (Validation step)\n\n"
            "# Technical Context\n"
            "- **Implementation Details**: Notes on architecture or tools.\n"
            "- **Dependencies**: Linked issues or PRs."
        )

    # Validate and normalize labels
    try:
        labels = validate_labels(labels, force=force)
    except ValueError as e:
        print(f"ERROR: {e}")
        return

    # Check for duplicates first
    safe_name_check = name.replace("'", "\\'")
    check_logic = [
        "from plane.db.models import Issue, Project",
        "p = Project.objects.get(identifier='AGENT')",
        f"exists = Issue.objects.filter(project=p, name__iexact={safe_django_repr(name)}, state__group__in=['backlog', 'unstarted', 'started']).exists()",
        "print('DUPLICATE_FOUND' if exists else 'CLEAN')",
    ]
    check_cmd = "\n".join(check_logic)
    check_output = run_django_command(check_cmd)

    if "DUPLICATE_FOUND" in check_output and not force:
        print(
            f'Error: An active issue with the name "{name}" already exists. Use --force to override.'
        )
        return

    logic = [
        "from plane.db.models import Issue, Project, State, Cycle, Module, ProjectMember, Label, EstimatePoint",
        "from django.utils import timezone",
        "p = Project.objects.get(identifier='AGENT')",
        f"s = State.objects.get(project=p, name={safe_django_repr(state_name)})",
    ]
    safe_name = safe_django_repr(name)
    safe_desc = safe_django_repr("<div>" + description + "</div>")

    create_args = [
        "project=p",
        "workspace=p.workspace",
        f"name={safe_name}",
        f"description_html={safe_desc}",
        f"priority='{priority}'",
        "state=s",
    ]

    if start_date:
        logic.append(
            f"start = timezone.datetime.strptime('{start_date}', '%Y-%m-%d').date()"
        )
        create_args.append("start_date=start")
    if target_date:
        logic.append(
            f"target = timezone.datetime.strptime('{target_date}', '%Y-%m-%d').date()"
        )
        create_args.append("target_date=target")

    if estimate is not None:
        logic.append(
            f"ep = EstimatePoint.objects.filter(estimate__project=p, value={estimate}).first()"
        )
        create_args.append("estimate_point=ep")

    logic.append(f"issue = Issue.objects.create({', '.join(create_args)})")

    if assignee_email:
        logic.append(
            f"member = ProjectMember.objects.get(project=p, member__email='{assignee_email}')"
        )
        logic.append(
            "issue.issue_assignee.create(assignee=member.member, project=p, workspace=p.workspace)"
        )

    if labels:
        for label_name in labels:
            logic.append(
                f"l, created = Label.objects.get_or_create(project=p, name__iexact='{label_name}', defaults={{'name': '{label_name}', 'workspace': p.workspace}})"
            )
            logic.append("if created:")
            logic.append(f"    print(f'Created missing label: {label_name}')")
            logic.append(
                "issue.label_issue.create(label=l, project=p, workspace=p.workspace)"
            )

    if cycle_name:
        logic.append(f"c = Cycle.objects.get(project=p, name='{cycle_name}')")
        logic.append(
            "from django.apps import apps; CI = apps.get_model('db', 'CycleIssue')"
        )
        logic.append(
            "CI.objects.create(issue=issue, cycle=c, project=p, workspace=p.workspace)"
        )

    if module_name:
        logic.append(f"m = Module.objects.get(project=p, name='{module_name}')")
        logic.append(
            "from django.apps import apps; MI = apps.get_model('db', 'ModuleIssue')"
        )
        logic.append(
            "MI.objects.create(issue=issue, module=m, project=p, workspace=p.workspace)"
        )

    logic.append("print(f'Created Issue: AGENT-{issue.sequence_id}')")

    cmd = "\n".join(logic)
    output = run_django_command(cmd)
    print(output)


def update_issue(
    sequence_id: str,
    state_name: str = None,
    description: str = None,
    priority: str = None,
    name: str = None,
    cycle_name: str = None,
    module_name: str = None,
    labels: list = None,
    append: bool = False,
    description_file: str = None,
    issue_type: str = None,
    start_date: str = None,
    target_date: str = None,
    estimate: int = None,
    force: bool = False,
):
    """Update an existing issue, optionally reading description from a file."""
    # Load description from file if provided
    if description_file:
        try:
            with open(description_file, "r", encoding="utf-8") as f:
                description = f.read()
        except Exception as e:
            print(f"Error reading description file: {e}")
            return

    seq_num = sequence_id.split("-")[-1]

    logic = [
        "from plane.db.models import Issue, Project, State, Cycle, Module, Label, EstimatePoint",
        "from django.utils import timezone",
        "p = Project.objects.get(identifier='AGENT')",
        f"issue = Issue.objects.get(project=p, sequence_id={seq_num})",
    ]

    # Apply standard prefixes if type is provided
    if issue_type:
        issue_type = issue_type.upper()
        if not name:
            # We need the current name to prefix it
            # But we can also just set a new name if provided
            pass
        elif not name.startswith(issue_type + ":"):
            name = f"{issue_type}: {name}"

    if state_name:
        logic.append(
            f"s = State.objects.get(project=p, name={safe_django_repr(state_name)})"
        )
        logic.append("issue.state = s")
    if description:
        if append:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            separator = "<hr/>"
            if not (description.startswith("<") and description.endswith(">")):
                new_part = f"<div><b>Update ({timestamp}):</b><br/>{description}</div>"
            else:
                new_part = f"<div><b>Update ({timestamp}):</b></div>{description}"

            logic.append("current_desc = issue.description_html or ''")
            logic.append(
                f"if current_desc and not current_desc.endswith('{separator}'):"
            )
            logic.append(f"    current_desc += '{separator}'")
            logic.append(
                f"issue.description_html = current_desc + {safe_django_repr(new_part)}"
            )
        else:
            final_desc = description
            if not (description.startswith("<") and description.endswith(">")):
                final_desc = f"<div>{description}</div>"
            logic.append(f"issue.description_html = {safe_django_repr(final_desc)}")
    if priority:
        logic.append(f"issue.priority = '{priority}'")
    if name:
        logic.append(f"issue.name = {safe_django_repr(name)}")

    if start_date:
        logic.append(
            f"issue.start_date = timezone.datetime.strptime('{start_date}', '%Y-%m-%d').date()"
        )
    if target_date:
        logic.append(
            f"issue.target_date = timezone.datetime.strptime('{target_date}', '%Y-%m-%d').date()"
        )
    if estimate is not None:
        logic.append(
            f"ep = EstimatePoint.objects.get(estimate__project=p, value={estimate})"
        )
        logic.append("issue.estimate_point = ep")

    logic.append("issue.save()")

    if cycle_name:
        logic.append(f"c = Cycle.objects.get(project=p, name='{cycle_name}')")
        logic.append(
            "from django.apps import apps; CI = apps.get_model('db', 'CycleIssue')"
        )
        logic.append("CI.objects.filter(issue=issue).delete()")
        logic.append(
            "CI.objects.create(issue=issue, cycle=c, project=p, workspace=p.workspace)"
        )

    if module_name:
        logic.append(f"m = Module.objects.get(project=p, name='{module_name}')")
        logic.append(
            "from django.apps import apps; MI = apps.get_model('db', 'ModuleIssue')"
        )
        logic.append("MI.objects.filter(issue=issue).delete()")
        logic.append(
            "MI.objects.create(issue=issue, module=m, project=p, workspace=p.workspace)"
        )

    # Validate and normalize labels
    if labels:
        try:
            labels = validate_labels(labels, force=force)
        except ValueError as e:
            print(f"ERROR: {e}")
            return

    if labels:
        logic.append("issue.label_issue.all().delete()")
        for label_name in labels:
            logic.append(
                f"l, created = Label.objects.get_or_create(project=p, name='{label_name}', defaults={{'name': '{label_name}', 'workspace': p.workspace}})"
            )
            logic.append("if created:")
            logic.append(f"    print(f'Created missing label: {label_name}')")
            logic.append("from plane.db.models import IssueLabel")
            logic.append(
                "IssueLabel.objects.create(issue=issue, label=l, project=p, workspace=p.workspace)"
            )

    logic.append(f"print(f'Updated Issue: AGENT-{seq_num}')")

    cmd = "\n".join(logic)
    output = run_django_command(cmd)
    print(output)


def create_comment(sequence_id: str, comment: str):
    if not comment.strip():
        print("Error: Comment cannot be empty.")
        return

    # Extract number from AGENT-5
    seq_num = sequence_id.split("-")[-1]

    logic = [
        "from plane.db.models import Issue, Project, IssueComment",
        "p = Project.objects.get(identifier='AGENT')",
        f"issue = Issue.objects.get(project=p, sequence_id={seq_num})",
    ]

    # Wrap in consistent HTML if not already
    if not (comment.strip().startswith("<") and comment.strip().endswith(">")):
        safe_comment = repr(f"<div>{comment.strip()}</div>")
    else:
        safe_comment = repr(comment.strip())

    # Use the project owner/workspace owner as the creator if possible
    logic.append("user = p.workspace.owner")
    logic.append(
        f"IssueComment.objects.create(issue=issue, project=p, workspace=p.workspace, "
        f"comment_html={safe_comment}, created_by=user, actor=user)"
    )
    logic.append(f"print(f'Added comment to Issue: AGENT-{seq_num}')")

    cmd = "\n".join(logic)
    output = run_django_command(cmd)
    print(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Native Plane PMS Manager")
    subparsers = parser.add_subparsers(dest="command")

    # List
    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--project-id", help="Project ID filter")
    list_parser.add_argument(
        "--state", help="Filter by state name (e.g., Todo, Backlog)"
    )
    list_parser.add_argument("--cycle", help="Filter by cycle/sprint name")
    list_parser.add_argument("--module", help="Filter by module name")
    list_parser.add_argument("--assignee", help="Filter by assignee email")
    list_parser.add_argument("--label", help="Filter by label name")
    list_parser.add_argument("--query", help="Text search in title and description")
    list_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Details
    details_parser = subparsers.add_parser("details", aliases=["get"])
    details_parser.add_argument("id", help="Issue ID (e.g., AGENT-1 or simply 1)")
    details_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Cycles
    subparsers.add_parser("cycles")

    # States
    subparsers.add_parser("states")

    # Modules
    modules_parser = subparsers.add_parser("modules")
    modules_parser.add_argument("--json", action="store_true")

    # Create
    create_parser = subparsers.add_parser("create")
    create_parser.add_argument("--name", required=True)
    create_parser.add_argument("--description", default="")
    create_parser.add_argument("--priority", default="medium")
    create_parser.add_argument("--state", default="Todo")
    create_parser.add_argument("--cycle", help="Cycle/Sprint name")
    create_parser.add_argument("--module", help="Module name")
    create_parser.add_argument("--assignee", help="Assignee email")
    create_parser.add_argument("--start-date", help="YYYY-MM-DD")
    create_parser.add_argument("--target-date", help="YYYY-MM-DD")
    create_parser.add_argument("--estimate", type=int, help="Estimate value")
    create_parser.add_argument("--labels", nargs="+", help="Space-separated labels")
    create_parser.add_argument(
        "--force", action="store_true", help="Force creation even if duplicate exists"
    )
    create_parser.add_argument(
        "--type",
        dest="issue_type",
        choices=["FEATURE", "FIX", "DOCS", "TASK", "PLAN", "REF", "BUG", "OPT"],
        help="Standard title prefix",
    )
    create_parser.add_argument(
        "--template", action="store_true", help="Use standard description boilerplate"
    )
    create_parser.add_argument(
        "--file", dest="description_file", help="Read description from this file path"
    )

    # Metadata lists
    members_parser = subparsers.add_parser("members")
    members_parser.add_argument("--json", action="store_true")
    labels_parser = subparsers.add_parser("labels")
    labels_parser.add_argument("--json", action="store_true")

    # Update
    update_parser = subparsers.add_parser("update")
    update_parser.add_argument(
        "id", help="Issue identifier (e.g., AGENT-5 or simply 5)"
    )
    update_parser.add_argument("--state", help="New state for the issue")
    update_parser.add_argument(
        "--description", help="New HTML description or text for the issue"
    )
    update_parser.add_argument(
        "--append", action="store_true", help="Append to existing description"
    )
    update_parser.add_argument("--priority", help="New priority for the issue")
    update_parser.add_argument("--name", help="New name for the issue")
    update_parser.add_argument("--cycle", help="New cycle/sprint name")
    update_parser.add_argument("--module", help="New module name")
    update_parser.add_argument("--labels", nargs="+", help="New space-separated labels")
    update_parser.add_argument(
        "--file", dest="description_file", help="Read description from this file path"
    )
    update_parser.add_argument(
        "--type", dest="issue_type", help="Standardized issue type (e.g., FEATURE, BUG)"
    )
    update_parser.add_argument("--start_date", help="Start date (YYYY-MM-DD)")
    update_parser.add_argument("--target_date", help="Target date (YYYY-MM-DD)")
    update_parser.add_argument("--estimate", type=int, help="Estimate points (integer)")
    update_parser.add_argument(
        "--force", action="store_true", help="Force skipping validation checks"
    )

    # Comment
    comment_parser = subparsers.add_parser("comment")
    comment_parser.add_argument(
        "id", help="Issue identifier (e.g., AGENT-5 or simply 5)"
    )
    comment_parser.add_argument("--comment", required=True, help="Comment text or HTML")

    # Projects
    projects_parser = subparsers.add_parser("projects")
    projects_parser.add_argument("--json", action="store_true")

    # Create Label
    label_create_parser = subparsers.add_parser("create-label")
    label_create_parser.add_argument("--name", required=True)
    label_create_parser.add_argument("--color", default="#3498db")

    # Fast List
    fast_list_parser = subparsers.add_parser("fast-list")
    fast_list_parser.add_argument("--state", help="Filter issues by state name")

    # Run Django
    django_parser = subparsers.add_parser("run_django")
    django_parser.add_argument("logic", help="Django ORM logic to run")

    args = parser.parse_args()

    try:
        if args.command == "list":
            list_issues(
                args.project_id,
                args.state,
                args.cycle,
                args.module,
                args.assignee,
                args.label,
                args.query,
                args.json,
            )
        elif args.command == "projects":
            list_projects(args.json)
        elif args.command == "modules":
            list_modules(args.json)
        elif args.command == "members":
            output = run_django_command(
                "from plane.db.models import ProjectMember, Project; p = Project.objects.get(identifier='AGENT'); print(list(ProjectMember.objects.filter(project=p).values('member__email', 'member__first_name', 'member__last_name')))"
            )
            if args.json:
                print(output)
            else:
                print(f"Project Members: \n{output}")
        elif args.command == "labels":
            output = run_django_command(
                "from plane.db.models import Label, Project; p = Project.objects.get(identifier='AGENT'); print(list(Label.objects.filter(project=p).values('name', 'id')))"
            )
            if args.json:
                print(output)
            else:
                print(f"Project Labels: \n{output}")
        elif args.command in ["details", "get"]:
            get_issue_details(args.id, getattr(args, "json", False))
        elif args.command == "cycles":
            list_cycles()
        elif args.command == "states":
            list_states()
        elif args.command == "create":
            create_issue(
                args.name,
                args.description,
                args.priority,
                args.state,
                args.cycle,
                args.module,
                args.assignee,
                args.start_date,
                args.target_date,
                args.estimate,
                args.labels,
                args.force,
                args.issue_type,
                args.template,
                args.description_file,
            )
        elif args.command == "update":
            update_issue(
                args.id,
                args.state,
                args.description,
                args.priority,
                args.name,
                args.cycle,
                args.module,
                args.labels,
                args.append,
                args.description_file,
                args.issue_type,
                args.start_date,
                args.target_date,
                args.estimate,
            )
        elif args.command == "comment":
            create_comment(args.id, args.comment)
        elif args.command == "create-label":
            create_label(args.name, args.color)
        elif args.command == "fast-list":
            fast_list_issues(args.state)
        elif args.command == "details" or args.command == "get":
            get_issue_details(args.id, args.json)
        elif args.command == "run_django":
            print(run_django_command(args.logic))
        else:
            parser.print_help()
    except Exception as e:
        print(f"Error: {e}")
