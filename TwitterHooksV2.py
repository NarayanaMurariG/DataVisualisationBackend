import requests
import json
import calendar
import time
import os.path
from Botometer import generate_random_bot_scores
from Util import create_organic_metrics

# export 'BEARER_TOKEN'='<your_bearer_token>' and replace with your BearerToken
bearer_token = 'PutYourKeyHere'
search_url = "https://api.twitter.com/2/tweets/search/recent"

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {'query': 'Elon Musk -is:retweet','tweet.fields': 'text,author_id,conversation_id,geo'}

def update_json_file(file_name, new_data):
    if os.path.exists(file_name):
        with open(file_name, 'r+') as file:
            file_data = json.load(file)
            if file_name == 'bot_data':
                file_data.update(new_data)
            else:
                file_data.extend(new_data)
            file.seek(0)
            json.dump(file_data, file, ensure_ascii=False, indent=4)
    else:
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(new_data, file, ensure_ascii=False, indent=4)

def dumpToPickleDB(keyword, json_data, type):
    gmt = time.gmtime()
    ts = calendar.timegm(gmt)

    # Naming Convention
    fileName = keyword + '_' + type + '_' + str(ts) + '.json'

    with open(fileName, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def get_recent_tweets_counts(keyword,size_per_keyword):
    # recent_tweets_url = "https://api.twitter.com/2/tweets/search/recent"
    # params = {'query': 'Bitcoin -is:retweet', 'tweet.fields': 'context_annotations,author_id,conversation_id,geo'}
    final_data_set = []
    final_data_set_without_geo = []
    count = 0
    data, tweets_without_geo, next_token = getTweetsBatch(keyword, None)
    final_data_set.extend(data)
    final_data_set_without_geo.extend(tweets_without_geo)
    count = count + len(data)
    while count < size_per_keyword and next_token:
        data, tweets_without_geo, next_token = getTweetsBatch(keyword, next_token)
        final_data_set.extend(data)
        final_data_set_without_geo.extend(tweets_without_geo)
        count = count + len(data)


    print(keyword + ' - Tweet Count' +str(len(final_data_set)))
    #List: [{'author_id': '1150334633285955584', 'geo': {'place_id': '2a93711775303f90'}, 'context_annotations': [{'domain': {'id': '46', 'name': 'Business Taxonomy', 'description': 'Categories within Brand Verticals that narrow down the scope of Brands'}, 'entity': {'id': '1557696848252391426', 'name': 'Financial Services Business', 'description': 'Brands, companies, advertisers and every non-person handle with the profit intent related to Banks, Credit cards, Insurance, Investments, Stocks '}}, {'domain': {'id': '46', 'name': 'Business Taxonomy', 'description': 'Categories within Brand Verticals that narrow down the scope of Brands'}, 'entity': {'id': '1557697333571112960', 'name': 'Technology Business', 'description': 'Brands, companies, advertisers and every non-person handle with the profit intent related to softwares, apps, communication equipments, hardwares'}}, {'domain': {'id': '69', 'name': 'News Vertical', 'description': 'News Categories like Entertainment or Technology'}, 'entity': {'id': '1046545033657081857', 'name': 'News', 'description': 'News'}}, {'domain': {'id': '69', 'name': 'News Vertical', 'description': 'News Categories like Entertainment or Technology'}, 'entity': {'id': '1585285924069335040', 'name': 'Business & finance news'}}, {'domain': {'id': '131', 'name': 'Unified Twitter Taxonomy', 'description': 'A taxonomy of user interests. '}, 'entity': {'id': '781974596148793345', 'name': 'Business & finance'}}, {'domain': {'id': '131', 'name': 'Unified Twitter Taxonomy', 'description': 'A taxonomy of user interests. '}, 'entity': {'id': '840160819388141570', 'name': 'Tech news', 'description': 'Tech News'}}, {'domain': {'id': '131', 'name': 'Unified Twitter Taxonomy', 'description': 'A taxonomy of user interests. '}, 'entity': {'id': '840161214890106880', 'name': 'Business news', 'description': 'Business & Finance News'}}, {'domain': {'id': '131', 'name': 'Unified Twitter Taxonomy', 'description': 'A taxonomy of user interests. '}, 'entity': {'id': '848920371311001600', 'name': 'Technology', 'description': 'Technology and computing'}}, {'domain': {'id': '131', 'name': 'Unified Twitter Taxonomy', 'description': 'A taxonomy of user interests. '}, 'entity': {'id': '1046545033657081857', 'name': 'News', 'description': 'News'}}, {'domain': {'id': '131', 'name': 'Unified Twitter Taxonomy', 'description': 'A taxonomy of user interests. '}, 'entity': {'id': '1585285924069335040', 'name': 'Business & finance news'}}, {'domain': {'id': '10', 'name': 'Person', 'description': 'Named people in the world like Nelson Mandela'}, 'entity': {'id': '808713037230157824', 'name': 'Elon Musk', 'description': 'Elon Musk'}}, {'domain': {'id': '65', 'name': 'Interests and Hobbies Vertical', 'description': 'Top level interests and hobbies groupings, like Food or Travel'}, 'entity': {'id': '781974596148793345', 'name': 'Business & finance'}}, {'domain': {'id': '66', 'name': 'Interests and Hobbies Category', 'description': 'A grouping of interests and hobbies entities, like Novelty Food or Destinations'}, 'entity': {'id': '857878777191211008', 'name': 'Leadership', 'description': 'Leadership'}}, {'domain': {'id': '131', 'name': 'Unified Twitter Taxonomy', 'description': 'A taxonomy of user interests. '}, 'entity': {'id': '808713037230157824', 'name': 'Elon Musk', 'description': 'Elon Musk'}}, {'domain': {'id': '131', 'name': 'Unified Twitter Taxonomy', 'description': 'A taxonomy of user interests. '}, 'entity': {'id': '1091420346660470784', 'name': 'Tech personalities', 'description': 'Tech Professionals'}}, {'domain': {'id': '131', 'name': 'Unified Twitter Taxonomy', 'description': 'A taxonomy of user interests. '}, 'entity': {'id': '1166406108623163392', 'name': 'Business personalities'}}], 'edit_history_tweet_ids': ['1586385784671596547'], 'text': 'Elon Musk about to make twitter PG-13 as shit', 'conversation_id': '1586385784671596547', 'id': '1586385784671596547'}]
    return final_data_set,tweets_without_geo

def filterForLocation(data):
    filtered_tweets = []
    tweets_without_geo = []
    for tweet in data:
        if 'geo' in tweet:
            filtered_tweets.append(tweet)
        else:
            tweets_without_geo.append(tweet)

    # filtered_tweets_without_geo = filter_data_set(tweets_without_geo)
    # convo_tweets_without_geo,usernames = get_tweet_conversation(filtered_tweets_without_geo)
    # bot_data = get_bot_data(usernames)
    # final_bot_data.update(bot_data)
    # merged_json = merge_all_jsons(conversation_data, tweet_data)
    return filtered_tweets, tweets_without_geo

def getTweetsBatch(keywords, next_token):
    recent_tweets_url = "https://api.twitter.com/2/tweets/search/recent"
    params = {'query': keywords+' -is:retweet', 'tweet.fields': 'text,author_id,conversation_id,geo,context_annotations,created_at,public_metrics'}

    if next_token != None:
        params['next_token'] = next_token

    # Below Response will contain 10 tweets and next_token containing next page of 10 tweets
    response = requests.get(recent_tweets_url, auth=bearer_oauth, params=params)
    # Response Json Body {'data':[],meta:{}}

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    else:
        data = response.json()['data']
        meta = response.json()['meta']

        # Will return only tweets which have location tagged to them
        data, tweets_without_geo = filterForLocation(data)
        print(keywords+" : Found "+str(len(data))+" with location")
        if meta['next_token'] is not None:
            return data, tweets_without_geo, meta['next_token']
        else:
            return data, tweets_without_geo, None

def filter_data_set(final_data_set):
    filtered_data_set = []
    for data in final_data_set:
        tweet = {'id': data['id'],
                 'author_id': data['author_id'],
                 'conversation_id': data['conversation_id'],
                 'text': data['text'],
                 'geo': data['geo']['place_id'],
                 'created_at': data['created_at'],
                 'public_metrics': data['public_metrics'],
                 'organic_metrics': create_organic_metrics()
                 }

        domains = set()
        if 'context_annotations' in data:
            context_annotations = data['context_annotations']
            for annotation in context_annotations:
                domains.add(annotation['domain']['name'])

        tweet['domains'] = list(domains)
        filtered_data_set.append(tweet)

    return filtered_data_set

def get_location_details(tweet_dataset):
    # tweet_dataset is a list of tweet data
    location_url = 'https://api.twitter.com/2/tweets'
    for tweet in tweet_dataset:
        # ?ids=1136048014974423040&expansions=geo.place_id&place.fields=contained_within,country,country_code,full_name,geo,id,name,place_type' - -header
        params = {'ids': tweet['id'], 'expansions': 'geo.place_id', 'place.fields': 'contained_within,country,country_code,full_name,geo,id,name,place_type'}
        response = requests.get(location_url, auth=bearer_oauth, params=params)

        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        else:
            data = response.json()['data']
            includes = response.json()['includes']
            tweet['geo.place_id'] = data[0]['geo']['place_id']
            tweet['country'] = includes['places'][0]['country']

    return tweet_dataset

def get_tweet_conversation(tweet_data):
    conversation_url = 'https://api.twitter.com/2/tweets'
    conversation_data = {}
    usernames = []
    for tweet in tweet_data:
        params = {'ids': tweet['conversation_id'],
                  'tweet.fields': 'author_id,conversation_id,created_at,in_reply_to_user_id,referenced_tweets',
                  'expansions': 'author_id,in_reply_to_user_id,referenced_tweets.id',
                  'user.fields': 'name,username'}
        response = requests.get(conversation_url, auth=bearer_oauth, params=params)

        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        else:
            data = response.json()['data'] # List of objects
            users = response.json()['includes']['users'] # List
            usernames.extend(users)
            if len(data) > 0:
                convo = data[0]
                item = {
                    'author_id': convo['author_id'],
                    'text': convo['text'],
                    'created_at': convo['created_at']
                }
                conversation_data[tweet['conversation_id']] = item
            else:
                conversation_data[tweet['conversation_id']] = {}

    return conversation_data, usernames

def get_bot_data(usernames):
    bot_scores = generate_random_bot_scores(usernames)
    return bot_scores

def build_dataset_for_keywords(requirements):

    final_json = []
    final_bot_data = {}

    final_json_without_geo = []
    for data in requirements:
        tweet_data,tweet_data_without_geo = get_recent_tweets_counts(data['keyword'], data['count'])
        tweet_data = filter_data_set(tweet_data)
        tweet_data = get_location_details(tweet_data)
        conversation_data, usernames = get_tweet_conversation(tweet_data)
        bot_data = get_bot_data(usernames)
        final_bot_data.update(bot_data)
        merged_json = merge_all_jsons(conversation_data, tweet_data)
        final_json.extend(merged_json)

        tweet_data_without_geo = filter_data_set_without_geo(tweet_data_without_geo)
        conversation_data_without_geo, usernames_without_geo = get_tweet_conversation(tweet_data_without_geo)
        bot_scores_without_geo = get_bot_data(usernames_without_geo)
        final_bot_data.update(bot_scores_without_geo)
        merged_json_without_geo = merge_all_jsons(conversation_data_without_geo,tweet_data_without_geo)
        final_json_without_geo.extend(merged_json_without_geo)

    update_json_file('tweet_data',final_json)
    update_json_file('bot_data',final_bot_data)
    update_json_file('tweet_data_without_geo',final_json_without_geo)

#Updating country to no location for tweets without geo
def filter_data_set_without_geo(final_data_set):
    filtered_data_set = []
    for data in final_data_set:
        tweet = {'id': data['id'],
                 'author_id': data['author_id'],
                 'conversation_id': data['conversation_id'],
                 'text': data['text'],
                 'country': 'No Location',
                 'created_at': data['created_at'],
                 'public_metrics': data['public_metrics'],
                 'organic_metrics': create_organic_metrics()
                 }

        domains = set()
        if 'context_annotations' in data:
            context_annotations = data['context_annotations']
            for annotation in context_annotations:
                domains.add(annotation['domain']['name'])

        tweet['domains'] = list(domains)
        filtered_data_set.append(tweet)
    return filtered_data_set

def merge_all_jsons(conversation_data,tweet_data):
    merged_json = []
    for tweet in tweet_data:
        tweet_id = tweet['id']
        conversation_id = tweet['conversation_id']
        tweet['conversation_data'] = conversation_data[conversation_id]

        merged_json.append(tweet)

    return merged_json

if __name__ == "__main__":
    # Below is a list of keywords and no of tweets to fetch per key word
    requirements = [
        {'keyword': 'Bonus', 'count': 1},
        {'keyword': 'Free', 'count': 1}
        # {'keyword': 'Midterms', 'count': 1},
        # {'keyword': 'Bitcoin', 'count': 1}
    ]
    build_dataset_for_keywords(requirements)

    # 3 files for each key word will be generated. 1. Tweet Data 2. Conversation Data. 2 Bot Scores for authors