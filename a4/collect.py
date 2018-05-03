from TwitterAPI import TwitterAPI
import pickle
import sys
import time

consumer_key = 'd6sotVosQVSHMDd3yszgwqwHf'
consumer_secret = 'dvlPjZzu1gR0yBKvInR1p8VZyR6PTuBY9exgoyXkWZivkhqdSk'
access_token = '770445094327578624-NTlUjjHMmCNPDpOcZuKfCTWM8XWNbso'
access_token_secret = 'vsUNj7E0voer8WCuaIwtHzxXdfZ1AMSw5NRCYeKYUdS14'


def get_twitter():
    return TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)


def robust_request(twitter, resource, params, max_tries=5):

    for i in range(max_tries):
        request = twitter.request(resource, params)
        if request.status_code == 200:
            return request
        else:
            print('Got error %s \nsleeping for 15 minutes.' % request.text)
            sys.stderr.flush()
            time.sleep(61 * 15)
def main():
    twitter = get_twitter()
    tweets = []
    n_tweets = 1000
    req = robust_request(twitter, 'search/tweets', {'q': 'iphone', 'count': 100})
    for r in req:
        tweets.append(r)
        if len(tweets) >= n_tweets:
            break
    f = tweets[-1]['id']
    for r1v in range(0, 9):
        req = robust_request(twitter, 'search/tweets', {'q': 'iphone', 'count': 100, 'max_id': f})
        for r in req:
            tweets.append(r)
        f = tweets[-1]['id']
    for i in tweets:
        if i['user']['lang'] == 'en':
            pickle.dump(tweets, open('tweet_64.pkl', 'wb'))
        else:
            pass
    f = open("grph.txt", "w+")
    hscreenname=[]
    for j in tweets:
        if j['user']['protected'] == False:
            hscreenname.append(j['user']['screen_name'])
    for l in set(hscreenname[:20]):
        request=robust_request(twitter,'followers/ids', {'screen_name': l,'count': 50})
        for r in request:
            f.write("%s,%s\n" %(l,r))



if __name__ == '__main__':
    main()
