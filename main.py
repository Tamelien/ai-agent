import os
import sys
import argparse

from enum import Enum
from dotenv import load_dotenv

from google import genai
from google.genai import types

import functions.call_function as function
from prompt import system_prompt 
from config import MAX_ITERATIONS

class FLAG(Enum):
    VERBOSE = "--verbose"

def parse_args(argv=None):
    parser = argparse.ArgumentParser()

    parser.add_argument("prompt", help="User prompt")
    parser.add_argument(FLAG.VERBOSE.value, action="store_true", help="Verbose output")
    return parser.parse_args(argv)

def main():
    load_dotenv()

    args = parse_args()
    prompt = args.prompt
    
    if not prompt:
        print("No prompt was entered.")
        sys.exit(1)
    
   
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if args.verbose:  
        print(f"User prompt: {prompt}")
       
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    for _ in range(MAX_ITERATIONS):
        try:
            response = generate_content(client, messages, args.verbose)   
        except Exception as e:
            if args.verbose:
               print(f"Error: {e}")
            break
       
        finished = (not getattr(response, "function_calls", None) and bool(getattr(response, "text", "")))
        print(finished)
        if finished:
            print("Final response:")
            print(response.text)
            break
    
def generate_content(client, messages, verbose):   

    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents= messages,
        config=types.GenerateContentConfig(tools=[function.available_functions],
                                           system_instruction=system_prompt),
    )    

    if (hasattr(response, "candidates") and response.candidates):
        for candidate in response.candidates:
            messages.append(candidate.content)   

    function_responses = []
    tool_parts = []
    if response.function_calls:
        for function_call_part in response.function_calls:
            function_call_result = function.call_function(function_call_part, verbose)
            print(function_call_result)
            if (not hasattr(function_call_result, "parts")
                or not function_call_result.parts
                or not hasattr(function_call_result.parts[0], "function_response")
                or not hasattr(function_call_result.parts[0].function_response, "response")):
                raise RuntimeError
            if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}") # type: ignore
                    um = getattr(response, "usage_metadata", None)
                    prompt_tokens = getattr(um, "prompt_token_count", "N/A") if um else "N/A"
                    response_tokens = getattr(um, "candidates_token_count", "N/A") if um else "N/A"

                    print(f"Prompt tokens: {prompt_tokens}")
                    print(f"Response tokens: {response_tokens}")

            function_responses.append(function_call_result.parts[0].function_response.response) # type: ignore
                    
            for fr in function_responses:
                tool_parts.append(
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response=fr,
                    )
                )

        messages.append(types.Content(role="user", parts = tool_parts))
    
    
    return response
    
    

if __name__ == "__main__":
    main()
