import requests
from geopy.geocoders import Nominatim
from datetime import datetime
import pytz

API_KEY = "<Enter Api Key Here>"  
RADIUS_KM = 15
ISS_NORAD_ID = 25544

def get_coordinates(city_name):
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(city_name)
    if location:
        return location.latitude, location.longitude
    return None, None

def convert_to_ist(utc_timestamp):
    utc_time = datetime.utcfromtimestamp(utc_timestamp)
    utc_time = pytz.utc.localize(utc_time)
    ist_time = utc_time.astimezone(pytz.timezone("Asia/Kolkata"))
    return ist_time.strftime("%Y-%m-%d %H:%M:%S IST")

def get_satellites_above(lat, lon, alt=0, category_id=0):
    url = f"https://api.n2yo.com/rest/v1/satellite/above/{lat}/{lon}/{alt}/{RADIUS_KM}/{category_id}/&apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("above", [])
    return []

def get_satellite_stats(norad_id):
    url = f"https://api.n2yo.com/rest/v1/satellite/tle/{norad_id}&apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        sat_name = data.get("info", {}).get("satname", "Unknown")
        tle = data.get("tle", "")
        print(f"\n Satellite Info for NORAD ID {norad_id}:")
        print(f"Name: {sat_name}")
        print("TLE Data:\n" + tle)
    else:
        print("Failed to retrieve satellite stats.")

def get_visual_passes(norad_id, lat, lon, alt=0, days=2, min_visibility=60):
    url = f"https://api.n2yo.com/rest/v1/satellite/visualpasses/{norad_id}/{lat}/{lon}/{alt}/{days}/{min_visibility}/&apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        passes = response.json().get("passes", [])
        if passes:
            next_pass = passes[0]
            start_time = convert_to_ist(next_pass["startUTC"])
            max_time = convert_to_ist(next_pass["maxUTC"])
            end_time = convert_to_ist(next_pass["endUTC"])
            print(f"\n Next visible pass of NORAD ID {norad_id}:")
            print(f"  ➤ Start Time: {start_time}")
            print(f"  ➤ Max Elevation Time: {max_time} at {next_pass['maxEl']}°")
            print(f"  ➤ End Time: {end_time}")
        else:
            print("No visible passes in the next few days.")
    else:
        print("Failed to get pass data.")

def main():
    city = input("Enter the city name: ")
    lat, lon = get_coordinates(city)

    if lat is None:
        print("Invalid city name.")
        return

    print(f"\n Latitude: {lat}\n Longitude: {lon}")

    satellites = get_satellites_above(lat, lon)

    print(f"\n Total Satellites above {city} in a {RADIUS_KM} km radius: {len(satellites)}")
    
    if not satellites:
        return

    print("\n List of satellites (Name + NORAD ID):")
    for i, sat in enumerate(satellites):
        print(f"{i+1}. {sat['satname']} (NORAD ID: {sat['satid']})")

    try:
        selected_norad = int(input("\n Enter a NORAD ID to view stats and next pass: "))
        get_satellite_stats(selected_norad)
        get_visual_passes(selected_norad, lat, lon)
    except ValueError:
        print("Invalid NORAD ID.")

    print("\n Getting ISS pass data...")
    get_visual_passes(ISS_NORAD_ID, lat, lon)

if __name__ == "__main__":
    main()
