                                             Athan Alexa Skill

By Mohamed Aboulela, Jordan Garcia, Zachary Hayes and Connor Hausmann

- The purpose of this skill is to allow for Alexa to be able to perform the Athan (call to prayer) five times a day, every day,
for every prayer, or when requested.

- Some features of our skill (you can ask it to):
  - play a call to prayer
  - pause/resume prayer
  - tell how many prayers are left in the day
  - tell when the next prayer time is
  - tell you prayer times of the day

This skill was created using python. Our platforms were GitHub Desktop and the Amazon Developer Console.

Computing/environments used: 
  - Amazon Web Service
    - Lambda/S3
  - Amazon Developer Console
    - Alexa Skills Kit
  
  
Libraries used: 
 
  - Alexa Skills Kit SDK (Python)
    - https://github.com/alexa/alexa-skills-kit-sdk-for-python
  - Alexa APIs (Python)
    - https://github.com/alexa/alexa-apis-for-python
  - Geopy
    - https://geopy.readthedocs.io/en/stable/
  - Pytz
    - http://pytz.sourceforge.net/
  - Beautiful Soup
    - https://www.crummy.com/software/BeautifulSoup/bs4/doc/
  - Datetime
    - https://docs.python.org/2/library/datetime.html
  - Requests
    - https://2.python-requests.org/en/master/
    
    
    
 Old Repo: https://github.com/JordanJGarcia/AthanAlexaSkill
 
 
 
 Division of Labor:
 
 Jordan Garcia
  - LaunchRequest, SessionEndedRequest, AudioPlayer Interface, AthanInfoIntent, CreatePlayDirective(), 
    playCallToPrayerIntent, AMAZON."intentName" Intents, get_user_time(), get_audio_file() 
    
    
    
    
How to run: 

You must have an Amazon developer account and an account with AWS. It is also assumed you know how to run an alexa skill with AWS Lambda. If you have both:

1) Go to https://aws.amazon.com/ and click on "Sign in to Console" in the top right. 
2) Once signed in, click on "Lambda" under the Compute section.
3) Click "Create Function" and set the runtime to Python 3.6 and register it to the role you have created for this function. 
4) Once in the function development environment, upload the "lambda.zip" file in ZipFolder directory as your Lambda function. 
5) Add "S3" and "Alexa Skills Kit" as triggers.
6) Now, go to https://developer.amazon.com and sign into your developer account. 
7) Under "Alexa" select "Alexa skills kit" and create an Invocation name and copy the "interactionModel.json" file, and paste it in the JSON editor for intents.
8) Save your model and ensure its linked to the Lambda function properly with the necessary permissions set. 
9) Build the model.

If you have an alexa device signed into the same account as your Amazon developer account you can use that device to test your custom skill. If not, you can use the "Test" section. However, not using a device will make use of the skill very limited. 
