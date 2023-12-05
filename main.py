import requests
import matplotlib.pyplot as plt
from datetime import datetime
# from spellchecker import SpellChecker. I have issues with this library but you should not have. Not sure why I do.
from textblob import TextBlob
import spotipy as sp
from spotipy.oauth2 import SpotifyClientCredentials


def get_weather_info(location):
    # Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key
    api_key = '47a5a30340051f02af63ef6263d70143'

    # OpenWeatherMap API endpoint for 5-day forecast by city name
    api_url = f'https://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}'

    try:
        # Make the API request
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            weather_data = response.json()

            # Extract relevant data for the next 5 days
            forecast = weather_data['list']

            # Initialize lists to store data for each day
            dates = []
            temperatures = []
            rains = []

            # Extract temperature and rain information for each day
            for item in forecast:
                timestamp = item['dt']
                date = datetime.utcfromtimestamp(timestamp).date()
                if date not in dates:
                    dates.append(date)
                    temperatures.append(item['main']['temp'] - 273.15)  # Convert to Celsius
                    if 'rain' in item:
                        rains.append(item['rain']['3h'])
                    else:
                        rains.append(0)

            # Create a bar graph to display temperature and rain for each day
            plt.figure(figsize=(10, 6))
            plt.bar(dates, temperatures, label='Temperature (°C)')
            plt.bar(dates, rains, label='Rain (mm)', alpha=0.5)
            plt.xlabel('Date')
            plt.ylabel('Value')
            plt.title(f'5-Day Weather Forecast for {location}')
            plt.legend()
            plt.show()
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def get_weather_recommendation(location):
    # Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key
    api_key = '47a5a30340051f02af63ef6263d70143'

    # OpenWeatherMap API endpoint for current weather data by city name
    api_url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}'

    try:
        # Make the API request
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            weather_data = response.json()

            # Extract relevant weather data
            temperature_celsius = weather_data['main']['temp'] - 273.15  # Convert to Celsius
            wind_speed = weather_data['wind']['speed']
            rain = weather_data.get('rain', {}).get('1h', 0)  # Rain in the last hour (mm)
            feels_like_celsius = weather_data['main']['feels_like'] - 273.15  # Convert to Celsius
            humidity = weather_data['main']['humidity']
            is_sunny = 'clear' in weather_data['weather'][0]['description'].lower()

            print(f"Weather details for {location}:")
            print(f"Temperature: {temperature_celsius:.2f}°C")
            print(f"Wind Speed: {wind_speed} m/s")
            print(f"Rain (last hour): {rain} mm")
            print(f"Feels Like: {feels_like_celsius:.2f}°C")
            print(f"Humidity: {humidity}%")
            print(f"Sunny: {'Yes' if is_sunny else 'No'}")

            if is_sunny:
                if temperature_celsius > 25:
                    print("Recommendation: Wear light and breathable clothing, sunglasses, and sunscreen.")
                elif temperature_celsius > 18:
                    print("Recommendation: Bring along a light jacket and don't forget your sunglasses.")
                else:
                    print("Recommendation: Wear layers and bring a jacket.")
            elif rain > 0:
                print("Recommendation: Get dressed for a rainy day! Don't forget your umbrella and waterproof jacket.")
            else:
                print("Recommendation: Dress comfortably for the day.")

        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def recommend_music(mood, location):
    # Customize your music recommendation logic based on mood and location
    # You can search for specific playlists, tracks, or artists on Spotify
    # I chose playlists related to mood but up for discussion

    # Define keywords for different moods (wecan customize these)
    mood_keywords = {
        "happy": "happy music",
        "upbeat": "upbeat music",
        "mellow": "mellow music",
        "rainy": "rainy day music",
        "neutral": "chill music"
    }

    # Search for playlists based on mood
    mood_keyword = mood_keywords.get(mood, "chill music")  # I chose "chill music" if mood is not recognized. Again up for discussion.
    # results = sp.search(q=mood_keyword, type='playlist', limit=5)  # Limit to 5 playlists. Up for discussion group
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    results = sp.search(q=track_name, type='track')

    if results and 'playlists' in results:
        playlists = results['playlists']['items']
        if playlists:
            print(f"Here are some {mood} playlists you might like in {location}:")

            for playlist in playlists:
                print(f"{playlist['name']}: {playlist['external_urls']['spotify']}")

        else:
            print(f"No {mood} playlists found.")
    else:
        print("An error occurred while searching for music.")


def main():
    # Prompt the user for their desired location
    location = input("Where is your desired location: ")

    # Get weather information and provide recommendations
    get_weather_info(location)

    # Ask if the user wants detailed weather information
    choice = input(f"Do you want detailed weather information for {location}? (yes/no): ").lower()

    if choice == 'yes':
        # Get detailed weather information and provide recommendations
        get_weather_recommendation(location)
    else:
        # Ask the user about their mood
        mood = input("How are you feeling today (happy/upbeat/mellow/rainy/neutral)? ").lower()

        # Recommend music based on mood and location
        recommend_music(mood, location)

    print(f"Have a great time in {location}!")

if __name__ == "__main__":
    main()
