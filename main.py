import streamlit as st
from dotenv import load_dotenv
load_dotenv() ##load all the nevironment variables
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

import os
import re

genai.configure(api_key=os.getenv("API_KEY"))

prompt="""You are Yotube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points.
After that, give your suggestion to learn the concept explained in video from 
other sources.
Please provide the summary of the text given here:  """

def extract_video_id(url):
    # Regular expression pattern to match YouTube video ID
    patterns = [
        r'^https:\/\/www\.youtube\.com\/watch\?v=([a-zA-Z0-9_-]+)',
        r'^https:\/\/youtu\.be\/([a-zA-Z0-9_-]+)',
    ]

    for pattern in patterns:
        match = re.match(pattern, url)
        if match:
            return match.group(1)
    
    return None

## getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id=extract_video_id(youtube_video_url)
        
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id,languages=['en', 'hi'])
        # print(transcript_text)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e
    
## getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text,prompt):

    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text

st.title("ClipNotes📝")
youtube_link = st.text_input("Enter YouTube Video URL:")
if youtube_link:
    video_id = extract_video_id(youtube_link)
    st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    try:
        transcript_text=extract_transcript_details(youtube_link)
        if transcript_text:
                summary=generate_gemini_content(transcript_text,prompt)
                st.markdown("## Detailed Notes:")
                st.write(summary)
    except:
        st.markdown("### Transcripts of this video are disabled !! Please try Another URL 😇")







