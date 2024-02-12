test = [{'id': 't3_1aloclp', 'parsedId': '1aloclp', 'url': 'https://www.reddit.com/r/digital_marketing/comments/1aloclp/tips_for_marketing_of_new_podcast/', 'username': 'LuckyFall6205', 'title': 'Tips for Marketing of New Podcast', 'communityName': 'r/digital_marketing', 'parsedCommunityName': 'digital_marketing', 'body': "I met a senior journalist at a B2B meeting, introduced by my dad. He's a script writer and content creator for documentaries, aged 62, seeking advice on better podcast marketing. \n\nI suggested using Spotify Advertising Manager, Google Ads, Meta Ads, etc. \n\nDespite being new to podcast marketing and more focused on content design and media buying, I felt a bit out of my element. Any additional tips would be appreciated!\n\nThe topic of podcast is [The focus on issues relevant to people's lives and society as a whole]", 'html': '&lt;!-- SC_OFF --&gt;&lt;div class="md"&gt;&lt;p&gt;I met a senior journalist at a B2B meeting, introduced by my dad. He&amp;#39;s a script writer and content creator for documentaries, aged 62, seeking advice on better podcast marketing. &lt;/p&gt;\n\n&lt;p&gt;I suggested using Spotify Advertising Manager, Google Ads, Meta Ads, etc. &lt;/p&gt;\n\n&lt;p&gt;Despite being new to podcast marketing and more focused on content design and media buying, I felt a bit out of my element. Any additional tips would be appreciated!&lt;/p&gt;\n\n&lt;p&gt;The topic of podcast is [The focus on issues relevant to people&amp;#39;s lives and society as a whole]&lt;/p&gt;\n&lt;/div&gt;&lt;!-- SC_ON --&gt;', 'numberOfComments': 2, 'flair': 'Discussion', 'upVotes': 0, 'isVideo': False, 'isAd': False, 'over18': False, 'createdAt': '2024-02-08T05:29:48.000Z', 'scrapedAt': '2024-02-12T20:40:28.124Z', 'dataType': 'post'}]
  
def process_json(json) : 
    new_jsons = []
    for json in test : 
        content = json['title'] + " " + json['body']
        new_json = {'id' : json['id'], 'body' : content, 'username' : json['username']}
        new_jsons.append(new_json)

    print(new_jsons)

test2 = process_json(test)
print(test2)