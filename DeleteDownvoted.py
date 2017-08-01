from time import sleep
import time
import praw
import Config

r = praw.Reddit(user_agent='Delete downvoted comments for /u/LinkFixBox')
r.login(username=Config.username, password=Config.password, disable_warning=True)

user = r.get_redditor('LinkFixBot')
past_deleted = []


def past_replies():
    try:
        with open("PastDeleted.txt", 'r')as file:
            print("Existing file found.")
            for id in file.readlines():
                id = comment.replace("\n", "").lower()
                past_deleted.append(id)

    except FileNotFoundError:
        with open("PastDeleted.txt", 'w'):
            print("No file found. New one created.")
            pass

past_replies()

while True:
    for comment in user.get_comments(limit=50):
        if comment.score <= 0 and comment.id not in past_deleted:
            comment.delete()
            past_deleted.append(comment.id)
            print("\n\n" + time.asctime(time.localtime(time.time())) + "\nComment by " + str(comment.author) + " "
                  "deleted.\n\n" + str(comment.body) + "\n")

    with open("PastDeleted.txt", 'w') as file:
        for item in past_deleted:
            file.write(str(item) + "\n")
    sleep(3)
