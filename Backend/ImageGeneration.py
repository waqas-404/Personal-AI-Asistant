# import asyncio
# from random import randint
# from PIL import Image
# import requests
# from dotenv import get_key
# import os
# from time import sleep

# #function to open and display images based on a given prompt
# def open_images(prompt):
#     folder_path = r"Data" #Folder where the images are stored
#     prompt = prompt.replace(" ", "_") # replace spaces in prompt with underscores
    
#     #generate the filenames for the images
#     Files = [f"{prompt}{i}.jpg" for i in range(1,5)]
    
#     for jpg_file in Files:
#         image_path = os.path.join(folder_path, jpg_file) #create the full path to the image file
        
#         try:
#             #try to open and display the image
#             img = Image.open(image_path)
#             print(f"Opening image: {image_path}")
#             img.show()
#             sleep(1)  # Pause for 1 second before showing the next image
            
#         except IOError:
#             print(f"Unable to open {image_path}")

# # API details for Hugging Face stable diffusion model
# API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
# headers = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"}

# #Async function to send a query to the Hugging Face API
# async def query(payload):
#     response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
#     return response.content

# # Async function to generate images based on the given prompt
# async def generate_images(prompt: str):
#     tasks = []
    
#     #create 4 image generation tasks
#     for _ in range(4):
#         payload = {
#             "inputs": f"{prompt}, quality=4k, sharpness = maximum, Ultra High details, high resolution, seed = {randint(0, 1000000)}",
#         }
#         task = asyncio.create_task(query(payload))
#         tasks.append(task)
        
#     #wait for all tasks to complete
#     image_bytes_list = await asyncio.gather(*tasks)
    
#     #save the generated images to files
#     for i, image_bytes in enumerate(image_bytes_list):
        
#         with open(fr"Data\{prompt.replace(' ', '_')}{i + 1}.jpg", "wb") as f:
#             f.write(image_bytes)

# # Wraper function to generate and open images
# def GenerateImages(prompt: str):
#     asyncio.run(generate_images(prompt))  #generate images asynchronously
#     open_images(prompt)  #open the generated images

# # Main loop to monitor for image generation requests
# while True:
    
#     try:
#         #read the status and prompt from the data file
#         with open(r"Frontend\Files\ImageGeneration.data", "r") as f:
#             Data: str = f.read()
        
#         Prompt, Status = Data.split(",")  #split the data into prompt and status
        
#         #if the status indicates and image generation request
#         if Status == "True":
#             print("Generating Images...")
#             ImageStatus = GenerateImages(prompt=Prompt)
            
#             #reset the status in the file after generating images
#             with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
#                 f.write("False,False")
#                 break #exit the loop after processing the request
            
#         else:
#             sleep(1) #wait for 1 second before checking again
    
#     except:
#         pass


import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
from time import sleep
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")
FLAG_FILE = os.path.join(BASE_DIR, "Frontend", "Files", "ImageGeneration.data")
DATA_DIR = os.path.join(BASE_DIR, "Data")

#function to open and display images based on a given prompt
def open_images(prompt):
    prompt_key = prompt.replace(" ", "_")
    files = [f"{prompt_key}{i}.jpg" for i in range(1, 5)]

    for name in files:
        image_path = os.path.join(DATA_DIR, name)

        if not os.path.exists(image_path):
            print("Not found:", image_path)
            continue

        # verify image is valid (not JSON error)
        try:
            with Image.open(image_path) as im:
                im.verify()
        except Exception as e:
            print("Invalid image:", image_path, e)
            continue

        print("Opening:", image_path)

        # Windows native open (Photos app)
        os.startfile(image_path)

        time.sleep(0.5)

# API details for Hugging Face stable diffusion model
API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")

headers = {"Authorization": f"Bearer {get_key(ENV_PATH, 'HuggingFaceAPIKey')}"}

#Async function to send a query to the Hugging Face API
async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    return response.content

# Async function to generate images based on the given prompt
async def generate_images(prompt: str):
    tasks = []
    
    #create 4 image generation tasks
    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4k, sharpness = maximum, Ultra High details, high resolution, seed = {randint(0, 1000000)}",
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)
        
    #wait for all tasks to complete
    image_bytes_list = await asyncio.gather(*tasks)
    
    #save the generated images to files
    for i, image_bytes in enumerate(image_bytes_list):
        
        out_path = os.path.join(DATA_DIR, f"{prompt.replace(' ', '_')}{i + 1}.jpg")
        with open(out_path, "wb") as f:
            f.write(image_bytes)

# Wraper function to generate and open images
def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt))  #generate images asynchronously
    open_images(prompt)  #open the generated images

# Main loop to monitor for image generation requests
while True:
    
    try:
        #read the status and prompt from the data file
        with open(r"Frontend\Files\ImageGeneration.data", "r") as f:
            Data: str = f.read()
        
        Prompt, Status = Data.split(",")  #split the data into prompt and status
        
        #if the status indicates and image generation request
        if Status == "True":
            print("Generating Images...")
            ImageStatus = GenerateImages(prompt=Prompt)
            
            #reset the status in the file after generating images
            with open(FLAG_FILE, "w", encoding="utf-8") as f:
                f.write("False,False")
                break #exit the loop after processing the request
            
        else:
            sleep(1) #wait for 1 second before checking again
    
    except:
        pass