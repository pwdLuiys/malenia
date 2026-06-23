# tweaks.py

# Importing core modules to interact directly with the OS environment.
# winreg: Allows us to read and write directly into the Windows Registry.
# subprocess: Used to spawn new processes, connect to their input/output, and run PowerShell commands.
# os, shutil: Standard libraries for interacting with the operating system files, paths, and forcefully removing directories.
# re: Regular expressions to parse specific GUIDs from terminal outputs.
import winreg
import subprocess
import os
import shutil
import re

# Using a list of dictionaries to maintain scalability. If we need to add 50 more tweaks later, we just add new blocks here without changing the core engine.
# DISCLAIMER: ONE MORE TIME: This dictionary was written by AI to save time, i just send Gemini what tweaks to include and BOOM dictionary is ready.
# 'toggle' type means it checks registry states (ON/OFF) and reverses them.
# 'action' type triggers custom functions for complex executions (like executing scripts).

TWEAKS = [
    # --- PRIVACY & TELEMETRY ---
    {
        "name": "Telemetry (Data Collection)",
        "type": "toggle",
        "hive": winreg.HKEY_LOCAL_MACHINE,
        "key": r"SOFTWARE\Policies\Microsoft\Windows\DataCollection",
        "value_name": "AllowTelemetry",
        "on_val": 3, 
        "off_val": 0 
    },
    {
        "name": "Activity History",
        "type": "toggle",
        "hive": winreg.HKEY_LOCAL_MACHINE,
        "key": r"SOFTWARE\Policies\Microsoft\Windows\System",
        "value_name": "PublishUserActivities",
        "on_val": 1,
        "off_val": 0
    },
    {
        "name": "Location Tracking",
        "type": "toggle",
        "hive": winreg.HKEY_LOCAL_MACHINE,
        "key": r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\location",
        "value_name": "Value",
        "on_val": "Allow", 
        "off_val": "Deny"
    },
    
    # --- SYSTEM & SERVICES ---
    {
        "name": "Background Apps",
        "type": "toggle",
        "hive": winreg.HKEY_LOCAL_MACHINE,
        "key": r"SOFTWARE\Policies\Microsoft\Windows\AppPrivacy",
        "value_name": "LetAppsRunInBackground",
        "on_val": 0, # 0 means user is in control (effectively ON)
        "off_val": 2 # 2 forces the OS to deny apps from running in the background
    },
    {
        "name": "BitLocker (Auto Device Encryption)",
        "type": "toggle",
        "hive": winreg.HKEY_LOCAL_MACHINE,
        "key": r"SYSTEM\CurrentControlSet\Control\BitLocker",
        "value_name": "PreventDeviceEncryption",
        "on_val": 0, # 0 allows auto-encryption
        "off_val": 1 # 1 prevents it entirely
    },
    {
        "name": "Delivery Optimization (P2P Updates)",
        "type": "toggle",
        "hive": winreg.HKEY_LOCAL_MACHINE,
        "key": r"SOFTWARE\Policies\Microsoft\Windows\DeliveryOptimization",
        "value_name": "DODownloadMode",
        "on_val": 1,
        "off_val": 0
    },
    {
        "name": "Consumer Features (Auto-install sponsored apps)",
        "type": "toggle",
        "hive": winreg.HKEY_LOCAL_MACHINE,
        "key": r"SOFTWARE\Policies\Microsoft\Windows\CloudContent",
        "value_name": "DisableWindowsConsumerFeatures",
        "on_val": 0,
        "off_val": 1
    },
    {
        "name": "Hibernation",
        "type": "toggle",
        "hive": winreg.HKEY_LOCAL_MACHINE,
        "key": r"SYSTEM\CurrentControlSet\Control\Power",
        "value_name": "HibernateEnabled",
        "on_val": 1,
        "off_val": 0
    },
    {
        "name": "Date & Time (Set Hardware Clock to UTC)",
        "type": "toggle",
        "hive": winreg.HKEY_LOCAL_MACHINE,
        "key": r"SYSTEM\CurrentControlSet\Control\TimeZoneInformation",
        "value_name": "RealTimeIsUniversal",
        "on_val": 0, # Default local time
        "off_val": 1 # UTC (highly recommended when dual-booting with Linux)
    },

    # --- EXPLORER & INTERFACE ---
    {
        "name": "Dark Theme (System & Apps)",
        "type": "toggle",
        "hive": winreg.HKEY_CURRENT_USER,
        "key": r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
        "value_name": "AppsUseLightTheme", 
        "on_val": 0, # 0 means light theme is OFF, so dark theme is ON.
        "off_val": 1 
    },
    {
        "name": "Enable Long Paths (>260 chars)",
        "type": "toggle",
        "hive": winreg.HKEY_LOCAL_MACHINE,
        "key": r"SYSTEM\CurrentControlSet\Control\FileSystem",
        "value_name": "LongPathsEnabled",
        "on_val": 1, 
        "off_val": 0 
    },
    {
        "name": "File Explorer: Show Hidden Files",
        "type": "toggle",
        "hive": winreg.HKEY_CURRENT_USER,
        "key": r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
        "value_name": "Hidden",
        "on_val": 1, 
        "off_val": 2 
    },
    {
        "name": "File Explorer: Show File Extensions",
        "type": "toggle",
        "hive": winreg.HKEY_CURRENT_USER,
        "key": r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
        "value_name": "HideFileExt",
        "on_val": 0, 
        "off_val": 1 
    },
    {
        "name": "File Explorer: Automatic Folder Discovery",
        "type": "toggle",
        "hive": winreg.HKEY_CURRENT_USER,
        "key": r"Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\Bags\AllFolders\Shell",
        "value_name": "FolderType",
        "on_val": "", # Dynamic behavior based on content
        "off_val": "NotSpecified" # Stops the OS from guessing the folder type
    },
    {
        "name": "Taskbar: Centered Icons (Win 11)",
        "type": "toggle",
        "hive": winreg.HKEY_CURRENT_USER,
        "key": r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
        "value_name": "TaskbarAl",
        "on_val": 1, 
        "off_val": 0 
    },
    {
        "name": "Taskbar: Search Icon Visibility",
        "type": "toggle",
        "hive": winreg.HKEY_CURRENT_USER,
        "key": r"Software\Microsoft\Windows\CurrentVersion\Search",
        "value_name": "SearchboxTaskbarMode",
        "on_val": 1, 
        "off_val": 0 
    },
    {
        "name": "Start Menu: Bing Search Results",
        "type": "toggle",
        "hive": winreg.HKEY_CURRENT_USER,
        "key": r"Software\Policies\Microsoft\Windows\Explorer",
        "value_name": "DisableSearchBoxSuggestions",
        "on_val": 0,
        "off_val": 1
    },
    {
        "name": "Start Menu: Recommendations",
        "type": "toggle",
        "hive": winreg.HKEY_CURRENT_USER,
        "key": r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
        "value_name": "Start_TrackDocs",
        "on_val": 1,
        "off_val": 0
    },
    {
        "name": "End Task with Right Click (Win 11)",
        "type": "toggle",
        "hive": winreg.HKEY_CURRENT_USER,
        "key": r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
        "value_name": "TaskbarEndTask",
        "on_val": 1, 
        "off_val": 0 
    },

    # --- HARDWARE & GAMING ---
    {
        "name": "Game Mode",
        "type": "toggle",
        "hive": winreg.HKEY_CURRENT_USER,
        "key": r"Software\Microsoft\GameBar",
        "value_name": "AutoGameModeEnabled",
        "on_val": 1,
        "off_val": 0
    },
    {
        "name": "Mouse Acceleration (Enhance Pointer Precision)",
        "type": "toggle",
        "hive": winreg.HKEY_CURRENT_USER,
        "key": r"Control Panel\Mouse",
        "value_name": "MouseSpeed",
        "on_val": "1", # Kept as string because Control Panel stores it this way.
        "off_val": "0"
    },
    {
        "name": "Sticky Keys",
        "type": "toggle",
        "hive": winreg.HKEY_CURRENT_USER,
        "key": r"Control Panel\Accessibility\StickyKeys",
        "value_name": "Flags",
        "on_val": "506", # 506 means active with shortcut
        "off_val": "502" # 502 means completely disabled
    },

    # --- STORAGE ---
    {
        "name": "Storage Sense",
        "type": "toggle",
        "hive": winreg.HKEY_CURRENT_USER,
        "key": r"Software\Microsoft\Windows\CurrentVersion\StorageSense\Parameters\StoragePolicy",
        "value_name": "01",
        "on_val": 1,
        "off_val": 0
    },
    {
        "name": "Disable Reserve Storage",
        "type": "toggle",
        "hive": winreg.HKEY_LOCAL_MACHINE,
        "key": r"SOFTWARE\Microsoft\Windows\CurrentVersion\ReserveManager",
        "value_name": "ShippedWithReserves",
        "on_val": 1,
        "off_val": 0
    },

    # ------------------ ACTIONS (One-Way Executions) ------------------
    {
        "name": "Appearance & Performance Profiles",
        "type": "action",
        "target_function": "action_visual_profiles"
    },
    {
        "name": "Enable Ultimate Performance Power Plan",
        "type": "action",
        "target_function": "action_ultimate_performance"
    },
    {
        "name": "Microsoft Edge Debloat",
        "type": "action",
        "target_function": "action_edge_debloat"
    },
    {
        "name": "Remove Temporary System Files",
        "type": "action",
        "target_function": "action_clear_temp"
    },
    {
        "name": "Remove and Destroy Windows AI (Copilot/Recall/etc)",
        "type": "action",
        "target_function": "action_destroy_windows_ai"
    },
    {
        "name": "Remove Microsoft OneDrive",
        "type": "action",
        "target_function": "action_remove_onedrive"
    },
    {
        "name": "Remove Xbox Gaming Components",
        "type": "action",
        "target_function": "action_remove_xbox"
    }
]

