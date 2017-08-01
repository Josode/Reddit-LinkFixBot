import praw
import Config
import time
import validators
import sys

# Current best working version. Bug: doesnt account for normal use of parenthesis.
# Fix: only reply if distance between []<-->() is less than 3 characters.
#

past_comments = []
blacklist = []
sub = "all"


# open past comments txt file and append all id's to list. create new file if doesnt exist
def past_replies():
    try:
        with open("PastComments.txt", 'r')as file:
            for comment in file.readlines():
                comment = comment.replace("\n", "").lower()
                past_comments.append(comment)

    except FileNotFoundError:
        with open("PastComments.txt", 'w'):
            print("No PastComments.txt file found. Creating.")
            pass


def blacklist_file():
    try:
        with open("Blacklist.txt", 'r')as file:
            for item in file.readlines():
                item = item.replace("\n", "").lower()
                past_comments.append(item)
        print("Blacklist: " + str(past_comments))

    except FileNotFoundError:
        with open("Blacklist.txt", 'w'):
            print("No Blacklist.txt file found. Creating.")
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
    subreddit = r.get_subreddit(sub)
    comments = subreddit.get_comments(limit=700)

    for comment in comments:
        if str(comment.subreddit) in blacklist or str(comment.author) in blacklist:
            break

        comment_string = comment.body
        comment_list = list(comment_string)

        if "[" in comment_list and "]" in comment_list and "(" in comment_list and ")" in comment_list and comment.id\
                not in past_comments:

            ind1 = comment_list.index("[")
            ind2 = comment_list.index("]")
            ind3 = comment_list.index("(")
            ind4 = comment_list.index(")")

            if ind1 < ind2 and ind3 < ind4:
                # and (ind2 + 3 <= ind3 or ind4 + 3 <= ind1):

                # extract text
                text = []
                for i in range(ind3+1, ind4):
                    text.append(comment_list[i])
                text_string = ''.join(text)

                # extract link
                link = []
                for i in range(ind1 + 1, ind2):
                    link.append(comment_list[i])
                link_string = ''.join(link)

                if validators.url(link_string) and not validators.url(text_string):

                    def send_reply():
                        print("\n\nComment found:\n" + comment_string)
                        print("subreddit: /r/" + str(comment.subreddit))
                        print("user: /u/" + str(comment.author))

                        comment.reply("It looks like you're trying to format a word into a link. Try this instead:"
                                      "\n\n > \[" + text_string + "](" + link_string + ")"
                                      "\n\n Result: " + "[" + text_string + "](" + link_string + ") "
                                      "\n\n***"
                                      "\n\n ^^Note: ^^Edits ^^appear ^^invisible ^^if ^^made ^^soon "
                                      "^^after ^^posting. "
                                      "^^| ^^I'm ^^a ^^bot, ^^beep ^^boop "
                                      "^^| ^^Downvote ^^to ^^DELETE. "
                                      "^^| [^^Contact ^^me]"
                                      "(http://www.reddit.com/message/compose/?to=LinkFixBot&subject=Contact+creator) "
                                      "^^| ^^[Opt-out]"
                                      "(http://www.reddit.com/message/compose/?to=LinkFixBot&subject=Opt+Out&message="
                                      + str(comment.author) +
                                      ") ^^| ^^[Feedback]"
                                      "(https://www.reddit.com/r/LinkFixBot/comments/6qys25/feedback_questions"
                                      "_complaints_etc_can_be_made_here/) ")

                        print("REPLY SENT! \n\n")
                        past_comments.append(comment.id)

                    # detects length between [] and (). If too far, doesn't reply
                    if ind3 < ind1:
                        if ind4 + 3 > ind1:
                            send_reply()
                        else:
                            break
                    elif ind1 < ind3:
                        if ind2 + 3 > ind3:
                            send_reply()
                        else:
                            break
                    else:
                        break

        with open("PastComments.txt", 'w') as file:
            for item in past_comments:
                file.write(str(item) + "\n")

    print("No Comments found...")

past_replies()
blacklist_file()
r = bot_login()

while True:
    try:
        run_bot(r)
    except:
        print(sys.exc_info()[0])

    time.sleep(1)
