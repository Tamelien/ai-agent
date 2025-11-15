import os
import sys
import argparse

from enum import Enum
from dotenv import load_dotenv

from google import genai
from google.genai import types

import functions.available_functions as function

class FLAG(Enum):
    VERBOSE = "--verbose"

def parse_args(argv=None):
    parser = argparse.ArgumentParser()

    parser.add_argument("prompt", help="User prompt")
    parser.add_argument(FLAG.VERBOSE.value, action="store_true", help="Verbose output")
    return parser.parse_args(argv)

def main():

    load_dotenv()

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    args = parse_args()
    prompt = args.prompt
    
   
    if not prompt:
        print("No prompt was entered.")
        sys.exit(1)
    
    messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]
        
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents= messages,
        config=types.GenerateContentConfig(tools=[function.available_functions],
                                           system_instruction=system_prompt),
    )
       
    if args.verbose:
        um = getattr(response, "usage_metadata", None)
        prompt_tokens = getattr(um, "prompt_token_count", "N/A") if um else "N/A"
        response_tokens = getattr(um, "candidates_token_count", "N/A") if um else "N/A"

        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

    if response.function_calls:
        for function_call_part in response.function_calls:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(response.text)

if __name__ == "__main__":
    main()