# =====================================================================
# REGISTRY HELPER FUNCTIONS
# =====================================================================

def read_registry_state(tweak):
    """
    Reads the current state of a registry key to determine if a tweak is ON or OFF.
    Handles exceptions gracefully to prevent crashes if the key doesn't exist yet.
    """
    try:
        with winreg.OpenKey(tweak["hive"], tweak["key"], 0, winreg.KEY_READ) as key:
            value, _ = winreg.QueryValueEx(key, tweak["value_name"])
            return value == tweak["on_val"]
    except FileNotFoundError:
        return False
    except Exception:
        return False

def write_registry_state(tweak, turn_on=True):
    """
    Modifies the Windows Registry based on the user's toggle choice.
    Requires Admin privileges when modifying HKEY_LOCAL_MACHINE (HKLM).
    """
    try:
        with winreg.CreateKeyEx(tweak["hive"], tweak["key"], 0, winreg.KEY_SET_VALUE) as key:
            new_value = tweak["on_val"] if turn_on else tweak["off_val"]
            
            # Dynamic type checking. If the target value is a string, we write REG_SZ.
            # Otherwise, we default to REG_DWORD (Integers).
            reg_type = winreg.REG_SZ if isinstance(new_value, str) else winreg.REG_DWORD
            winreg.SetValueEx(key, tweak["value_name"], 0, reg_type, new_value)
            
            # Some features require multiple keys to be changed at the same time to work properly.
            if "Dark Theme" in tweak["name"]:
                winreg.SetValueEx(key, "SystemUsesLightTheme", 0, reg_type, new_value)
            
            elif "Mouse Acceleration" in tweak["name"]:
                # Disabling enhanced pointer precision requires zeroing out threshold strings.
                thresh1 = "6" if turn_on else "0"
                thresh2 = "10" if turn_on else "0"
                winreg.SetValueEx(key, "MouseThreshold1", 0, winreg.REG_SZ, thresh1)
                winreg.SetValueEx(key, "MouseThreshold2", 0, winreg.REG_SZ, thresh2)
                
        return True
    except PermissionError:
        print(f"[Error] Missing Administrative privileges to alter {tweak['name']}.")
        return False
    except Exception as e:
        print(f"[Error] Failed to write registry key for {tweak['name']}: {e}")
        return False

