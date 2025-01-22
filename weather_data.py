import requests
import os
import argparse
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime

# Load environment variables from the .env file
load_dotenv()

# Get the access key from environment variables
access_key = os.getenv("ACCESS_KEY")  # Ensure the key matches your .env file

# Make sure the access key exists
if not access_key:
    raise ValueError("Access key is missing. Make sure it's set in the environment variables.")

# Set up argument parsing
parser = argparse.ArgumentParser(description="Fetch weather data for specified locations.")
parser.add_argument(
    "locations",
    nargs="+",
    help="List of locations to fetch weather data for, separated by spaces. Example: London Singapore Shanghai",
)

args = parser.parse_args()
locations = args.locations  # List of locations passed as arguments

# Base URL for the Weatherstack API
base_url = "https://api.weatherstack.com/current"

# Prepare a list to store weather data
weather_data = []

# Loop through each location and fetch data
for location in locations:
    params = {
        "access_key": access_key,
        "query": location
    }
    
    try:
        # Make the API request
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an error for bad HTTP responses (4xx or 5xx)
        
        # Parse the JSON response
        data = response.json()
        
        if "current" in data:
            # Include all relevant keys from the response
            weather = {
                "Location": data.get("location", {}).get("name", location),
                "Region": data.get("location", {}).get("region"),
                "Country": data.get("location", {}).get("country"),
                "Latitude": data.get("location", {}).get("lat"),
                "Longitude": data.get("location", {}).get("lon"),
                "Local Time": data.get("location", {}).get("localtime"),
                "Temperature": data["current"].get("temperature"),
                "Humidity": data["current"].get("humidity"),
                "Weather Description": ", ".join(data["current"].get("weather_descriptions", [])),
                "Wind Speed": data["current"].get("wind_speed"),
                "Wind Direction": data["current"].get("wind_dir"),
                "Pressure": data["current"].get("pressure"),
                "Precipitation": data["current"].get("precip"),
                "Feels Like": data["current"].get("feelslike"),
                "Visibility": data["current"].get("visibility"),
                "Observation Time": data["current"].get("observation_time"),
                "Request Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            weather_data.append(weather)
        else:
            print(f"No weather data found for {location}. Error: {data.get('error')}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {location}: {e}")

# Convert the weather data into a DataFrame for better visualization and saving
df = pd.DataFrame(weather_data)

# Save the DataFrame to a CSV file
df.to_csv("all_weather_data.csv", index=False)

# Print the DataFrame
print(df)
