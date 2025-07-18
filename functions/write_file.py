import os

def write_file(working_directory, file_path, content):
    cwd = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(cwd, file_path))

    if not abs_file_path.startswith(cwd):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        target_dir = os.path.dirname(abs_file_path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        with open(abs_file_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
    