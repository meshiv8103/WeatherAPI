import requests
import sys

API_KEY = "c28dc0d779a39ea11ebbd857a4c8845f"  
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
favourite_cities = []

def get_weather_details(city):
    try:
        params = {"q": city, "appid": API_KEY, "units": "metric"}
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        weather_info = {
            "City": data["name"],
            "Temperature": f"{data['main']['temp']}°C",
            "Weather": data["weather"][0]["description"].capitalize(),
            "Humidity": f"{data['main']['humidity']}%",
            "Wind Speed": f"{data['wind']['speed']} m/s"
        }
        return weather_info
    except requests.exceptions.HTTPError as e:
        return f"Error: {e.response.json()['message']}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def display_weather(weather_info):
    if isinstance(weather_info, dict):
        print("\nWeather Details:")
        for key, value in weather_info.items():
            print(f"{key}: {value}")
    else:
        print(weather_info)

def add_to_favourites(city):
    global favourite_cities
    if city in favourite_cities:
        print(f"{city} is already in your favourites.")
    elif len(favourite_cities) >= 3:
        print("You can only have up to 3 favourite cities. Remove one before adding another.")
    else:
        favourite_cities.append(city)
        print(f"{city} added to favourites.")

def list_favourites():
    if not favourite_cities:
        print("No favourite cities added yet.")
        return

    print("\nFavourite Cities:")
    for city in favourite_cities:
        print(f"\nCity: {city}")
        weather_info = get_weather_details(city)
        display_weather(weather_info)

def update_favourites():
    global favourite_cities
    print("\nCurrent Favourite Cities:")
    for idx, city in enumerate(favourite_cities, start=1):
        print(f"{idx}. {city}")
    
    try:
        choice = int(input("Enter the number of the city you want to remove: "))
        if 1 <= choice <= len(favourite_cities):
            removed_city = favourite_cities.pop(choice - 1)
            print(f"{removed_city} removed from favourites.")
            new_city = input("Enter the name of the new city to add: ")
            add_to_favourites(new_city)
        else:
            print("Invalid choice.")
    except ValueError:
        print("Please enter a valid number.")

def main():
    while True:
        print("\n--- Weather Management App ---")
        print("1. Search for Weather Details of a City")
        print("2. Add a City to Favourites")
        print("3. List Favourite Cities")
        print("4. Remove Favourite Cities")
        print("5. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            city = input("Enter the name of the city: ")
            weather_info = get_weather_details(city)
            display_weather(weather_info)
        elif choice == "2":
            city = input("Enter the name of the city to add to favourites: ")
            add_to_favourites(city)
        elif choice == "3":
            list_favourites()
        elif choice == "4":
            update_favourites()
        elif choice == "5":
            print("Thank you")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
