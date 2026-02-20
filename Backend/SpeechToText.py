from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt
import time

#load env variables
env_vars = dotenv_values(".env")

#get the input language setting from env variables
InputLanguage = env_vars.get("InputLanguage")

#desing the html code for speech recognition interface
HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

# replace the language setting in the HTML code within the input language from the env variables
HtmlCode = str(HtmlCode).replace("recognition.lang = ' ';", f"recognition.lang = '{InputLanguage}';")

#write the modified code to the file
with open(r"Data/Voice.html", "w") as f:
    f.write(HtmlCode)
    
# Get the current working directory
current_dir = os.getcwd()
#generat the file path
Link = f"{current_dir}/Data/Voice.html"

#set chrome options for webdriver
chrome_options = Options()
user_agent = (
    "Mozilla/5.0 (X11; Linux x86_64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)
chrome_options.add_argument(f"user-agent={user_agent}")
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
# chrome_options.add_argument("--headless=new")

#Initialize chrome webdriver using the ChromeDriverManager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

#define the path for temporary file

TempDirPath = rf"{current_dir}/Frontend/Files"
os.makedirs(TempDirPath, exist_ok=True)

#Function to set the assistant status by writing it to a file
def SetAssistantStatus(Status):
    with open(rf"{TempDirPath}/Status.data", "w", encoding='utf-8') as file:
        file.write(Status)

#Function to modify query to ensure proper punctuation and formatting
def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "why", "which", "whose", "whom",
                      "can you", "what's", "where's", "how's", "do you", "if"]
    # check if the query is a question and add a question mark if necessary
    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        # Add a period if the query is not a question
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."
    return new_query.capitalize()

#Function to translate text into English using the mtranslate
def UniversalTranslator(Text):
    english_translation= mt.translate(Text, "en", "auto")
    return english_translation.capitalize()

#Function to perform speech recognition using the webdriver
def SpeechRecognition():
    #open html file in the browser
    driver.get("file:///" + Link)
    #start speech recognition by clicking the start button
    driver.find_element(by=By.ID, value="start").click()
    
    while True:
        try:
            # Get the recognized text from the html output element
            Text = driver.find_element(by=By.ID, value="output").text
            
            if Text:
                # stop recognition by clicking thhe stop button
                driver.find_element(by=By.ID, value="end").click()
                
                #if the input language is  English return the  modified query
                if InputLanguage.lower() == "en" or "en" in InputLanguage.lower():
                    return QueryModifier(Text)
                else:
                    #if the input language is not english, tranlate the text and then return it
                    SetAssistantStatus("Translating....")
                    return QueryModifier(UniversalTranslator(Text))
        except Exception as e:
            pass
        time.sleep(0.1)
        
# Main execution block
if __name__ == "__main__":
    while True:
        # continuously perform speech recognition and print the recognized text
        Text = SpeechRecognition()
        print(Text)

