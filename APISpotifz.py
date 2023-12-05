from dotenv import load_dotenv
import os
import base64
import requests
import json

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

def get_token():
    if not client_id or not client_secret:
        raise ValueError("CLIENT_ID and CLIENT_SECRET environment variables must be set")

    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + auth_base64,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': 'client_credentials'}

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()  
        json_result = response.json()
        token = json_result.get('access_token')
        if not token:
            raise KeyError("Access token not found in the API response")
        return token
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error making the request to the Spotify API: {str(e)}")
    except KeyError as e:
        raise RuntimeError(f"Error parsing the API response: {str(e)}")

try:
    token = get_token()
    print(token)
except Exception as e:
    print(f"An error occurred: {str(e)}")

    
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import pandas as pd

def get_top_songs_by_location(location):
    # Load Spotify API credentials from environment variables
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')

    # Initialize Spotify client
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Search for playlists related to the user's location
    query = f"top songs in {location}"
    playlists = sp.search(q=query, type='playlist', limit=1)

    if not playlists['playlists']['items']:
        return None  # No playlists found for the location

    # Get the URI of the top playlist
    top_playlist_uri = playlists['playlists']['items'][0]['uri']

    # Get the tracks from the playlist
    tracks = sp.playlist_tracks(top_playlist_uri, limit=50)

    # Extract track information (name and artist)
    top_songs = []
    for track in tracks['items']:
        track_info = {
            'Song Name': track['track']['name'],
            'Artist': ', '.join([artist['name'] for artist in track['track']['artists']])
        }
        top_songs.append(track_info)

    return top_songs, top_playlist_uri

def main():
    location = input("What is your desired location? ")
    top_songs, playlist_uri = get_top_songs_by_location(location)

    if top_songs:
        df = pd.DataFrame(top_songs)
        print(f"Top 50 Songs in {location}:")
        print(df)

        # Ask the user if they want the link to the playlist
        choice = input("Would you like the link to the suggested playlist? (yes/no): ")
        if choice.lower() == "yes":
            playlist_url = f"https://open.spotify.com/playlist/{playlist_uri.split(':')[-1]}"
            print(f"Playlist Link: {playlist_url}")

if __name__ == "__main__":
    main()
