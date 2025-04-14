import re
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s[ap]m\s*-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    
    # Create DataFrame
    df = pd.DataFrame({'date': dates, 'msg': messages})
    
    # Clean and convert dates
    df['date'] = df['date'].str.replace('\u202f', ' ', regex=False)
    df['date'] = df['date'].str.replace('\xa0', ' ', regex=False)
    df['date'] = df['date'].str.strip()
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y, %I:%M %p -', errors='coerce')
    
    # Process users and messages
    users = []
    messages_list = []
    
    for msg in df['msg']:
        # Handle both user messages and system notifications
        if ': ' in msg:
            user, message = msg.split(': ', 1)  # Split on first colon only
            users.append(user.strip())
            messages_list.append(message.strip())
        else:
            users.append('Group_Notification')
            messages_list.append(msg.strip())
    
    # Add columns after processing all messages
    df['user'] = users
    df['message'] = messages_list
    df.drop(columns=['msg'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    
    return df

# def preprocess1(data):
#     pattern = '\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s[ap]m?\s*-\s'
#     msg = re.split(pattern,data)[1:]
#     dates = re.findall(pattern,data)

#     df = pd.DataFrame({'date': dates, 'msg': msg})
#     df['date'] = df['date'].str.replace('\u202f', ' ', regex=False)
#     df['date'] = df['date'].str.replace('\xa0', ' ', regex=False)  # optional extra safety
#     df['date'] = df['date'].str.strip() 
#     df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y, %I:%M %p -')

#     users = []
#     messages_list = []  # Changed variable name to avoid conflict

#     for msg in df['msg']:  # Changed loop variable to 'msg'
#         entry = re.split('([\w\W]+?):\s', msg)
#         if len(entry) >= 3:  # Check if split found a colon (returns 3 parts)
#             users.append(entry[1])  # User is in the second group
#             messages_list.append(entry[2])  # Message is in the third group
#         else:
#             # Handle cases where the message doesn't have a colon
#             users.append('Group_Notification')
#             messages_list.append(msg)  # Use the original message

#         df['user'] = users
#         df['message'] = messages_list
#         df.drop(columns=['msg'], inplace=True)
    

#     return df
