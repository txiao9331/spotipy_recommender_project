import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
from IPython.display import IFrame,display
import numpy as np
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

import pickle


def find_song(song):
    counter = 0
    retry = True
    offset = 0
    # all_track_info = []
    
    while retry:
        # search for songs with offset
        song_results = sp.search(q=song, market="GB", limit=5, offset=offset)

        track_info = []
        # store info
        for track in song_results['tracks']['items']:
            counter += 1  # add No. of track
            track_id = track['id']
            track_name = track['name']
            artist_names = ', '.join([artist['name'] for artist in track['artists']])
            track_info.append({'track_id': track_id, 'track_name':track_name,'artist_names': artist_names,'number': counter})
        
        # create dataframe
        track_df = pd.DataFrame(track_info)
        
        # display results
        print(f"Results {offset+1}-{offset+len(track_df)}:")
        display(track_df)
        
        # ask user if satisfied
        user_input = input("Do you find the song? (y/n)").lower()
        if user_input not in ["y","n"]:
            print('Input invalid, try again')
            user_input = input("Do you find the song? (y/n)").lower()
        elif user_input == 'n':
            offset += 5  # adjust offset for next search
            retry = True
        elif user_input == 'y':
            break
    return track_df

def select_track(tracks_df):
    while True:
        track_number = input('Please input the number of the song: ')

        if track_number.isdigit():
            track_number = int(track_number)
            if track_number in tracks_df['number'].values:
                # Perform actions for valid track number
                track_id = tracks_df.loc[tracks_df['number'] == track_number, 'track_id'].iloc[0]
                break  # Exit the loop if the input is valid
            else:
                print("Invalid track number. Please input a number within the range.")
        else:
            print("Invalid input. Please input a valid number.")
    return track_id

def embed_track(track_id):
    return IFrame(src="https://open.spotify.com/embed/track/"+track_id+"?utm_source=generator",
            #src="spotify:track:3rTIcUMMP2Ez33DfjJlb9e:autoplay:true",
            width="320",
            height="80",
            frameborder="0",
            allowtransparency="true",
            allow="encrypted-media",
            )

def user_track_features(track_id):
    user = sp.audio_features(track_id)[0]
    user_feature = pd.DataFrame([user],index=["user_track"])
    user_feature['is_explicit'] = False
    user_feature['popularity'] = 51
    audio_features_model_on = ['is_explicit','popularity', 'danceability', 'energy', 'key',
        'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness',
        'liveness', 'valence', 'tempo', 'time_signature']
    user_features = user_feature[audio_features_model_on]
    return user_features

def user_predict_km100(user_features):
    # load models with pickle
    with open('../spotipy_data/model_km100.pickle', 'rb') as handle:
        km100 = pickle.load(handle)
    with open('../spotipy_data/scaler.pickle', 'rb') as handle:
        scaler = pickle.load(handle)

    # fit the features
    scaled_features = scaler.transform(user_features)
    scaled_features

    # predict
    user_cluster = km100.predict(scaled_features)
    user_cluster = user_cluster[0]
    return user_cluster


def play_song(track_id):
    return IFrame(src="https://open.spotify.com/embed/track/"+track_id,
        width="320",
        height="80",
        frameborder="0",
        allowtransparency="true",
        allow="encrypted-media",
        )

def random_recommendation(user_cluster):
    tracks_clustered_df = pd.read_csv('../spotipy_data/tracks_clustered_df2.csv')
    tracks_recommendation = tracks_clustered_df[tracks_clustered_df['cluster_km100'] == user_cluster]
    tracks_recommendation_random = tracks_recommendation.sample(n=3).reset_index(drop=True)
    tracks_recommendation_random = tracks_recommendation_random[['artist_id','artist_name','track_id','track_name']]
    return tracks_recommendation_random

def recommendation(user_cluster):
    tracks_recommendation_random = random_recommendation(user_cluster)

    satisfied = False
    while not satisfied:
        display(tracks_recommendation_random)

        # Ask user if satisfied
        satisfaction = input("Maybe another 3? (y/n): ").strip().lower()
        if satisfaction == "n":
            satisfied = True
        elif satisfaction == "y":
            # Sample 3 new random tracks
            tracks_recommendation_random = random_recommendation(user_cluster)
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")
    
    return tracks_recommendation_random


def user_predict_km200(user_features):
    # load models with pickle
    with open('../spotipy_data/km200.pickle', 'rb') as handle:
        km200 = pickle.load(handle)
    with open('../spotipy_data/scaler.pickle', 'rb') as handle:
        scaler = pickle.load(handle)

    # fit the features
    scaled_features = scaler.transform(user_features)
    scaled_features

    # predict
    user_cluster = km200.predict(scaled_features)
    user_cluster = user_cluster[0]
    return user_cluster

def random_recommendation2(user_cluster):
    tracks_clustered_df = pd.read_csv('../spotipy_data/tracks_clustered_df2.csv')
    tracks_recommendation = tracks_clustered_df[tracks_clustered_df['cluster_km200'] == user_cluster]
    tracks_recommendation_random = tracks_recommendation.sample(n=3).reset_index(drop=True)
    tracks_recommendation_random = tracks_recommendation_random[['artist_id','artist_name','track_id','track_name']]
    return tracks_recommendation_random

def recommendation2(user_cluster):
    tracks_recommendation_random = random_recommendation2(user_cluster)

    satisfied = False
    while not satisfied:
        display(tracks_recommendation_random)

        # Ask user if satisfied
        satisfaction = input("Maybe another 3? (y/n): ").strip().lower()
        if satisfaction == "n":
            satisfied = True
        elif satisfaction == "y":
            # Sample 3 new random tracks
            tracks_recommendation_random = random_recommendation2(user_cluster)
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")
    
    return tracks_recommendation_random