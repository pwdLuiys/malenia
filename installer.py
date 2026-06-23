#lets import the essencials again
import subprocess
# 'subprocess' lets Python run terminal/cmd commands just like a real user.

# Master dictionary containing all requested applications, categorized.
# I asked Gemini to provide this dictionary, im not writing it myself wtf.
# NOTE: This IDs, ideas and etc was inspired by Chris Titus Tech's Windows tool.
# https://github.com/ChrisTitusTech/winutil
# im trying to learn from him and make an ever better 'wintool', but NEVER trying just to copy his code and stole the credit for his hard work.
# I didnt even knew some names out there of certain programns...
# 
# 
# DISCLAIMER: Some code are written by AI (Claude and Gemini), i did NOT just write a prompt: "Make me a program that do this, and that..." NAH.
# I did it myself, the logic, flow and structure, tool, libraries, but some lists like the next one "Software Catalog" was written by AI.
# And ofc some repetetive code as well. 

SOFTWARE_CATALOG = {
    "Browsers": [
        {"name": "Brave", "id": "Brave.Brave"},
        {"name": "Arc", "id": "TheBrowserCompany.Arc"},
        {"name": "Vivaldi", "id": "VivaldiTechnologies.Vivaldi"},
        {"name": "Chrome", "id": "Google.Chrome"},
        {"name": "Chromium", "id": "Hibbiki.Chromium"},
        {"name": "Waterfox", "id": "Waterfox.Waterfox"},
        {"name": "Edge", "id": "Microsoft.Edge"},
        {"name": "Zen Browser", "id": "zen-browser.zen"},
        {"name": "Zen Browser (Twilight)", "id": "zen-browser.zen-twilight"},
        {"name": "Firefox", "id": "Mozilla.Firefox"},
        {"name": "Firefox Developer Edition", "id": "Mozilla.Firefox.DeveloperEdition"},
        {"name": "LibreWolf", "id": "LibreWolf.LibreWolf"},
        {"name": "Mullvad Browser", "id": "MullvadVPN.MullvadBrowser"},
        {"name": "Tor Browser", "id": "TorProject.TorBrowser"},
        {"name": "Ungoogled Chromium", "id": "eloston.ungoogled-chromium"},
        {"name": "Opera", "id": "Opera.Opera"},
        {"name": "Opera GX", "id": "Opera.OperaGX"}
    ],
    "Communications": [
        {"name": "Telegram", "id": "Telegram.TelegramDesktop"},
        {"name": "WhatsApp", "id": "WhatsApp.WhatsApp"},
        {"name": "Discord", "id": "Discord.Discord"},
        {"name": "Chatterino", "id": "Chatterino.Chatterino"},
        {"name": "Element", "id": "Element.Element"},
        {"name": "Zoom", "id": "Zoom.Zoom"},
        {"name": "Proton Mail", "id": "Proton.ProtonMail"},
        {"name": "Microsoft Teams", "id": "Microsoft.Teams"},
        {"name": "TeamSpeak 3 (Legacy)", "id": "TeamSpeakSystems.TeamSpeak3"},
        {"name": "TeamSpeak (New)", "id": "TeamSpeakSystems.TeamSpeakClient"}
    ],
    "Development": [
        {"name": "CMake", "id": "Kitware.CMake"},
        {"name": "Cursor", "id": "Anysphere.Cursor"},
        {"name": "ZED", "id": "Zed.Zed"},
        {"name": "Neovim", "id": "Neovim.Neovim"},
        {"name": "Vim", "id": "vim.vim"},
        {"name": "Lua", "id": "Lua.Lua"},
        {"name": "JetBrains Toolbox", "id": "JetBrains.Toolbox"},
        {"name": "Python 3", "id": "Python.Python.3.12"},
        {"name": "Go", "id": "GoLang.Go"},
        {"name": "GitHub Desktop", "id": "GitHub.GitHubDesktop"},
        {"name": "Git", "id": "Git.Git"},
        {"name": "Node.js (LTS)", "id": "OpenJS.NodeJS.LTS"},
        {"name": "VSCode", "id": "Microsoft.VisualStudioCode"},
        {"name": "Visual Studio 2022 Community", "id": "Microsoft.VisualStudio.2022.Community"},
        {"name": "VSCodium", "id": "VSCodium.VSCodium"},
        {"name": "Rust", "id": "Rustlang.Rustup"},
        {"name": "Ruby", "id": "RubyInstallerTeam.Ruby"},
        {"name": "Lazygit", "id": "jesseduffield.lazygit"},
        {"name": "Unity Hub", "id": "Unity.UnityHub"},
        {"name": "Unreal Engine (via Epic Games)", "id": "EpicGames.EpicGamesLauncher"}
    ],
    "Games": [
        {"name": "Steam", "id": "Valve.Steam"},
        {"name": "Ubisoft Connect", "id": "Ubisoft.Connect"},
        {"name": "EA App", "id": "ElectronicArts.EADesktop"},
        {"name": "Epic Games Launcher", "id": "EpicGames.EpicGamesLauncher"},
        {"name": "GOG Galaxy", "id": "GOG.Galaxy"},
        {"name": "Heroic Games Launcher", "id": "HeroicGamesLauncher.HeroicGamesLauncher"},
        {"name": "Itch.io", "id": "ItchIo.Itch"},
        {"name": "Overwolf", "id": "Overwolf.Overwolf"},
        {"name": "Medal.tv", "id": "Medal.Medal"},
        {"name": "Prism Launcher", "id": "PrismLauncher.PrismLauncher"},
        {"name": "CurseForge", "id": "Overwolf.CurseForge"},
        {"name": "Vortex (Nexus Mods)", "id": "NexusMods.Vortex"}
    ],
    "Microsoft": [
        {"name": "DISMTools", "id": "CodingWonders.DISMTools"},
        {"name": ".NET Desktop Runtime 6", "id": "Microsoft.DotNet.DesktopRuntime.6"},
        {"name": ".NET Desktop Runtime 8", "id": "Microsoft.DotNet.DesktopRuntime.8"},
        {"name": ".NET Desktop Runtime 9", "id": "Microsoft.DotNet.DesktopRuntime.9"},
        {"name": "NTLite", "id": "NLite.NTLite"},
        {"name": "NuGet", "id": "Microsoft.NuGet"},
        {"name": "OneDrive", "id": "Microsoft.OneDrive"},
        {"name": "PowerShell", "id": "Microsoft.PowerShell"},
        {"name": "PowerToys", "id": "Microsoft.PowerToys"},
        {"name": "Sysinternals Process Monitor", "id": "Microsoft.Sysinternals.ProcessMonitor"},
        {"name": "Windows Terminal", "id": "Microsoft.WindowsTerminal"},
        {"name": "Windows Terminal Preview", "id": "Microsoft.WindowsTerminal.Preview"},
        {"name": "Windows Terminal Canary", "id": "Microsoft.WindowsTerminal.Canary"},
        {"name": "Visual C++ Redistributable (x86)(2015-2022x)", "id": "Microsoft.VCRedist.2015+.x86"},
        {"name": "Visual C++ Redistributable (x64)(2015-2022x)", "id": "Microsoft.VCRedist.2015+.x64"},
        {"name": "Visual C++ Redistributable (All in One: abbodi1406)", "id": "abbodi1406.vcredist"},
    ],
    "Multimedia": [
        {"name": "VLC Media Player", "id": "VideoLAN.VLC"},
        {"name": "AIMP", "id": "AIMP.AIMP"},
        {"name": "Audacity", "id": "Audacity.Audacity"},
        {"name": "OBS Studio", "id": "OBSProject.OBSStudio"},
        {"name": "K-Lite Codec Pack Standard", "id": "CodecGuide.K-LiteCodecPack.Standard"},
        {"name": "GIMP", "id": "GIMP.GIMP"},
        {"name": "HandBrake", "id": "HandBrake.HandBrake"},
        {"name": "ImageGlass", "id": "ImageGlass.ImageGlass"}
    ],
    "Tools": [
        {"name": "HWiNFO", "id": "REALiX.HWiNFO"},
        {"name": "HWMonitor", "id": "CPUID.HWMonitor"},
        {"name": "CPU-Z", "id": "CPUID.CPU-Z"},
        {"name": "CrystalDiskInfo", "id": "CrystalDewWorld.CrystalDiskInfo"},
        {"name": "CrystalDiskMark", "id": "CrystalDewWorld.CrystalDiskMark"},
        {"name": "Ventoy", "id": "Ventoy.Ventoy"},
        {"name": "XAMPP", "id": "ApacheFriends.XAMPP"},
        {"name": "WireGuard", "id": "WireGuard.WireGuard"},
        {"name": "AdGuard", "id": "Adguard.Adguard"},
        {"name": "ProtonVPN", "id": "Proton.ProtonVPN"},
        {"name": "NordVPN", "id": "NordSecurity.NordVPN"},
        {"name": "Advanced IP Scanner", "id": "Famatech.AdvancedIPScanner"},
        {"name": "Angry IP Scanner", "id": "AngryIPScanner.AngryIPScanner"},
        {"name": "FFmpeg", "id": "Gyan.FFmpeg"},
        {"name": "yt-dlp", "id": "yt-dlp.yt-dlp"}
    ],
    "Cloud": [
        {"name": "Google Drive", "id": "Google.Drive"},
        {"name": "Dropbox", "id": "Dropbox.Dropbox"},
        {"name": "Proton Drive", "id": "Proton.ProtonDrive"},
        {"name": "TeraBox", "id": "Flextech.TeraBox"}
    ],
    "Utilities": [
        {"name": "Spotify", "id": "Spotify.Spotify"},
        {"name": "1Password", "id": "1Password.1Password"},
        {"name": "7-Zip", "id": "7zip.7zip"},
        {"name": "NanaZip", "id": "M2Team.NanaZip"},
        {"name": "AnyDesk", "id": "AnyDeskSoftwareGmbH.AnyDesk"},
        {"name": "Bitwarden", "id": "Bitwarden.Bitwarden"},
        {"name": "Files App", "id": "yairm210.FilesApp"},
        {"name": "MSI Afterburner", "id": "Guru3D.Afterburner"},
        {"name": "OpenRGB", "id": "CalcProgrammer1.OpenRGB"},
        {"name": "SignalRGB", "id": "WhirlwindFX.SignalRGB"},
        {"name": "Rufus", "id": "Rufus.Rufus"},
        {"name": "qBittorrent", "id": "qBittorrent.qBittorrent"},
        {"name": "WinRAR", "id": "RARLab.WinRAR"},
        {"name": "Oracle VirtualBox", "id": "Oracle.VirtualBox"},
        {"name": "TeamViewer", "id": "TeamViewer.TeamViewer"},
        {"name": "Process Lasso", "id": "Bitsum.ProcessLasso"},
        {"name": "Proton Pass", "id": "Proton.ProtonPass"},
        {"name": "TreeSize Free", "id": "JAMSoftware.TreeSize.Free"},
        {"name": "Revo Uninstaller", "id": "VSRevoGroup.RevoUninstaller.Free"}
    ]
}

