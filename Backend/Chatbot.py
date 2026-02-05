from groq import Groq
from json import load,dump
import datetime
from dotenv import dotenv_values

env_vars = dotenv_values(".env")

# retrieve specific environment variables for username, assitant name, api
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

#initailize groq client using api key
client = Groq(api_key=GroqAPIKey)

#initialize empty list to store chat messages
# messages = []

#provide system message that provides context to ai chatbot about its role and behavour
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI agent named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

#list of system instructions for the chatbot
SystemChatBot = [
    {"role": "system", "content": System}
]

#attempt to load the chat log from json file
try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
except FileNotFoundError:
    # if file doesnot exist create an empty json file for chatlog
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)
    
# function to get realtime data and time information
def RealtimeInformation():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date= current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")
    
    #format informatiion into string
    data = f"Please use this real-time information if needed, \n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours, {minute} minutes, {second} seconds. \n"
    return data

#function to modify the chatbot's response for better formatting
def AnswerModifier(Answer):
    lines = Answer.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = "\n".join(non_empty_lines)
    return modified_answer

#main chatbot function to handle user queries
def ChatBot(Query):
    """ This function sends the user's query to the chatbot and returns the AI's response. """ 
    messages = []  # ensure messages is always defined
    try:
        #load the exsiting chatlog from json file
        with open(r"Data\ChatLog.json", "r") as f:
            messages = load(f)
            
        #append the user queries to messages list
        messages.append({"role": "user", "content": f"{Query}"})
        
        # Make a request to Groq api for a response
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages = SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,
            max_tokens = 1024,
            temperature=0.7,
            top_p=1,
            stream = True,
            stop=None
        )
        Answer = ""
        
        for chunk in completion:
            if chunk.choices[0].delta.content: # check if there is content in current chunk
                Answer += chunk.choices[0].delta.content #append the content in the answer
        Answer = Answer.replace("</s>", "")
        
        #Append the chatbot's response to the message list
        messages.append({"role": "assistant", "content": Answer})
        
        #save the updated chatlog to json file
        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f, indent=4)
            
        #return the formatted response
        return AnswerModifier(Answer=Answer)
    
    except Exception as e:
        print(f"Error: {e}")
        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f, indent=4)
        return ChatBot(Query)

#main program entry point
if __name__ == "__main__":
    while True:
        user_input = input("Enter your question: ")
        print(ChatBot(user_input))
        