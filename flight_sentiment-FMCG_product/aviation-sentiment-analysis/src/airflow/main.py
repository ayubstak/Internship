from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import pandas as pd
import numpy as np
import os
import snscrape.modules.twitter as sntwitter
import datetime
import re
import nltk
import matplotlib.pyplot as plt

# get dag directory path
dag_path = os.getcwd()

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(5)
}

aviation_sentiment_dag = DAG(
    'aviation_sentiment',
    default_args=default_args,
    description='extract, transform, and load aviation sentiment data',
    schedule_interval=timedelta(days=7),
    catchup=False
)

def extract_data():
    # Calculate the date range for the last seven days
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=7)

    # Convert dates to string format for the query
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    # Formulate the query
    query = f"Super Air Jet lang:id since:{start_date_str} until:{end_date_str}"
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

    # Calculate the week number of the current date
    current_week = datetime.date.today().isocalendar()[1]

    # Formulate the filename with the week number
    filename = f"tweets_super_air_jet_{current_week}.csv"

    # Full path for the CSV file
    csv_file_path = f"{dag_path}/processed_data/{filename}"

    # to save to csv
    df.to_csv(csv_file_path, index=False)

    return df

def clean_data(df):
    features = df.iloc[:, 3].values

    processed_features = []

    for sentence in range(0, len(features)):
        # Remove all the special characters
        processed_feature = re.sub(r'\W', ' ', str(features[sentence]))
        # remove all single characters
        processed_feature= re.sub(r'\s+[a-zA-Z]\s+', ' ', processed_feature)
        # Remove single characters from the start
        processed_feature = re.sub(r'\^[a-zA-Z]\s+', ' ', processed_feature)
        # Substituting multiple spaces with single space
        processed_feature = re.sub(r'\s+', ' ', processed_feature, flags=re.I)
        # Removing prefixed 'b'
        processed_feature = re.sub(r'^b\s+', '', processed_feature)
        # Converting to Lowercase
        processed_feature = processed_feature.lower()
        processed_features.append(processed_feature)

    df['content'] = processed_features

    # Calculate the week number of the current date
    current_week = datetime.date.today().isocalendar()[1]

    # Formulate the filename with the week number
    filename = f"cleaned_tweets_super_air_jet_{current_week}.csv"

    # Full path for the CSV file
    csv_file_path = f"{dag_path}/processed_data/{filename}"

    # to save to csv
    df.to_csv(csv_file_path, index=False)

task_1 = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=aviation_sentiment_dag,
)

task_2 = PythonOperator(
    task_id='clean_data',
    python_callable=clean_data,
    dag=aviation_sentiment_dag,
)

task_1 >> task_2