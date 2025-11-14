import os

def get_files_info(working_directory, directory="."):
    
    abs_path_base = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(abs_path_base, directory))

    if not (target_path.startswith(abs_path_base + os.sep) or target_path == abs_path_base):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(target_path):
        return f'Error: "{directory}" is not a directory'

    try:            
        list_dir = os.listdir(target_path)
        
        content_dir = ""
        for item in list_dir:
            full_path = os.path.abspath(os.path.join(target_path, item))
            is_dir = os.path.isdir(full_path)
            size = os.path.getsize(full_path)
            content_dir += f"- {item}: file_size={size} bytes, is_dir={is_dir}\n"
    
        return content_dir
    
    except Exception as e:
        return f"Error: {e}"
    

    
