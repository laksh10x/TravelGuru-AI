import os
import shutil
import json

def copy_json_files():
    """
    Copy the test.json and test_flight.json files to the src/pages directory
    """
    # Get current directory
    current_dir = os.getcwd()
    print(f"Current directory: {current_dir}")
    
    # Define source and destination paths
    src_files = ['test.json', 'test_flight.json']
    dest_dir = os.path.join(current_dir, 'src', 'pages')
    
    print(f"Destination directory: {dest_dir}")
    
    # Check if destination directory exists
    if not os.path.exists(dest_dir):
        print(f"Creating directory: {dest_dir}")
        os.makedirs(dest_dir, exist_ok=True)
    
    # Copy files
    for file in src_files:
        src_path = os.path.join(current_dir, file)
        dest_path = os.path.join(dest_dir, file)
        
        if os.path.exists(src_path):
            print(f"Copying {src_path} to {dest_path}")
            shutil.copy2(src_path, dest_path)
            print(f"File copied successfully: {os.path.getsize(dest_path)} bytes")
        else:
            print(f"Source file does not exist: {src_path}")

if __name__ == "__main__":
    copy_json_files() 