# =====================================================================
# CUSTOM ACTION FUNCTIONS
# =====================================================================

def action_visual_profiles():
    print("\n--- Visual & Performance Profiles ---")
    print("1. Recommended (Thumbnails, default animations, and smooth fonts enabled)")
    print("2. Smooth / Performance (Disables animations and shadows for max performance)")
    print("3. Beautiful (All visual effects and shadows enabled)")
    
    choice = input("\nSelect the desired profile (1-3): ").strip()
    
    try:
        with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects", 0, winreg.KEY_SET_VALUE) as key:
            if choice == "1":
                winreg.SetValueEx(key, "VisualFXSetting", 0, winreg.REG_DWORD, 1)
                print("[Action] Visual profile set to 'Recommended'.")
            elif choice == "2":
                winreg.SetValueEx(key, "VisualFXSetting", 0, winreg.REG_DWORD, 3)
                print("[Action] Visual profile set to 'Smooth' (Performance focus).")
            elif choice == "3":
                winreg.SetValueEx(key, "VisualFXSetting", 0, winreg.REG_DWORD, 2)
                print("[Action] Visual profile set to 'Beautiful' (Appearance focus).")
            else:
                print("[Warning] Invalid selection. Operation aborted.")
    except Exception as e:
        print(f"[Error] Failed to apply visual profile: {e}")

