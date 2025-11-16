import os
from google.genai import types
from functions.config import MAX_CHARS
 

def get_file_content(working_directory, file_path):

    base_path = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(base_path, file_path))

    if not (target_path.startswith(base_path + os.sep) or target_path == base_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:

        with open(target_path,"r", encoding="utf-8", errors="replace") as f:
            file_content_string = f.read(MAX_CHARS)
            extra = f.read(1)
        
        if extra:
            file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'
    
    except Exception as e:
        return f"Error: {e}"

    return file_content_string 

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Read the file and return its contents limited to {MAX_CHARS} characters, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to read the file from, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)