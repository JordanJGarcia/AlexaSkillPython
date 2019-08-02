"""
    Lambda function code for our Athan Alexa Skill

    Jordan Garcia
    Zachary Hays
    Mohamed Aboulela
    Connor Hausman

    CIS4930: Python Programming
"""
import logging
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response
from ask_sdk_model.interfaces.audioplayer.audio_item import AudioItem
from ask_sdk_model.interfaces.audioplayer.audio_item_metadata import AudioItemMetadata
from ask_sdk_model.interfaces.audioplayer.play_directive import PlayDirective
from ask_sdk_model.interfaces.audioplayer.stop_directive import StopDirective
from ask_sdk_model.interfaces.audioplayer.stream import Stream
from ask_sdk_model.interfaces.audioplayer.play_behavior import PlayBehavior

import requests
import urllib.request
import time
from bs4 import BeautifulSoup

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

"""
    Launch Request handling. 
"""


@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    """
        Handler for Skill Launch.
    """
    # type: (HandlerInput) -> Response
    speech_text = "Welcome to our Athan Skill. To understand what this skill can do, ask for help now"

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("A Call to Prayer", speech_text)).set_should_end_session(
        False).response


"""
    Session Ended Request Handling
"""

@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    """
        Handler for Session End.
    """
    # type: (HandlerInput) -> Response
    return handler_input.response_builder.response


@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    """
        Catch all exception handler, log exception and
        respond with custom message.
    """
    # type: (HandlerInput, Exception) -> Response
    logger.error(exception, exc_info=True)

    speech = "Sorry, there was some problem. Please try again!"
    handler_input.response_builder.speak(speech).ask(speech)

    return handler_input.response_builder.response


"""
    Intent Request handling
"""

@sb.request_handler(can_handle_func=is_intent_name("AthanInfoIntent"))
def athan_info_intent_handler(handler_input):
    """
        Handler for Athan_Info Intent.
    """
    # type: (HandlerInput) -> Response
    speech_text = "You are asking for information about our Athan Alexa Skill"

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Athan Info", speech_text)).set_should_end_session(
        True).response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    """
        Handler for Help Intent.
    """
    # type: (HandlerInput) -> Response
    speech_text = "You can ask me to play a call to prayer, set the lighting for the prayer, and inform you of future prayer times."

    return handler_input.response_builder.speak(speech_text).ask(
        speech_text).set_card(SimpleCard(
            "Athan Info", speech_text)).response


@sb.request_handler(
    can_handle_func=lambda handler_input:
        is_intent_name("AMAZON.CancelIntent")(handler_input) or
        is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent_handler(handler_input):
    """
        Single handler for Cancel and Stop Intent.
    """
    # type: (HandlerInput) -> Response
    speech_text = "Thank you for using our skill. Goodbye!"
    sd = StopDirective()

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Goodbye!", speech_text)).add_directive(sd).response
        
        
def createPlayDirective(offset=0):
    """
        Helper function to create prayer playback
    """
    # type: (None) -> PlayDirective
    
    m_data = AudioItemMetadata(title='A Call to Prayer')
    strm = Stream(token='AdhanMakkah', url='https://adhanmakkahfile.s3.amazonaws.com/AdhanMakkah.mp3', offset_in_milliseconds=int(offset))
    a_item = AudioItem(stream=strm, metadata=m_data)
    
    return PlayDirective(PlayBehavior.REPLACE_ALL, a_item)
    

@sb.request_handler(can_handle_func=is_intent_name("playCallToPrayerIntent"))
def play_call_to_prayer_handler(handler_input):
    """
        Will stream the audio file with the call to prayer.
    """
    # type: (HandlerInput) -> Response

    speech_text = "Beginning the call to prayer..."
    pd = createPlayDirective()
    
    # need to get time of day to play appropriate prayer
    return handler_input.response_builder.speak(speech_text).set_should_end_session(True).add_directive(pd).response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.PauseIntent"))
def pause_handler(handler_input):
    """
        Pause Intent handling
    """
    
    sd = StopDirective()
    print(sd.to_str())
    return handler_input.response_builder.speak("Pausing...").add_directive(sd).set_should_end_session(True).response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.ResumeIntent"))
def resume_handler(handler_input):
    """
        Resume Intent handling
    """
    print("Printing request envelope...")
    print(handler_input.request_envelope)
    
    offset = handler_input.request_envelope.context.audio_player.offset_in_milliseconds
    pd = createPlayDirective(offset)
    
    return handler_input.response_builder.add_directive(pd).set_should_end_session(True).response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.LoopOffIntent"))
def loop_off_handler(handler_input):
    """
        Loop Off Intent Handling
    """
    # type: (Handler_input) -> Response 
    
    speech_text = "Sorry, you cannot loop the prayer."

    return handler_input.response_builder.speak(speech_text).set_should_end_session(False).response

@sb.request_handler(can_handle_func=is_intent_name("AMAZON.LoopOnIntent"))
def loop_on_handler(handler_input):
    """
        Loop on Handling
    """
    # type: (Handler_input) -> Response 

    speech_text = "Sorry, you cannot loop the prayer."

    return handler_input.response_builder.speak(speech_text).set_should_end_session(False).response

@sb.request_handler(can_handle_func=is_intent_name("AMAZON.NextIntent"))
def next_handler(handler_input):
    """
        Next Intent Handling
    """
    # type: (Handler_input) -> Response 

    speech_text = "Sorry, this is the only audio file that will play at the moment."

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Cannot play next!", speech_text)).response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.PreviousIntent"))
def previous_handler(handler_input):
    """
        Previous Intent Handling
    """
    # type: (Handler_input) -> Response
    
    speech_text = "Sorry, this is the only audio file that will play at the moment."
    
    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Cannot play previous!", speech_text)).response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.RepeatIntent"))