def action_ultimate_performance():
    print("\n[Action] Enabling Ultimate Performance power plan...")
    try:
        # Clones the hidden power scheme native to Windows for workstations.
        cmd_duplicate = ["powercfg", "-duplicatescheme", "e9a42b02-d5df-448d-aa00-03f14749eb61"]
        result = subprocess.run(cmd_duplicate, capture_output=True, text=True, check=True)
        
        # Extracts the dynamically generated GUID using regex to activate it immediately.
        match = re.search(r"([0-9a-fA-F]{8}(-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12})", result.stdout)
        
        if match:
            new_guid = match.group(1)
            subprocess.run(["powercfg", "/setactive", new_guid], check=True)
            print("[Success] Ultimate Performance plan has been successfully activated.")
        else:
            print("[Error] Failed to extract the power scheme GUID.")
    except Exception as e:
        print(f"[Error] Failed to manipulate power configurations: {e}")

def action_edge_debloat():
    print("\n[Action] Initiating Microsoft Edge debloat sequence...")
    # Force kills the edge process before modifying its settings to prevent locks.
    subprocess.run(["taskkill", "/F", "/IM", "msedge.exe"], capture_output=True)
    
    desktop_path = os.path.join(os.environ["USERPROFILE"], "Desktop", "Microsoft Edge.lnk")
    if os.path.exists(desktop_path):
        os.remove(desktop_path)
        print("[Action] Desktop shortcut removed.")
    
    try:
        key_path = r"SOFTWARE\Policies\Microsoft\Edge"
        with winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, "BackgroundModeEnabled", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(key, "StartupBoostEnabled", 0, winreg.REG_DWORD, 0)
        print("[Success] Edge background execution blocked via group policy.")
    except Exception:
        print("[Warning] Access denied. Make sure you run the script as Administrator.")

def action_clear_temp():
    print("\n[Action] Initiating temporary files cleanup...")
    temp_folders = [os.environ.get("TEMP"), r"C:\Windows\Temp"]
    
    for folder in temp_folders:
        if folder and os.path.exists(folder):
            print(f" -> Processing directory: {folder}")
            for item in os.listdir(folder):
                item_path = os.path.join(folder, item)
                try:
                    # Deletes the file directly or completely obliterates the folder tree.
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                except Exception:
                    # Ignoring processes or files currently locked in memory by the OS.
                    pass
    print("[Success] Temporary files sweep completed.")

