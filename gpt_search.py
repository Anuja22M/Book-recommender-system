from openai import OpenAI
import os

def get_book_recommendations(prompt, api_key=None, model="Llama-4-Maverick-17B-128E-Instruct"):
    """
    Get book recommendations based on a user prompt.
    
    Parameters:
    - prompt: User's request for book recommendations
    - api_key: OpenAI API key (if None, will try to get from environment)
    - model: Model to use for recommendations
    
    Returns:
    - Tuple of (recommendations_text, error_message)
    """
    # Initialize the client with API key from argument or environment variable
    client = OpenAI(
        api_key=api_key or os.getenv("SAMBANOVA_API_KEY"),
        base_url=os.getenv("SAMBANOVA_BASE_URL")
    )
    
    # Add specific instruction to the prompt to ensure proper formatting
    enhanced_prompt = f"""
    {prompt}
    
    Please provide a well-formatted list of book recommendations with the following information:
    1. Book titles
    2. Authors
    3. Genres
    """
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a knowledgeable literary assistant specializing in book recommendations."},
                {"role": "user", "content": enhanced_prompt}
            ],
            temperature=0.7  # Balanced between creativity and consistency
        )
        
        return response.choices[0].message.content, None
        
    except Exception as e:
        return None, f"Error getting recommendations: {str(e)}"

# This allows the file to be imported in other files while also being runnable directly
if __name__ == "__main__":
    # Simple command-line interface for testing
    import argparse
    
    parser = argparse.ArgumentParser(description="Get book recommendations from AI")
    parser.add_argument("prompt", nargs="?", default=None, help="Your request for book recommendations")
    parser.add_argument("--api-key", default=None, help="OpenAI API key (optional if set as environment variable)")
    parser.add_argument("--model", default="gpt-3.5-turbo", help="Model to use (default: gpt-3.5-turbo)")
    
    args = parser.parse_args()
    
    # If no prompt provided as argument, ask for it
    if not args.prompt:
        args.prompt = input("Enter your book recommendation request: ")
    
    recommendations, error = get_book_recommendations(args.prompt, args.api_key, args.model)
    
    if error:
        print(f"Error: {error}")
    else:
        print("\n" + "="*80 + "\n")
        print(recommendations)
        print("\n" + "="*80 + "\n")