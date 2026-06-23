# Lets import the detect module
from detect import analyze_gpu, detect_gpu
from scraper import search_driver
# Importing the newly created software installer module
from installer import prompt_software_selection
from uninstaller import prompt_software_removal

def display_menu():
    """
    Prints a clean and stylized Command Line Interface (CLI) menu 
    for the Malenia Post Format Tool application.
    """
    print("\n========================================")
    print("     MALENIA POST FORMAT TOOL (CLI)     ")
    print("========================================")
    print("1. Download GPU Drivers")
    print("2. Install Essential Software")
    print("3. Uninstall System Software")
    print("4. Exit Application")
    print("========================================")

if __name__ == "__main__":
    # Main application loop to keep the CLI running until explicit exit command (basic stuff but important to explain)
    while True:
        display_menu()
        user_choice = input("Select an option (1-4): ").strip()

        if user_choice == "1":
            # Confirmation step to ensure the user did not trigger the process by mistake
            confirm_task = input("\nAre you sure you want to initialize the GPU Driver Download task? (y/n): ").strip().lower()
            
            if confirm_task == 'y':
                print("\n[System] Initializing hardware assessment pipeline...")
                
                # simple var to store the list of GPUs found
                gpu_list = detect_gpu()
                
                # simple var to store the brand of the GPU
                brand = analyze_gpu(gpu_list)
                
                # Iterate over the GPUs found and print their model and brand
                for gpu in gpu_list:
                    print(f"GPU model: {gpu}")
                    print(f"GPU brand: {brand}")
                    search_driver(brand)
            elif confirm_task == 'n':
                print("\n[Action Log] Task cancelled by the user. Returning to main menu.")
            else:
                print("\n[Input Error] Invalid confirmation input. Task aborted.")

        elif user_choice == "2":
            # Initializes the software installation logic handling
            prompt_software_selection()

        elif user_choice == "3":
            # Initializes the uninstallation logic handling
            prompt_software_removal()

        elif user_choice == "4":
            print("\n[System] Shutting down Malenia Post Format Tool. Goodbye.")
            break # Breaks the while loop, safely closing the execution
            
        else:
            print("\n[Input Error] Invalid selection. Please enter a number between 1 and 3.")