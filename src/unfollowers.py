from auth import get_api_with_tokens
import tweepy
import os


def getFollowersIds(api, username):
	followers_ids = []

	for follower_id in tweepy.Cursor(api.followers_ids, username).items():
		followers_ids.append(str(follower_id))

	return followers_ids

def writeFollowersIds(api, username, PATH_FILENAME):

	followers_ids = getFollowersIds(api, username)

	with open(PATH_FILENAME, "wb") as f:
		for follower_id in followers_ids:

			follower_id = follower_id+"\n"

			f.write(bytes(follower_id, "utf_8"))


def readFollowersIds(PATH_FILENAME):

	followers_ids = []

	with open(PATH_FILENAME, "rb") as f:
		for line in f:
			followers_ids.append(line.rstrip().decode("utf_8"))

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


def get_unfollowers(ROOT_DIR):

	api = get_api_with_tokens()

	USERNAME = input("Insert the @ of the account: ").rstrip()

	ROOT_DIR = os.path.join(ROOT_DIR, "tmp")
	PATH_FILENAME = os.path.join(ROOT_DIR, f"followers_ids_{USERNAME}.txt")

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