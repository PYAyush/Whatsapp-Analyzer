import pandas as pd
import re

def preprocess(data):
    # Define the pattern to split messages and extract dates
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?(?:AM|PM|am|pm)?\s?[–-]\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Create a DataFrame with messages and dates
    df = pd.DataFrame({"message_date": dates, "user_message": messages})
    df["message_date"] = df["message_date"].str.replace('\u202f', ' ', regex=False)

    # Parse date with 12-hour format and am/pm
    df["message_date"] = pd.to_datetime(df["message_date"], format="%d/%m/%y, %I:%M %p - ")

    df.rename(columns={"message_date": "date"}, inplace=True)

    # Split user and message
    user = []
    messages = []
    for message in df["user_message"]:
        if ": " in message:
            user.append(message.split(": ")[0])
            messages.append(message.split(": ")[1])
        else:
            user.append("Niswarth")
            messages.append(message)

    df["user"] = user
    df["message"] = messages
    df.drop(columns=["user_message"], inplace=True)

    # Add additional columns for analysis
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df