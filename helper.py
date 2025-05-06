# helper.py
# from app import num_messages
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
extract = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user  != "Overall":
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())
    num_media_messages = df[df['message']=='<Media omitted>\n'].shape[0]

    #fetch links
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))
    return num_messages, len(words), num_media_messages, len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x, df

def create_wordcloud(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    temp = ' '.join(df['message'])
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white').generate(temp)
    return wc

from collections import Counter
import pandas as pd

# Function to get the most common words used by a user
def most_common_words(selected_user, df):
    # Load stop words
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read()

    # Filter data for the selected user
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Exclude media messages
    temp = df[~df['message'].str.contains(r"Your security code with ~.*? changed\. Tap to learn more\.", na=False)]
    temp = df[df['message'] != '<Media omitted>\n']

    words = []

    # Process messages to extract words
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    # Create a DataFrame of the most common words
    return_df = pd.DataFrame(Counter(words).most_common(20), columns=['Word', 'Frequency'])
    return return_df

# extracting emojis from the messages
def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df
def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap