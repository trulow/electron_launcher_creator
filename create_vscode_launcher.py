#!/usr/bin/env python3
"""
create_vscode_launcher.py

This script creates a launcher for Visual Studio Code that enforces the use of OpenGL rendering
through the '--use-angle=gl' argument. The resulting launcher can be double-clicked to launch
VS Code with OpenGL rendering without needing to interact with a terminal.

Usage:
    python create_vscode_launcher.py [app_name] [app_path]

Arguments:
    app_name (optional): Name of the launcher (default: "VS Code with OpenGL")
    app_path (optional): Path where the launcher will be saved (default: Desktop)
"""

import os
import sys
import subprocess
import shutil

def create_shell_launcher(app_name="VS Code with OpenGL", app_path=None):
    """
    Create a shell script launcher for VS Code with OpenGL rendering.

    Args:
        app_name (str): Name of the launcher
        app_path (str): Path where the launcher will be saved
    """
    print(f"Creating shell launcher '{app_name}'...")

    # Set default path to Desktop if not provided
    if app_path is None:
        app_path = os.path.expanduser("~/Desktop")
        print(f"Using default output path: {app_path}")
    else:
        print(f"Using specified output path: {app_path}")

    # Ensure the directory exists
    if not os.path.exists(app_path):
        print(f"Creating directory: {app_path}")
        os.makedirs(app_path)

    # Full path to the shell script
    script_path = os.path.join(app_path, f"{app_name}.command")
    print(f"Full script path: {script_path}")

    # Create the shell script
    shell_script = """#!/bin/bash
open "/Applications/Visual Studio Code.app" --args --use-angle=gl
"""

    with open(script_path, "w") as f:
        f.write(shell_script)

    # Make the script executable
    os.chmod(script_path, 0o755)

    print(f"Launcher '{app_name}.command' created successfully at '{app_path}'.")
    print(f"You can now double-click '{app_name}.command' to launch VS Code with OpenGL rendering.")

    return script_path

def create_app_bundle(app_name="VS Code with OpenGL", app_path=None):
    """
    Create a macOS application bundle that launches VS Code with OpenGL rendering.

    Args:
        app_name (str): Name of the application
        app_path (str): Path where the application will be saved
    """
    print(f"Creating application bundle '{app_name}'...")

    # Set default path to Desktop if not provided
    if app_path is None:
        app_path = os.path.expanduser("~/Desktop")
        print(f"Using default output path: {app_path}")
    else:
        print(f"Using specified output path: {app_path}")

    # Ensure the directory exists
    if not os.path.exists(app_path):
        print(f"Creating directory: {app_path}")
        os.makedirs(app_path)

    # Full path to the application
    app_bundle_path = os.path.join(app_path, f"{app_name}.app")
    print(f"Full application path: {app_bundle_path}")

    # Create the directory structure
    contents_dir = os.path.join(app_bundle_path, "Contents")
    macos_dir = os.path.join(contents_dir, "MacOS")
    resources_dir = os.path.join(contents_dir, "Resources")

    os.makedirs(macos_dir, exist_ok=True)
    os.makedirs(resources_dir, exist_ok=True)

    # Create the Info.plist file
    info_plist = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>{app_name}</string>
    <key>CFBundleIconFile</key>
    <string>code_gl.icns</string>
    <key>CFBundleIdentifier</key>
    <string>com.user.{app_name.replace(" ", "")}</string>
    <key>CFBundleName</key>
    <string>{app_name}</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
</dict>
</plist>
"""

    with open(os.path.join(contents_dir, "Info.plist"), "w") as f:
        f.write(info_plist)

    # Create the executable shell script
    executable = f"""#!/bin/bash
open "/Applications/Visual Studio Code.app" --args --use-angle=gl
"""

    executable_path = os.path.join(macos_dir, app_name)
    with open(executable_path, "w") as f:
        f.write(executable)

    # Make the script executable
    os.chmod(executable_path, 0o755)

    # Copy the icon file
    shutil.copy("./icons/code_gl.icns", resources_dir)

    print(f"Application '{app_name}.app' created successfully at '{app_path}'.")
    print(f"You can now double-click '{app_name}.app' to launch VS Code with OpenGL rendering.")

    return app_bundle_path

def main():
    print("Starting VS Code launcher creator...")

    # Parse command-line arguments
    app_name = "VS Code with OpenGL"
    app_path = os.path.expanduser("~/Desktop")

    if len(sys.argv) > 1:
        app_name = sys.argv[1]
        print(f"Using custom app name: {app_name}")
    else:
        print(f"Using default app name: {app_name}")

    if len(sys.argv) > 2:
        app_path = sys.argv[2]
        print(f"Using custom app path: {app_path}")
    else:
        print(f"Using default app path: {app_path}")

    # Check if VS Code exists
    vscode_path = "/Applications/Visual Studio Code.app"
    if not os.path.exists(vscode_path):
        print(f"Warning: VS Code not found at {vscode_path}")
        print("The launcher will still be created, but it may not work if VS Code is not installed.")
    else:
        print(f"Found VS Code at {vscode_path}")

    # Create both a shell launcher and an app bundle
    shell_path = create_shell_launcher(app_name, app_path)
    app_bundle_path = create_app_bundle(app_name, app_path)

    print("\nCreated two launchers:")
    print(f"1. Shell script: {shell_path}")
    print(f"2. Application bundle: {app_bundle_path}")
    print("\nYou can use either one to launch VS Code with OpenGL rendering.")

    print("Script completed.")

if __name__ == "__main__":
    main()
