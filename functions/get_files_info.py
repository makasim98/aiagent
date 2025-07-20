import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    cwd = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(cwd, directory))

    if not full_path.startswith(cwd):
        return(f'Error: Cannot list "{directory}" as it is outside the permitted working directory') 
    if os.path.isfile(full_path):
        return f'Error: "{directory}" is not a directory'    

    result = []

    try:
        dir = os.listdir(full_path)
        for item in dir:
            path = os.path.join(full_path, item)
            is_dir = os.path.isdir(path)
            file_size = os.path.getsize(path)
            result.append(f" - {item}: file_size={file_size} bytes, is_dir={is_dir}")
    except Exception as e:
        return f"Error: {e}"

    return "\n".join(result)


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself."
            ),
        },
    ),
)