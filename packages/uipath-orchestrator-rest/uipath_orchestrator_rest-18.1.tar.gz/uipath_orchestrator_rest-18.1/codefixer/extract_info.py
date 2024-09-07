import re

ruffoutput_path = "codefixer/ruff_output.txt"  # Modify this with the actual file path

searchpattern_ruff = r"(.*):(\d+):(\d+): (.*)"
searchpattern_code = r"'{([a-zA-z]+)}'"
replacepattern_code = r"\\'{\1}\\'"
# Open the file for reading
with open(ruffoutput_path, "r") as file:
    lines = file.readlines() 
    for line in lines[:-1]:
        error_message = line.strip()
        
        # Use regex to extract the file path, line number, and content to replace
        match = re.match(searchpattern_ruff, error_message)
        if match:
            file_path = match.group(1)
            line_number = int(match.group(2))
            
            # Now you have the file path, line number, and content to replace
            # You can perform the desired actions here
            print(f"File Path: {file_path}")
            print(f"Line Number: {line_number}")
            with open(file_path, "r+") as target_file:
                target_lines = target_file.readlines()
                if 1 <= line_number <= len(target_lines):
                    line_content = target_lines[line_number - 1]
                    print("Original line: " + line_content)
                    target_lines[line_number - 1] = re.sub(searchpattern_code, replacepattern_code, line_content)
                    # Move the file cursor to the beginning and truncate the file
                    target_file.seek(0)
                    #target_file.truncate()                  
                    # Write the updated content back to the same file
                    target_file.writelines(target_lines)    
                    print(f"Updated Line Content: {target_lines[line_number - 1].strip()}")
        else:
            print(f"Error: Failed to extract information from the error message: {error_message}")
