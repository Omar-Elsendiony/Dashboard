from anthropic import Anthropic
import os


def get_claude_client():
    """Initialize and return Claude client"""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")
    return Anthropic(api_key=api_key)

# Helper function to call Claude
def call_claude(prompt, model="claude-3-5-sonnet-20241022", max_tokens=4000, temperature=0.1):
    """
    Call Claude API with the given prompt
    
    Args:
        prompt (str): The prompt to send to Claude
        model (str): Claude model to use (default: claude-3-5-sonnet-20241022)
        max_tokens (int): Maximum tokens to generate
        temperature (float): Temperature for response generation
    
    Returns:
        str: Claude's response content
    """
    client = get_claude_client()
    
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.content[0].text
