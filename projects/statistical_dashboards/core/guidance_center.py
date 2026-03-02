import pandas as pd


class GuidanceCenter:
    """
    Centralized repository for help content, KPI definitions, and statistical education.
    Implements Requirement R1.
    """

    @staticmethod
    def get_kpi_dictionary():
        """Returns a list of core KPIs with definitions, formulas, and recommendations."""
        return [
            {
                "KPI": "UPH (Units Per Hour)",
                "Domain": "Warehouse",
                "Definition": "Items processed per associate-hour.",
                "Formula": "Total Units / Total Active Hours",
                "Recommendation": "Use Bar charts for site comparison, Line charts for shift trends.",
                "Target": "> 80",
            },
            {
                "KPI": "LSR (Late Shipment Rate)",
                "Domain": "Logistics",
                "Definition": "Percentage of orders missed.",
                "Formula": "(Late / Total) * 100",
                "Recommendation": "Use Gauge charts for real-time tracking, Pie charts for root cause analysis.",
                "Target": "< 4.0%",
            },
            {
                "KPI": "IRA (Inventory Record Accuracy)",
                "Domain": "Warehouse",
                "Definition": "Accuracy of physical vs system counts.",
                "Formula": "(Matches / Total Counts) * 100",
                "Recommendation": "Use Scatter plots for bin-level precision, Area charts for long-term health.",
                "Target": "> 99.8%",
            },
        ]

    @staticmethod
    def get_statistical_primer():
        """Returns introductory explanations for AI/ML concepts used in the dashboard."""
        return {
            "Linear Regression": {
                "Title": "Finding Relationships",
                "Explanation": "Linear regression tries to draw a straight line through your data to predict one value based on another. For example, 'If I increase shelf height by 1 foot, how much does stow speed decrease?'",
                "Key Metric": "R-Squared (0 to 1): Close to 1 means the line fits the data very well. Below 0.3 means the relationship is weak.",
            },
            "K-Means Clustering": {
                "Title": "Grouping Like Items",
                "Explanation": "Clustering looks at your data and finds 'natural' groups based on similarities. It's like sorting a bowl of mixed fruit into piles of apples, oranges, and bananas without being told what they are.",
                "Use Case": "Identifying different types of customers or high-risk inventory zones.",
            },
            "Hypothesis Testing (T-Test)": {
                "Title": "Is the Difference Real?",
                "Explanation": "A T-Test checks if the difference between two groups (e.g., Team A vs Team B) is likely due to chance or if it's statistically significant.",
                "Key Metric": "P-Value: If it's less than 0.05, there's a 95% chance the difference is real and not just luck.",
            },
        }

    @staticmethod
    def get_dashboard_blueprints():
        """Returns structured layouts for different analysis types."""
        return {
            "Warehouse Efficiency": [
                "1. Metrics Row: UPH, D2S, ASN Accuracy",
                "2. Trend Chart: Hourly UPH throughout the shift",
                "3. Regression: Shelf Height vs Process Time",
                "4. Anomaly Table: Top 5 outliers in productivity",
            ],
            "Financial Health": [
                "1. Metrics Row: Cash on Hand, Burn Rate, Runway",
                "2. Line Chart: Revenue vs Expenses (6 months)",
                "3. Correlation Heatmap: Marketing Spend vs New Leads",
                "4. Forecast: Predictive 3-month cash flow",
            ],
        }

    @staticmethod
    def get_data_import_guide():
        """Returns detailed column and formatting requirements for different data domains."""
        return {
            "Warehouse (Operational)": {
                "Required Columns": [
                    {
                        "Name": "timestamp",
                        "Format": "YYYY-MM-DD HH:MM",
                        "Required": True,
                    },
                    {"Name": "associate_id", "Format": "String", "Required": True},
                    {
                        "Name": "process_type",
                        "Format": "Pick|Stow|Pack",
                        "Required": True,
                    },
                    {"Name": "units", "Format": "Integer", "Required": True},
                    {"Name": "location_id", "Format": "String", "Required": False},
                ],
                "Value Formatting": "Use 24-hour clock for timestamps. Units must be positive integers.",
                "SOP Reference": "/warehouse-associate",
            },
            "Inventory Accuracy": {
                "Required Columns": [
                    {"Name": "sku", "Format": "String", "Required": True},
                    {"Name": "expected_qty", "Format": "Integer", "Required": True},
                    {"Name": "counted_qty", "Format": "Integer", "Required": True},
                    {"Name": "bin_id", "Format": "String", "Required": True},
                ],
                "Value Formatting": "Ensure SKUs match the master catalog. Bin IDs should follow site-standard nomenclature.",
                "SOP Reference": "/warehouse-inventory",
            },
            "Financial (Core)": {
                "Required Columns": [
                    {"Name": "date", "Format": "YYYY-MM-DD", "Required": True},
                    {"Name": "account", "Format": "String", "Required": True},
                    {"Name": "amount", "Format": "Decimal", "Required": True},
                    {"Name": "currency", "Format": "ISO Code", "Required": True},
                    {"Name": "category", "Format": "Revenue|Expense", "Required": True},
                ],
                "Value Formatting": "Amounts: positive for credits, negative for debits.",
                "SOP Reference": "/fi-development",
            },
        }

    @staticmethod
    def generate_csv_template(domain: str) -> str:
        """Generates a CSV header string for the specified domain."""
        guides = GuidanceCenter.get_data_import_guide()
        guide = guides.get(domain)
        if not guide:
            return ""

        headers = [col["Name"] for col in guide["Required Columns"]]
        return ",".join(headers) + "\n"

    @staticmethod
    def get_system_architecture():
        """Returns the mermaid diagram and description for the agent ecosystem."""
        return {
            "title": "Antigravity Hyper-Fidelity Architecture",
            "description": "Multi-view C4 architectural model covering System Context (L1), Container Boundaries (L2), and Execution Sequence (L3).",
            "mermaid": """
graph TD
    %% 1. SYSTEM CONTEXT (L1)
    subgraph L1_Context ["L1: System Context"]
        User["Developer/Analyst"] -->|Directs| Factory["Antigravity Agent Factory"]
        Factory -->|Integrated Documentation| Wiki["DeepWiki / GitHub"]
        Factory -->|Task Management| Plane["Plane PMS (Docker Stack)"]
        Factory -->|Knowledge Base| Qdrant["Qdrant RAG (Vector Data)"]
    end

    %% 2. CONTAINER BOUNDARIES (L2)
    subgraph L2_Containers ["L2: Container Diagram"]
        subgraph Local_Env ["Client Host"]
            Conda["Conda: cursor-factory"]
            VS_Agent["VS Code Agentic UI"]
        end

        subgraph Core_Services ["Dockerized Infrastructure"]
            subgraph Plane_PMS ["Plane Stack"]
                P_API["plane-api (Django)"]
                P_DB["plane-db (Postgres)"]
            end

            subgraph RAG_Infra ["RAG Stack"]
                Q_Vectors["Qdrant Core"]
                P_Docs["Parent Store (Disk)"]
            end
        end

        subgraph Orchestration ["Factory Brain"]
            MSO["Master Orchestrator"]
            Specialists["Specialist Agents (PAIS/WQSS/KM)"]
        end
    end

    %% 3. EXECUTION SEQUENCE (L3 - Abstracted)
    subgraph L3_Sequence ["L3: Core Execution Path"]
        S_PAIS["Specialist"] -->|"1. search_library()"| RAG_API["RAG Bridge"]
        RAG_API -->|"2. vector_query"| Q_Vectors
        RAG_API -->|"3. context_hydration"| P_Docs
        S_PAIS -->|"4. run_command()"| P_API
    end

    %% Cross-Layer Links
    VS_Agent --> Conda
    Conda --> MSO
    MSO --> Specialists
    Specialists --> RAG_API
    Specialists --> P_API
""",
        }
