import praw
import Config
import time
import validators



past_comments = []
blacklist = ['suicidewatch', 'selfharm', 'depression', 'BitcoinAllBot', 'Cairns', 'also_stl', 'SixSpeedDriver']


# open past comments txt file and append all id's to list. create new file if doesnt exist
def past_replies():
    try:
        with open("PastComments.txt", 'r')as file:
            for comment in file.readlines():
                comment = comment.replace("\n", "").lower()
                past_comments.append(comment)

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


def check_eligible(comment):

    comment_string = comment.body
    comment_list = list(comment_string)

    if "[" in comment_list and "]" in comment_list and "(" in comment_list and ")" in comment_list and comment.id \
            not in past_comments:

        ind1 = comment_list.index("[")
        ind2 = comment_list.index("]")
        ind3 = comment_list.index("(")
        ind4 = comment_list.index(")")

        if ind1 < ind2 and ind3 < ind4:
            # and (ind2 + 3 <= ind3 or ind4 + 3 <= ind1):

            # extract text
            text = []
            for i in range(ind3 + 1, ind4):
                text.append(comment_list[i])
            text_string = ''.join(text)

            # extract link
            link = []
            for i in range(ind1 + 1, ind2):
                link.append(comment_list[i])
            link_string = ''.join(link)

            if validators.url(link_string) and not validators.url(text_string):
                return True


def run_bot(r):
    subreddit = r.get_subreddit("all")
    comments = subreddit.get_comments(limit=500)

    for comment in comments:

        if comment.subreddit in blacklist or comment.author in blacklist:
            print("Blacklisted subreddit or user.")
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

                    print("\n\nComment found:\n" + comment_string)
                    print("Waiting 30 seconds for ninja edit...")
                    time.sleep(30)

                    # re-check if comment is formatted wrong
                    if check_eligible(comment):
                        pass
                    else:
                        print("\nComment edited. Canceling reply.")
                        break

                    comment.reply("It looks like you're trying to format a word into a link. Try this instead:"
                                  "\n\n > \[" + text_string + "](" + link_string + ")"
                                  "\n\n Result: " + "[" + text_string + "](" + link_string + ") "
                                  "\n\n***"
                                  "\n\n ^^Please ^^note: ^^Edits ^^won't ^^appear ^^visible ^^if ^^made ^^soon ^^after "
                                                                                             "^^posting. "
                                  "^^| ^^I'm ^^a ^^bot, ^^beep ^^boop "
                                  "^^| ^^Downvote ^^to ^^delete. "
                                  "^^| [^^Contact ^^me]"
                                  "(http://www.reddit.com/message/compose/?to=LinkFixBot&subject=Feedback) "
                                  "^^| ^^[Opt-out]"
                                  "(http://www.reddit.com/message/compose/?to=LinkFixBot&subject=Opt+Out&message="
                                  "name+of+Subreddit+or+user+Opting+out:) "
                                  "^^|")

                    print("REPLY SENT! \n\n")
                    past_comments.append(comment.id)

        with open("PastComments.txt", 'w') as file:
            for item in past_comments:
                file.write(str(item) + "\n")

    print("No Comments found...")

past_replies()
r = bot_login()

while True:
    run_bot(r)
    time.sleep(10)

