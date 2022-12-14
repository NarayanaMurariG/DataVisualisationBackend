# DataVisualisationBackend


Dependencies needed : requests (Command to install: pip install requests)
<br>
Python >= 3.0.0 is needed.
<br>
Replace Bearer Token in line 13 of TwitterHooks to your token from twitter dev account.

There are 2 scripts which can be used and:
1. TwitterHooksBulkFetchV2.py: Will fetch tweets in bulk and no of tweets equals count per keyword. Most will not have location details.
2. TwitterHooksV2.py: Will fetch no of tweets with location as specified in requirements for each keyword.

## Instructions to run
There is a requirements list in main method of above two python scripts.
<br>
In that requirements list we have to add dictionaries with two key-value pairs. They are:
<br>
1. keyword: 'Value is the keyword of tweets we want to search'
2. count: 'no of tweets with above keyword to be fetched'

<br> 
For TwitterHooksV2.py the sum of all counts of keywords should be less than 5 (Due to rate limit of API).
It is because we observed, for every 100 tweets we fetch only 1-3 tweets will have location.

<br> 
For TwitterHooksBulkFetchV2.py the sum of all counts of keywords should be less than 400 (Due to rate limit of API)


