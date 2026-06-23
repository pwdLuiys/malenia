import os
import socket
import ssl
import urllib.error
import urllib.request

import requests
from bs4 import BeautifulSoup

# im watching FURIA x AURORA rn, FURIA won omg, thats amaizing.
# Big fan of Counter Strike 2 :)
# Spirit 1 x Falcons 1
# Theyre in DUST 2 now, decider map for the grand final, 7 to 7 rounds... lets see
# Update: 3 Falcons - 0 Furia (i forgot to say it here)
# FURIA lost in the finals, im sad :(


def scrape_nvidia():
    """
    Connects to the official NVIDIA App website, parses the HTML content,
    searches for a direct download link matching the target keywords,
    and returns the URL of the installer executable (.exe).
    """
    print(
        "\n[Scraper] Entering NVIDIA website to search for the NVIDIA App installer..."
    )

    # Target URL for the NVIDIA App software page
    # If they change the URL, this will need to be updated, as the scraper will not work with the new URL.
    # If you read this and the URL is no longer valid, please contact me.
    url = "https://www.nvidia.com/en-us/software/nvidia-app/"
    # NVIDIA PLEASE DONT CHANGE THE URL.

    # Standard browser User-Agent header to prevent the server from blocking the automated request
    # Silly but necessary to avoid detection as a bot.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        # Performing the HTTP GET request to fetch the webpage content
        response = requests.get(url, headers=headers, timeout=10)

        # Check if the request was successful (HTTP Status Code 200)
        # HTTP Status Code 200 indicates a successful request btw
        if response.status_code == 200:
            # Parsing the raw HTML content using BeautifulSoup (Im sorry NVIDIA)
            # This is like transforming HTML into a structured format (a tree of tags) so we can easily navigate and extract data :)
            soup = BeautifulSoup(response.content, "html.parser")

            # Initializing the variable that will store the final link
            driver_link = None

            # Iterating through all anchor tags (<a>) that contain an 'href' attribute
            for link in soup.find_all("a", href=True):
                href = link["href"]

                # Check if the link contains the keyword 'download' and ends with '.exe'
                if "download" in href and href.endswith(".exe"): # type: ignore
                    # In my IDE rn the "endswith" is causing error... but it works fine in the terminal. Dont question me.
                    # Extracting the absolute URL from the href attribute
                    driver_link = link.get("href")
                    # as soon as we find a suitable link, we break out of the loop
                    break

            # Validating if a suitable link was found during the loop
            if driver_link:
                print(f"Successfully found target installer link: {driver_link}")
                return driver_link
            else:
                print(
                    "Warning: No driver installer link matched the criteria in the HTML."
                )
                return None
        else:
            print(
                f"Error: Failed to access NVIDIA page. Status code: {response.status_code}"
                # This could be due to a network issue, a DNS problem, or a timeout (if your network is slow as fuck)
                # I might consider adding a retry mechanism here or just adding a longer timeout
            )
            return None

    except requests.exceptions.RequestException as e:
        # Gracefully catching any network, DNS, or timeout exception from the requests library
        print(f"[Scraper] A network error occurred during scraping: {e}")
        return None


def scrape_amd():
    """
    Connects to the official AMD Driver Support website, parses the HTML content,
    searches for the direct Auto-Detect / Minimal Setup installer link (.exe),
    and returns the absolute URL string.
    """
    print("\n[Scraper] Entering AMD website to search for the Auto-Detect installer...")
    url = "https://www.amd.com/en/support/download/drivers.html"

    # same bla bla bla, but more "security" from AMD's website, theyre more likely to block requests from generic user-agents
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            driver_link = None

            # Iterating through all links on the AMD support page
            for link in soup.find_all("a", href=True):
                href = link["href"]

                # Matching criteria: Must contain 'minimalsetup' or 'auto-detect' or 'amd-software' and end with '.exe'
                if (
                    "minimalsetup" in href.lower()
                    or "auto-detect" in href.lower()
                    or "amd-software" in href.lower()
                ) and href.endswith(".exe"):
                    driver_link = href
                    break

            if driver_link:
                print(
                    f"[Scraper] Successfully found AMD target installer link: {driver_link}"
                )
                return driver_link
            else:
                print(
                    "[Scraper] Warning: No AMD installer link matched the criteria in the HTML."
                )
                return None
        else:
            print(
                f"[Scraper] Error: Failed to access AMD page. Status code: {response.status_code}"
            )
            return None
    except requests.exceptions.RequestException as e:
        print(f"[Scraper] A network error occurred during AMD scraping: {e}")
        return None


