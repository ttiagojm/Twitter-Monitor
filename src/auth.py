from tweepy import OAuthHandler, API
from dotenv import load_dotenv
import sys
import os
import webbrowser

load_dotenv()

# Tokens
tokens = {
    "CONSUMER_KEY": os.getenv("CONSUMER_KEY"),
    "CONSUMER_SECRET": os.getenv("CONSUMER_SECRET"),
    "ACCESS_TOKEN": os.getenv("ACCESS_TOKEN"),
    "ACCESS_TOKEN_SECRET": os.getenv("ACCESS_TOKEN_SECRET"),
}

def get_api_with_tokens():

    try:
        auth = OAuthHandler(tokens["CONSUMER_KEY"], tokens["CONSUMER_SECRET"])
        auth.secure = True
        auth.set_access_token(tokens["ACCESS_TOKEN"], tokens["ACCESS_TOKEN_SECRET"])
        api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    except BaseException as e:
        print("Error in get_api_with_tokens()", e)
        sys.exit(1)

    return api

def get_api():

    try:
        auth = OAuthHandler(tokens["CONSUMER_KEY"], tokens["CONSUMER_SECRET"])

        try:
            redirect_url = auth.get_authorization_url()
            webbrowser.open(redirect_url)
        except Exception as e:
            print("Error getting request token")
            print(e)

        verifier = input("Paste the code from your browser: ")

        try:
            auth.get_access_token(verifier)
        except:
            print("Error getting access token")
            sys.exit(1)

        auth.secure = True
        #auth.set_access_token(tokens["ACCESS_TOKEN"], tokens["ACCESS_TOKEN_SECRET"])
        api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    except BaseException as e:
        print("Error in get_api()", e)
        sys.exit(1)

    return api