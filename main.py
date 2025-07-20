import os, sys
from dotenv import load_dotenv
from google.genai import Client, types

from prompts import system_prompt
from functions.call_function import available_functions, call_function
from config import MAX_AI_ITERS

def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if args.count == 0:
        print("My AI Code Assistant")
        print("Error: No prompt provided")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How would I add exponention operation to my calculator?"')
        sys.exit(1)

    
    api_key = os.environ.get("GEMINI_API_KEY")
    client = Client(api_key=api_key)

    user_prompt = sys.argv[1]
    
    if verbose:
        print(f"User prompt: {user_prompt}\n")
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    for i in range(MAX_AI_ITERS):
        try:
            response = generate_content(client, messages, verbose)
            if response:
                print("Final response:")
                print(response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")

        if i == MAX_AI_ITERS-1:
            print(f"Maximum iterations ({MAX_AI_ITERS}) reached, exiting!")
            sys.exit(1)

      

def generate_content(client: Client, messages: list, verbose:bool):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions]
        ),
    )
    
    for resp_candidate in response.candidates:
        messages.append(resp_candidate.content)

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if not response.function_calls:
        return response.text
    
    function_responses = []
    for function_call_part in response.function_calls:
        call_result = call_function(function_call_part, verbose)
        messages.append(types.Content(role="tool", parts=call_result.parts))

        if (
            not call_result.parts
            or not call_result.parts[0].function_response.response
        ):
            raise Exception(f"Error: No function call result'")
        elif verbose:
            print(f"-> {call_result.parts[0].function_response.response}")
        function_responses.append(call_result.parts[0])

    if not function_responses:
        raise Exception("No function responses generated, exiting.")

if __name__ == "__main__":
    main()
