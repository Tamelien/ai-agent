from google.genai import types
from enum import Enum
from functions.get_file_content import schema_get_file_content
from functions.get_file_content import get_file_content
from functions.get_files_info import schema_get_files_info
from functions.get_files_info import get_files_info
from functions.write_file import schema_write_file
from functions.write_file import write_file
from functions.run_python_file import schema_run_python_file
from functions.run_python_file import run_python_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
)

DISPATCH = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

def call_function(function_call_part, verbose=False):

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

   
    

    if not function_call_part.name in DISPATCH:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    func = DISPATCH[function_call_part.name]
    function_call_part.args["working_directory"] = "./calculator"

    try:
        function_result = func(**function_call_part.args)

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": function_result},
                )
            ],
        )


    except Exception as e:
       return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {e}"},
                )
            ],
        )
