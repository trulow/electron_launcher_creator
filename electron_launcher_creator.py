#!/usr/bin/env python3
"""
electron_launcher_creator.py

This script creates AppleScript applications that launch Electron-based applications
with the --use-angle=gl argument. The resulting applications can be double-clicked
to launch with OpenGL rendering without needing to interact with a terminal.

Usage:
    python electron_launcher_creator.py [--app APP_PATH] [--name APP_NAME] [--output OUTPUT_PATH]
    python electron_launcher_creator.py --scan-dir DIRECTORY
    python electron_launcher_creator.py --list-only

Arguments:
    --app APP_PATH: Path to the Electron application (.app)
    --name APP_NAME: Name for the launcher application (default: original name + " with OpenGL")
    --output OUTPUT_PATH: Path where the launcher will be saved (default: Desktop)
    --scan-dir DIRECTORY: Scan a directory for Electron applications
    --list-only: Only list detected Electron applications without creating launchers
"""

import os
import sys
import subprocess
import tempfile
import argparse
import glob
import platform

def is_electron_app(app_path):
    """
    Check if the application is an Electron app.
    
    Args:
        app_path (str): Path to the application
        
    Returns:
        bool: True if it's an Electron app, False otherwise
    """
    # Check for common Electron indicators
    electron_indicators = [
        "Electron Framework.framework",
        "electron.asar",
        "app.asar"
    ]
    
    for indicator in electron_indicators:
        if glob.glob(os.path.join(app_path, "**", indicator), recursive=True):
            return True
    
    return False

def get_app_name(app_path):
    """
    Extract the application name from the path.
    
    Args:
        app_path (str): Path to the application
        
    Returns:
        str: Application name
    """
    # Extract the base name without extension
    base_name = os.path.basename(app_path)
    if base_name.endswith('.app'):
        base_name = base_name[:-4]
    
    return base_name

def create_launcher(app_path, app_name=None, output_path=None):
    """
    Create an AppleScript application that launches an Electron app with OpenGL rendering.
    
    Args:
        app_path (str): Path to the Electron application
        app_name (str): Name for the launcher application
        output_path (str): Path where the launcher will be saved
    """
    # Expand user directory if needed
    app_path = os.path.expanduser(app_path)
    
    # Set default app name if not provided
    if app_name is None:
        original_name = get_app_name(app_path)
        app_name = f"{original_name} with OpenGL"
    
    # Set default output path to Desktop if not provided
    if output_path is None:
        output_path = os.path.expanduser("~/Desktop")
    
    # Ensure the output directory exists
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    # Full path to the launcher application
    launcher_path = os.path.join(output_path, f"{app_name}.app")
    
    # Create a temporary AppleScript file
    with tempfile.NamedTemporaryFile(suffix='.applescript', mode='w', delete=False) as temp_file:
        # Escape spaces in the app path for shell command
        escaped_app_path = app_path.replace(' ', '\\ ')
        
        applescript_content = f"""
        on run
            do shell script "open {escaped_app_path} --args --use-angle=gl"
        end run
        """
        temp_file.write(applescript_content)
        temp_file_path = temp_file.name
    
    try:
        # Compile the AppleScript into an application
        subprocess.run([
            "osacompile",
            "-o", launcher_path,
            temp_file_path
        ], check=True)
        
        print(f"Launcher '{app_name}' created successfully at '{output_path}'.")
        print(f"You can now double-click '{app_name}.app' to launch the application with OpenGL rendering.")
    finally:
        # Clean up the temporary file
        os.unlink(temp_file_path)

def find_electron_apps(directory=None):
    """
    Find Electron applications in the specified directory.
    
    Args:
        directory (str): Directory to scan for Electron applications
        
    Returns:
        list: List of paths to Electron applications
    """
    if directory is None:
        directory = "/Applications"
    
    directory = os.path.expanduser(directory)
    
    # Find all .app bundles in the directory
    app_paths = glob.glob(os.path.join(directory, "*.app"))
    
    # Filter for Electron applications
    electron_apps = []
    for app_path in app_paths:
        if is_electron_app(app_path):
            electron_apps.append(app_path)
    
    return electron_apps

def main():
    # Check if running on macOS
    if platform.system() != "Darwin":
        print("Error: This script only works on macOS")
        sys.exit(1)
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Create launchers for Electron applications with OpenGL rendering")
    parser.add_argument("--app", help="Path to the Electron application (.app)")
    parser.add_argument("--name", help="Name for the launcher application")
    parser.add_argument("--output", help="Path where the launcher will be saved")
    parser.add_argument("--scan-dir", help="Scan a directory for Electron applications")
    parser.add_argument("--list-only", action="store_true", help="Only list detected Electron applications without creating launchers")
    
    args = parser.parse_args()
    
    if args.app:
        # Create a launcher for a specific application
        create_launcher(args.app, args.name, args.output)
    elif args.scan_dir or args.list_only:
        # Scan for Electron applications
        scan_dir = args.scan_dir if args.scan_dir else "/Applications"
        electron_apps = find_electron_apps(scan_dir)
        
        if not electron_apps:
            print(f"No Electron applications found in {scan_dir}")
            return
        
        print(f"Found {len(electron_apps)} Electron applications:")
        for i, app_path in enumerate(electron_apps, 1):
            app_name = get_app_name(app_path)
            print(f"{i}. {app_name} ({app_path})")
        
        if args.list_only:
            return
        
        # Ask which applications to create launchers for
        print("\nEnter the numbers of the applications to create launchers for (comma-separated),")
        print("or 'all' for all applications, or 'q' to quit:")
        choice = input("> ")
        
        if choice.lower() == 'q':
            return
        
        if choice.lower() == 'all':
            selected_apps = electron_apps
        else:
            try:
                indices = [int(idx.strip()) - 1 for idx in choice.split(',')]
                selected_apps = [electron_apps[idx] for idx in indices if 0 <= idx < len(electron_apps)]
            except (ValueError, IndexError):
                print("Invalid selection")
                return
        
        # Create launchers for selected applications
        for app_path in selected_apps:
            create_launcher(app_path, output_path=args.output)
    else:
        # No arguments provided, show help
        parser.print_help()

if __name__ == "__main__":
    main()
