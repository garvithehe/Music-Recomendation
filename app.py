from flask import Flask, request, render_template
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Initialize the Flask app
app = Flask(__name__)

# Spotify credentials
client_credentials_manager = SpotifyClientCredentials(
    client_id='ccf3dc620b69421eab3d7c8c9f073ceb',
    client_secret='56a3fe23b36e4285b39838dc4801e6e6'
)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Function to get track ID by song name
def get_track_id(song_name):
    results = sp.search(q=song_name, type='track', limit=1)
    if results['tracks']['items']:
        return results['tracks']['items'][0]['id']
    else:
        return None

# Function to find similar songs by song name
def find_similar_songs_by_name(song_name):
    track_id = get_track_id(song_name)
    if track_id:
        audio_features = sp.audio_features(tracks=[track_id])[0]

        recommendations = sp.recommendations(
            seed_tracks=[track_id],
            target_danceability=audio_features['danceability'],
            target_energy=audio_features['energy'],
            target_loudness=audio_features['loudness'],
            target_instrumentalness=audio_features['instrumentalness'],
            target_valence=audio_features['valence'],
            target_tempo=audio_features['tempo'],
            limit=7
        )

        recommended_tracks = [
            {"name": track['name'], "artist": track['artists'][0]['name']}
            for track in recommendations['tracks']
        ]
        return recommended_tracks
    else:
        return None

# Home route
@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = None
    if request.method == 'POST':
        song_name = request.form['song_name']
        recommendations = find_similar_songs_by_name(song_name)
    return render_template('index.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
