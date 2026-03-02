import os
import json
import logging
from typing import List, Optional, Dict, Any, Annotated, Sequence
from typing_extensions import TypedDict

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from core.config_manager import config_manager

logger = logging.getLogger(__name__)


# --- LangGraph State Definition ---
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    is_verified: bool
    verification_feedback: Optional[str]


class AIManager:
    """
    Handles interactions with Google Gemini LLMs for analytical insights and NLQ.
    Implements Phase 3: Agentic Intelligence Layer with LangGraph.
    """

    def __init__(
        self, model_name: Optional[str] = None, temperature: Optional[float] = None
    ):
        llm_config = config_manager.get_llm_config()

        self.model_name = model_name or llm_config.get(
            "primary_model", "gemini-2.5-flash"
        )
        self.temperature = (
            temperature
            if temperature is not None
            else llm_config.get("default_temperature", 0.0)
        )
        self.fallback_model = llm_config.get("fallback_model", "gemini-2.5-flash-lite")

        self.api_key = os.environ.get("GEMINI_API_KEY")

        # Configure LangSmith Tracing
        os.environ["LANGSMITH_TRACING"] = "true"
        os.environ["LANGSMITH_PROJECT"] = "antigravity-stats-dashboard"

        try:
            self.llm = ChatGoogleGenerativeAI(
                model=self.model_name,
                google_api_key=self.api_key,
                temperature=self.temperature,
                convert_system_message_to_human=True,
            )
        except Exception as e:
            logger.error(f"Failed to initialize LLM with model {self.model_name}: {e}")
            self.llm = ChatGoogleGenerativeAI(
                model=self.fallback_model,
                google_api_key=self.api_key,
                temperature=self.temperature,
                convert_system_message_to_human=True,
            )

    def _patch_tool_schema(self, tool_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Strips 'additionalProperties' from tool schema for Gemini compatibility."""

        def clean_schema(s):
            if not isinstance(s, dict):
                return
            if "additionalProperties" in s:
                del s["additionalProperties"]
            for v in s.values():
                if isinstance(v, dict):
                    clean_schema(v)
                elif isinstance(v, list):
                    for item in v:
                        clean_schema(item)

        new_tool = json.loads(json.dumps(tool_dict))
        if "parameters" in new_tool:
            clean_schema(new_tool["parameters"])
        return new_tool

    def generate_insight(self, context: str, data_summary: str) -> str:
        """Generates a plain-language insight based on statistical results."""
        system_prompt = (
            "You are an expert data scientist at Antigravity Factory. "
            "Explain complex results clearly and concisely using Markdown."
        )
        user_prompt = f"Context: {context}\nResults:\n{data_summary}"

        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt),
            ]
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            logger.error(f"Error generating AI insight: {e}")
            return f"Error: {str(e)}"

    def nlq_to_action(self, query: str, context: Dict[str, Any]) -> Any:
        """
        Agentic entry point: Processes NLQ through a LangGraph reasoning loop with L0 Verification.
        """
        from core.tools import DATA_TOOLS
        from core.database import db_manager
        from core.data_manager import DataManager

        dm = DataManager()
        tools = DATA_TOOLS

        # Proper binding with schema patching for Gemini
        # We must bind the tools to the LLM. LangChain's bind_tools handles the conversion to OpenAI/Gemini format.
        # However, for Gemini we often need to ensure the schema is clean.
        self.llm_with_tools = self.llm.bind_tools(tools)

        def chatbot(state: AgentState):
            # The Analyst: Proposes insights and handles tool calls
            return {"messages": [self.llm_with_tools.invoke(state["messages"])]}

        def verifier(state: AgentState):
            """
            The Verifier: Cross-checks the Analyst's last response against tool outputs.
            Implements Axiom 0: Truth.
            """
            last_msg = state["messages"][-1].content
            # Find the most recent tool outputs to compare against
            tool_outputs = [
                m.content for m in state["messages"] if hasattr(m, "tool_call_id")
            ]

            verification_prompt = (
                "You are the L0 Verification Agent. Your ONLY job is to verify if the Analyst's "
                "claims match the raw tool outputs exactly. \n\n"
                f"Analyst Claim: {last_msg}\n\n"
                f"Raw Data Context: {' | '.join(tool_outputs[-2:] if tool_outputs else ['No tool data'])}\n\n"
                "If there is any discrepancy (even minor rounding), provide a correction and set 'verified' to false. "
                "If it matches perfectly, say 'VERIFIED' and set 'verified' to true."
            )

            # Ensure we wrap in HumanMessage as Gemini often requires it
            v_msg = [HumanMessage(content=verification_prompt)]
            v_res = self.llm.invoke(v_msg).content

            is_verified = "VERIFIED" in v_res.upper()

            if is_verified:
                return {
                    "is_verified": True,
                    "messages": [
                        SystemMessage(content="Verification passed: Axiom 0 confirmed.")
                    ],
                }
            else:
                return {
                    "is_verified": False,
                    "messages": [
                        SystemMessage(
                            content=f"Verification failed: {v_res}. Please correct your response based on the raw data."
                        )
                    ],
                }

        def verification_router(state: AgentState):
            if state.get("is_verified"):
                return END
            # Limit the refinement loops to prevent infinite cycles
            if len(state["messages"]) > 10:
                return END
            return "chatbot"

        workflow = StateGraph(AgentState)
        workflow.add_node("chatbot", chatbot)
        workflow.add_node("tools", ToolNode(tools))
        workflow.add_node("verifier", verifier)

        workflow.add_edge(START, "chatbot")
        workflow.add_conditional_edges("chatbot", tools_condition)
        workflow.add_edge("tools", "chatbot")

        # After the chatbot responds without a tool call, send to verifier
        workflow.add_conditional_edges(
            "chatbot",
            lambda x: "verifier" if not tools_condition(x) == "tools" else "tools",
        )

        # Verifier decision
        workflow.add_conditional_edges("verifier", verification_router)

        app = workflow.compile()

        # Add system context
        system_msg = SystemMessage(
            content=(
                "You are the Antigravity AI Assistant. You have access to the project's datasets. "
                f"Current Context: {json.dumps(context)}. "
                "Use tools to answer user questions about data accurately."
            )
        )

        initial_state = {
            "messages": [system_msg, HumanMessage(content=query)],
            "is_verified": False,
        }
        result = app.invoke(initial_state)

        # We want to return the last message from the chatbot (the Analyst),
        # but only if the Verifier eventually passed or we timed out.
        # result["messages"] contains the conversation.
        # The list of messages looks like: [System, Human, AI(Chatbot), Tool, AI(Chatbot), System(Verifier Outcome)]

        # Find the last message from the Analyst (the "chatbot" node)
        # Note: result["messages"] is a list of all messages.
        for msg in reversed(result["messages"]):
            if isinstance(msg, (BaseMessage)) and not isinstance(msg, SystemMessage):
                content = msg.content
                break
        else:
            content = result["messages"][-1].content

        if isinstance(content, list):
            # Extract text from content parts for Gemini/LangChain compatibility
            text_parts = [
                part.get("text", "") if isinstance(part, dict) else str(part)
                for part in content
                if not isinstance(part, dict) or part.get("type") == "text"
            ]
            return "\n".join(text_parts)
        return content
