import win32com.client


def detect_gpu():
    try:
        # Make sure to import win32com.client before using it
        # create a wmi object to query the Win32_VideoController class
        wmi = win32com.client.GetObject("winmgmts:")
        # query the Win32_VideoController class to get the name of each GPU
        video_controllers = wmi.ExecQuery("SELECT Name FROM Win32_VideoController")

        # create a list to store the names of the GPUs found
        gpus_found = []

        # iterate over the video controllers and add their names to the list
        for controller in video_controllers:
            gpus_found.append(controller.Name)
            print(f"Detected: {controller.Name}")
        return gpus_found
    except Exception as e:
        print(f"Possible error within wmi: {e}")
        return []


def analyze_gpu(gpus_found):
    if not gpus_found:
        print("None GPU detected")
        # Seriously how? Your not supposed to have 0 GPUs... like if PSUs are considered a "GPU" too, i just gonna let this pass and make this if else bro
        return []

    gpu_zero = gpus_found[0].upper()
    if "NVIDIA" in gpu_zero:
        return "NVIDIA"
    elif "AMD" in gpu_zero or "RADEON" in gpu_zero:
        return "AMD"
    elif "INTEL" in gpu_zero:
        return "INTEL"
    else:
        return "Unknown"
        # So you make your own... or something like that? holly homelab. Calm down Linus Torvald, Pornelius Hubersson, or anyone else


# Listen idk WHY i created two defs just for it... but it works, im going to change it later, i just wanted to get it working first.
# Or maybe not.. who knows?
