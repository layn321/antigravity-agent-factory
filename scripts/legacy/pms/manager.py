#!/usr/bin/env python3
\"\"\"
Plane Management System (PMS) Manager — Legacy CLI for Local Docker Instance.

This is the original manager script maintained for historical compatibility and
for environments still running the local 12-container Plane Docker stack.
\"\"\"
import argparse
import os
import sys
import json
import requests
import uuid
import subprocess
from datetime import datetime

# --- Configuration ---
API_BASE = os.environ.get(\"PLANE_API_BASE\", \"http://localhost:8000/api/v1\")
WORKSPACE_SLUG = os.environ.get(\"PLANE_WORKSPACE\", \"antigravity\")
PROJECT_ID = os.environ.get(\"PLANE_PROJECT_ID\")
API_KEY = os.environ.get(\"PLANE_API_TOKEN\")

def list_issues():
    url = f\"{API_BASE}/workspaces/{WORKSPACE_SLUG}/projects/{PROJECT_ID}/work-items/\"
    headers = {\"x-api-key\": API_KEY}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        issues = resp.json()
        for issue in issues:
            print(f\"[{issue.get('sequence_id')}] {issue.get('name')} ({issue.get('state')})\")
    else:
        print(f\"Error: {resp.status_code}\")

def list_states():
    url = f\"{API_BASE}/workspaces/{WORKSPACE_SLUG}/projects/{PROJECT_ID}/states/\"
    headers = {\"x-api-key\": API_KEY}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        states = resp.json()
        for state in states:
            print(f\"{state.get('name')}: {state.get('id')}\")

def create_issue(name, description, priority, state, cycle=None, module=None, assignee=None, start_date=None, target_date=None, estimate=None, labels=None):
    url = f\"{API_BASE}/workspaces/{WORKSPACE_SLUG}/projects/{PROJECT_ID}/work-items/\"
    headers = {\"x-api-key\": API_KEY, \"Content-Type\": \"application/json\"}
    payload = {
        \"name\": name,
        \"description_html\": description,
        \"priority\": priority,
        \"state\": state,
    }
    if cycle: payload[\"cycle\"] = cycle
    if module: payload[\"module\"] = module
    if assignee: payload[\"assignees\"] = [assignee]
    if start_date: payload[\"start_date\"] = start_date
    if target_date: payload[\"target_date\"] = target_date
    if estimate: payload[\"estimate_point\"] = estimate
    if labels: payload[\"labels\"] = labels

    resp = requests.post(url, headers=headers, json=payload)
    if resp.status_code in (200, 201):
        print(f\"Created: {resp.json().get('sequence_id')}\")
    else:
        print(f\"Error: {resp.status_code} - {resp.text}\")

def update_issue(issue_id, state=None, description=None, priority=None, name=None, append=False):
    url = f\"{API_BASE}/workspaces/{WORKSPACE_SLUG}/projects/{PROJECT_ID}/work-items/{issue_id}/\"
    headers = {\"x-api-key\": API_KEY, \"Content-Type\": \"application/json\"}

    payload = {}
    if state: payload[\"state\"] = state
    if description: payload[\"description_html\"] = description
    if priority: payload[\"priority\"] = priority
    if name: payload[\"name\"] = name

    resp = requests.patch(url, headers=headers, json=payload)
    if resp.status_code == 200:
        print(f\"Updated: {issue_id}\")
    else:
        print(f\"Error: {resp.status_code}\")

def create_comment(issue_id, comment):
    url = f\"{API_BASE}/workspaces/{WORKSPACE_SLUG}/projects/{PROJECT_ID}/work-items/{issue_id}/comments/\"
    headers = {\"x-api-key\": API_KEY, \"Content-Type\": \"application/json\"}
    payload = {\"comment_html\": f\"<div>{comment}</div>\"}
    resp = requests.post(url, headers=headers, json=payload)
    if resp.status_code in (200, 201):
        print(f\"Commented on: {issue_id}\")

def run_django_command(logic):
    # This remains for local Docker legacy support
    cmd = f\"docker exec -it plane-api python manage.py shell -c \\\"{logic}\\\"\"
    return os.popen(cmd).read()

if __name__ == \"__main__\":
    parser = argparse.ArgumentParser(description=\"PMS Legacy Manager\")
    subparsers = parser.add_subparsers(dest=\"command\")

    subparsers.add_parser(\"list\")
    subparsers.add_parser(\"states\")

    create_p = subparsers.add_parser(\"create\")
    create_p.add_argument(\"--name\", required=True)
    create_p.add_argument(\"--description\", default=\"\")
    create_p.add_argument(\"--priority\", default=\"medium\")
    create_p.add_argument(\"--state\", required=True)
    create_p.add_argument(\"--cycle\")
    create_p.add_argument(\"--module\")
    create_p.add_argument(\"--assignee\")
    create_p.add_argument(\"--start-date\")
    create_p.add_argument(\"--target-date\")
    create_p.add_argument(\"--estimate\")
    create_p.add_argument(\"--labels\", nargs=\"*\")

    update_p = subparsers.add_parser(\"update\")
    update_p.add_argument(\"--id\", required=True)
    update_p.add_argument(\"--state\")
    update_p.add_argument(\"--description\")
    update_p.add_argument(\"--priority\")
    update_p.add_argument(\"--name\")
    update_p.add_argument(\"--append\", action=\"store_true\")

    comment_p = subparsers.add_parser(\"comment\")
    comment_p.add_argument(\"--id\", required=True)
    comment_p.add_argument(\"--comment\", required=True)

    django_p = subparsers.add_parser(\"run_django\")
    django_p.add_argument(\"--logic\", required=True)

    args = parser.parse_args()

    if not API_KEY:
        print(\"Error: PLANE_API_TOKEN not set.\")
        sys.exit(1)

    try:
        if args.command == \"list\":
            list_issues()
        elif args.command == \"states\":
            list_states()
        elif args.command == \"create\":
            create_issue(...) # Simplified for legacy documentation purposes
        elif args.command == \"update\":
            update_issue(...) # Simplified
        elif args.command == \"comment\":
            create_comment(args.id, args.comment)
        elif args.command == \"run_django\":
            print(run_django_command(args.logic))
        else:
            parser.print_help()
    except Exception as e:
        print(f\"Error: {e}\")
