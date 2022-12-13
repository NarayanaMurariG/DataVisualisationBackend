import random
from statistics import mean

"""
    This below function is used to generate synthetic data for the bot scores
    in place of botomerter.org API.  
"""
def generate_random_bot_scores(users):
    bot_scores = {}

    for user in users:
        fake_follower = round(random.uniform(0.00, 100.00), 2)
        financial = round(random.uniform(0.00, 100.00), 2)
        self_declared = round(random.uniform(0.00, 100.00), 2)
        spammer = round(random.uniform(0.00, 100.00), 2)

        data = (fake_follower, financial, self_declared, spammer)
        overall = mean(data)

        item = {
            'fake_follower': fake_follower,
            'financial': financial,
            'overall': overall,
            'self_declared': self_declared,
            'spammer': spammer
        }
        author_id = user['id']
        bot_scores[author_id] = item

    return bot_scores


def generate_random_bot_scores_v2(author_ids):
    bot_scores = {}

    for author_id in author_ids:
        fake_follower = round(random.uniform(0.00, 100.00), 2)
        financial = round(random.uniform(0.00, 100.00), 2)
        self_declared = round(random.uniform(0.00, 100.00), 2)
        spammer = round(random.uniform(0.00, 100.00), 2)

        data = (fake_follower, financial, self_declared, spammer)
        overall = mean(data)

        item = {
            'fake_follower': fake_follower,
            'financial': financial,
            'overall': overall,
            'self_declared': self_declared,
            'spammer': spammer
        }
        bot_scores[author_id] = item

    return bot_scores