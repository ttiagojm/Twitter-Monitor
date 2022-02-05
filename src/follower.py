from .config import FOLLOWERS_PATHS, LIST_KEYWORDS, LIST_OF_PEOPLE
from .utils import serialize, deserialize

from tweepy import Cursor, error
from tqdm import tqdm
from time import sleep
from random import randint, uniform
import os

def print_information():
    print("[+] You are searching for people in friends of these people: \n")
    print("\n".join(["@" + person for person in LIST_OF_PEOPLE]))

    print("[+] You are searching for people with one of these keyword on their bio: \n")
    print("\n".join([keyword for keyword in LIST_KEYWORDS]))


def favorite_people(api):

    # serialize id's first, if needed
    if not os.path.exists(FOLLOWERS_PATHS["IDS_FILENAME"]):
        for person in LIST_OF_PEOPLE:
            serialize(FOLLOWERS_PATHS["IDS_FILENAME"], api.get_user(person).id_str)

    # get them
    people_ids = []

    for person in deserialize(FOLLOWERS_PATHS["IDS_FILENAME"]):
        people_ids.append(person)

    return people_ids


def filter_followings(api, people_ids):

    # if files exist dont loop
    if os.path.exists(FOLLOWERS_PATHS["FOLLOWINGS_FILENAME"]):
        return

    for id in people_ids:
        print("[!] ", str(api.get_user(id).screen_name).upper())

        # Fix progress bar, need to know how many iterations
        # https://stackoverflow.com/questions/48935907/tqdm-not-showing-bar
        total_iter = api.get_user(id).friends_count

        with tqdm(total=total_iter) as pbar:

            for friend in tqdm(Cursor(api.friends, screen_name=api.get_user(id).screen_name).items()):
                sleep(uniform(0, 1))

                if any(key.lower() in (friend.description).lower() for key in LIST_KEYWORDS) and not friend.following:
                    serialize(FOLLOWERS_PATHS["FOLLOWINGS_FILENAME"], friend.id_str)
                
                # Increment progess bar
                pbar.update(1)


def follow_followings(api):

    for id in deserialize(FOLLOWERS_PATHS["FOLLOWINGS_FILENAME"]):
        while True:
            try:
                api.create_friendship(id)
                sleep(randint(1, 5))

                # we did it
                print("[+] Followed: " + api.get_user(id).screen_name + " | " + id)
                break

            except error.TweepError as e:
                # Timeout for following many people
                # lets sleep and try again
                if e.args[0][0]["code"] == 161:

                    print("Sleeping for 15 minutes zzz")
                    sleep(900)
                    print("Trying again...")

                # Generic Tweepy error
                else:
                    print(e)
                    break


def follow_people(api):

    print_information()

    # get people id's
    people_ids = favorite_people(api)

    # filter friends from people id's
    filter_followings(api, people_ids)

    # follow people
    follow_followings(api)
