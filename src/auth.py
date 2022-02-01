from tweepy import OAuthHandler, API
from dotenv import load_dotenv
import sys
import os
import webbrowser

load_dotenv()

# consumer tokens
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
# tokens
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")


def get_api_with_tokens():

    try:
        auth = OAuthHandler(os.environ["CONSUMER_KEY"], os.environ["CONSUMER_SECRET"])
        auth.secure = True
        auth.set_access_token(os.environ["ACCESS_TOKEN"], os.environ["ACCESS_TOKEN_SECRET"])
        api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    except BaseException as e:
        print("Error in get_api_with_tokens()", e)
        sys.exit(1)

    return api

def get_api():
    # consumer tokens
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")

    # tokens
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    try:
        auth = OAuthHandler(consumer_key, consumer_secret)

        try:
            redirect_url = auth.get_authorization_url()
            webbrowser.open(redirect_url)
        except:
            print("Error getting request token")

        verifier = input("Paste the code from your browser::")

        try:
            auth.get_access_token(verifier)
        except:
            print("Error getting access token")
            sys.exit(1)

        # auth.secure = True
        auth.set_access_token(auth.access_token, auth.access_token_secret)
        api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    except BaseException as e:
        print("Error in get_api()", e)
        sys.exit(1)

    return api
