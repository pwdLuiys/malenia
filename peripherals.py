# Importing the necessary modules for network requests, OS pathing, and subprocess execution.
import os
import requests
from bs4 import BeautifulSoup
import urllib.request
from installer import execute_package_install
#from scraper import manage_download_path

#DISCLAIMER: I had a HUGE list of peripherals sofwares, including Elgato, Attack Shark, and more. But no all of them have a "universal link for all models in one software"
# Most of them u have GO TO THE OFFICIAL WEBSITE and select by hand the model you want to download.
# I plan to make a script that automatically downloads the model you want from the official website just by providing the model name.
# But that's not yet implemented ofc, it'll be a future improvement.
# This dictionary maps the software to their respective Winget IDs.
# 'type' defines if we use the native Winget API (direct install) or our custom Scraper (file download).
# Once more... this list was made by AI, i used Gemini to search for the Winget IDs and make the dictionary.
PERIPHERALS_CATALOG = [
    {
        "name": "Logitech G HUB",
        "type": "winget",
        "id": "Logitech.GHUB"
    },
    {
        "name": "Razer Synapse 4",
        "type": "winget",
        "id": "Razer.Synapse"
    },
    {
        "name": "Corsair iCUE",
        "type": "winget",
        "id": "Corsair.iCUE"
    },
    {
        "name": "SteelSeries GG",
        "type": "winget",
        "id": "SteelSeries.GG"
    },
    {
        "name": "HyperX NGENUITY",
        "type": "winget",
        "id": "HP.HyperXNGENUITY"
    },
    {
        "name": "MSI Center",
        "type": "winget",
        "id": "MSI.MSICenter"
    },
    {
        "name": "HP OMEN Gaming Hub",
        "type": "winget",
        "id": "9NQDW009T0T5"
    },
    {
        "name": "Glorious Core",
        "type": "scraper",
        "url": "https://www.gloriousgaming.com/pages/software"
    }
]

def scrape_and_download_glorious(dest_path):
    """
    Custom scraper for Glorious Core.
    Parses the official HTML to extract the dynamic .exe installer link.
    """
    target_url = "https://www.gloriousgaming.com/pages/software"
    print("\n[Scraper Engine] Connecting to Glorious Gaming servers...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(target_url, headers=headers, timeout=10)
        response.raise_for_status() 
        
        soup = BeautifulSoup(response.text, "html.parser")
        download_link = None
        
        # Searching strictly for the .exe file as requested
        for a_tag in soup.find_all("a", href=True):
            href = str(a_tag["href"])
            if "GloriousCORE" in href and ".zip" in href.lower():
                download_link = href
                break
                
        if not download_link:
            print("[Scraper Error] Direct .exe download link not found in the HTML structure. Glorious might have updated their site.")
            return

        if download_link.startswith("//"):
            download_link = "https:" + download_link
            
        print(f"[Scraper] Discovered valid installer link: {download_link}")
        
        file_name = download_link.split("/")[-1] 
        final_file_path = os.path.join(dest_path, file_name)
        
        print(f"[Scraper Engine] Downloading file (this might take a few minutes)...")
        urllib.request.urlretrieve(download_link, final_file_path)
        print(f"[Success] Glorious Core successfully downloaded to: {final_file_path}")
        
    except requests.exceptions.RequestException as e:
        print(f"[Network Error] Failed to connect to the Glorious website: {e}")
    except Exception as e:
        print(f"[Critical Error] Scraper processing failed: {e}")

def manage_download_path():
    """
    Determines the target directory for downloaded installers.
    Reused logic from the GPU scraper module.
    """
    default_dir = os.path.join(os.environ.get("USERPROFILE"), "Downloads", "Malenia_Peripherals")
    
    print(f"\n[Directory Manager] The default download directory is: {default_dir}")
    choice = input("Do you want to download the installer(s) here? (y/n): ").strip().lower()
    
    if choice == 'y' or choice == '':
        target_dir = default_dir
    else:
        target_dir = input("Enter the full custom path (e.g., D:\\MyPrograms): ").strip()
        if not target_dir:
            print("[Warning] Invalid path provided. Falling back to the default directory.")
            target_dir = default_dir
            
    # Creating the directory safely if it doesn't exist
    if not os.path.exists(target_dir):
        try:
            os.makedirs(target_dir)
            print(f"[System] Directory '{target_dir}' created successfully.")
        except Exception as e:
            print(f"[Error] Failed to create directory. Falling back to standard Downloads folder. Error: {e}")
            target_dir = os.path.join(os.environ.get("USERPROFILE"), "Downloads")
            
    return target_dir

def prompt_peripherals_menu():
    """
    Renders the Peripherals catalog, parses user input, and distributes 
    tasks to their respective engines (System Install vs File Download).
    """
    print("\n========================================")
    print("     PERIPHERALS SOFTWARE MANAGEMENT    ")
    print("========================================")
    
    for i, peripheral in enumerate(PERIPHERALS_CATALOG, start=1):
        peripheral["index"] = i
        print(f"{i}. {peripheral['name']}")
    print("========================================")

    user_input = input("\nEnter the numbers of the software you want to process, separated by spaces (e.g., '1 2 8'): ").strip()
    if not user_input:
        print("[Action Log] No input provided. Returning to main menu.")
        return

    # Parsing strings to integers safely
    selected_indexes = []
    for token in user_input.split():
        if token.isdigit():
            selected_indexes.append(int(token))
            
    # Validating against the catalog bounds
    valid_selections = [p for p in PERIPHERALS_CATALOG if p["index"] in selected_indexes]
    
    if not valid_selections:
        print("[Action Log] No valid options selected. Aborting.")
        return

    print("\n[PREVIEW] The following tasks will be executed:")
    for app in valid_selections:
        action_text = "Install directly via OS" if app["type"] == "winget" else "Download installer via Scraper"
        print(f" -> {app['name']} [{action_text}]")

    confirm = input("\nDo you wish to proceed? (y/n): ").strip().lower()
    
    if confirm == 'y':
        # We only prompt for a download path if a scraper-based software (Glorious) was selected
        requires_download_path = any(app["type"] == "scraper" for app in valid_selections)
        target_directory = manage_download_path() if requires_download_path else None
        
        print("\n[System] Initiating batch peripheral software pipeline...")
        for app in valid_selections:
            if app["type"] == "winget":
                execute_package_install(app["id"], app["name"])
            elif app["type"] == "scraper":
                scrape_and_download_glorious(target_directory)
                
        print("\n[System Log] Peripheral software pipeline completed.")
    else:
        print("[Action Log] Operation cancelled by the user.")