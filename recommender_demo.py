import pandas as pd
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pickle
import streamlit as st

# Initialize Spotify API

# Fetch client ID and client secret from environment variables
client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')

if not client_id or not client_secret:
    raise Exception("Please set the SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET environment variables.")

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

def find_song(song):
    if 'offset' not in st.session_state:
        st.session_state.offset = 0

    song_results = sp.search(q=song, market="GB", limit=5, offset=st.session_state.offset)
    track_info = [{
        'track_id': track['id'],
        'track_name': track['name'],
        'artist_names': ', '.join(artist['name'] for artist in track['artists']),
        'number': idx + 1 + st.session_state.offset
    } for idx, track in enumerate(song_results['tracks']['items'])]

    track_df = pd.DataFrame(track_info)
    if not track_df.empty:
        st.write(f"Results {st.session_state.offset + 1}-{st.session_state.offset + len(track_df)}:")
        st.dataframe(track_df[['number', 'track_name', 'artist_names']])

    if st.button('Load more results', key='load_more_results'):
        st.session_state.offset += 5  # Increment the offset

    return track_df

def select_track(tracks_df):
    st.subheader('Select a Song')
    track_number = st.selectbox('Please select the number of the song:', tracks_df['number'])
    st.write("")  # Add space for clarity
    if st.button('Confirm'):
        st.session_state.track_id = tracks_df.loc[tracks_df['number'] == track_number, 'track_id'].iloc[0]
        return st.session_state.track_id
    else:
        return None  # Return None if "Confirm" button is not clicked

def embed_track(track_id):
    track_url = f"https://open.spotify.com/embed/track/{track_id}?utm_source=generator"
    st.components.v1.iframe(track_url, width=320, height=80)

def user_track_features(track_id):
    features = sp.audio_features(track_id)[0]  # Retrieve audio features from Spotify API
    
    # Create a DataFrame for a single track's features
    features_df = pd.DataFrame([features], index=["user_track"])

    # Ensure only the features used during model training are included for prediction
    # The list of features should match exactly those you've used during training
    audio_features_model_on = [
        'is_explicit', 'popularity', 'danceability', 'energy', 'key', 
        'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 
        'liveness', 'valence', 'tempo', 'time_signature'
    ]

    # Assume you need to manually set 'is_explicit' and 'popularity' for this example
    features_df['is_explicit'] = False  # This should be updated based on actual track info if available
    features_df['popularity'] = 50  # This should be fetched or estimated if not available in audio_features

    # Select only the relevant features for the model
    user_features = features_df[audio_features_model_on].copy()

    return user_features

def user_predict_km100(user_features):
    with open('spotipy_data/model_km100.pickle', 'rb') as handle:
        km100 = pickle.load(handle)
    with open('spotipy_data/scaler.pickle', 'rb') as handle:
        scaler = pickle.load(handle)

    scaled_features = scaler.transform(user_features)
    user_cluster = km100.predict(scaled_features)[0]
    return user_cluster

def random_recommendation(user_cluster):
    tracks_clustered_df = pd.read_csv('spotipy_data/tracks_clustered_df2.csv')
    tracks_recommendation = tracks_clustered_df[tracks_clustered_df['cluster_km100'] == user_cluster]
    return tracks_recommendation.sample(n=3).reset_index(drop=True)


def recommendation(user_cluster):
    # Initialize or maintain the state for recommendations
    if 'recommendation_index' not in st.session_state:
        st.session_state.recommendation_index = 0

    # Fetch new recommendations
    tracks_recommendation_random = random_recommendation(user_cluster)
    st.write("Recommended tracks:")
    st.dataframe(tracks_recommendation_random[['artist_name', 'track_name']])

    # Embed each track using Spotify's iframe
    for index, row in tracks_recommendation_random.iterrows():
        track_url = f"https://open.spotify.com/embed/track/{row['track_id']}?utm_source=generator"
        st.components.v1.iframe(track_url, width=320, height=80)

    # Button for confirming satisfaction with recommendations
    if st.button('Satisfied with recommendations'):
        st.session_state.show_start_over = True  # Set flag to show "Start Over" button

        if 'show_start_over' in st.session_state and st.session_state.show_start_over:
            if st.button('Start Over', key='start_over_after_satisfaction'):
                st.session_state.clear()  # Clear the session state to reset all stored variables
                st.rerun()  # Rerun the app from the beginning

    elif st.button('Get new recommendations'):
        # Fetch and display new recommendations
        st.session_state.recommendation_index += 1  # Update the state for new recommendations
        st.rerun()  # Optionally rerun to refresh recommendations


# Define a function to apply gradient background color to the sidebar
def set_sidebar_style():
    st.markdown("""
        <style>
            .sidebar .sidebar-content {
                background-image: linear-gradient(to bottom, #00b300, #009900); /* Adjust gradient colors as per your preference */
            }
        </style>
    """, unsafe_allow_html=True)

# Call the function to apply the gradient background color
set_sidebar_style()


# Initialize the app
def main():
    st.title('Spotify Music Recommender System')

    # Place the "Start Again" button at the top of the page
    if st.button('Start Again'):
        st.session_state.clear()  # Clear all session state
        st.rerun()  # Rerun the application from the beginning
    # Insert Spotify logo in sidebar
    st.sidebar.image("img/Spotify_Logo_CMYK_Green.png", use_column_width=True, width=100)
    st.sidebar.header('Start from here!')
    # Continue with the rest of your app
    song = st.sidebar.text_input('Please write a song that you like:', key='song_input')
    if song:
        tracks_df = find_song(song)
        if not tracks_df.empty:
            if 'track_id' not in st.session_state or st.session_state.track_id is None:
                st.session_state.track_id = select_track(tracks_df)
            if st.session_state.track_id:
                embed_track(st.session_state.track_id)
                user_features = user_track_features(st.session_state.track_id)
                user_cluster = user_predict_km100(user_features)
                if st.button('Get Recommendations'):
                    recommendation(user_cluster)

if __name__ == "__main__":
    main()
