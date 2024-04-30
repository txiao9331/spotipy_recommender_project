import streamlit as st
import pandas as pd
import numpy as np
import datetime
from PIL import Image


import melo_func as mf


# with st.sidebar:
#     song = st.text_input('Please input the name of song', 'Flowers')

#     st.button("Reset")
#     st.button("Done", type="primary")

# tracks_df = mf.find_song3(song)
# edited_df = st.data_editor(tracks_df)

# favorite_command = edited_df.loc[edited_df["rating"].idxmax()]["command"]
# st.markdown(f"Your favorite command is **{favorite_command}** 🎈")

import streamlit as st
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

if True:
    print('hello')

# # ###### To run streamlit page type in terminal 
# # ######## streamlit run file_name.py

# ####### Title + text
st.title('Welcome to Streamlit my first web page')
st.header('This is freakin coool!')

def find_song3(song):
    # counter = 0
    retry = True
    offset = 0
        
    while retry:
        # Search for songs with offset
        song_results = sp.search(q=song, market="GB", limit=5, offset=offset)

        track_info = []
        # Store info
        for track in song_results['tracks']['items']:
            # counter += 1  # Add No. of track
            track_id = track['id']
            track_name = track['name']
            artist_names = ', '.join([artist['name'] for artist in track['artists']])
            track_info.append({'track_id': track_id, 'track_name':track_name,'artist_names': artist_names,'check':False})
        
        # Create dataframe
        track_df = pd.DataFrame(track_info)
        
        # Display results
        st.write(f"Results {offset+1}-{offset+len(track_df)}:")
        st.write(track_df)
        
        # Ask user if satisfied
        user_input = st.radio("Do you find the song?", ('Yes', 'No'))
        if user_input == 'No':
            offset += 5  # Adjust offset for next search
            retry = True
        elif user_input == 'Yes':
            break
    return track_df


st.sidebar.title('Song Search')
st.sidebar.write('Enter the name of the song you want to search for:')
song_name = st.sidebar.text_input('Song Name', 'Flowers')

if st.sidebar.button('Search'):
    result_df = find_song3(song_name)
    if result_df is not None:  # Check if result_df is not None before displaying
        st.title("Search Results")
        st.write("Your search is complete. Here are the details:")
        edited_df = st.data_editor(result_df, num_rows="dynamic")
        if edited_df is not None and "check" in edited_df.columns:
            if edited_df["check"].any():
                song_search = edited_df.loc[edited_df["check"].idxmax()]["track_name"]
                st.markdown(f"The song you searched for is **{song_search}** 🎈")
