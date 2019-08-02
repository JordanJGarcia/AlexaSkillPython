#!/usr/bin/env python3

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

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Goodbye!", speech_text)).response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.FallbackIntent"))
def fallback_handler(handler_input):
    """
        AMAZON.FallbackIntent is only available in en-US locale.
        This handler will not be triggered except in that locale,
        so it is safe to deploy on any locale.
    """
    # type: (HandlerInput) -> Response
    speech = (
        "The Athan skill can't help you with that."
        "You can ask for help to get more info.")
    reprompt = "Ask for help to get more information."
    # handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.speak(speech).ask(reprompt).response


# to link to lambda_handler
handler = sb.lambda_handler()
