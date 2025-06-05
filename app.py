import gradio as gr
import asyncio
import os
from agent_workflow import workflow
import traceback

async def run_influencer_analysis(channel_name, target_cpm, currency):
    """
    Run the influencer marketing analysis workflow
    """
    try:
        # Construct the query
        query = f"Calculate the recommended price for '{channel_name}' YouTube channel to achieve a target CPM of {target_cpm} {currency}, based on their recent video views."
        
        # Run the workflow
        handler = workflow.run(user_msg=query)
        response = await handler
        
        # Extract the final content
        if hasattr(response, "response"):
            if hasattr(response.response, "content"):
                final_content = response.response.content
            else:
                final_content = str(response.response)
        elif hasattr(response, "content"):
            final_content = response.content
        else:
            final_content = str(response)
        
        # Clean up the response to remove any "assistant:" prefix
        if final_content.startswith("assistant:"):
            final_content = final_content[10:].strip()
        
        return final_content
        
    except Exception as e:
        error_msg = f"An error occurred during analysis: {str(e)}\n\nFull traceback:\n{traceback.format_exc()}"
        return error_msg

def analyze_influencer(channel_name, target_cpm, currency):
    """
    Wrapper function to run async workflow in Gradio
    """
    if not channel_name.strip():
        return "Please enter a YouTube channel name or URL."
    
    if not target_cpm or target_cpm <= 0:
        return "Please enter a valid target CPM value."
    
    # Run the async function
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(run_influencer_analysis(channel_name, target_cpm, currency))
        return result
    finally:
        loop.close()

# Create the Gradio interface
def create_interface():
    # Custom CSS for modern, clean typography
    custom_css = """
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    }
    
    .gradio-container {
        font-family: 'Inter', sans-serif !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em !important;
    }
    
    .gr-button {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        letter-spacing: 0.01em !important;
    }
    
    .gr-textbox, .gr-dropdown, .gr-number {
        font-family: 'Inter', sans-serif !important;
        font-weight: 400 !important;
    }
    
    label {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
    }
    
    .markdown {
        font-family: 'Inter', sans-serif !important;
        line-height: 1.6 !important;
    }
    
    #result_markdown {
        background-color: #f8fafc !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        padding: 16px !important;
        margin-top: 8px !important;
        min-height: 300px !important;
        color: #1e293b !important;
    }
    
    #result_markdown * {
        color: #1e293b !important;
    }
    
    #result_markdown h1, #result_markdown h2, #result_markdown h3, #result_markdown h4 {
        color: #0f172a !important;
        margin-top: 1em !important;
        margin-bottom: 0.5em !important;
        font-weight: 600 !important;
    }
    
    #result_markdown strong {
        color: #0f172a !important;
        font-weight: 600 !important;
        background-color: #e0e7ff !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
    }
    
    #result_markdown ul, #result_markdown ol {
        margin-left: 1.5em !important;
        margin-bottom: 1em !important;
        color: #374151 !important;
    }
    
    #result_markdown li {
        margin-bottom: 0.5em !important;
        color: #374151 !important;
    }
    
    #result_markdown p {
        color: #374151 !important;
        line-height: 1.6 !important;
        margin-bottom: 1em !important;
    }
    
    #result_markdown code {
        background-color: #f1f5f9 !important;
        color: #475569 !important;
        padding: 2px 4px !important;
        border-radius: 3px !important;
        font-family: 'Courier New', monospace !important;
    }
    """
    
    with gr.Blocks(
        title="ValuatorAI - Influencer Marketing Price Calculator", 
        theme=gr.themes.Soft(),
        css=custom_css
    ) as demo:
        gr.Markdown("""
        # 🎯 ValuatorAI - Influencer Marketing Price Calculator
        
        Calculate the recommended price for YouTube influencer collaborations based on their recent video performance and your target CPM.
        """)
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("## 📊 Input Parameters")
                
                channel_name = gr.Textbox(
                    label="YouTube Channel Name or URL",
                    placeholder="Enter channel name (e.g., 'Matthew Berman') or YouTube URL",
                    value="Matthew Berman"
                )
                
                with gr.Row():
                    target_cpm = gr.Number(
                        label="Target CPM",
                        value=25,
                        minimum=0.1,
                        step=0.1,
                        info="Cost per thousand impressions you want to achieve"
                    )
                    
                    currency = gr.Dropdown(
                        label="Currency",
                        choices=["EUR", "USD", "GBP", "CAD", "AUD"],
                        value="EUR"
                    )
                
                analyze_btn = gr.Button("🔍 Analyze Channel", variant="primary", size="lg")
            
            with gr.Column():
                gr.Markdown("## 📈 Analysis Results")
                
                result_output = gr.Markdown(
                    value="Results will appear here after analysis...",
                    elem_id="result_markdown"
                )
        
        # Example section
        with gr.Accordion("💡 How it works", open=False):
            gr.Markdown("""
            ### The Analysis Process:
            
            1. **Video Data Collection**: Fetches recent video statistics from the specified YouTube channel
            2. **Performance Analysis**: Calculates median view counts to get a representative performance metric
            3. **Price Calculation**: Uses the formula: `(Target CPM ÷ 1000) × Median Views = Recommended Price`
            4. **Professional Recommendation**: Provides a detailed explanation of the pricing strategy
            
            ### Example Channels to Try:
            - Matthew Berman
            - Marques Brownlee
            - Peter McKinnon
            - MrBeast
            
            ### Tips:
            - Higher CPM targets result in higher recommended prices
            - The calculation is based on recent video performance
            - Consider seasonal variations and content type when setting your CPM target
            """)
        
        # Event handlers
        analyze_btn.click(
            fn=analyze_influencer,
            inputs=[channel_name, target_cpm, currency],
            outputs=[result_output],
            show_progress=True
        )
        
        # Allow Enter key to trigger analysis
        channel_name.submit(
            fn=analyze_influencer,
            inputs=[channel_name, target_cpm, currency],
            outputs=[result_output],
            show_progress=True
        )
    
    return demo

if __name__ == "__main__":
    # Check if required environment variables are set
    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️  Warning: GOOGLE_API_KEY environment variable not set!")
        print("Please set your Google API key in the .env file")
    
    demo = create_interface()
    
    print("🚀 Starting ValuatorAI Interface...")
    print("📊 This tool calculates influencer marketing prices based on YouTube channel performance")
    
    # Launch the interface
    demo.launch(
        server_name="0.0.0.0",  # Allow external connections
        server_port=7860,       # Default Gradio port
        share=False,            # Set to True if you want a public link
        show_error=True
    )