def verify_winget_availability():
    #Some windows (for whatever reason) dont even have winget installed by default. (bcs of certain custom ISOs)
    # So we need to check if it's available before proceeding.
    """
    Checks if 'winget' is recognized by the system environment.
    """
    try:
        # Im going to TRY explain what is happening here:
            # Run 'winget --version' to check if it's available, the text=True flag captures the output as text, not bytes, and check=True makes python raise error if the command fails for any reason on Windows.
            # So if the command succeeds winget its installed, if it fails we return False to indicate it's not available.
            # I think u can understand, otherwise why your looking at the comments?
        result = subprocess.run(["winget", "--version"], capture_output=True, text=True, check=True)
        return result.returncode == 0
    except FileNotFoundError: #if the "winget", "--version" dont get anything positive from the text... is not available, return False, simple as that.
        return False

def execute_package_install(package_id, package_name):
    """
    Triggers the installation of a specific package using Winget.
    Includes flags to silently accept agreements and prevent interactive prompts.
    """
    print(f"\n[Installer] Proceeding with the installation of: {package_name} ({package_id})")
    
    try:
        # Winget execution command with silent agreement flags (we dont want the user to be prompted...)
        command = [
            "winget", "install", "-e", "--id", package_id, 
            "--accept-package-agreements", "--accept-source-agreements"
        ]
            
        subprocess.run(command, check=True)
        print(f"[Success] {package_name} was successfully installed.")
    except subprocess.CalledProcessError:
        print(f"[Error] Winget encountered an error while installing {package_name}. It might be already installed or the ID changed.")

