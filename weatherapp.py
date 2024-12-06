import tkinter as tk
import requests
import ttkbootstrap as ttk
from tkinter import messagebox
from PIL import Image, ImageTk

# Function to get weather information from OpenWeatherMap API
def get_weather(city):
    API_key = "e31090baa90152d9bd6e779fb3a0245e"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    res = requests.get(url)

    if res.status_code == 404:
        messagebox.showerror("Error", "City not found")
        return
    
    # Parse the response JSON to get the weather information
    weather = res.json()
    icon_id = weather['weather'][0]['icon']
    temperature = weather['main']['temp'] - 273.15
    description = weather['weather'][0]['description']
    city = weather['name']
    country = weather['sys']['country']

    # Get the icon URL and return all the weather information
    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    return (icon_url, temperature, description, city, country)
    
# Function to search for weather for a city
def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return
    # if the city is found, unpack the weather information
    icon_url, temperature, description, city, country = result
    location_label.configure(text=f"{city}, {country}")
    
    # Get the weather icon image from the URL and update icon label
    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon
    
    # update the temperature and description labels
    temperature_label.configure(text=f"Temperature: {temperature:.2f}°C")
    description_label.configure(text=f"Description: {description}")

root = ttk.Window(themename="morph")
root.title("Weather App")
root.geometry("1920x1080")

# Title label
title_label = tk.Label(root, text="Welcome to the Weather App", font=("Helvetica", 24))
title_label.pack(pady=10)

# Label for city entry
entry_label = tk.Label(root, text="Enter A City", font=("Helvetica", 16))
entry_label.pack(pady=5)

# Entry widget -> to enter the city name
city_entry = ttk.Entry(root, font=("Helvetica", 18))
city_entry.pack(pady=10)

# Bind the Enter key to the search function
city_entry.bind("<Return>", lambda event: search())

# Button widget -> to search for the weather information
search_button = ttk.Button(root, text="Search", command=search, bootstyle="warning")
search_button.pack(pady=10)

# Label widget -> to show the city/country name
location_label = tk.Label(root, font=("Helvetica", 25))
location_label.pack(pady=20)

# Label widget -> to show the weather icon
icon_label = tk.Label(root)
icon_label.pack()

# Label widget -> to show the temperature
temperature_label = tk.Label(root, font=("Helvetica", 20))
temperature_label.pack()

# Label widget -> to show the weather description
description_label = tk.Label(root, font=("Helvetica", 20))
description_label.pack()

root.mainloop()