def repeat_handler(handler_input):
    """
        Cancel Intent Handling
    """
    # type: (Handler_input) -> Response 
    
    speech_text = "Sorry, repeat is not supported for this."

    return handler_input.response_builder.speak(speech_text).set_should_end_session(False).response
    

@sb.request_handler(can_handle_func=is_intent_name("AMAZON.ShuffleOffIntent"))
def shuffle_off_handler(handler_input):
    """
        Shuffle off Intent Handling
    """
    # type: (Handler_input) -> Response 

    speech_text = "Sorry, I cannot shuffle a call to prayer"
    
    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Cannot shuffle!", speech_text)).response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.ShuffleOnIntent"))
def shuffle_on_handler(handler_input):
    """
        Shuffle on Intent Handling
    """
    # type: (Handler_input) -> Response 

    speech_text = "Sorry, I cannot shuffle a call to prayer"
    
    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Cannot shuffle!", speech_text)).response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.StartOverIntent"))
def start_over_handler(handler_input):
    """
        Start Over Intent Handling
    """
    # type: (Handler_input) -> Response 
    
    speech_text = "Restarting the call to prayer..."
    pd = createPlayDirective()
    
    return handler_input.response_builder.speak(speech_text).set_should_end_session(True).add_directive(pd).response
    

@sb.request_handler(can_handle_func=is_intent_name("AMAZON.FallbackIntent"))
def fallback_handler(handler_input):
    """
        AMAZON.FallbackIntent is only available in en-US locale.
        This handler will not be triggered except in that locale,
        so it is safe to deploy on any locale.
    """
    # type: (HandlerInput) -> Response
    speech = (
        "The Athan skill can't help you with that. You can ask for help to get more info."
    )

    reprompt = "Ask for help to get more information."
    # handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.speak(speech).ask(reprompt).response


@sb.request_handler(can_handle_func=is_intent_name("timesintent"))
def times_handler(handler_input):
    """
        times output
    """
    # type: (HandlerInput) -> Response

    time1,time2,time3,time4,time5 = webscrape()

    speech = (
        "Today's prayer times are: "
        + time1 + ", " + time2 + ", " + time3 + ", " + time4 + ", and " + time5
    )

    reprompt = "Ask for help to get more information."
    # handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.speak(speech).ask(reprompt).response


def webscrape():
    #Sets the URL for the scrape
    url = 'https://www.islamicfinder.org/world/united-states/4174715/tallahassee-prayer-times/'
    #Connects to the URL
    response = requests.get(url)
    
    #Parses the HTML code and saves it to the created soup object
    soup = BeautifulSoup(response.text, "html.parser")
        
    #Finds specified instances of the <span> subclass
    #Parses the text from the line of HTML code
        
    FAJR    = soup.findAll('span')[28]
    f_time  = FAJR.text
        
    DHUHR   = soup.findAll('span')[32]
    d_time  = DHUHR.text
        
    ASR     = soup.findAll('span')[34]
    a_time  = ASR.text
        
    MAGHRIB = soup.findAll('span')[36]
    m_time  = MAGHRIB.text
        
    ISHA    = soup.findAll('span')[38]
    i_time  = ISHA.text
        
    return f_time,d_time,a_time,m_time,i_time