def build_app_mapping():
    """
    Iterates through the catalog, assigns a sequential numeric ID to each software,
    and returns a mapping dictionary to link user inputs to package definitions.
    """
    app_mapping = {}
    current_index = 1
    
    print("\n========================================")
    print("      SOFTWARE INSTALLATION CATALOG     ")
    print("========================================")
    
    for category, apps in SOFTWARE_CATALOG.items():
        print(f"\n--- {category} ---")
        for app in apps:
            print(f"{current_index}. {app['name']}")
            app_mapping[current_index] = app
            current_index += 1
            
    print("\n========================================")
    return app_mapping

def prompt_software_selection():
    """
    Displays the catalog to the user, parses the space-separated numeric inputs,
    and orchestrates the Winget download/installation pipeline.
    """
    # 1. Hard check for Winget before displaying anything
    if not verify_winget_availability():
        print("\n[Fatal Error] Winget is not recognized on this system.")
        print("[Action Log] Since third-party managers were disabled, this tool requires a native Windows 11 environment with Winget installed.")
        return

    # 2. Build catalog and display options
    app_mapping = build_app_mapping()
    
    user_input = input("\nEnter the numbers of the software you want to install, separated by spaces (e.g., '1 42 15'): ").strip()
    
    if not user_input:
        print("[Action Log] No input provided. Returning to main menu.")
        return
        
    # 3. Parse and filter input
    # Here we going to filter only the numbers (and valid numbers) through the list.
    selected_numbers = []
    for item in user_input.split():
        if item.isdigit():
            selected_numbers.append(int(item))
        else:
            print(f"[Input Warning] '{item}' is not a valid number and will be ignored.")

    valid_apps_to_install = []
    #if the user enter a number that is not in the app_mapping, it will be ignored. Simple :)
    for num in selected_numbers:
        if num in app_mapping:
            valid_apps_to_install.append(app_mapping[num])
        else:
            print(f"[Input Warning] Number '{num}' is out of range and will be ignored.")
            
    if not valid_apps_to_install: # If no valid apps were found, just return to the main menu.
        print("[Action Log] No valid software selections were found. Aborting operation.")
        return
        
    # 4. Final Confirmation
    print("\n[Confirmation] The following applications have been queued for installation:")
    for app in valid_apps_to_install:
        print(f" -> {app['name']}")
        
    confirm = input("\nDo you wish to proceed with the automated installation via Winget? (y/n): ").strip().lower()
    
    if confirm == 'y':
        for app in valid_apps_to_install:
            execute_package_install(app['id'], app['name'])
            
        print("\n[System Log] All queued installations have concluded.")
    else:
        print("\n[Action Log] Installation cancelled by the user. Returning to main menu.")