from .config import UNFOLLOWER_PATHS, threshold_followers, lastMonth
from .utils import thread_jobs, serialize, deserialize
from tweepy import Cursor
import os
import datetime


def read_write_ids(filename, mode, ids=None):
    """ I/O function that writes id list to a file and read from it"""

    # Write id list on a file
    if mode == "w":
        # Save the ids on a file
        for idt in ids:
            serialize(filename, str(idt))

    # Read id file to an list
    else:
        ids = []

        for idt in deserialize(filename):
            ids.append(idt)

        return ids


def get_friends_ids(api):
    # Just get all ids of all people that the account follow
    return [user.id for user in Cursor(api.friends, screen_name=api.me().screen_name).items()]


def get_mention_ids(api):
    # Get ids where the account had been mentioned (range of 1 month)
    mention_ids = []
    for mentions in Cursor(api.mentions_timeline).pages():
        for mention in mentions:
            mention_ids.append(mention.user.id)

    # Get my last tweets and get the user ids from replies (range of 1 month)
    isBreak = False

    for tweets in Cursor(api.user_timeline).pages():

        # Only break if we already got all the tweets of the last month
        if isBreak:
            break

        for tweet in tweets:
            if tweet.in_reply_to_user_id != api.me().id or tweet.in_reply_to_user_id != None:

                tweet_date = datetime.datetime.strptime(str(tweet.created_at), "%Y-%m-%d %H:%M:%S").date()

                # break if we already got all the tweets of the last month
                if lastMonth > tweet_date:
                    isBreak = True
                    break

                else:
                    mention_ids.append(tweet.in_reply_to_user_id)

    return mention_ids


def following_mention_ids(api, ids):
    """
        This function has the mention_ids and make sure if the account follow them
        if not ... don't make sense to unfollow them

        returns the ids list only with the ones that the account follow
    """

    ids = list(set(ids))

    following_mention_ids = []
    for idt in ids:
        if api.show_friendship(source_id=idt, target_id=api.me().id)[0].followed_by:
            following_mention_ids.append(idt)

    return following_mention_ids


def friend_follows_me(api, ids):
    """
        This function has the friends ids and verify if they follow the account
        if yes, the script will not unfollow them

        return an list with friends following the account
    """
    followed_me = []
    for idt in ids:
        if api.show_friendship(source_id=idt, target_id=api.me().id)[0].following:
            followed_me.append(idt)

    return followed_me


def big_accounts(api, ids):
    """ Verify if an account has a lot of followers and/or is verified"""

    big_accs = []

    for idt in ids:
        usr = api.get_user(idt)

        if int(usr.followers_count) >= threshold_followers or usr.verified == True:
            big_accs.append(idt)

    return big_accs


def unfollow(api, friends_ids, not_unfollow_ids):
    """ Create a list of unique ids to unfollow """

    # Get all the matched ids
    not_unfollow_ids = list(set(friends_ids) & set(not_unfollow_ids))

    # Remove the macthed ids to the list of all friends
    for idt in not_unfollow_ids:
        friends_ids.remove(idt)

    # Now we can unfollow the remaining
    for idt in friends_ids:
        api.destroy_friendship(idt)
        print("[-] Unfollow @" + api.get_user(idt).screen_name)

    return


def unfollow_people(api):

    """ I/O different ids """

    # All friends/following ID's

    if os.path.exists(UNFOLLOWER_PATHS["FRIENDS_FILE"]):
        ids = thread_jobs(read_write_ids, UNFOLLOWER_PATHS["FRIENDS_FILE"], "r")
    else:
        ids = thread_jobs(get_friends_ids, api)
        thread_jobs(read_write_ids, UNFOLLOWER_PATHS["FRIENDS_FILE"], "w", ids)

    print("Friends number: ", len(ids))

    # Get mention and reply ids

    if os.path.exists(UNFOLLOWER_PATHS["MENTIONS_FILE"]):
        mention_ids = thread_jobs(read_write_ids, UNFOLLOWER_PATHS["MENTIONS_FILE"], "r")
    else:
        mention_ids = thread_jobs(get_mention_ids, api)
        mention_ids = thread_jobs(following_mention_ids, api, mention_ids)
        thread_jobs(read_write_ids, UNFOLLOWER_PATHS["MENTIONS_FILE"], "w", mention_ids)

    print("Mention and reply number: ", len(mention_ids))

    # Get friends that follow the account too

    if os.path.exists(UNFOLLOWER_PATHS["FRIENDS_FOLLOWERS_FILE"]):
        friends_followers_ids = thread_jobs(read_write_ids, UNFOLLOWER_PATHS["FRIENDS_FOLLOWERS_FILE"], "r")
    else:
        friends_followers_ids = thread_jobs(friend_follows_me, api, ids)
        thread_jobs(read_write_ids, UNFOLLOWER_PATHS["FRIENDS_FOLLOWERS_FILE"], "w", friends_followers_ids)

    print("Friends and Followers number: ", len(friends_followers_ids))

    # Get big accounts ids

    if os.path.exists(UNFOLLOWER_PATHS["BIG_ACCOUNTS_FILE"]):
        big_accs_ids = thread_jobs(read_write_ids, UNFOLLOWER_PATHS["BIG_ACCOUNTS_FILE"], "r")
    else:
        big_accs_ids = thread_jobs(big_accounts, api, ids)
        thread_jobs(read_write_ids, UNFOLLOWER_PATHS["BIG_ACCOUNTS_FILE"], "w", big_accs_ids)

    print("Big accounts number: ", len(big_accs_ids))

    """ Treat the ids """

    # Remove duplicates using set() and convert again to a list
    # All this lists have ids that are not supose to be unfollowed
    mention_ids = list(set(mention_ids))
    friends_followers_ids = list(set(friends_followers_ids))
    big_accs_ids = list(set(big_accs_ids))

    # Concatenate all the ids to keep following
    not_unfollow = list(set(mention_ids + friends_followers_ids + big_accs_ids))
    print("People not to unfollow number: ", len(not_unfollow))

    # Now let's create a final list with only the ids to unfollow
    thread_jobs(unfollow, api, ids, not_unfollow)