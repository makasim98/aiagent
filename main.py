import os, sys
from dotenv import load_dotenv
from google.genai import Client, types

from prompts import system_prompt
from functions.call_function import available_functions, call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    clien = Client(api_key=api_key)

    if len(sys.argv) < 2:
        print("No prompt privided")
        sys.exit(1)

    user_prompt = sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    response = clien.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions]
        ),

    )

    is_verbose = "--verbose" in sys.argv
    if is_verbose:
        print(f"User prompt: {user_prompt}")

    print(response.text)
    
    for call in response.function_calls:
        call_result = call_function(call, is_verbose)

        if not call_result.parts[0].function_response.response:
            raise Exception(f"Error: A fatal error occured when calling '{call.name}' with arguments '{call.args}'")
        elif is_verbose:
            print(f"-> {call_result.parts[0].function_response.response}")

    if is_verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