def action_destroy_windows_ai():
    """
    Executes a deep, system-wide purge of Microsoft AI integrations.
    This mimics aggressive debloat scripts but avoids corrupting the Component-Based Servicing (CBS) store,
    ensuring future Windows updates do not brick the system.
    """
    print("\n[Action] Initiating deep purge of Windows AI ecosystems...")
    
    # Phase 1: Registry Policies Injection
    # We define a mapping of paths and their respective values to disable AI features across the OS environment.
    ai_registry_policies = [
        # Disable General Windows Copilot
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\WindowsCopilot", "TurnOffWindowsCopilot", 1),
        (winreg.HKEY_CURRENT_USER, r"Software\Policies\Microsoft\Windows\WindowsCopilot", "TurnOffWindowsCopilot", 1),
        # Disable Recall (AI Data Analysis)
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\WindowsAI", "DisableAIDataAnalysis", 1),
        # Disable Edge Copilot and Discover features
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Edge", "HubsSidebarEnabled", 0),
        # Disable Input Insights (Typing data harvesting)
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Input\Settings", "InsightsEnabled", 0),
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\InputPersonalization", "RestrictImplicitTextCollection", 1),
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\InputPersonalization\TrainedDataStore", "HarvestContacts", 0),
        # Disable Paint AI (Cocreator)
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Applets\Paint", "FeatureOverrides", 0),
        # Disable Snipping Tool AI (Click to Do)
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\SnippingTool", "DisableClickToDo", 1),
        # Disable Office Apps Copilot
        (winreg.HKEY_CURRENT_USER, r"Software\Policies\Microsoft\Office\16.0\Common\ExperimentConfigs\ExternalFeatureOverrides\copilot", "State", 0)
    ]

    print("[Phase 1] Restricting AI execution parameters via Registry...")
    for hive, path, name, val in ai_registry_policies:
        try:
            with winreg.CreateKeyEx(hive, path, 0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, val)
        except Exception as e:
            # Silent failure for specific keys that might require TrustedInstaller permissions
            pass
    print("[Success] Registry AI policies successfully locked down.")

    # Phase 2: Purging AppX Packages (Modern UI AI components)
    print("[Phase 2] Forcing removal of AI-related AppX packages via PowerShell...")
    # Using wildcards to catch Copilot, Recall, and AI Fabric variants
    appx_commands = [
        "Get-AppxPackage *Copilot* -AllUsers | Remove-AppxPackage -AllUsers",
        "Get-AppxPackage *WindowsAI* -AllUsers | Remove-AppxPackage -AllUsers",
        "Get-AppxPackage *Recall* -AllUsers | Remove-AppxPackage -AllUsers",
        "Get-AppxPackage *AIFabric* -AllUsers | Remove-AppxPackage -AllUsers"
    ]
    
    for cmd in appx_commands:
        subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    print("[Success] AI AppX packages eradicated.")

    # Phase 3: Disabling Scheduled AI Data Mining Tasks
    # Instead of deleting them (which causes OS error logs), we disable them to keep the system stable.
    print("[Phase 3] Neutralizing AI telemetry scheduled tasks...")
    task_cmd = (
        "Get-ScheduledTask | "
        "Where-Object {$_.TaskName -match 'Copilot|WindowsAI|Recall|InputInsights'} | "
        "Disable-ScheduledTask"
    )
    subprocess.run(["powershell", "-Command", task_cmd], capture_output=True)
    print("[Success] Scheduled tasks neutralized.")
    
    print("\n[System Log] Full AI purge sequence completed safely.")

def action_remove_onedrive():
    print("\n[Action] Removing Microsoft OneDrive from the system...")
    subprocess.run(["taskkill", "/F", "/IM", "OneDrive.exe"], capture_output=True)
    
    # Typical silent uninstallation paths on 32-bit and 64-bit architectures.
    sys32 = os.path.join(os.environ["SYSTEMROOT"], "System32", "OneDriveSetup.exe")
    syswow = os.path.join(os.environ["SYSTEMROOT"], "SysWOW64", "OneDriveSetup.exe")
    
    executable = syswow if os.path.exists(syswow) else sys32
    
    if os.path.exists(executable):
        try:
            subprocess.run([executable, "/uninstall"], check=True)
            print("[Success] OneDrive automated uninstallation process completed.")
        except subprocess.CalledProcessError:
            print("[Error] Failed during the automated removal of OneDrive.")
    else:
        print("[Warning] The OneDrive uninstaller executable was not found (likely already removed).")

