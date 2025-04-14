# Electron OpenGL Launcher Creator

This repository contains scripts to create launcher applications for Electron-based applications that enforce the use of OpenGL rendering through the `--use-angle=gl` argument. This is particularly useful for applications that experience graphical issues on macOS.

## Background

Electron applications on macOS can sometimes experience graphical issues due to the rendering backend used. By forcing the application to use OpenGL rendering with the `--use-angle=gl` argument, many of these issues can be resolved.

The scripts in this repository automate the process of creating launcher applications that you can double-click to open Electron applications with OpenGL rendering, without having to interact with the terminal.

## Scripts

### 1. `create_vscode_launcher.py`

This script creates a launcher specifically for Visual Studio Code.

#### Usage

```bash
python create_vscode_launcher.py [app_name] [app_path]
```

#### Arguments

- `app_name` (optional): Name of the launcher application (default: "VS Code with OpenGL")
- `app_path` (optional): Path where the launcher will be saved (default: Desktop)

#### Example

```bash
python create_vscode_launcher.py "VS Code GL" ~/Applications
```

This will create a launcher application named "VS Code GL.app" in the ~/Applications directory.

### 2. `electron_launcher_creator.py`

This script is more versatile and can create launchers for any Electron application. It can also scan directories to find Electron applications.

#### Usage

```bash
# Create a launcher for a specific application
python electron_launcher_creator.py --app APP_PATH [--name APP_NAME] [--output OUTPUT_PATH]

# Scan a directory for Electron applications
python electron_launcher_creator.py --scan-dir DIRECTORY

# List Electron applications without creating launchers
python electron_launcher_creator.py --list-only
```

#### Arguments

- `--app APP_PATH`: Path to the Electron application (.app)
- `--name APP_NAME`: Name for the launcher application (default: original name + " with OpenGL")
- `--output OUTPUT_PATH`: Path where the launcher will be saved (default: Desktop)
- `--scan-dir DIRECTORY`: Scan a directory for Electron applications
- `--list-only`: Only list detected Electron applications without creating launchers

#### Examples

```bash
# Create a launcher for VS Code
python electron_launcher_creator.py --app "/Applications/Visual Studio Code.app"

# Create a launcher with a custom name
python electron_launcher_creator.py --app "/Applications/Slack.app" --name "Slack GL"

# Scan the Applications directory for Electron applications
python electron_launcher_creator.py --scan-dir "/Applications"

# List all Electron applications in the Applications directory
python electron_launcher_creator.py --list-only
```

## Requirements

- macOS (the scripts are designed specifically for macOS)
- Python 3.6 or higher

## How It Works

The scripts create AppleScript applications that launch the target Electron application with the `--use-angle=gl` argument. The resulting launcher can be double-clicked like any other macOS application, providing a seamless experience.

## Troubleshooting

If the launcher doesn't work as expected, try the following:

1. Ensure the path to the original application is correct
2. Check if the application is actually an Electron application
3. Try running the application directly from the terminal with the `--use-angle=gl` argument to see if it resolves the issue
