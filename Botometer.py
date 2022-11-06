import random
from statistics import mean

def generate_random_bot_scores(users):
    bot_scores = {}

    """
		"fake_follower": 3.0,
		"financial": 2.7,
		"overall": 5.0,
		"self_declared": 3.6,
		"spammer": 2.7
	"""

    for user in users:
        fake_follower = round(random.uniform(0.00, 100.00), 2)
        financial = round(random.uniform(0.00, 100.00), 2)
        self_declared = round(random.uniform(0.00, 100.00), 2)
        spammer = round(random.uniform(0.00, 100.00), 2)

        data = (fake_follower,financial,self_declared,spammer)
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
