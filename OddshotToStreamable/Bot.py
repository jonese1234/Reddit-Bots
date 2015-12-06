__author__ = 'Rhys Jones'

# Import Block
import os
import requests
import urllib3
from bs4 import BeautifulSoup
import praw
import time
from pprint import pprint
import os.path
import sys

# Info Block
uStreamable = '############'
pStreamble = '############'

uReddit = '################'
pReddit = '###############'

id_save = '#####################'
postnumber_save = '##########################'

app_id = '############'
app_secret = '##############'
app_uri = 'https://127.0.0.1:65010/authorize_callback'
app_ua = '/u/jonese1234 Oddshot_to_Streamable comment poster at /u/OddshotToStreamable'
app_scopes = 'account creddits edit flair history identity livemanage modconfig modcontributors modflair modlog modothers modposts modself modwiki mysubreddits privatemessages read report save submit subscribe vote wikiedit wikiread'
app_account_code = '########################'
app_refresh = '#########################'

##postnum = 58

#already_done = set({'3re9nz', '3rdo83', '3ra1vs'})

subreddits = 'OddshotToStreamable, Test0324, GlobalOffensive'
stringsubrredits = subreddits.replace(', ', '+')
# Code Block

def redditlogin():
    rpraw = praw.Reddit(app_ua)
    rpraw.set_oauth_app_info(app_id, app_secret, app_uri)
    rpraw.refresh_access_information(app_refresh)
    return rpraw

def submitiontest():
    r = praw.Reddit('submitiontest /u/jonese1234')
    submission = r.get_submission(submission_id= "3ra1vs")
    pprint(vars(submission))

def oddshotfinder():
    print('Logging in')
    rpraw = redditlogin()
    prawWords = ['oddshot.tv']
    attempts = 1

    while attempts <= 1001:
        subreddit = rpraw.get_domain_listing('oddshot.tv', sort='new')
        id_list_location = os.path.join(id_save, "ids.txt")
        for submission in rpraw.get_domain_listing('oddshot.tv', sort='new', limit=50):
            op_link = submission.url.lower()
            is_oddshot = any(string in op_link for string in prawWords)
            post_id = submission.id
            try:
                if post_id not in open(id_list_location).read() and is_oddshot:
                    link = submission.url
                    postid = submission.id
                    posttitle = submission.title
                    urlposttitle = posttitle.replace(" ", "+")
                    redditlink = submission.permalink
                    print('Video Url: ' + link)
                    print('Reddit Post Id: ' + postid)
                    print('Reddit Post Title: ' + posttitle)
                    print('Url Post Title: ' + urlposttitle)
                    print('Reddit Comment URL: ' + redditlink)
                    oddshotvideosource(link, postid, urlposttitle)
                    #submission.add_comment('Testing 1, 2, 3')
                    time.sleep(30)
                else:
                    print('No New Oddshot Posts')
                    attempts += 1
                    print('No. Of Attempts: ' + str(attempts))
                    time.sleep(10)
            except AttributeError:
                pass
            except praw.errors.InvalidSubmission:
                pass

    if attempts == 1000:
        print("Failed to find oddshot in 1000 attempts")



def oddshotvideosource(link, postid, posttitle):
    link = link
    r = requests.get(link)
    postid = postid
    posttitle = posttitle
    plain_text = r.text
    #print(r.text)
    soup = BeautifulSoup(plain_text, "html.parser")
    link_source = soup.find('source', src=True, href=False)
    true_link = link_source.get('src')
    print('Video source link: ' + true_link)
    streamableupload(true_link, postid, posttitle)




def streamableupload(videourl, postid, posttitle):
    url = 'https://api.streamable.com/import?url='
    postid = postid
    videourl = videourl
    posttitle = posttitle
    print('Uploading Video')
    r = requests.get(url + videourl + '&title=' + posttitle, auth=(uStreamable, pStreamble))
    shortcode = r.json()['shortcode']
    #print(shortcode)
    posturl = ("http://www.streamable.com/" + shortcode)
    print('Streamable link: ' + posturl)
    time.sleep(30)
    print('Probably uploaded')
    redditCommentPost(posturl, postid)

def log_id(id):
    id_list_location = os.path.join(id_save, "ids.txt")
    id_list = open(id_list_location, 'a+')
    tofile = id
    id_list.write(tofile)
    id_list.write("\n")
    id_list.close()

def redditCommentPost(posturl, postid):
    num_list_location = os.path.join(postnumber_save, "postnumber.txt")
    postnum = open(num_list_location, 'r').read()
    postid = postid
    posturl = posturl
    rpraw = redditlogin()
    posted = False
    comment = '[Streamable Link](' + posturl + ')\n****\n^I ^am ^an ^Automated ^bot! ^So ^Dont ^Bully ^Me! ^(o_o) ^| ^Post ^No. ^: ^' + postnum + ' ^| ^- ^[Faq](https://www.reddit.com/r/OddshotToStreamable/wiki/faq) ^- ^|'
    while not posted:
        try:
            submission = rpraw.get_submission(submission_id=postid)
            submission.add_comment(comment)
            print('Posting Comment')
            print(comment)
            print('Updateing IDs')
            log_id(postid)
            print('Adding 1 to Postnum')
            writepostnum()
            posted = True
            time.sleep(10)
        except praw.errors.InvalidSubmission:
            log_id(postid)
            posted = True
            time.sleep(10)
            pass
        except praw.errors.RateLimitExceeded:
            time.sleep(600)


def writepostnum():
    num_list_location = os.path.join(postnumber_save, "postnumber.txt")
    postnumber_file = open(num_list_location, 'r')
    file = postnumber_file.read()
    newpostnum = int(file) + 1
    print('New post number: ' + str(newpostnum))
    open(num_list_location, 'w').write(str(newpostnum))
    postnumber_file.close()

def botstart():
    post_number = 1
    print('The Oddshot to Streamable bot is starting')
    time.sleep(3)
    while True:
        print('Post Session ' + str(post_number))
        oddshotfinder()
        post_number += 1
        print('Sleep Time')
        time.sleep(600)


botstart()