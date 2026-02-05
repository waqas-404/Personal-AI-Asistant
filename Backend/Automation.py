from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
import urllib.parse
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os

#load the env variables from .env file
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

#define CSS CLASSES for parsing specific elements to HTML content
classes = ["zCubwf", "hgKElc", "LTKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta",
           "IZ6rdc", "05uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table__webanswers-table", "dDoNO ikb48b gsrt", "sXLaOe", 
           "LWkfke", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

#define a user-agent for making web requests
useragent = 'Mozilla/5.0 (Windows NT 10.0: Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

#Initailize the Groq client with the API Key
client = Groq(api_key = GroqAPIKey)

#predefined professional responses for user interaction
professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at you service for any additional questions or support you may need-don't hesitate to ask.",
]

#List to store messages
messages = []

# system messages to provide context to the chatbot
SystemChatBot = [
    {"role": "system", "content": f"Hello, I am {os.environ['username']}, You're a content writer. You have to write content like letters, applications, stories and create music symphonies "}
]

#function to perform search
def GoogleSearch(Topic):
    search(Topic) #use pywhatkit's search function to perform a Google Search
    return True #indicate success

#function to generate content using AI  and save it as a file
def Content(Topic):
    
    #nested function to open a file in notepad.
    def OpenNotepad(File):
        default_text_editor = "notepad.exe" #default text editor
        subprocess.Popen([default_text_editor, File]) #open the file in notepad
    
    #nested function to generate content using AI chatbot
    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"})
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", #specify the AI model
            messages = SystemChatBot + messages, 
            max_tokens = 2048,
            temperature= 0.7, #adjust the response randomness
            top_p = 1, #use nucleus sampling for response diversity
            stream = True, #enable streaming response
            stop = None #allow the model to determine stopping conditions
        )
        
        Answer = "" #initialize and empty string for the response
        
        #proceed streamed response chunks
        for chunk in completion:
            if chunk.choices[0].delta.content: #check for content in the current chunk
                Answer += chunk.choices[0].delta.content #append the content to the answer
        
        Answer = Answer.replace("</s>", "") #remove unwanted tokens from the response
        messages.append({"role": "assistant", "content": Answer}) # add the AI response to the messages
        return Answer
    
    Topic: str = Topic.replace("Content ", "") #remove the "Content" from the topic
    ContentByAI = ContentWriterAI(Topic) #generate content using AI
    
    #Save the generate content to a text file
    with open(rf"Data\{Topic.lower().replace(' ', '')}.txt", "w", encoding="utf-8") as file:
        file.write(ContentByAI) #write the content to the file
        file.close()
    
    OpenNotepad(rf"Data\{Topic.lower().replace(' ', '')}.txt") #open the file in Notepad
    return True #indicate success

#Function to search for a topic on youtube
def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}" #construct the YouTube search URL
    webbrowser.open(Url4Search) #open the search URL  in the web browser
    return True #Indicate success

#define function to play a video on YouTube
def PlayYoutube(query):
    playonyt(query) # Use pywhatkit's playonyt function to play the video
    return True