@sb.request_handler(can_handle_func=is_intent_name("getTimeIntent"))
def get_time_handler(handler_input):
    
    deviceId = handler_input.request_envelope.context.system.device.device_id
    URL = "https://api.amazonalexa.com/v2/devices/" + str(deviceId) + "/settings/System.timeZone"
    TOKEN =  handler_input.request_envelope.context.system.api_access_token
    HEADER = {'Accept': 'application/json',
             'Authorization': 'Bearer {}'.format(TOKEN)}
             
    r = requests.get(URL, headers=HEADER)
    
    print(r.json())
    
    if r.status_code == 200:
        return handler_input.response_builder.speak("Your time info has been printed to console.").set_should_end_session(True).response
    else:
        return handler_input.response_builder.speak("Access denied bitch").set_should_end_session(True).response
        
   # return handler_input.response_builder.speak("Your time info has been printed to console.").set_should_end_session(True).response



@sb.request_handler(can_handle_func=is_intent_name("PrayerRemainingIntent"))
def prayers_remaining_handler(handler_input):
    """
        Handler for Prayer Remaining Intent.
    """
    f_time, d_time, a_time, m_time, i_time = webscrape()
    
    #Split string variable into two different variables 
    
    f_hours, f_amPM = f_time.split()
    d_hours, d_amPM = d_time.split()
    a_hours, a_amPM = a_time.split()
    m_hours, m_amPM = m_time.split()
    i_hours, i_amPM = i_time.split()
    
    #Get User's Time (???)
    
    crnt_time_in_min = user_time_scrape()
    
    #Convert scraped times to Military (if needed)
    f_time_in_min = None
    if f_amPM == "PM":
        f_hr, f_min = f_hours.split(':')
        f_hr = int(f_hr) + 12
        f_time_in_min = f_hr * 60 + int(f_min)
    else:
        f_hr, f_min = f_hours.split(':')
        f_time_in_min = int(f_hr) * 60 + int(f_min)
    
    d_time_in_min = None
    if d_amPM == "PM":
        d_hr, d_min = d_hours.split(':')
        d_hr = int(d_hr) + 12
        d_time_in_min = d_hr * 60 + int(d_min)
    else:
        d_hr, d_min = d_hours.split(':')
        d_time_in_min = int(d_hr) * 60 + int(d_min)

    a_time_in_min = None
    if a_amPM == "PM":
        a_hr, a_min = a_hours.split(':')
        a_hr = int(a_hr) + 12
        a_time_in_min = a_hr * 60 + int(a_min)
    else:
        a_hr, a_min = a_hours.split(':')
        a_time_in_min = int(a_hr) * 60 + int(a_min)

    m_time_in_min = None
    if m_amPM == "PM":
        m_hr, m_min = m_hours.split(':')
        m_hr = int(m_hr) + 12
        m_time_in_min = m_hr * 60 + int(m_min)
    else:
        m_hr, m_min = m_hours.split(':')
        m_time_in_min = int(m_hr) * 60 + int(m_min)

    i_time_in_min = None
    if i_amPM == "PM":
        i_hr, i_min = i_hours.split(':')
        i_hr = int(i_hr) + 12
        i_time_in_min = i_hr * 60 + int(i_min)
    else:
        i_hr, i_min = i_hours.split(':')
        i_time_in_min = int(i_hr) * 60 + int(i_min)

    speech_text = None
    if f_time_in_min > crnt_time_in_min:
        speech_text = "The remaining prayers are Fajr, Dhuhr, Asr, Maghrib and Isha"
    elif d_time_in_min > crnt_time_in_min:
        speech_text = "The remaining prayers are Dhuhr, Asr, Maghrib and Isha"
    elif a_time_in_min > crnt_time_in_min:
        speech_text = "The remaining prayers are Asr, Maghrib and Isha"
    elif m_time_in_min > crnt_time_in_min:
        speech_text = "The remaining prayers are Maghrib and Isha" 
    elif i_time_in_min > crnt_time_in_min:
        speech_text = "The remaining prayer is Isha" 
    
    # type: (HandlerInput) -> Response

    return handler_input.response_builder.speak(speech_text).ask(
        speech_text).set_card(SimpleCard(
            "Athan Info", speech_text)).response

