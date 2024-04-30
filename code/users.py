import pandas as pd
import spotipy
import json
from spotipy.oauth2 import SpotifyClientCredentials
from IPython.display import IFrame
from flask import Flask, request

app = Flask(__name__)

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
