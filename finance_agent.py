from textwrap import dedent
from agno.agent import Agent
from agno.run.agent import RunOutput
from agno.models.google import Gemini
from agno.models.openai import OpenAIChat
from agno.models.groq import Groq

def generate_financial_plan(provider: str, api_key: str, financial_goals: str, current_situation: str) -> str:
    if provider.lower() == "gemini":
        model = Gemini(id="gemini-1.5-flash", api_key=api_key)
    elif provider.lower() == "openai":
        model = OpenAIChat(id="gpt-4o", api_key=api_key)
    elif provider.lower() == "groq":
        model = Groq(id="llama-3.3-70b-specdec", api_key=api_key)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

    planner = Agent(
        model=model,
        instructions=[
            "Generate a personalized financial plan with suggested budgets and investment strategies.",
            "CRITICAL: The output MUST be ONLY a single Markdown table (Category, Strategy, Amount, Timeline).",
            "Do NOT include any text outside the table.",
            "Keep the plan concise to ensure fast generation."
        ],
    )

    # Run the planner with the gathered context
    planner_prompt = f"Financial goals: {financial_goals}\nCurrent situation: {current_situation}"
    plan: RunOutput = planner.run(planner_prompt, stream=False)
    
    return plan.content