def scrape_intel():
    """
    Validates the persistent endpoint for the Intel Driver & Support Assistant.
    Since Intel provisions a direct static endpoint that directly acts as the binary
    stream source, we securely return the validated destination endpoint.
    """
    print("\nValidating Intel direct installer endpoint repository...")
    driver_link = "https://dsadata.intel.com/installer"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        # Performing a fast HEAD request to check availability before launching heavy transport operations
        response = requests.head(
            driver_link, headers=headers, allow_redirects=True, timeout=10
        )
        if response.status_code == 200:
            print(
                f"[Scraper] Successfully validated Intel persistent link: {driver_link}"
            )
            return driver_link
        else:
            print(
                f"[Scraper] Error: Intel endpoint answered with unusual status code: {response.status_code}"
            )
            return None
    except requests.exceptions.RequestException as e:
        print(f"[Scraper] A network error occurred during Intel verification: {e}")
        return None


def execute_driver_download(driver_link, target_directory, brand):
    """
    Attempts to download the executable file from the provided URL using urllib with a strict timeout,
    saving it into the user-defined target directory.
    """

    #So, INTEL drivers had problem, whenever i tried do download them, the file name NEVER came correctly, so i have to manually define this if/else to define the file name based on the brand var.
    if brand == "INTEL":
        file_name = "Intel-Driver-and-Support-Assistant-Installer.exe"
    else:
        file_name = driver_link.split("/")[-1]

    full_destination_path = os.path.join(target_directory, file_name)

    print(f"\n[Download] Commencing download of {file_name}...")
    print(f"[Download] Saving file to target location: {full_destination_path}")

    try:
        ssl_context = ssl._create_unverified_context()

        # Creating a specific Request object to inject complete browser headers
        # This simulates a real user click from the AMD driver page to bypass silent drops
        request_object = urllib.request.Request(
            driver_link,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Referer": "https://www.intel.com/"
                if brand == "INTEL"
                else "https://www.amd.com/",
                "Accept": "*/*",
                "Connection": "keep-alive",
            },
        )

        # Opening the connection with a strict 15-second timeout to prevent infinite freezing
        print("[Download] Connecting to the remote binary repository...")
        with urllib.request.urlopen(
            request_object, timeout=15, context=ssl_context
        ) as response:
            # Creating or overwriting the target file in binary mode
            with open(full_destination_path, "wb") as local_file:
                # Reading the stream in small chunks (8KB) to ensure low RAM footprint
                while True:
                    chunk = response.read(8192)
                    if not chunk:
                        break
                    local_file.write(chunk)

        print(
            f"[Success] Download complete! File securely saved at: {os.path.abspath(full_destination_path)}"
        )
        return os.path.abspath(full_destination_path)

    except urllib.error.URLError as e:
        print(
            f"[Download Error] Network or timeout failure during urllib transport: {e.reason}"
        )
        return None
    except socket.timeout:
        print(
            "[Download Error] Connection timed out. AMD server refused to stream the file data."
        )
        return None
    except Exception as e:
        print(
            f"[Download Error] An unexpected error occurred while writing the file: {e}"
        )
        return None


