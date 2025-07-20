import os
from google.genai import types
from config import MAX_READ_CHARS

def get_file_content(working_directory, file_path):
    cwd = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(cwd, file_path))

    if not abs_file_path.startswith(cwd):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(abs_file_path, "r") as f:
            file_content_str = f.read(MAX_READ_CHARS)
            if os.path.getsize(abs_file_path) > MAX_READ_CHARS:
                  file_content_str += f"[...File \"{file_path}\" truncated at 10000 characters]"
            return file_content_str

    except Exception as e:
        return f"Error: {e}"
    

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first {MAX_READ_CHARS} characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory."
            ),
        },
        required=["file_path"],
    ),
)