from __future__ import print_function
import datetime
from datetime import datetime as dt
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import subprocess
from selenium import webdriver
import pytz
import os
import time
import pyttsx3
import speech_recognition as sr
from selenium.webdriver.common.by import By

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
MONTHS = ["january", "february", "march", "april", "may", "june","july", "august", "september","october", "november", "december"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DAY_EXTENTIONS = ["rd", "th", "st",'nd']

def speak(text):
    engine=pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def getaudio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source,timeout=10)
        said=''
        try:
            said = r.recognize_google(audio)
            
        except Exception as e:
            pass

    return said

def main(day):
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "C:\\Users\\Asanda Khathide\\OneDrive - Nelson Mandela University\\Documents\\My pracs\Internship PROJECTS\\Voice Assistant Project\\Voice_Assistant\\credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    date=datetime.datetime.combine(day,datetime.time.min)
    end_date=datetime.datetime.combine(day,datetime.time.max)
    utc=pytz.UTC
    date=date.astimezone(utc)
    end_date=end_date.astimezone(utc)


    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=date.isoformat(),
            timeMax=end_date.isoformat(),
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
       speak('you have no events that day')
    else:
     speak('you have ' + str(len(events)) + ' events that day')

      

    # Prints the start and name of the next 10 events
    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      print(start, event["summary"])
      start_time=str(start.split('T')[1]).split('+')[0] 
      if int(start_time.split(':')[0]) < 12:
        start_time = start_time + 'am'
      else:
        start_time=str(int(start_time.split(':')[0])-12)+start_time.split(':')[1]
        start_time = start_time + 'pm'

      speak(event['summary']+' at '+start_time)

  except HttpError as error:
    print(f"An error occurred: {error}")

def get_date(text):
   text=text.lower()
   today=datetime.date.today()

   if text.count('today')>0:
      return today
   
   day=-1
   day_of_the_week=-1
   month=-1
   year=today.year

   for word in text.split():
      if word in  MONTHS:
         month=MONTHS.index(word)+1
      elif word in DAYS:
         day_of_the_week=DAYS.index(word)
      elif word.isdigit():
         day=int(word)
      else:
         for ext in DAY_EXTENTIONS:
            found=word.find(ext)
            if found>0:
               try:
                  day=int(word[:found])
               except:
                  pass
   if month < today.month and month !=-1:
      year=year+1
   if day< today.day and month==-1 and day !=-1:
      month=month+1
   if month==-1 and day ==-1 and day_of_the_week!=-1:
      current_day_of_the_week=today.weekday()
      dif=day_of_the_week-current_day_of_the_week

      if dif<0:
         dif+=7
         if text.count('next')>=1:
            dif+=7

      return today+datetime.timedelta(dif)
   if month ==-1 or day==-1:
      return None
   return datetime.date(month=month,day=day,year=year)

def note(text):
   date=datetime.datetime.now()
   file_name=str(date).replace(':','-')+'note.txt'
   with open(file_name,'w') as f:
      f.write(text)    

   subprocess.Popen(['notepad.exe',file_name])

def search_google(query):
    # Initialize Chrome WebDriver
     options = webdriver.ChromeOptions()

     options.add_argument('--disable-gpu') 
     driver = webdriver.Chrome(options=options)
   
     search_query = '+'.join(query.split())
     search_url = f"https://www.google.com/search?q={search_query}"

    # Open Google search in Chrome
     driver.get(search_url)

     search_results = driver.find_elements(By.CSS_SELECTOR, '.rc')

     for result in search_results:
        print(result.text)

     time.sleep(20)

    # Close the WebDriver
     driver.quit()

def tell_time():
    # Get the current date and time
    current_time = dt.now()

    # Format the time as a string
    time_str = current_time.strftime("%I:%M %p")  # Format as "hh:mm AM/PM"

    speak(f'The current time is: {time_str}')

def tell_date():
    # Get the current date
    current_date = dt.now()

    # Format the date as a string
    date_str = current_date.strftime("%B %d, %Y")  # Format as "Month Day, Year"

    # Print or return the formatted date string
    speak(f'Today\'s date is:{date_str} ')
    # return date_str  # If you want to return the date instead of printing it

wake='turn on'
print("Listening...")

while True:
   
   Calender_str = ['what do i have', 'do i have plans', 'am i busy']
   note_str = ['remember this', 'write this down', 'make a note']
   query_str = ['search this', 'google this for me', 'i have a question']


   text=getaudio().lower()
   if text.count(wake)>0:
      print(text)
      speak('I am ready')
      text=getaudio().lower()
      Calender_str=['what do i have','do i have plans','am i busy']
      note_str=['remember this','write this down','make a note']
      query_str=['Search this','google this for me','i have a question']
      print(text)
      for phrase in Calender_str:
         if phrase in text.lower():
            date=get_date(text)
            if date:
               main(date)
            else:
               speak('Please Try Again')
            break
      

      for phrase in note_str:
         if phrase in text.lower():
            speak('What would you like me to write down')
            note_text=getaudio().lower()
            note(note_text)
            speak('i\'ve made a note of that')
            break

      for phrase in query_str:
         if phrase in text.lower():
            speak('What would you like me to find out')
            query_text=getaudio().lower()
            search_google(query_text)
            break

      if 'time' in text:
        tell_time()
      if 'date' in text:
        tell_date()
      print("Listening...")


    