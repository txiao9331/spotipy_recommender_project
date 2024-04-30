import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pickle
import time
import streamlit as st
import random

# Initialize Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

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
        track_id = tracks_df.loc[tracks_df['number'] == track_number, 'track_id'].iloc[0]
        return track_id
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
    with open('../spotipy_data/model_km100.pickle', 'rb') as handle:
        km100 = pickle.load(handle)
    with open('../spotipy_data/scaler.pickle', 'rb') as handle:
        scaler = pickle.load(handle)

    scaled_features = scaler.transform(user_features)
    user_cluster = km100.predict(scaled_features)[0]
    return user_cluster

def random_recommendation(user_cluster):
    tracks_clustered_df = pd.read_csv('../spotipy_data/tracks_clustered_df2.csv')
    tracks_recommendation = tracks_clustered_df[tracks_clustered_df['cluster_km100'] == user_cluster]
    return tracks_recommendation.sample(n=3).reset_index(drop=True)


random.seed()
def recommendation(user_cluster):
    while True:
        tracks_recommendation_random = random_recommendation(user_cluster)
        st.write("Recommended tracks:")
        st.dataframe(tracks_recommendation_random[['artist_name', 'track_name']])
        
        # Generate unique keys using random numbers
        unique_key_satisfied = f"satisfied_with_recommendations_{random.randint(1, 1000000)}"
        unique_key_new = f"get_new_recommendations_{random.randint(1, 1000000)}"
        
        if st.button('Satisfied with recommendations', key=unique_key_satisfied):
            break  # Exit the loop if the user is satisfied
        if st.button('Get new recommendations', key=unique_key_new):
            # Sleep to ensure unique keys on rapid button presses
            time.sleep(1)
            continue
    return tracks_recommendation_random


# Initialize the app
def main():
    st.title('Music Recommender System')
    song = st.text_input('Please write a song that you like:', key='song_input')
    if song:
        tracks_df = find_song(song)
        if not tracks_df.empty:
            track_id = select_track(tracks_df)
            if track_id:
                embed_track(track_id)
                user_features = user_track_features(track_id)
                user_cluster = user_predict_km100(user_features)
                if st.button('Get Recommendations'):
                    recommendation(user_cluster)

if __name__ == "__main__":
    main()