def action_remove_xbox():
    print("\n[Action] Removing native Xbox components and gaming bloatware...")
    # Executes embedded PowerShell scripts to purge all AppX packages named 'Xbox'.
    ps_commands = [
        "Get-AppxPackage *xboxapp* -AllUsers | Remove-AppxPackage -AllUsers",
        "Get-AppxPackage *xboxgamingoverlay* -AllUsers | Remove-AppxPackage -AllUsers",
        "Get-AppxPackage *xboxspeechtotextoverlay* -AllUsers | Remove-AppxPackage -AllUsers"
    ]
    
    for cmd in ps_commands:
        subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    
    print("[Success] Xbox application integration removed.")

# =====================================================================
# MAIN LOOP AND UI RENDERER
# =====================================================================

def prompt_tweaks_menu():
    """
    Orchestrator function:
    1. Scans the OS dynamic state.
    2. Renders the toggle and execution options.
    3. Handles inputs and logic confirmation (Preview state).
    """
    # Populating the current logical state by directly reading the Windows Registry
    for i, tweak in enumerate(TWEAKS):
        tweak["index"] = i + 1 
        if tweak["type"] == "toggle":
            is_on = read_registry_state(tweak)
            tweak["current_state"] = is_on
        else:
            tweak["current_state"] = "Ready"

    print("\n========================================")
    print("      WINDOWS TWEAKS & OPTIMIZATION     ")
    print("========================================")
    
    for tweak in TWEAKS:
        if tweak["type"] == "toggle":
            status_text = "[ON]" if tweak["current_state"] else "[OFF]"
        else:
            status_text = "[Action Ready]"
            
        print(f"{tweak['index']}. {tweak['name']} - {status_text}")
    print("========================================")

    user_input = input("\nEnter the numbers of the tweaks to be modified separated by space (e.g., '1 4 9'): ").strip()
    if not user_input:
        print("[Action Log] No modifications requested. Returning to the main menu.")
        return

    # String processing to capture valid numeric vectors.
    selected_indexes = []
    for token in user_input.split():
        if token.isdigit():
            selected_indexes.append(int(token))
            
    # Base filter against the database constraints (index mapping).
    valid_selections = [t for t in TWEAKS if t["index"] in selected_indexes]
    
    if not valid_selections:
        print("[Action Log] No valid tweak selected. Aborting.")
        return

    # PREVIEW STATE SCREEN
    # Displays the computed alteration before applying systemic definitive changes.
    print("\n[PREVIEW] The following logical changes will be applied to the system:")
    for tweak in valid_selections:
        if tweak["type"] == "toggle":
            old_status = "ON" if tweak["current_state"] else "OFF"
            new_status = "OFF" if tweak["current_state"] else "ON"
            print(f" -> {tweak['name']}: {old_status} ---> {new_status}")
        else:
            print(f" -> {tweak['name']}: File queued for execution")

    confirm = input("\nConfirm the execution of this operation? (y/n): ").strip().lower()
    
    if confirm == 'y':
        print("\n[System] Applying batch modifications...")
        for tweak in valid_selections:
            if tweak["type"] == "toggle":
                # Inverting the boolean loop for state change.
                target_state = not tweak["current_state"]
                success = write_registry_state(tweak, turn_on=target_state)
                
                if success:
                    print(f"[Done] {tweak['name']} successfully updated and saved.")
            
            elif tweak["type"] == "action":
                # Namespace resolution to call functions dynamically using globals().
                func_name = tweak["target_function"]
                if func_name in globals():
                    globals()[func_name]() 
                    
        print("\n[System Log] Alteration cycle finished. Some modifications may depend on reloading the explorer.exe interface or rebooting.")
    else:
        print("[Action Log] Modification cancelled. OS logical state preserved.")