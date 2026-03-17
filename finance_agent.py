from textwrap import dedent
from agno.agent import Agent
from agno.run.agent import RunOutput
from agno.models.google import Gemini

def generate_financial_plan(gemini_api_key: str, financial_goals: str, current_situation: str) -> str:
    planner = Agent(
        name="Planner",
        role="Generates a personalized financial plan based on user preferences",
        model=Gemini(id="gemini-2.5-flash", api_key=gemini_api_key),
        description=dedent(
            """\
        You are a senior financial planner. Given a user's financial goals and current financial situation,
        your goal is to generate a personalized financial plan that meets the user's needs and preferences.
        """
        ),
        instructions=[
            "Given a user's financial goals and current financial situation, generate a personalized financial plan that includes suggested budgets, investment plans, and savings strategies.",
            "Ensure the plan is well-structured and informative.",
            "Ensure you provide a nuanced and balanced plan.",
            "CRITICAL: The output MUST be formatted as a single, comprehensive Markdown table. Use columns such as Category, Strategy/Action, Estimated Amount/Percentage, and Timeline/Notes.",
            "Do NOT include any paragraphs of text outside the table. The entire response should be the Markdown table.",
            "Never make up facts or plagiarize."
        ],
        add_datetime_to_context=True,
    )

    # Run the planner with the gathered context
    planner_prompt = f"Financial goals: {financial_goals}\nCurrent situation: {current_situation}"
    plan: RunOutput = planner.run(planner_prompt, stream=False)
    
    return plan.content
