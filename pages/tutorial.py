import streamlit as st
import os

def tutorial_page():
    st.title("Tutorials Page")
    st.write("**Learn how to use this interface**")
    
    # Path to local video file
    video_path = "Videos/video1.mp4"
    
    if os.path.exists(video_path):
        with open(video_path, 'rb') as video_file:
            video_bytes = video_file.read()
            st.video(video_bytes, start_time=0)
    else:
        st.warning(f"Video file not found at: {video_path}")


if __name__ == "__main__":
    tutorial_page()
