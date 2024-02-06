from apify_client import ApifyClient
# Simple module, input the JSON input of the reddit scraper via the docs here : {https://apify.com/trudax/reddit-scraper/api/client/python} and then input that into the apify_reddit_agent method to get the returned value of the scrape.
def apify_reddit_agent(json_input) :    
    info_array = []
    client = ApifyClient('apify_api_fKZ25ERj0eKmcONf6XJtjoGbrLbL7s1WrYyh')

    run_input=json_input


    run = client.actor("trudax/reddit-scraper-lite").call(run_input=run_input)

    for item in client.dataset(run["defaultDatasetId"]).iterate_items() : 
        info_array.append(item)
        print(item)
        print("""

    """)
    return info_array
