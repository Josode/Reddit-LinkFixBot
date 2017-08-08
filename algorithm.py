import validators


def isFaltyLink(comment):

    comment_list = list(comment)

    if "[" in comment_list and "]" in comment_list and "(" in comment_list and ")" in comment_list:

        index_1 = comment_list.index("[")
        index_2 = comment_list.index("]")
        index_3 = comment_list.index("(")
        index_4 = comment_list.index(")")

        if index_1 < index_2 and index_3 < index_4:

            link = []
            for i in range(index_1 + 1, index_2):
                link.append(comment_list[i])
            linkstr = ''.join(link)
            print(linkstr)

            text = []
            for i in range(index_3 + 1, index_4):
                text.append(comment_list[i])
            textstr = ''.join(text)
            print(textstr)

            if validators.url(linkstr) and not validators.url(textstr):
                print("successfully found a faulty link.")
            else:
                print("this link is fine.")
    else:

        print("this link is fine.")


isFaltyLink("[Classic Australia](https://www.theguardian.com/australia-news/2016/oct/24/australia-giant-spider-mouse-carry-horrifying-impressive)")

'''
test cases:
[https://youtube.com](video)



'''