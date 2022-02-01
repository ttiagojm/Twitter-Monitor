from  follower import follow_people
from unfollower import unfollow_people
from unfollowers import get_unfollowers
from pathlib import Path
import argparse
from os import makedirs, path
import sys

ROOT_DIR = Path(__file__).parent.parent

# Create directory for temporary files
try:
    makedirs(path.join(ROOT_DIR, "tmp"), exist_ok = True)
except OSError as error:
    print("[!] For some reason it was impossible to create the tmp folder. Exiting...")
    sys.exit(1)

parser = argparse.ArgumentParser()

parser.add_argument("--option", type=str, help="Insert follower, unfollower or unfollowers")

args = parser.parse_args()

if args.option == "follower":
    print("[+] Let's follow some people!")
    follow_people(ROOT_DIR)

elif args.option == "unfollower":
    print("[+] Let's unfollow some people!")
    unfollow_people(ROOT_DIR)

elif args.option == "unfollowers":
    print("[+] Let's check who unfollowed you!")
    get_unfollowers(ROOT_DIR)