import re 
import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
extractor=URLExtract()

def user_messages(value):
    message=value.split(":")
    message=message[-1].split("\n")[0]
    return message
def user_name(value):
    message=value.split(":")
    return message[0]

def chats_to_data(data):
    temp="temp"
    # f=open(f"C://Users//jbbon//OneDrive//Desktop//Projects//WhatssApp_Chat_Analyzer//WhatsApp Chat with LOL//{file_name}.txt","r",encoding="utf-8")
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    # data=f.read()
    messages = re.split(pattern, data)
    messages = [msg for msg in messages if msg] 
    dates=re.findall(pattern,data)
    df=pd.DataFrame({"User_message":messages,"dates":dates})
    df["dates"]=pd.to_datetime(df["dates"],format='%m/%d/%y, %H:%M - ')
    df["user"]=df["User_message"].apply(user_name)
    df["User_message"]=df["User_message"].apply(user_messages)
    df["Date"]=df["dates"].dt.date
    df["Month"]=df["dates"].dt.month
    df["Year"]=df["dates"].dt.year
    df["Hour"]=df["dates"].dt.hour
    df["Minute"]=df["dates"].dt.minute
    df.to_csv(f"C://Users//jbbon//OneDrive//Desktop//Projects//WhatssApp_Chat_Analyzer//{temp}.csv",index=False)
    return df


def fetch_stats(user,df):
    if user!="All Members":
        df=df[df["user"]==user]

    num_messages=df.shape[0]

    words=[]
    for word in df["User_message"]:
        words.extend(word.split())

    media_shared=df[df["User_message"]==" <Media omitted>"].shape[0]

    links_shared=[]
    for message in df["User_message"]:
        links_shared.extend(extractor.find_urls(message))
    return num_messages,words,media_shared,links_shared

def most_active_user(df):
    x=df["user"].value_counts().head()
    df=round((df["user"].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={"index":"Name","user":"Percent"})
    return x,df

def wordcloud(user,df):
    if user!="All Members":
        df=df[df["user"]==user]

    wc=WordCloud(width=500,height=600,font_step=2,background_color="white")
    df_wc=wc.generate(df["User_message"].str.cat(sep=" "))
    return df_wc
        
        