from math import log10
import random


"""
    Creating organic metrics and converting onto a
    log scale
"""
def create_organic_metrics():
    """
        "organic_metrics": {
         "impression_count": 3880,
         "like_count": 8,
         "reply_count": 0,
         "retweet_count": 4
         "url_link_clicks": 3
         "user_profile_clicks": 2
        }
    """
    data = {
        'impression_count': log10(random.randint(0, 1000000) + 100),
        'like_count': log10(random.randint(0, 100000) + 100),
        'reply_count': log10(random.randint(0, 1000) + 100),
        'retweet_count': log10(random.randint(0, 1000) + 100),
        'url_link_clicks': log10(random.randint(0, 1000) + 100),
        'user_profile_clicks': log10(random.randint(0, 1000) + 100)
    }
    return data


