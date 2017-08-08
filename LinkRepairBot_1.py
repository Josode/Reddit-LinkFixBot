import time

import praw

from LinkRepairBot import Config

past_comments = []


# open past comments txt file and append all id's to list. create new file if doesnt exist
def past_replies():
    try:
        with open("PastComments.txt", 'r')as file:
            for comment in file.readlines():
                comment = comment.replace("\n", "").lower()
                past_comments.append(comment)

            print(str(past_comments))
    except FileNotFoundError:
        with open("PastComments.txt", 'w'):
            pass


def bot_login():
    r=praw.Reddit(username=Config.username,
                  password=Config.password,
                  client_id=Config.client_id,
                  client_secret=Config.client_secret,
                  user_agent="I will fix your failed links!")

    r.login(username=Config.username, password=Config.password, disable_warning=True)
    return r


def run_bot(r):
    subreddit = r.get_subreddit("all")
    comments = subreddit.get_comments(limit=500)

    for comment in comments:
        str_comment = comment.body.lower()

        if comment.subreddit == "Dream_Market" or comment.subreddit == "hardwareswap":
            break

        if "[" in str_comment and "]" in str_comment and "(" in str_comment and ")" in str_comment and comment.id not in past_comments:
            raw_comment_list = list(str_comment)

            # extract text
            ind3 = raw_comment_list.index("(")
            ind4 = raw_comment_list.index(")")
            text = []
            for i in range(ind3+1, ind4):
                text.append(raw_comment_list[i])
            textstr = ''.join(text)

            if "http" in textstr:
                break

            print("\ntext extracted: " + textstr)

            # extract link
            ind = raw_comment_list.index("[")
            ind2 = raw_comment_list.index("]")
            link = []
            for i in range(ind + 1, ind2):
                link.append(raw_comment_list[i])
            linkstr = ''.join(link)
            print("link extracted: " + linkstr)

            if "http" in linkstr:
                past_comments.append(comment.id)
                comment.reply("It looks like you're trying to format a word into a link. Try this instead:"
                              "\n\n \[" + textstr + "](" + linkstr + ")"
                              "\n\n Result: " + "[" + textstr + "](" + linkstr + ")"
                              "\n\n ^^I ^^am ^^new ^^and ^^I ^^might ^^still ^^have ^^bugs. ^^Sorry ^^if ^^I "
                              "^^wrongfully ^^replied!")

                print("Comment found. Reply SENT!.\n")
            else:
                "NOT replying."

    print("No Comments found...")

past_replies()
r = bot_login()

while True:
    run_bot(r)
    with open("PastComments.txt", 'w') as file:
        for item in past_comments:
            file.write(item + "\n")

    time.sleep(5)