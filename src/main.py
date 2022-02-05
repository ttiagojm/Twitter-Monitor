from .auth import get_api, get_api_with_tokens
from .follower import follow_people
from .unfollower import unfollow_people
from .unfollowers import get_unfollowers

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--option", type=str, help="Insert follower, unfollower or unfollowers")

args = parser.parse_args()


if args.option == "follower":
    print("[+] Let's follow some people!")
    follow_people(get_api())

elif args.option == "unfollower":
    print("[+] Let's unfollow some people!")
    unfollow_people(get_api())

elif args.option == "unfollowers":
    print("[+] Let's check who unfollowed you!")
    get_unfollowers(get_api_with_tokens())

else:
    parser.print_help()