# check_active_follower

## venv
```
$ python3 -m venv venv
$ . ./venv/bin/activate
```

## pip
```
$ python3 -m pip install --upgrade pip
$ pip install -r requirements.txt
```

## source.py
```
source.py 17
client = tweepy.Client('your BEARER_TOKEN', wait_on_rate_limit=True)
or
add BEARER_TOKEN in os.environ

$ python3 source.py
username > [username (example:mi0256)]
```

get BEARER_TOKEN from TwitterAPI v2  

source.py make data.json(savefile)  
If it stops running, it will resume reading Data.json.

[Tweepy Docs](https://docs.tweepy.org/en/stable/)
