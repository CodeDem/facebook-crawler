import urllib
import json
import csv
import datetime

def main():
	page_name = "ENTER THE PAGE ID"
	graph_url = "https://graph.facebook.com/"
	token = "ENTER YOUR ACCESS TOKEN"
	post = create_post_url(graph_url, token, page_name)
	post_json = to_json(post)
	json_fbposts = post_json['data']


	next_page = True
	counter = 0
	start_time = datetime.datetime.now()
	print "Now scanning page"
	with open('facebook.csv','wb') as file:
		csv.writer(file).writerow(["Post_ID","Post_Link","Post_Message","Post_datetime","Likes","Love","Sad","haha","angry","wow","Comments_count","Shares_Count"])
	while next_page:
			for post in json_fbposts:

		            try:
						tag = post["id"]
						message = '' if 'message' not in post.keys() else unicode_normalize(post['message'])
						status_published = datetime.datetime.strptime(post['created_time'],'%Y-%m-%dT%H:%M:%S+0000')
						status_published = status_published + datetime.timedelta(hours=-5)
						status_published = status_published.strftime('%Y-%m-%d %H:%M:%S')
						link_to = "www.facebook.com/"+tag
						reactions = getReactionsForStatus(tag, token)
						like = reaction_count("like", reactions)
						love = reaction_count("love",reactions)
						wow = reaction_count("wow", reactions)
						sad = reaction_count("sad", reactions)
						haha = reaction_count("haha", reactions)
						angry =reaction_count("angry", reactions)
						comments = reaction_count("comments", reactions)
						share = shares(reactions)
						with open('facebook.csv','a') as file:
							csv.writer(file).writerow([tag,link_to, message, status_published, like,love,sad,haha,angry,wow,comments,share])
						counter += 1
						if counter % 100 == 0:
							print "%s post prossed:%s" % (counter, datetime.datetime.now())
							if 'paging' in reactions.keys():
								post = to_json(urllib.urlopen(reactions['paging']['next']))
							else:
								next_page = false


		            except Exception:
		                print "Vedio or non text post/ No shares"

def create_post_url(graph_url,access_token, page_name):
	post_link = page_name+ "/posts/?key=value&access_token="+ access_token
	post_url = graph_url + post_link
	return post_url

def getReactionsForStatus(status_id, access_token):


    base = "https://graph.facebook.com/v2.6"
    node = "/%s" % status_id
    reactions = "/?fields=" \
			"shares,comments.summary(true),"\
            "reactions.type(LIKE).limit(0).summary(total_count).as(like)" \
            ",reactions.type(LOVE).limit(0).summary(total_count).as(love)" \
            ",reactions.type(WOW).limit(0).summary(total_count).as(wow)" \
            ",reactions.type(HAHA).limit(0).summary(total_count).as(haha)" \
            ",reactions.type(SAD).limit(0).summary(total_count).as(sad)" \
            ",reactions.type(ANGRY).limit(0).summary(total_count).as(angry)"
    parameters = "&access_token=%s" % access_token
    url = base + node + reactions + parameters

    # retrieve data
    data = to_json(url)

    return data

def unicode_normalize(text):
    return text.translate({ 0x2018:0x27, 0x2019:0x27, 0x201C:0x22, 0x201D:0x22,
                            0xa0:0x20 }).encode('utf-8')

def reaction_count(type, reactions):
	data = reactions[type]["summary"]["total_count"]
	return data
def shares(reactions):
	data = reactions["shares"]["count"]
	return data




def to_json(post_url):
	web_request = urllib.urlopen(post_url)
	response = web_request.read()
	post_json = json.loads(response)
	return post_json

main()