@sb.request_handler(can_handle_func=is_intent_name("NextPrayerIntent"))
def next_prayer_handler(handler_input):
    """
        Handler for Prayer Remaining Intent.
    """
    f_time, d_time, a_time, m_time, i_time = webscrape()
    
    #Split string variable into two different variables 
    
    f_hours, f_amPM = f_time.split()
    d_hours, d_amPM = d_time.split()
    a_hours, a_amPM = a_time.split()
    m_hours, m_amPM = m_time.split()
    i_hours, i_amPM = i_time.split()
    
    #Get User's Time (???)
    
    crnt_time_in_min = user_time_scrape()
    
    #Convert scraped times to Military (if needed)
    f_time_in_min = None
    if f_amPM == "PM":
        f_hr, f_min = f_hours.split(':')
        f_hr = int(f_hr) + 12
        f_time_in_min = f_hr * 60 + int(f_min)
    else:
        f_hr, f_min = f_hours.split(':')
        f_time_in_min = int(f_hr) * 60 + int(f_min)
    
    d_time_in_min = None
    if d_amPM == "PM":
        d_hr, d_min = d_hours.split(':')
        d_hr = int(d_hr) + 12
        d_time_in_min = d_hr * 60 + int(d_min)
    else:
        d_hr, d_min = d_hours.split(':')
        d_time_in_min = int(d_hr) * 60 + int(d_min)

    a_time_in_min = None
    if a_amPM == "PM":
        a_hr, a_min = a_hours.split(':')
        a_hr = int(a_hr) + 12
        a_time_in_min = a_hr * 60 + int(a_min)
    else:
        a_hr, a_min = a_hours.split(':')
        a_time_in_min = int(a_hr) * 60 + int(a_min)

    m_time_in_min = None
    if m_amPM == "PM":
        m_hr, m_min = m_hours.split(':')
        m_hr = int(m_hr) + 12
        m_time_in_min = m_hr * 60 + int(m_min)
    else:
        m_hr, m_min = m_hours.split(':')
        m_time_in_min = int(m_hr) * 60 + int(m_min)

    i_time_in_min = None
    if i_amPM == "PM":
        i_hr, i_min = i_hours.split(':')
        i_hr = int(i_hr) + 12
        i_time_in_min = i_hr * 60 + int(i_min)
    else:
        i_hr, i_min = i_hours.split(':')
        i_time_in_min = int(i_hr) * 60 + int(i_min)

    next_prayer = None
    speech_text = None
    if f_time_in_min > crnt_time_in_min:
        next_prayer = "Fajr"
    elif d_time_in_min > crnt_time_in_min:
        next_prayer = "Dhuhr"
    elif a_time_in_min > crnt_time_in_min:
        next_prayer = "Asr"
    elif m_time_in_min > crnt_time_in_min:
        next_prayer = "Maghrib"
    elif i_time_in_min > crnt_time_in_min:
        next_prayer = "Isha"
    
    
    # type: (HandlerInput) -> Response

    speech_text = "The next prayer is " + next_prayer 

    return handler_input.response_builder.speak(speech_text).ask(
        speech_text).set_card(SimpleCard(
            "Athan Info", speech_text)).response

def user_time_scrape():
    #Used to get current times
    
    #Sets the URL for the scrape
    url = 'https://www.timeanddate.com/worldclock/usa/tallahassee'

    #Connects to the URL
    response = requests.get(url)

    #Parses the HTML code and saves it to the created soup object
    soup = BeautifulSoup(response.text, "html.parser")

    #Finds specified instances of the <span> subclass
    #Parses the text from the line of HTML code

    Time            = soup.findAll('span')[2]
    crnt_time       = Time.text
    num_time, amPM  = crnt_time.split()
    hrs, mins, secs = num_time.split(':')

    if amPM == "pm":
        hrs = int(hrs)+12
    
    # Convert to minutes for easy comparison
    
    time_in_min = int(hrs) * 60 + int(mins)

    return(time_in_min)


# to link to lambda_handler
handler = sb.lambda_handler()
