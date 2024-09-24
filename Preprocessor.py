import re
import pandas as pd
from datetime import datetime

def preprocess(data):
    # Adjust the regex pattern to match your chat format correctly
    # Assuming format: "dd/mm/yy, HH:MM - user: message"
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    # Split the data into messages and dates
    messages = re.split(pattern, data)[1:]  # Skip the first empty entry
    dates = re.findall(pattern, data)  # Find all dates

    # Create a DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Convert message_date type (make sure to adjust format to match the actual date format)
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ', errors='coerce')

    # Rename columns for clarity
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if len(entry) > 2:  # Ensure that there are enough parts to extract user and message
            users.append(entry[1])  # Username is the second element
            messages.append(" ".join(entry[2:]))  # Message is everything after the username
        else:
            users.append('group_notification')
            messages.append(entry[0] if entry else '')

    df['user'] = users
    df['message'] = messages

    # Drop the original user_message column
    df.drop(columns=['user_message'], inplace=True)

    # Extract additional date features
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Create a period for each message
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append('23-00')
        elif hour == 0:
            period.append('00-01')
        else:
            period.append(f"{hour:02}-{hour + 1:02}")  # Format to ensure two digits

    df['period'] = period

    return df
