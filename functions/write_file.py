import os
from google.genai import types

def write_file(working_directory, file_path, content):
    cwd = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(cwd, file_path))

    if not abs_file_path.startswith(cwd):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        target_dir = os.path.dirname(abs_file_path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)

        with open(abs_file_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=f"Writes content to a file within the working directory. Creates the file if it doesn't exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be writtent to the file."                
            )
        },
        required=["file_path", "content"],
    ),
)