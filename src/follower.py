from src.auth import get_api
from tweepy import Cursor, error
from tqdm import tqdm
from time import sleep
from random import randint, uniform
import sys
import os

LIST_OF_PEOPLE = [
    "tiago_j_m"
]

LIST_KEYWORDS = [
    "Developer"
]


IDS_FILENAME = "favourite_people.txt"
FOLLOWINGS_FILENAME = "followings.txt"


def print_information():
    print("[+] You are searching for people in friends of these people: \n")
    print("\n".join(["@" + person for person in LIST_OF_PEOPLE]))

    print("[+] You are searching for people with one of these keyword on their bio: \n")
    print("\n".join([keyword for keyword in LIST_KEYWORDS]))


def serialize(filename, data):
    try:
        with open(filename, "a+") as f:
            f.write(data + '\n' if (data[-1] != '\n') else '')

    except Exception as e:
        print(e)
        sys.exit(1)


def deserialize(filename):
    try:
        with open(filename, "r") as f:
            for line in f:
                yield line.rstrip()

    except Exception as e:
        print(e)
        sys.exit(1)


def favorite_people(api, ROOT_DIR):

    PATH_IDS_FILENAME = os.path.join(ROOT_DIR, IDS_FILENAME)

    # serialize id's first, if needed
    if not os.path.exists(PATH_IDS_FILENAME):
        for person in LIST_OF_PEOPLE:
            serialize(PATH_IDS_FILENAME, api.get_user(person).id_str)

    # get them
    people_ids = []

    for person in deserialize(PATH_IDS_FILENAME):
        people_ids.append(person)

    return people_ids


def filter_followings(api, people_ids, ROOT_DIR):

    PATH_FOLLOWINGS_FILENAME = os.path.join(ROOT_DIR, FOLLOWINGS_FILENAME)

    # if files exist dont loop
    if os.path.exists(PATH_FOLLOWINGS_FILENAME):
        return

    for id in people_ids:
        print("[!] ", str(api.get_user(id).screen_name).upper())
        for friend in tqdm(Cursor(api.friends, screen_name=api.get_user(id).screen_name).items()):
            sleep(uniform(0, 1))

            if any(key in (friend.description).lower() for key in LIST_KEYWORDS) and not friend.following:
                serialize(PATH_FOLLOWINGS_FILENAME, friend.id_str)


def follow_followings(api, ROOT_DIR):
    PATH_FOLLOWINGS_FILENAME = os.path.join(ROOT_DIR, FOLLOWINGS_FILENAME)

    for id in deserialize(PATH_FOLLOWINGS_FILENAME):
        try:
            api.create_friendship(id)
            print("[+] Followed: ", api.get_user(id).screen_name)
            sleep(randint(1, 5))
        except error.TweepError as e:
            print(e)
            pass


def follow_people(ROOT_DIR):

    # create root dir for save files (tmp folder)
    ROOT_DIR = os.path.join(ROOT_DIR, "tmp")

    print_information()

    # get api
    api = get_api()

    # get people id's
    people_ids = favorite_people(api, ROOT_DIR)

    # filter friends from people id's
    filter_followings(api, people_ids, ROOT_DIR)

    # follow people
    follow_followings(api, ROOT_DIR)
