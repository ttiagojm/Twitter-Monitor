# Script where some variables are created
from pathlib import Path
import os
import datetime
import sys

# Paths
ROOT_DIR = Path(__file__).parent.parent
TMP_DIR = os.path.join(ROOT_DIR, "tmp")

FOLLOWERS_PATHS = {
    "IDS_FILENAME": os.path.join(TMP_DIR, "favourite_people.txt"),
    "FOLLOWINGS_FILENAME": os.path.join(TMP_DIR, "followings.txt")
}


UNFOLLOWER_PATHS = {
    "FRIENDS_FILE": os.path.join(TMP_DIR, "ids.txt"),
    "MENTIONS_FILE": os.path.join(TMP_DIR, "mention_ids.txt"),
    "FRIENDS_FOLLOWERS_FILE": os.path.join(TMP_DIR, "friends_followers.txt"),
    "BIG_ACCOUNTS_FILE": os.path.join(TMP_DIR, "big_accounts.txt"),
}

# Create dirs
try:
    os.makedirs(os.path.join(ROOT_DIR, "tmp"), exist_ok = True)
    print("[+] tmp folder was created!\n")
except OSError as error:
    print("[!] For some reason it was impossible to create the tmp folder. Exiting...\n")
    sys.exit(1)


# Lists
LIST_OF_PEOPLE = [
    "tiago_j_m"
]

LIST_KEYWORDS = [
    "Coding"
]

# Constants

# Followers threshold for big accounts
threshold_followers = 5000

# Since date until some date (in this case 30 days)
lastMonth = datetime.date.today() - datetime.timedelta(days=30)