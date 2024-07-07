import streamlit as st
from Pre_prossed_functions import *
import pandas as pd
import matplotlib.pyplot as plt

st.sidebar.title("WhatsApp Chat Analyzer")
chat_file=st.sidebar.file_uploader("Upload your file Here : ")
if chat_file is not None:
    bytes_data=chat_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=chats_to_data(data)


    unique_users=df["user"].unique()
    unique_users=[user for user in unique_users if len(user)<25]
    unique_users=[user for user in unique_users if "left" not in user]
    unique_users=[user for user in unique_users if "You" not in user]
    unique_users.insert(0,"All Members")
    unique_user=st.sidebar.selectbox("Select a User : ",unique_users)
    if st.sidebar.button("Show Analysis"):
        num_messages,num_words,media_shared,links_shared=fetch_stats(unique_user,df)
        if unique_user=="All Members":
            st.dataframe(df)
        else:
            st.dataframe(df[df["user"]==unique_user])

        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(len(num_words))
        with col3:
            st.header("Total Media Shared")
            st.title((media_shared))
        with col4:
            st.header("Total Links Shared")
            st.title(len(links_shared))\
            

        # if unique_user=="All Members":
        st.title("Most Active Users ")
        x,new_df=most_active_user(df)

        fig,ax=plt.subplots()

        col11,col22=st.columns(2)

        with col11:
            ax.bar(x.index,x.values)
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
            
        with col22:
            st.dataframe(new_df)

        df_wc=wordcloud(unique_user,df)
        fig,ax=plt.subplots()

        ax.imshow(df_wc)
        st.pyplot(fig)