#Function to oopen a application or a relevent webpage
def OpenApp(app, sess=requests.session()):
    app = (app or "").strip().lower()

    web_apps = {
        "youtube": "https://www.youtube.com",
        "instagram": "https://www.instagram.com",
        "facebook": "https://www.facebook.com",
        "gmail": "https://mail.google.com",
        "whatsapp": "https://web.whatsapp.com",
        "chatgpt": "https://chat.openai.com",
        "openai": "https://openai.com",
        "notion": "https://www.notion.so",
        "canva": "https://www.canva.com",
        "figma": "https://www.figma.com",
        "etsy": "https://www.etsy.com",
        "google": "https://www.google.com",
        "maps": "https://maps.google.com",
        "google maps": "https://maps.google.com",      
                                 
    }
    
    # 1) Try to open installed app first
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except Exception:
        pass
    
    # 2) If not installed, open website if known
    if app in web_apps:
        webbrowser.open(web_apps[app])
        return True

    # 3) Final fallback: open a Google search page (no scraping)
    q = urllib.parse.quote_plus(app)
    webbrowser.open(f"https://www.google.com/search?q={q}")
    return True
    # try:
    #     appopen(app, match_closest=True, output=True, throw_error=True) #attempt to opent the app
    #     return True 
    # except:
    #     #nested function to extract links from HTML content
    #     def extract_links(html):
    #         if html is None:
    #             return []
    #         soup = BeautifulSoup(html, 'html.parser') #parse the HTML content
    #         links = soup.find_all('a', {'jsname': 'UWckNb'}) #Find the relevant links
    #         return [link.get('href') for link in links] #return the links
    #     # Nested function to perform google search and retrieve HTML
    #     def search_google(query):
    #         url = f"https://www.google.com/search?q={query}" # Construct the Google search URL
    #         headers = {"User-Agent":useragent}  # Use the predefned user-agent
    #         response = sess.get(url, headers=headers)  #perform the GET request.
            
    #         if response.status_code == 200:
    #             return response.text #return the HTML content
    #         else:
    #             print("Failed to retrieve search results.") #print error message
    #         return None
        
    #     html = search_google(app) #perform the google search
        
    #     if html:
    #         link = extract_links(html)[0] # Extract the first link from the search results
    #         webopen(link) # Open the link in the web browser
            
    #     return True

# Function to close an application
def CloseApp(app):
    if "chrome" in app:
        pass  # Skip if the app is chrome
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True) # Attempt to close the app
            return True # Indicate success
        except:
            return False # Indicate failure
        
# Function to execute system level commands.
def System(command):
    
    #nested function to mute the system volume
    def mute():
        keyboard.press_and_release("volume mute") #simulate the mute key press
        
    #nested function to unmute the system volume
    def unmute():
        keyboard.press_and_release("volume mute") #simulate the unmute key press
        
    #nested function to increase the system volume
    def volume_up():
        keyboard.press_and_release("volume up") #simulate the volume up key press
    
    #nested function to decrease the system volume
    def volume_down():
        keyboard.press_and_release("volume down") #simulate the volume down key press
        
    #Execute the appropriate command
    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()
    
    return True

# Asynchronous function to translate and execute user commands
async def TranslateAndExecute(commands: list[str]):
    
    funcs = [] #list to store asynchronous tasks
    
    for command in commands:
        if command.startswith("open "): #handle 'open' commands
            
            if "open it" in command: #ignore "open it" commands
                pass
            
            if "open file" == command: # ignore 'open file' commands
                pass
            
            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open"))  #schedule app opening
                funcs.append(fun)
                
            
        elif command.startswith("general "):  #placeholder for general commands
            pass
        
        elif command.startswith("realtime "): # placeholder for real-time commands
            pass
        
        elif command.startswith("close "):  #handle "close" commands
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close ").strip())  #schedule app closing
            funcs.append(fun)
        
        elif command.startswith("play "): # handle "play " commands
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play ").strip())  #schedule YouTube video playback
            funcs.append(fun)
            
        elif command.startswith("content "): #handle "content" commands
            fun = asyncio.to_thread(Content, command.removeprefix("content ").strip())  #schedule content generation
            funcs.append(fun)
            
        elif command.startswith("google search "): #handle google search commands
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search ").strip())  #schedule google search
            funcs.append(fun)
        
        elif command.startswith("youtube search "): #handle youtube search commands
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search ").strip())  #schedule youtube search
            funcs.append(fun)
            
        elif command.startswith("system "): #handle system commands
            fun = asyncio.to_thread(System, command.removeprefix("system ").strip())  #schedule system command execution
            funcs.append(fun)
            
        else:
            print(f"No Function Found For {command}") #print error for unrecognized commands
            
    results = await asyncio.gather(*funcs, return_exceptions=True)

    for r in results:
        if isinstance(r, Exception):
            print("Automation task error:", repr(r))
            
 #execute all scheduled tasks concurrently
    
    for result in results: #process the results
        if isinstance(result, str):
            yield result
        else:
            yield result

#asynchronous function to automate command execution
async def Automation(commands: list[str]):
    
    async for result in TranslateAndExecute(commands): #tranlate and execute commands
        pass
    
    return True #indicate success