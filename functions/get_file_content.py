import os
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