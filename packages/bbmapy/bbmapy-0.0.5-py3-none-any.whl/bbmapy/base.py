import os
import sys
import subprocess
from typing import List, Dict, Union, Tuple
from rich import print as rprint
from rich.markup import escape

def find_bbtools_path():
    # Check if we're running from an installed package
    if getattr(sys, 'frozen', False):
        # We're running from a bundle (e.g., PyInstaller)
        base_path = sys._MEIPASS
    else:
        # We're running from a normal Python environment
        base_path = os.path.abspath(os.path.dirname(__file__))
    
    # Navigate up to the project root
    original_base_path = base_path
    while not os.path.exists(os.path.join(base_path, 'vendor')):
        new_base_path = os.path.dirname(base_path)
        if new_base_path == base_path:  # We've reached the root directory
            raise FileNotFoundError(f"Could not find BBTools directory. Started search from: {original_base_path}")
        base_path = new_base_path
    
    bbtools_path = os.path.join(base_path, 'vendor', 'bbmap')
    
    if not os.path.exists(bbtools_path):
        raise FileNotFoundError(f"BBTools directory not found at {bbtools_path}")
    
    return bbtools_path

try:
    BBTOOLS_PATH = find_bbtools_path()
    os.environ["PATH"] = f"{BBTOOLS_PATH}/current/:{os.environ['PATH']}"
except FileNotFoundError as e:
    print(f"Error: {e}")
    sys.exit(1)

def _pack_args(kwargs: Dict[str, Union[str, bool, int]]) -> List[str]:
    args = []
    
    for key, value in kwargs.items():
        if key in ['Xmx', 'Xms', 'da', 'ea', 'eoom']:
            if isinstance(value, bool) and value:
                args.append(f"-{key}")
            elif value is not None:
                args.append(f"-{key}{str(value)}")
        elif key == "in_file":
            args.append(f"in={str(value)}")
        elif isinstance(value, bool) and value:
            args.append(key)
        elif value is not None:
            args.append(f"{key}={str(value)}")
    
    return args

def _run_command(tool: str, args: List[str], capture_output: bool = False) -> Union[None, Tuple[str, str]]:
    command = [os.path.join(BBTOOLS_PATH, tool)] + args
    escaped_command = ' '.join(escape(str(arg)) for arg in command)
    
    if capture_output:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Command failed: {escaped_command}\nError: {escape(result.stderr)}")
        return result.stdout, result.stderr
    else:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        while True:
            stdout_line = process.stdout.readline()
            stderr_line = process.stderr.readline()
            
            if not stdout_line and not stderr_line and process.poll() is not None:
                break
            
            if stdout_line:
                rprint(escape(stdout_line.strip()))
            if stderr_line:
                rprint("[bold red]" + escape(stderr_line.strip()) + "[/bold red]")
        
        if process.returncode != 0:
            raise RuntimeError(f"Command failed: {escaped_command}")
        
        return None