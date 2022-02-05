from .config import TMP_DIR
from .utils import serialize, deserialize
import tweepy
import os


def getFollowersIds(api, username):
	followers_ids = []

	for follower_id in tweepy.Cursor(api.followers_ids, username).items():
		followers_ids.append(str(follower_id))

	return followers_ids

def writeFollowersIds(api, username, PATH_FILENAME):

	followers_ids = getFollowersIds(api, username)

	for follower_id in followers_ids:
		serialize(PATH_FILENAME, follower_id)


def readFollowersIds(PATH_FILENAME):

	followers_ids = []

	for idt in deserialize(PATH_FILENAME):
		followers_ids.append(idt)

	return followers_ids


def getMissingIds(api, f_ids_file, f_ids_api):

	# IDs that are on file but not on the API (unfollowers)
	unfollowers = list( set(f_ids_file) - set(f_ids_api) )

	for unfollower in unfollowers:

		try:
			usr = api.get_user(int(unfollower))
			print("\n\n#=====================#")
			print("@" + usr.screen_name)
			print("Desc: " + usr.description)

		except:
			print("Account doesn't exist anymore or something happened to it: ", str(unfollower))
	print("\n\n")


def get_unfollowers(api):

	USERNAME = input("Insert the @ of the account: ").rstrip()

	PATH_FILENAME = os.path.join(TMP_DIR, f"followers_ids_{USERNAME}.txt")

	# Write all followers
	if not os.path.exists(PATH_FILENAME):
		print("### Creating files with IDs ###")
		writeFollowersIds(api, USERNAME, PATH_FILENAME)

	# Read and count followers from file
	f_ids_file = readFollowersIds(PATH_FILENAME)

	# Get followers IDs from Twitter's APIs
	f_ids_api = getFollowersIds(api, USERNAME)

	getMissingIds(api, f_ids_file, f_ids_api)

	# Update file
	writeFollowersIds(api, USERNAME, PATH_FILENAME)