def manage_download_path(driver_link):
    """
    Handles user interaction regarding the destination folder, checks if a file
    with the exact same name already exists in that path, and asks the user
    if they wish to overwrite it or abort the operation.
    """
    # Extracting the file name from the URL to use for the local existence check
    file_name = driver_link.split("/")[-1]

    # Defining the default Windows user 'Downloads' folder path dynamically
    user_home = os.path.expanduser("~")
    default_downloads_folder = os.path.join(user_home, "Downloads")

    print(
        f"\n[Path Setup] Default download directory is set to: {default_downloads_folder}"
    )

    # Loop to determine and validate the chosen download directory path
    while True:
        user_choice = (
            input("Do you want to download to the default Downloads folder? (y/n): ")
            .strip()
            .lower()
        )

        if user_choice == "y":
            chosen_directory = default_downloads_folder
            break
        elif user_choice == "n":
            custom_path = input(
                "Enter the full absolute path where you want to save the file: "
            ).strip()
            # Validating if the directory provided by the user actually exists on the operating system
            if os.path.exists(custom_path) and os.path.isdir(custom_path):
                chosen_directory = custom_path
                break
            else:
                print(
                    "[Path Error] The path entered does not exist or is not a directory. Please try again."
                )
        else:
            print("[Input Error] Invalid entry. Please type 'y' for Yes or 'n' for No.")

    # Constructing the complete file path to verify its existence prior to downloading
    target_file_path = os.path.join(chosen_directory, file_name)

    # Checking if a file with the exact same name already exists in the target directory
    if os.path.exists(target_file_path):
        print(
            f"\n[Conflict Alert] A file named '{file_name}' already exists at this location."
        )

        # Loop to handle user confirmation regarding overwriting the file
        while True:
            overwrite_choice = (
                input(
                    "Do you want to delete the existing file and download the new one? (y/n): "
                )
                .strip()
                .lower()
            )

            if overwrite_choice == "y":
                try:
                    print(f"[File System] Removing older file: {target_file_path}")
                    # Safely removing the pre-existing file from the disk
                    os.remove(target_file_path)
                    print("[File System] Old file successfully removed.")
                    break
                except Exception as e:
                    print(f"[File System Error] Failed to delete existing file: {e}")
                    print(
                        "[Action Log] Aborting download task due to file system lock."
                    )
                    return None
            elif overwrite_choice == "n":
                print(
                    "[Action Log] Task cancelled by the user. The existing file was preserved."
                )
                return None
            else:
                print(
                    "[Input Error] Invalid entry. Please type 'y' to overwrite or 'n' to cancel."
                )

    # If there is no conflict or the conflict was resolved by deletion, proceed to download
    return chosen_directory


def search_driver(brand):
    """
    Main orchestrator for the scraping and download workflow based on the detected hardware brand.
    """
    if brand == "NVIDIA":
        # Step 1: Scrape the NVIDIA page to discover the installer link
        discovered_link = scrape_nvidia()

        if discovered_link:
            # Step 2: Interact with the user to manage paths, checks, and conflicts
            target_folder = manage_download_path(discovered_link)

            # Step 3: If a valid path is returned (and user didn't cancel), execute the urllib download
            if target_folder:
                execute_driver_download(discovered_link, target_folder, brand)
        else:
            print(
                "[Orchestrator] Aborting workflow because no valid installer link could be extracted."
            )

    elif brand == "AMD":
        # Step 1: Scrape the AMD page to discover the installer link
        discovered_link = scrape_amd()

        if discovered_link:
            # Step 2: Interact with the user to manage paths, checks, and conflicts
            target_folder = manage_download_path(discovered_link)

            # Step 3: If a valid path is returned (and user didn't cancel), execute the urllib download
            if target_folder:
                execute_driver_download(discovered_link, target_folder, brand)
        else:
            print(
                "[Orchestrator] Aborting workflow because no valid installer link could be extracted."
            )
    elif brand == "INTEL":
        # Step 1: Scrape the Intel page to discover the installer link
        discovered_link = scrape_intel()

        if discovered_link:
            # Step 2: Interact with the user to manage paths, checks, and conflicts
            target_folder = manage_download_path(discovered_link)

            # Step 3: If a valid path is returned (and user didn't cancel), execute the urllib download
            if target_folder:
                execute_driver_download(discovered_link, target_folder, brand)
        else:
            print(
                "[Orchestrator] Aborting workflow because no valid installer link could be extracted."
            )
