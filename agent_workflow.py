import os
import statistics
import math
import io
import json
import asyncio
from contextlib import redirect_stdout
from src.tools.youtube_api import fetch_video_statistics, resolve_channel_id

from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core.agent.workflow import FunctionAgent, AgentWorkflow
from llama_index.core.tools import FunctionTool
from dotenv import load_dotenv

load_dotenv()


llm = GoogleGenAI(model="gemini-2.0-flash-lite", api_key=os.getenv("GOOGLE_API_KEY"), temperature=0)


# --- Custom Python Execution Tool ---
def execute_python_code(code_string: str) -> str:
    """
    Executes a given string of Python code and returns its stdout.
    The code should use print() for the output you want to capture.
    Available modules: statistics, math, json.
    Example: print(statistics.median([1, 2, 3, 4, 5]))
    Args:
        code_string (str): The Python code string to execute.
    """
    allowed_globals = {
        "statistics": statistics,
        "math": math,
        "json": json,
        "__builtins__": __builtins__,
    }
    output_buffer = io.StringIO()
    try:
        with redirect_stdout(output_buffer):
            exec(code_string, allowed_globals, {})
        return output_buffer.getvalue().strip()
    except Exception as e:
        return f"Error executing Python code: {e}\nCode: {code_string}"


python_tool = FunctionTool.from_defaults(
    fn=execute_python_code,
    name="python_code_executor",
    description="Executes a provided string of Python code and returns the result from stdout. Use this for calculations like median, averages, or specific formulas. Ensure your code string includes print() statements for the desired output.",
)

# --- Agent Definitions ---

# Agent 1: Video Statistics Specialist
video_statistics_specialist = FunctionAgent(
    name="VideoStatisticsSpecialist",
    description="Analyzes engagement statistics for recent videos on a YouTube channel by fetching data.",
    system_prompt="""You are a Video Statistics Specialist. Your task is to gather data about a YouTube channel.
    1. Given a channel name or URL, use the `resolve_channel_id` tool to get the official YouTube Channel ID.
    2. Then, using the Channel ID, use the `fetch_video_statistics` tool to get statistics (views, likes, comments, favorites) for its recent videos.
    3. Extract the view counts from the statistics and present them clearly in your response.
    4. Once you have the view counts, hand off control to the PythonScriptExecutor to calculate the median.
    
    Your response should include the view counts in a clear format like: "View counts: [123, 456, 789]" """,
    llm=llm,
    tools=[
        fetch_video_statistics,
        resolve_channel_id,
    ],
    can_handoff_to=["PythonScriptExecutor"],
)

# Agent 2: Python Script Executor
# Takes raw data and performs calculations
python_script_executor = FunctionAgent(
    name="PythonScriptExecutor",
    description="Executes Python scripts for calculations on provided data.",
    system_prompt="""You are a Python Script Executor. Your role is to perform calculations on data provided from the previous agent.
    1. Look for view counts data in the previous agent's response.
    2. Extract the numerical view counts from the data.
    3. Generate Python code to calculate the median of the view counts using the statistics module.
    4. Use the 'python_code_executor' tool to execute this Python script.
    5. Present the median result clearly and hand off control to the MetricsCalculator.
    
    Make sure your Python code uses print() to output the result clearly.
    Example: "view_counts = [123, 456, 789]; import statistics; print(f'Median view count: {statistics.median(view_counts)}')" """,
    llm=llm,
    tools=[python_tool],
    can_handoff_to=["MetricsCalculator"],
)

# Agent 3: Metrics Calculator
# Takes calculated data and marketing goals to calculate final metrics
metrics_calculator = FunctionAgent(
    name="MetricsCalculator",
    description="Calculates influencer marketing metrics using provided data and parameters.",
    system_prompt="""You are an Influencer Marketing Metrics Calculator and advisor. This is the final step in the workflow.
    1. Extract the median view count from the previous agent's response.
    2. Extract the target CPM from the original user request (e.g., "25 EUR").
    3. Generate Python code to calculate the recommended price using the formula: (Target CPM / 1000) * Median Views.
    4. Use the 'python_code_executor' tool to execute the calculation.
    5. After getting the calculation results, provide a natural language response explaining the recommendation.
    
    Your response should be conversational and informative, explaining:
    - The recommended price for the influencer collaboration
    - The basis for this calculation (median views and target CPM)
    - A brief summary of the key metrics
    
    Example Python code for calculation:
    ```python
    median_views = [extracted_number]
    target_cpm = 25
    price = (target_cpm / 1000) * median_views
    print(f"Recommended Price: {round(price, 2)}")
    print(f"Median Views: {median_views}")
    print(f"Target CPM: {target_cpm}")
    ```
    
    After executing the calculation, format your response like a professional marketing consultant providing advice to a client.""",
    llm=llm,
    tools=[python_tool],
)


# --- AgentWorkflow Setup ---
workflow = AgentWorkflow(
    agents=[video_statistics_specialist, python_script_executor, metrics_calculator],
    root_agent="VideoStatisticsSpecialist",
    verbose=True,
)


# --- Workflow Execution ---
async def main():
    initial_query = "Calculate the recommended price for 'Matthew Berman' YouTube channel to achieve a target CPM of 25 EUR, based on their recent video views."
    print(f'Running workflow with initial query: "{initial_query}"\n')

    try:
        # Run the workflow
        handler = workflow.run(user_msg=initial_query)

        # Get the final result
        response = await handler

        if hasattr(response, "response"):
            if hasattr(response.response, "content"):
                final_content = response.response.content
            else:
                final_content = str(response.response)
        elif hasattr(response, "content"):
            final_content = response.content
        else:
            final_content = str(response)

        print(f"Final content: {final_content}")
    except Exception as e:
        print(f"\n--- An error occurred during workflow execution ---")
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
