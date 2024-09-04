import os
import time
import sys
import argparse
import subprocess

print("\033[032m", end="")

def changeBracks(line):
    while '{' in line:
        bracIndex = line.index("{")
        line = line[:bracIndex] + ":" + line[bracIndex+1:]
        while bracIndex > 0 and line[bracIndex - 1] == " ":
            line = line[:bracIndex - 1] + line[bracIndex:]
    while '}' in line:
        bracIndex = line.index("}")
        line = line[:bracIndex] + line[bracIndex+1:]
        while bracIndex < len(line) and line[bracIndex] == " ":
            line = line[:bracIndex] + line[bracIndex+1:]    
    return line

def get_file_path(file_name):
    if file_name.endswith(".py"):
        print("""
For some reason, while I was coding, I forgot to consider that you might input .py files.
But womp womp.
I'm too lazy to change my code. I alr wasted 3 hours of my time thinking how to fool-proof my interpreter.
So I ain't got the time to change stuff.
Change your file name to '.by' and come back later...
        """)
        input("Press Enter to exit...")
        sys.exit()

    if os.path.basename(file_name) == file_name:
        return os.path.join(os.getcwd(), file_name)
    return file_name

def read_code(code) -> str:
    processed_code = ''
    firstBrac = 0
    for line in code.splitlines():
        is_dict = line.count('=') == 1
        is_f_string = 'f"' in line or "f'" in line
        is_format = '.format(' in line

        if is_dict:
            if "{" in line and "}" not in line:
                firstBrac = 1
                
        if is_dict or is_f_string or is_format:
            processed_code += f"{line}\n"
        
        else:
            if firstBrac and "}" in line:
                processed_code += f"{line}\n"
                firstBrac = 0
                continue
            processed_code += changeBracks(line) + "\n"
    
    return processed_code

def read_file(file_path):
    try:
        with open(file_path, 'r') as code_file:
            return code_file.read()
    except FileNotFoundError:
        print("File not found!")
        input("Press Enter to exit...")
        sys.exit()
    except Exception as e:
        print(f"An error occurred: {e}")
        input("Press Enter to exit...")
        sys.exit()
        
def execute(code, file_name, keep_file):
    name = os.path.basename(file_name).split('.')[0] + ".py"
    
    with open(name, 'w') as file:
        file.write(f"import sys\n__exe__ = sys.executable\n\n{code}")
    
    start = time.time()
    
    # Use subprocess.run for better control and compatibility
    result = subprocess.run([sys.executable, name], capture_output=True, text=True)
    end = time.time()
    
    timeElapsed = (end - start) * 1000
    
    if not keep_file:
        os.remove(name)

    print("------------")
    print("Exit code:", result.returncode)
    print(f"Elapsed time: {timeElapsed:.2f} ms")
    if result.stdout:
        print("Output:\n", result.stdout)
    if result.stderr:
        print("Errors:\n", result.stderr)

def translate_only(code, file_name):
    name = os.path.basename(file_name).split('.')[0] + "_translated.by"
    
    with open(name, 'w') as file:
        file.write(code)
    
    print(f"Translated file saved as: {name}")

def main():
    parser = argparse.ArgumentParser(description="Translate and optionally execute a file.")
    parser.add_argument('file', type=str, help='Path to the file to be processed.')
    parser.add_argument('--keep', action='store_true', help='Keep the translated file after execution.')
    parser.add_argument('--translate-only', action='store_true', help='Only translate the file without executing it.')
    args = parser.parse_args()

    file_path = get_file_path(args.file)
    code = read_file(file_path)
    processed_code = read_code(code)

    if args.translate_only:
        translate_only(processed_code, file_path)
    else:
        execute(processed_code, file_path, args.keep)
        
if __name__ == '__main__':
    main()
