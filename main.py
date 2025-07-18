import os, sys
from dotenv import load_dotenv
from google.genai import Client, types


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    cliend = Client(api_key=api_key)

    if len(sys.argv) < 2:
        print("No prompt privided")
        sys.exit(1)

    user_prompt = sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    response = cliend.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
    )
    if "--verbose" in sys.argv:
        print(f"User prompt: {user_prompt}")

    print(response.text)

    if "--verbose" in sys.argv:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
