import snscrape.modules.twitter as sntwitter
import pandas as pd

query = "Air Asia lang:id until:2023-06-27 since:2023-03-23"
tweets = []
limit = 10000

for tweet in sntwitter.TwitterSearchScraper(query).get_items():
    if len(tweets) == limit:
        break
    else:
        if tweet.inReplyToUser and tweet.mentionedUsers is not None:
            tweets.append([tweet.user.id, tweet.user.username, tweet.date, tweet.rawContent, tweet.id, tweet.replyCount, tweet.retweetCount, tweet.likeCount, tweet.inReplyToUser.username, [user.username for user in tweet.mentionedUsers], tweet.hashtags])
        elif tweet.inReplyToUser is not None and tweet.mentionedUsers is None:
            tweets.append([tweet.user.id, tweet.user.username, tweet.date, tweet.rawContent, tweet.id, tweet.replyCount, tweet.retweetCount, tweet.likeCount, tweet.inReplyToUser.username, tweet.mentionedUsers, tweet.hashtags])
        elif tweet.inReplyToUser is None and tweet.mentionedUsers is not None:
            tweets.append([tweet.user.id, tweet.user.username, tweet.date, tweet.rawContent, tweet.id, tweet.replyCount, tweet.retweetCount, tweet.likeCount, tweet.inReplyToUser, [user.username for user in tweet.mentionedUsers], tweet.hashtags])
        else:
            tweets.append([tweet.user.id, tweet.user.username, tweet.date, tweet.rawContent, tweet.id, tweet.replyCount, tweet.retweetCount, tweet.likeCount, tweet.inReplyToUser, tweet.mentionedUsers, tweet.hashtags])
        
df = pd.DataFrame(tweets, columns=['userId', 'username', 'date', 'content', 'tweetId', 'replyCount', 'retweetCount', 'likeCount', 'inReplyToUser', 'mentionedUsers', 'hashtags'])
print(df)

# to save to csv
df.to_csv('tweets_air asia2.csv')