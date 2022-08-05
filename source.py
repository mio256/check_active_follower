import os
import pprint
import json
import tweepy


def id_to_username(id: str):
    response = client.get_user(id=id)
    return response.data.username


def username_to_id(username: str):
    response = client.get_user(username=username)
    return response.data.id


client = tweepy.Client(os.environ['BEARER_TOKEN'], wait_on_rate_limit=True)

dict = {}

if os.path.isfile('data.json'):
    with open('data.json', 'r') as fp:
        dict = json.load(fp)
    response = client.get_tweet(dict['latest'], tweet_fields='created_at')
    latest = response.data.created_at
    me = id_to_username(dict['me'])
    print('{}の{}からの集計結果 5いいね以上'.format(me, latest))
    list = sorted(dict.items(), key=lambda x: x[1], reverse=True)
    for index in range(len(list)):
        if list[index][1] >= 5:
            if list[index][0] != 'latest' and list[index][0] != 'me' and list[index][0] != 'cnt':
                # print('{} {}'.format(list[index][0], list[index][1]))
                print('@{} {}'.format(id_to_username(list[index][0]), list[index][1]))
        else:
            break
    me = dict['me']
    cnt = dict['cnt']
    end_time = response.data.created_at
else:
    me = username_to_id(input('username>'))
    dict['me']=me
    cnt = 0
    end_time = None

for users_tweets in tweepy.Paginator(
    client.get_users_tweets,
    id=me,
    exclude=['retweets', 'replies'],
    # tweet_fields=['public_metrics'],
    max_results=100,
    end_time=end_time
):
    for tweet in users_tweets.data:
        cnt += 1
        for liking_users in tweepy.Paginator(
            client.get_liking_users,
            id=tweet.id,
            max_results=100
        ):
            try:
                for liking_user in liking_users.data:
                    print('cnt:{} id:{} like:{}'.format(cnt, tweet.id, liking_user.id))
                    if liking_user.id in dict:
                        dict[liking_user.id] += 1
                    else:
                        dict[liking_user.id] = 1
            except Exception as e:
                pass
            dict['latest'] = tweet.id
            dict['cnt'] = cnt
            with open('data.json', 'w') as fp:
                json.dump(dict, fp)

pprint.pprint(dict)

list = sorted(dict.items(), key=lambda x: x[1], reverse=True)

print('直近80日の{}ツイートを集計した結果 5いいね以上'.format(cnt))

for index in range(len(list)):
    if list[index][1]>=5:
        if list[index][0] != 'latest' and list[index][0] != 'me' and list[index][0] != 'cnt':
            print('@{} {}'.format(id_to_username(list[index][0]), list[index][1]))
    else:
        break
