import sys
import time
import praw
import validators
from LinkRepairBot import Config

# Current working version

past_comments = []
blacklist = []
sub = "all"
comments_limit = 800
secs = 40


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
                blacklist.append(item)

    except FileNotFoundError:
        with open("Blacklist.txt", 'w'):
            print("No Blacklist.txt file found. Creating.")
            pass


def bot_login():
    reddit = praw.Reddit(username=Config.username,
                         password=Config.password,
                         client_id=Config.client_id,
                         client_secret=Config.client_secret,
                         user_agent="I will fix failed text-link markdown and delete at downvote of a user."
                                    "By /u/Josode")
    print(reddit.user.me())

    return reddit


def run_bot(r):
    subreddit = r.subreddit(sub)
    comments = subreddit.stream.comments()

    def check(comment_list):

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

                if "(" in link_string or ")" in link_string:
                    return False

                if validators.url(link_string) and not validators.url(text_string):
                    # detects length between [] and (). If too far, doesn't reply
                    if ind3 < ind1:
                        if ind4 + 3 > ind1:
                            return True
                        else:
                            return False
                    elif ind1 < ind3:
                        if ind2 + 3 > ind3:
                            return True
                        else:
                            return False
                    else:
                        return False

        with open("PastComments.txt", 'w') as file:
            for item in past_comments:
                file.write(str(item) + "\n")

        return False

    for comment in comments:
        if str(comment.subreddit) in blacklist or str(comment.author) in blacklist:
            continue

        comment_str = comment.body
        comment_lst = list(comment_str)
        id = comment.id

        def send_reply():
            print("Comment still eligible:\n" + comment_str)
            print("Subreddit: /r/" + str(comment.subreddit))
            print("Author: /u/" + str(comment.author))

            ind1 = comment_lst.index("[")
            ind2 = comment_lst.index("]")
            ind3 = comment_lst.index("(")
            ind4 = comment_lst.index(")")

            # extract text
            text = []
            for i in range(ind3 + 1, ind4):
                text.append(comment_lst[i])
            text_string = ''.join(text)

            # extract link
            link = []
            for i in range(ind1 + 1, ind2):
                link.append(comment_lst[i])
            link_string = ''.join(link)

            reply = ("It looks like you're trying to format a word into a link. Try this instead:"
                     "\n\n > \[" + text_string + "](" + link_string + ")"
                     "\n\n Result: " + "[" + text_string + "](" + link_string + ") "
                     "\n\n Got it fixed? **Downvote to delete.**"
                     "\n\n***"
                     "\n\n ^^Note: ^^Edits ^^appear ^^invisible ^^if ^^made ^^soon "
                     "^^after ^^posting. "
                     "^^| ^^I'm ^^a ^^bot, ^^beep ^^boop "
                     "^^| [^^Contact ^^me]"
                     "(http://www.reddit.com/message/compose/?to=LinkFixBot&subject=Contact+creator) "
                     "^^| ^^[Opt-out]"
                     "(http://www.reddit.com/message/compose/?to=LinkFixBot&subject=Opt+Out&message="
                     + str(comment.author) +
                     ") ^^| ^^[Feedback]"
                     "(https://www.reddit.com/r/LinkFixBot/comments/6qys25/feedback_questions"
                     "_complaints_etc_can_be_made_here/) ")

            comment.reply(reply)

            print("REPLY SENT! \n\n")
            past_comments.append(comment.id)

        if check(comment_list=comment_lst):
            print("\n\nComment Found. \nWaiting {} seconds...".format(str(secs)))
            time.sleep(secs)
            new_comment = r.comment(id).body
            comment_lst = list(new_comment)
            print('new comment: ' + new_comment)

            if check(comment_list=comment_lst):
                send_reply()
            else:
                print('Ninja edit occurred. NOT replying.\n\n')
                continue

    print("No Comments found...")

past_replies()
blacklist_file()
r = bot_login()
print("Running bot on /r/" + sub)

while True:
    try:
        run_bot(r)
    except:
        print("Excepting HTTP error.")
    time.sleep(0)
