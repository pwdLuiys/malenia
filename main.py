# Lets import the detect module
from detect import analyze_gpu, detect_gpu
from scraper import search_driver

# the main thing...
if __name__ == "__main__":
    # simple var to store the list of GPUs found (the detect_gpu() function returned a list containing the names of the GPUs)
    gpu_list = detect_gpu()
    # simple var to store the brand of the GPU (the analyze_gpu() function returned the brand of the GPU)
    brand = analyze_gpu(gpu_list)
    # Iterate over the GPUs found and print their model and brand (maybe your rich and have more than one...)
    for gpu in gpu_list:
        print(f"GPU model: {gpu}")
        print(f"GPU brand: {brand}")
        search_driver(brand)
