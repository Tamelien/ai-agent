import os
import sys
from dotenv import load_dotenv
from google import genai



def main():

    load_dotenv()

    args = sys.argv[1:]
    
    if not args:
        print("No prompt was entered.")
        sys.exit(1)
    
    prompt = " ".join(args)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents= prompt
    )  
    print(response.text)
    print(f"Prompt tokens: {getattr(response.usage_metadata, "prompt_token_count", "N/A")}")
    print(f"Response tokens: {getattr(response.usage_metadata, "candidates_token_count","N/A")}")

if __name__ == "__main__":
    main()
