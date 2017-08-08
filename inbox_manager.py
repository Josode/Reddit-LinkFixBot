import praw
from LinkRepairBot import Config

def bot_login():
    r=praw.Reddit(username=Config.username,
                  password=Config.password,
                  client_id=Config.client_id,
                  client_secret=Config.client_secret,
                  user_agent="I will fix your failed links!")

    r.login(username=Config.username, password=Config.password, disable_warning=True)
    return r


def run_bot(r):
    for reply in r.inbox.submission_replies():
        print("\nauthor: {}".format(reply.author))
        print("content: {}".format(reply))

r = bot_login()
while True:
    run_bot(r)