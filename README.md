# Malenia Post Format Tool (MaleniaPF)

![MaleniaPF Banner](https://github.com/sluiys/malenia/raw/main/malenia.webp)

MaleniaPF is an automated utility for post-formatting Windows systems. It streamlines driver acquisition, software installation, system cleanup, and OS-level optimizations through a unified Command Line Interface (CLI).

## Quick Start (One-Liner Execution)

You do not need to install Python or clone the repository to run this tool. Simply open an elevated **PowerShell** terminal (run as Administrator) and execute the following command:

```powershell
irm https://raw.githubusercontent.com/sluiys/malenia/main/run.ps1 | iex
```
This command automatically streams the MaleniaPF execution kernel to your system memory, triggers administrative elevation, and cleans up temporary traces after exit.
Tool Modules & Functionality

The program is organized into 6 core modules accessible via the main menu.
1. GPU Driver Management

    Automatic Detection: Queries system hardware to identify NVIDIA, AMD, or Intel graphics controllers.

    Driver Scraper: Connects to official vendor websites to retrieve the latest driver installation payloads directly.

2. Software Installer

    Automated Deployment: Uses the Windows Package Manager (Winget) to perform silent, non-interactive installations of essential software (Browsers, Development tools, Media, etc.).

    Batch Processing: Allows users to queue multiple applications and install them in a single sequence.

3. System Uninstaller

    Shell Removal: Executes official uninstallation binaries for software identified by the system.

    Residual Scrubber: Automatically scans system directories (%AppData%, %LocalAppData%, %ProgramData%) to remove orphaned configuration files and temporary folders left behind by uninstalled apps.

4. Windows Tweaks & Optimization

    Registry Policy Engine: toggles OS features by modifying Windows Registry keys.

    Telemetry & AI Purge: Aggressively removes or disables Windows AI components (Copilot, Recall, WindowsAI packages), telemetry data harvesting, and background monitoring tasks.

    Ultimate Performance: Enables the hidden "Ultimate Performance" power scheme to prioritize hardware throughput.

    Debloat Engine: Cleans up Edge background processes, removes system-level bloatware, and disables unnecessary startup recommendations.

5. Peripheral Software Manager

    Universal Deployment: Installs vendor-specific peripheral software (Logitech G HUB, Razer Synapse, Corsair iCUE, etc.) via Winget.

    Targeted Scrapers: Specifically handles vendor software that does not follow standard distribution repositories, using custom web scraping to pull the latest official installers directly to your download folder.

Usage Guide

    Run the deployment command in an Administrator PowerShell window.

    Navigate the menu by typing the number corresponding to the desired module.

    For multi-selection lists (e.g., Software Installer), enter numbers separated by spaces (e.g., 1 3 5).

    Follow the on-screen prompts. The tool will request confirmation before executing any destructive operations (like uninstallation or system scrubbing).

Troubleshooting

    Execution Policy: If the One-Liner command fails due to script execution policies, run this command once in your PowerShell to permit remote script execution: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser.

    Privileges: If you attempt to run modules that modify system registry keys without Administrative access, the application will issue a permission error. Always ensure your terminal is elevated.
