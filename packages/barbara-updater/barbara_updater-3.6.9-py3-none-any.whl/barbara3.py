# 9/5/24 added set position of scraped frame in national radar to prevent dead ends
# 9/4a/24 working to fix error while trying to make station models. This will be 3.6.8 
# 9/4/24 working to fix connection aborted error will be ver3.6.7
# this 9/2b/24 will be renamed 9/2c/24 on all other devices and will be ver 3.6.6
# 9/2b/24 changing this version (on bubba's old device) from other 9/2b/24 versions
# 9/2/24 Selenium set up correctly, a and b obs sites buttons working again
# 8/29/24 also programmatically install pytz and certifi this will be version 3.6.4 - not working on mine
# 8/28/24 testing to successfully import folium v3.6.3
# as of 8/23/24 this is the latest version (8/21/24) that's working w/o overlapping, but concerns about folium install
# 8/21A/24 change local radar queue function to avoid dead ends
# then had to install folium programmatically, correctly. ver 3.6.2
# ver 3.6.0 with maps for land sites, back buttons and stored user choices on page choose
# 8/21/24 Ver 3.6.0 brief delay message when random sites chosen & improved greeting message
# 8/20B/24 prevent display of back button on page choose when xs length > 0
# 8/20B/24 previous choices stored from page choose for reference and reuse
# 8/20A/24 now frame1 back button working for all products during initial set up
# 8/20/24 finish install back buttons & other small things - not working for all products
# 8/19A/24 back buttons installed up through reg sat choice
# 8/19/24 add back buttons - started to mess up on page_choose
# 8/18D eliminates delay before showing map of 3 random sites
# 8/18C will add map to show 3 random sites. 18D eliminates blank delay
# 8/18B all 3 working with map, flash before the map fixed - took out update idletasks
# 8/18A has first two stations working, often with a flash before map is displayed. 18B will work to get all 3
# 8/18/24 some a variables deleted (pg 138) will add new map and technique to bobs on 18A
# 8/17A/24 replace5nearby aobs check land working great. 17B will add color coding - giving up for now
# 8/17/24 replace5nearby layout set. Map not redrawn upon each site choice on 8/17A
# 8/12A/24 replace5nearby layout very close to goal. Buttons slow response
# 8/12/24 replace5nearby includes the new techniques for aobs_check_land
# 8/12/24 Have to change sounding functions back because of problems with 'img_label_sounding'
# 8/12/24 is 3.5.2 back to old error catching for radiosonde, calling next function or hide upon an error
# 8/10/24 will be 3.5.1 - only call hide functions to prevent overlapping images
# 8/10/24 working on double imaging with new ideas from pages 134-135 only call next function once
# 8/9A/24 adding error checking to include WebDriverException for station plots - aborted this idea for now
# 8/9/24 VERSION 3.5.0 random sites and buttons for sites. Check for functional buoys in def check_buoy
# 8/6B/24 brought in option to random choose 3 sites - confusion with variables:
# aobs_site, aobs_url, alternative_town_1, alternative_state_1
# 8/5A/24 ensure duplicate ntl sat labels not produced
# 8/5/24 ensure duplicate lcl radar labels not produced
# 8/2/24 added _forget labels commands to situation of a failed station plots
# 7/31A/24 more code to catch wifi drops for lcl radar
# 7/25/24 more _forget after sarah's display version 3.4.10
# 7/22/24 update ncar radar choose map
# 7/17A/24 further improving NWS radar complete set of frames, order of frames, speed
# 7/17/24 refining clearing disk space
# 7/16/24 working with updated NWS radar
# 7/15/24 removing logging from development machine
# 7/14/24 will include block to _forget labels in show sounding and display baro trace.
# 7/12/24 trying to fix double imaging after inserting NCAR radar
# 7/11A/24 included variable VERSION
# 7/11A/24 inserted code at the end of station center input to test if scraped_frame
# is blank, then call for show_scraped_frame
# for 7/8A/24 working to insert code to free up disk space programmatically
# on 7-8-24 will insert old ucar radar to replace nws radar
# 7/7/24 Attempt to fix radar loop with no echoes
# 7/4/24 need to run legacy version of rp OS 32-bit, x11, not Wayland

import subprocess
import sys

# Function to install a package using pip
def install_package(package_name):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package_name}: {e}")

# Check and install folium, pytz, and certifi if they are not already installed
try:
    import folium
except ImportError:
    install_package("folium")
    import folium

try:
    import pytz
except ImportError:
    install_package("pytz")
    import pytz

try:
    import certifi
except ImportError:
    install_package("certifi")
    import certifi


#import smbus
import smbus2 as smbus
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
import time
from time import strftime
import datetime as dt
from datetime import datetime, timedelta, timezone
#from datetime import timedelta #needed for determining display of 12z or 0z radiosonde
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
matplotlib.rcParams['toolbar'] = 'None'
import matplotlib.animation as animation
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import json
from matplotlib import rcParams
import io
from io import BytesIO
from PIL import Image
import matplotlib.image as mpimg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import traceback
import re
import imageio
from matplotlib.animation import FuncAnimation
import os
from math import radians, sin, cos, sqrt, atan2
import geopy.distance
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.exc import GeocoderTimedOut
import urllib.parse
from geopy.exc import GeocoderUnavailable
import subprocess
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException, SessionNotCreatedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import threading #allows to manage hang ups in solenium
import tkinter as tk
from tkinter import IntVar, Checkbutton
import tkinter.font as tkFont
from tkinter import ttk, IntVar
from tkinter import ttk, IntVar, messagebox
from tkinter import PhotoImage
from tkinter import font  # Import the font module
from tkinter import Tk, Label
from PIL import Image, ImageDraw, ImageFont, ImageTk, ImageChops
import urllib.parse
from collections import deque
from matplotlib.widgets import Button
import matplotlib.ticker as ticker
import warnings
#from memory_profiler import profile
import itertools
from itertools import cycle, islice
import psutil
import shutil # used to determine how to take screenshot on different systems and disk cleanup
import gc
import threading
from queue import Queue, Empty
from threading import Thread
from functools import partial
import logging
import traceback
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from tkinter import Tk, Button, simpledialog
import base64 # to write lcl radar urls
import random # for choosing sites near aobs_site
import pytz
import concurrent.futures # to scan large lists to assemble observation stations
import folium # these 4 needed for maps when displaying the 5 possible observation sites
import ssl
import certifi
from selenium.webdriver.chrome.service import Service as ChromeService
from dateutil.parser import parse # to handle reading obs formats
import urllib3 # included 9/4/24 to help with connection error while getting lightning

VERSION = "3.6.9"

# Define a fixed path for the screenshot
SCREENSHOT_PATH = '/home/santod/screenshot.png'
screenshot_filename = 'screenshot.png'   

RANDOM_NWS_API_ENDPOINT = "https://api.weather.gov"
RANDOM_NWS_API_STATIONS_ENDPOINT = f"{RANDOM_NWS_API_ENDPOINT}/stations"
RANDOM_NWS_API_LATEST_OBSERVATION_ENDPOINT = f"{RANDOM_NWS_API_ENDPOINT}/stations/{{station_id}}/observations/latest"

neighboring_states = {
    "ME": ["NH"],
    "NH": ["ME", "VT", "MA"],
    "VT": ["NH", "MA", "NY"],
    "MA": ["NH", "VT", "NY", "CT", "RI"],
    "RI": ["MA", "CT"],
    "CT": ["MA", "RI", "NY"],
    "NY": ["VT", "MA", "CT", "NJ", "PA"],
    "NJ": ["NY", "PA", "DE"],
    "PA": ["NY", "NJ", "DE", "MD", "WV", "OH"],
    "DE": ["PA", "NJ", "MD"],
    "MD": ["PA", "DE", "WV", "VA", "DC"],
    "DC": ["MD", "VA"],
    "VA": ["MD", "WV", "KY", "TN", "NC", "DC"],
    "WV": ["PA", "MD", "VA", "KY", "OH"],
    "NC": ["VA", "TN", "GA", "SC"],
    "SC": ["NC", "GA"],
    "GA": ["NC", "SC", "FL", "AL", "TN"],
    "FL": ["GA", "AL"],
    "AL": ["TN", "GA", "FL", "MS"],
    "TN": ["KY", "VA", "NC", "GA", "AL", "MS", "AR", "MO"],
    "KY": ["WV", "VA", "TN", "MO", "IL", "IN", "OH"],
    "OH": ["PA", "WV", "KY", "IN", "MI"],
    "MI": ["OH", "IN", "WI"],
    "IN": ["MI", "OH", "KY", "IL"],
    "IL": ["WI", "IN", "KY", "MO", "IA"],
    "WI": ["MI", "IL", "IA", "MN"],
    "MN": ["WI", "IA", "SD", "ND"],
    "IA": ["MN", "WI", "IL", "MO", "NE", "SD"],
    "MO": ["IA", "IL", "KY", "TN", "AR", "OK", "KS", "NE"],
    "AR": ["MO", "TN", "MS", "LA", "TX", "OK"],
    "LA": ["AR", "MS", "TX"],
    "MS": ["TN", "AL", "LA", "AR"],
    "TX": ["OK", "AR", "LA", "NM"],
    "OK": ["KS", "MO", "AR", "TX", "NM", "CO"],
    "KS": ["NE", "MO", "OK", "CO"],
    "NE": ["SD", "IA", "MO", "KS", "CO", "WY"],
    "SD": ["ND", "MN", "IA", "NE", "WY", "MT"],
    "ND": ["MN", "SD", "MT"],
    "MT": ["ND", "SD", "WY", "ID"],
    "WY": ["MT", "SD", "NE", "CO", "UT", "ID"],
    "CO": ["WY", "NE", "KS", "OK", "NM", "UT"],
    "NM": ["CO", "OK", "TX", "AZ", "UT"],
    "AZ": ["CA", "NV", "UT", "NM"],
    "UT": ["ID", "WY", "CO", "NM", "AZ", "NV"],
    "NV": ["ID", "UT", "AZ", "CA", "OR"],
    "ID": ["MT", "WY", "UT", "NV", "OR", "WA"],
    "OR": ["WA", "ID", "NV", "CA"],
    "WA": ["ID", "OR"],
    "CA": ["OR", "NV", "AZ"],
    "AK": [],
    "HI": [],
}

aobs_station_identifier = ""
bobs_station_identifier = ""
cobs_station_identifier = ""
a_town_state = ""
b_town_state = ""
c_town_state = ""

aobs_url = "" #included when making random sites work. Hopefully will eventually be able to take out.
bobs_url = ""
cobs_url = ""

# Create buttons with custom font size (adjust font size as needed)
button_font = ("Helvetica", 16, "bold")

global inHg_correction_factor
inHg_correction_factor = 1

global create_virtual_keyboard
#global keyboard_window
# Ensure global variables are defined at the top of your script
global current_target_entry
current_target_entry = None  # This will hold the currently focused entry widget

# Global declaration of page_choose_choice_vars according to rewriting 3/27/24
page_choose_choice_vars = []

# Initialize hold_box_variables with 0 for the first ten indices
hold_box_variables = [0] * 12  # Creates a list with ten zeros

# Additional setup code can go here


# Global variable declaration for email functions
global email_entry
email_entry = None

iterate_flag = False

cobs_only_click_flag = False #set up for buttons to change 1 posted obs at a time
bobs_only_click_flag = False
aobs_only_click_flag = False

refresh_flag = False
# to determine if user has chosen reg sat view
has_submitted_choice = False

# to signal if user has chosen random sites
random_sites_flag = False
# flag established to track whether img_label_national_radar is forgotten to smooth displays
national_radar_hidden = False

# Global variables for images
img_tk_national_radar = None
img_label_national_radar = None
img_label_national_satellite = None
img_label_satellite = None
img_label_sfc_map = None
baro_img_label = None

img_label = None # added 7/11/24 while working on saving dead end runs. Lightning & Station plots
img_label_sounding = None
vort_img_label = None

label_lcl_radar = None # to manage transition from ntl radar to lightning this had to be defined too

last_national_radar_scrape_time = None
last_national_satellite_scrape_time = None
last_national_sfc_map_scrape_time = None
last_vorticity_scrape_time = None
last_sounding_scrape_time = None
last_station_model_scrape_time = None

# set GUI buttons to None
scraped_to_frame1 = None
maps_only_button = None
pic_email_button = None
reboot_button = None

# for lightning display when scraped with selenium
lightning_max_retries = 2

last_forget_clock = datetime.now()

i = 0

alternative_town_1 = ""
alternative_state_1 = ""

alternative_town_2 = ""
alternative_state_2 = ""

alternative_town_3 = ""
alternative_state_3 = ""

def get_disk_usage(path):
    total, used, free = shutil.disk_usage(path)
    return total, used, free

def clean_apt_cache():
    try:
        subprocess.run(['sudo', 'apt-get', 'clean'], check=True)
        subprocess.run(['sudo', 'apt-get', 'autoclean'], check=True)
        subprocess.run(['sudo', 'apt-get', 'autoremove', '-y'], check=True)
        print("APT cache cleaned.")
    except subprocess.CalledProcessError as e:
        print(f"Error cleaning APT cache: {e}")

def clean_up_directory(directory, free_up_threshold=100 * 1024 * 1024):
    """
    Clean up files in the given directory if free disk space is below the threshold.
    :param directory: Directory to clean up
    :param free_up_threshold: Minimum free space required (in bytes)
    """
    try:
        total, used, free = get_disk_usage(directory)
        print(f"Before cleanup - Total: {total}, Used: {used}, Free: {free}")

        if free < free_up_threshold:
            print(f"Freeing up space in {directory}")
            for root, dirs, files in os.walk(directory, topdown=False):
                for name in files:
                    file_path = os.path.join(root, name)
                    try:
                        os.remove(file_path)
                        print(f"Deleted file: {file_path}")
                    except Exception as e:
                        print(f"Error deleting file {file_path}: {e}")

                for name in dirs:
                    dir_path = os.path.join(root, name)
                    try:
                        os.rmdir(dir_path)
                        print(f"Deleted directory: {dir_path}")
                    except Exception as e:
                        print(f"Error deleting directory {dir_path}: {e}")

        total, used, free = get_disk_usage(directory)
        print(f"After cleanup - Total: {total}, Used: {used}, Free: {free}")
    except FileNotFoundError as e:
        print(f"Directory not found: {directory}")

def additional_cleanup():
    """
    Perform additional cleanup tasks such as removing tmp files.
    """
    tmp_directories = ['/tmp', '/var/tmp']
    for directory in tmp_directories:
        clean_up_directory(directory, free_up_threshold=100 * 1024 * 1024)

def reboot_system():
    root.quit()
    os.system('sudo reboot')
    
def check_password(event):
    global key_sequence
    key_sequence += event.char  # Append pressed key to the sequence

    # Define your password (key sequence)
    password = '2barbaraterminal'  # You can choose a more complex password

    # Check if the correct sequence was entered
    if key_sequence.endswith(password):
        exit_full_screen(event)
        key_sequence = ''  # Reset sequence after successful password entry
    elif len(key_sequence) > len(password):  # Reset if sequence gets too long without a match
        key_sequence = key_sequence[-len(password):]  # Keep only the last few presses

def exit_full_screen(event):
    root.attributes("-fullscreen", False)  # This exits full screen mode
    root.bind('<Escape>', lambda e: None)  # Disable further Escape actions or rebind as needed

def start_fullscreen():
    root.geometry("1024x600")
    root.attributes('-zoomed', True)
    root.title("The Weather Observer")
    root.attributes('-fullscreen', True)  # no decoration

# Create a tkinter window
root = tk.Tk()
root.title("The Weather Observer")
root.geometry("1024x576+0+-1")

# Initialize key sequence storage
key_sequence = ''

# Bind all keypresses to the check_password function
root.bind('<Key>', check_password)

# Set up fullscreen and other startup configurations
root.after(4000, start_fullscreen)

lcl_radar_zoom_clicks = tk.IntVar(value=0) # establish variable for zoom on lcl radar

# Define StringVar for labels
left_site_text = tk.StringVar()
left_temp_text = tk.StringVar()
left_water_temp_text = tk.StringVar()
left_wind_text = tk.StringVar()

middle_site_text = tk.StringVar()
middle_temp_text = tk.StringVar()
middle_water_temp_text = tk.StringVar()
middle_wind_text = tk.StringVar()

right_site_text = tk.StringVar()
right_temp_text = tk.StringVar()
right_water_temp_text = tk.StringVar()
right_wind_text = tk.StringVar()

time_stamp_text = tk.StringVar()

# Use a smaller font for the buoys
buoy_font = font.Font(family="Helvetica", size=11, weight="bold")

# Use the default font size (14) for the regular condition when posting observations
obs_font = font.Font(family="Helvetica", size=14, weight="bold")

def get_location():
    try:
        response = requests.get('http://ip-api.com/json')
        data = response.json()
        if data['status'] == 'success':
            lat = data['lat']
            lon = data['lon']
            return lat, lon
    except requests.exceptions.RequestException:
        pass
    return None, None

# Function to convert pressure from Pascals to inches of mercury
def pascals_to_inches_hg(pascals):
    """Converts pressure in Pascals to inches of mercury."""
    return pascals / 3386.389

def get_aobs_site(latitude, longitude):
    global baro_input  # Global variable for barometric pressure
    global aobs_site   # Global variable for the name of the town and state
    
    baro_input = None  # Initialize to None or any default value
    
    try:
        # Make the initial API request to get location and station information
        response = requests.get(f'https://api.weather.gov/points/{latitude},{longitude}')
        if response.status_code != 200:
            print("Failed to fetch data from the National Weather Service.")
            return False
        data = response.json()

        # Extract location information
        location = data['properties']['relativeLocation']['properties']
        town = location['city']
        state = location['state']
        aobs_site = f"{town}, {state}"  # Update global variable with location name

        # Extract the URL to the nearest observation stations
        stations_url = data['properties']['observationStations']

        # Get the list of nearby weather stations
        response = requests.get(stations_url)
        if response.status_code != 200:
            print("Failed to fetch station list from the National Weather Service.")
            return False
        stations_data = response.json()

        # Loop through the stations to find one with a barometric pressure reading
        for station_url in stations_data['observationStations']:
            try:
                station_observation_response = requests.get(f"{station_url}/observations/latest")
                if station_observation_response.status_code != 200:
                    continue  # Skip if the station's observation data can't be accessed

                observation_data = station_observation_response.json()

                # Attempt to get the barometric pressure
                if 'barometricPressure' in observation_data['properties'] and 'value' in observation_data['properties']['barometricPressure']:
                    barometric_pressure_pascals = observation_data['properties']['barometricPressure']['value']
                    if barometric_pressure_pascals is not None:
                        # Convert to inches of mercury and update the global variable
                        baro_input = pascals_to_inches_hg(barometric_pressure_pascals)
                        return aobs_site
            except Exception as e:
                print(f"Error accessing data for station {station_url}: {e}")
                continue

        # If the loop completes without finding a valid pressure reading
        print(f"Location: {aobs_site}")
        print("No stations with a current barometric pressure reading were found.")
        return False

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

#@profile
def generate_aobs_url(latitude, longitude, aobs_site=''):
    aobs_url = f"https://forecast.weather.gov/MapClick.php?lon={longitude}&lat={latitude}"
    if aobs_site:
        aobs_url += f"&site={aobs_site}"
    print("line 381. aobs_url: ", aobs_url)    
    return aobs_url

# Example usage
location = get_location()
if location:
    latitude, longitude = location
    aobs_site = get_aobs_site(latitude, longitude)

# Set the background color in Tkinter to light blue
tk_background_color = "lightblue"
root.configure(bg=tk_background_color)

# Create a frame to serve as the transparent overlay
transparent_frame = tk.Frame(root, bg=tk_background_color, bd=0, highlightthickness=0)
transparent_frame.grid(row=0, column=0, sticky="nw")
# Make the frame transparent by setting its background color and border
transparent_frame.config(bg=tk_background_color, bd=0, highlightthickness=0)

# Create a Matplotlib figure and axis
fig = Figure(figsize=(12.5, 6))
ax = fig.add_subplot(1, 1, 1)

# Set the background color of matplotlib to match Tkinter
fig.patch.set_facecolor(tk_background_color)

# Create a frame for the barograph
baro_frame = tk.Frame(root, width=12.5, height=6)

# Embed the Matplotlib figure in a tkinter frame
canvas = FigureCanvasTkAgg(fig, master=baro_frame)
canvas_widget = canvas.get_tk_widget()
# Use next line to position matplotlib in window. pady pushes inmage down from top
canvas_widget.grid(row=1, column=0, padx=(20,0), pady=15, sticky="s")

# Set the background color of the frame to light blue
baro_frame.configure(bg=tk_background_color)

# The last frame defined in this series will appear to user
# Create scraped images frame
scraped_frame = tk.Frame(root, bg=tk_background_color)

# Create main user GUI frame
frame1 = tk.Frame(root, bg=tk_background_color)
frame1.grid(row=0, column=0)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Prepare frame1 for grid layout for the keyboard and other elements
for i in range(20):  # Match this with total_columns in create_virtual_keyboard
    frame1.grid_columnconfigure(i, weight=1)

def forget_frame1_and_show_scraped_and_transparent_frames():
        frame1.grid_forget()
        show_transparent_frame()
        scraped_frame.grid(row=0, column=0, sticky="nsew")

# the "?" character is used a a space-filling placeholder. So the code in this
# function will need to change if the '?' key needs to be functional
def create_virtual_keyboard(parent, start_row):
    keyboard_layout = [
        ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'Backspace'],
        ['Tab', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '?', '?', '?', '?'],
        [' ', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],  # Skip button creation for ' '
        [' ', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '.', '@']  # Skip button creation for ' '
    ]
    key_widths = {
        'Backspace': 7,
        'Tab': 5,
        'Space': 30  # Adjusted to be equivalent to about 6 regular keys
    }
    default_width = 5  # Default width for regular letter keys
    default_height = 2  # Assuming a uniform height for all keys

    for i, row in enumerate(keyboard_layout):
        col_index = 0  # Start placing keys from the first column
        for j, key in enumerate(row):
            if key == ' ':  # Skip creating a button if the key is meant to be an empty space
                col_index += 1
                continue
            width = key_widths.get(key, default_width)
            # Apply special padding to the first key in each row
            if j == 0:  # First key in the row
                padx = (50, 1)  # Increase left padding for the first key
            else:
                padx = (1, 1)  # Standard padding for all other keys
            
            # Modify here for invisible buttons
            if key == '?':  # Assuming '?' is your placeholder for extra buttons
                btn = tk.Button(parent, text='', state='disabled', relief='flat', width=width, height=default_height, bg=frame1.cget('bg'), bd=0, highlightthickness=0)
            else:
                btn = tk.Button(parent, text=key.strip(), command=lambda k=key: key_pressed(k) if key != '?' else None, width=width, height=default_height)
            
            btn.grid(row=start_row + i, column=col_index, sticky="w", padx=padx, pady=1)
            col_index += 1

    # Place the space bar separately to manage its width independently
    space_bar = tk.Button(parent, text="Space", command=lambda: key_pressed(" "), width=key_widths['Space'], height=default_height)
    space_bar.grid(row=start_row + 4, column=0, columnspan=8, sticky="nsew", padx=(200, 1), pady=1)

def key_pressed(key_value):
    global current_target_entry
    if current_target_entry:
        if key_value == 'Backspace':
            current_text = current_target_entry.get()[:-1]
            current_target_entry.delete(0, tk.END)
            current_target_entry.insert(0, current_text)
        elif key_value == 'Space':
            current_target_entry.insert(tk.END, ' ')
        elif key_value == 'Tab':
            # Implement Tab functionality to move to the next text input
            try:
                next_widget = current_target_entry.tk_focusNext()
                next_widget.focus_set()
                set_current_target(next_widget)
            except Exception as e:
                print(f"Error moving to next input: {e}")
        else:
            current_target_entry.insert(tk.END, key_value)
                        
def clear_frame(frame1):
    for widget in frame1.winfo_children():
        if isinstance(widget, (tk.Label, tk.Button, tk.Checkbutton, tk.Entry)):
            widget.destroy()

def close_GUI():
    root.destroy()

def refresh_choices():
    global alternative_town_1, alternative_state_1, alternative_town_2, alternative_state_2, alternative_town_3, alternative_state_3   
    global refresh_flag, box_variables
    global img_label_national_satellite, label_lcl_radar,  img_label_national_radar, baro_img_label, img_label_sfc_map 
    refresh_flag = True
    
    transparent_frame.grid_forget()
    # Clear the transparent_frame display
    for widget in transparent_frame.winfo_children():        
        widget.destroy()
        
    scraped_frame.grid_forget()
    # Don't destroy scraped frame during loop displays will crash
        
    baro_frame.grid_forget()

    #avoid getting stuck trying to display radiosonde while user updates display choices
    box_variables[8] = 0
       
    # 5/23/24 include code to get rid of all the images used to fill gaps
    if img_label_national_satellite and img_label_national_satellite.winfo_exists():
        img_label_national_satellite.grid_forget() 
    
    if label_lcl_radar and label_lcl_radar.winfo_exists():
        label_lcl_radar.grid_forget()
        
    if img_label_national_radar and img_label_national_radar.winfo_exists():
        img_label_national_radar.grid_forget()
    
    if baro_img_label and baro_img_label.winfo_exists():
        baro_img_label.grid_forget() # changed to _forget from destroy 7/25/24
        
    if img_label_sfc_map and img_label_sfc_map.winfo_exists():
        img_label_sfc_map.grid_forget()
        print("line 535. -forget sfc_map in refresh choices.")
        
    frame1.grid(row=0, column=0, sticky="nsew") 
    
    alternative_town_1 = " "
    alternative_state_1 = " "

    alternative_town_2 = " "
    alternative_state_2 = " "

    alternative_town_3 = " "
    alternative_state_3 = " "

    land_or_buoy()

def change_maps_only():
    global refresh_flag, baro_img_label, img_label_national_radar, label_lcl_radar, img_label_national_satellite, img_label_sfc_map, box_variables  
    refresh_flag = True

    transparent_frame.grid_forget()
    
    for widget in transparent_frame.winfo_children():        
        widget.destroy()
        
    scraped_frame.grid_forget()
    # Don't destroy scraped frame during loop displays will crash       
    baro_frame.grid_forget()
    
    #avoid getting stuck trying to display radiosonde while user updates display choices
    box_variables[8] = 0
       
    # 5/9/24 include code to get rid of all the images used to fill gaps
    if img_label_national_satellite and img_label_national_satellite.winfo_exists():
        img_label_national_satellite.grid_forget() 
    
    if label_lcl_radar and label_lcl_radar.winfo_exists():
        label_lcl_radar.grid_forget()
        
    if img_label_national_radar and img_label_national_radar.winfo_exists():
        img_label_national_radar.grid_forget()
    
    if baro_img_label and baro_img_label.winfo_exists():
        baro_img_label.grid_forget()
        
    if img_label_sfc_map and img_label_sfc_map.winfo_exists():
        img_label_sfc_map.grid_forget()
        #print("line 581. _forget in change maps only.")

    frame1.grid(row=0, column=0, sticky="nsew")
    
    page_choose()

def email_to_maps():
    global refresh_flag
    refresh_flag = False
    # wondering if _forget labels is needed here 6/30/24
    # forget frame1 GUI
    frame1.grid_forget()
    # return to map images
    #Do I need to use lift?
    scraped_frame.grid(row=0, column=0, sticky="nsew")
    transparent_frame.grid(row=0, column=0, sticky="nw")    

def submit_pic_email():
    global email_entry  # Declare the use of the global variable
    
    to_email = email_entry.get()  # Get the email address from the entry widget
    if not to_email:
        print("No email address provided.")
        return

    # Email details
    from_email = 'picturesfromtheweatherobserver@gmail.com'
    subject = 'Weather Observer Screenshot - Do Not Reply'
    body = 'Attached is the screenshot from the Weather Observer.'

    # Set up the email message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Attach the screenshot
    with open(screenshot_filename, 'rb') as attachment:
        img = MIMEImage(attachment.read(), name=screenshot_filename)
        msg.attach(img)

    # For example:
    try:
        # Connect to Gmail's SMTP server and send the email
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(from_email, 'apedhdhxnyhkfepv')  # Use your app password
        #server.login(from_email, os.getenv('EMAIL_APP_PASSWORD'))  # Use the environment variable 
        server.send_message(msg)
        server.quit()
        # Clear the current display
        for widget in frame1.winfo_children():
            if isinstance(widget, (tk.Checkbutton, tk.Label, tk.Button, tk.Entry)):
                widget.destroy()
                
        # I think these need to stay. 
        transparent_frame.grid_forget()
        scraped_frame.grid_forget()
        baro_frame.grid_forget()
        
        frame1.grid(row=0, column=0, sticky="nsew")
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.geometry('1024x600')

        label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
        label1.grid(row=0, column=0, columnspan=20, padx=50, pady=(50,0), sticky="nw")

        finish_text = "Your email was sent successfully"
        finish_label = tk.Label(frame1, text=finish_text, font=("Helvetica", 16), bg=tk_background_color, justify="left")
        finish_label.grid(row=1, column=0, columnspan=20, padx=50, pady=25, sticky='nw')

        return_text = "Click the button to return to the maps"
        return_label = tk.Label(frame1, text=return_text, font=("Helvetica", 16), bg=tk_background_color, justify="left")
        return_label.grid(row=2, column=0, columnspan=20, padx=50, pady=25, sticky='nw') 

        return_button = tk.Button(frame1, text="Return", command=email_to_maps, font=("Helvetica", 16, "bold"))
        return_button.grid(row=3, column=0, columnspan=20, padx=50, pady=(15,0), sticky='nw')
        
    except Exception as e:
        print("line 611. failed to send email: ", e)
        # Clear the current display
        for widget in frame1.winfo_children():
            if isinstance(widget, (tk.Checkbutton, tk.Label, tk.Button, tk.Entry)):
                widget.destroy()
        
        transparent_frame.grid_forget()
        scraped_frame.grid_forget()
        baro_frame.grid_forget()
        
        frame1.grid(row=0, column=0, sticky="nsew")
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.geometry('1024x600')

        label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
        label1.grid(row=0, column=0, columnspan=20, padx=50, pady=(50,0), sticky="nw")

        not_sent_text = "Your email was not able to be sent"
        not_sent_label = tk.Label(frame1, text=not_sent_text, font=("Helvetica", 16), bg=tk_background_color, justify="left")
        not_sent_label.grid(row=1, column=0, columnspan=20, padx=50, pady=25, sticky='nw')
        
        not_sent_text = "Try another email address or return to the Maps"
        not_sent_label = tk.Label(frame1, text=not_sent_text, font=("Helvetica", 16), bg=tk_background_color, justify="left")
        not_sent_label.grid(row=2, column=0, columnspan=20, padx=50, pady=25, sticky='nw')
        
        email_button = tk.Button(frame1, text="Email", command=pic_email, font=("Helvetica", 16, "bold"))
        email_button.grid(row=3, column=0, columnspan=20, padx=50, pady=(15,0), sticky='nw')
        
        maps_button = tk.Button(frame1, text="Maps", command=email_to_maps, font=("Helvetica", 16, "bold"))
        maps_button.grid(row=3, column=1, columnspan=20, padx=50, pady=(15,0), sticky='nw')

# Function to set environment variables for display
def set_display_env():
    os.environ['DISPLAY'] = ':0'
    os.environ['XAUTHORITY'] = '/home/santod/.Xauthority'
    os.environ['XDG_RUNTIME_DIR'] = '/run/user/1000'

# Function to take screenshot using grim
def take_screenshot_with_grim(screenshot_filename):
    print("line 668. Trying to use grim for taking a screenshot.")
    try:
        result = subprocess.run(['grim', screenshot_filename], capture_output=True, text=True)
        if result.returncode == 0:
            print("line 672. Grim successfully took the screenshot.")
            return True
        else:
            print("line 675. Grim failed with error")
    except Exception as e:
        print("line 677. Error while using grim")
    return False

# Function to take screenshot using scrot
def take_screenshot_with_scrot(screenshot_filename):
    print("line 682. Trying to use scrot for taking a screenshot.")
    try:
        result = subprocess.run(['scrot', screenshot_filename, '--overwrite'], capture_output=True, text=True)
        if result.returncode == 0:
            print("line 686. Scrot successfully took the screenshot.")
            return True
        else:
            print("line 689. Scrot failed with error")
    except Exception as e:
        print("line 691. Error while using scrot")
    return False

# Function to check if the image is black
def is_black_image(image_path):
    """Utility function to check if an image is completely black."""
    try:
        image = Image.open(image_path)
        return not image.getbbox()
    except Exception as e:
        print("line 701. Error opening image for black check")
        return True

# Main function to take screenshot and handle errors
def pic_email():
    global email_entry, refresh_flag  # Use the global variable
    refresh_flag = True

    # Ensure display and runtime directory environment variables are set correctly
    set_display_env()

    # Determine which screenshot command to use
    screenshot_filename = SCREENSHOT_PATH
    grim_path = shutil.which('grim')
    scrot_path = shutil.which('scrot')

    screenshot_taken = False

    if grim_path and not screenshot_taken:
        screenshot_taken = take_screenshot_with_grim(screenshot_filename)

    if scrot_path and not screenshot_taken:
        screenshot_taken = take_screenshot_with_scrot(screenshot_filename)

    if not screenshot_taken:
        print("line 726. Failed to take screenshot with both grim and scrot.")
        raise RuntimeError("Failed to take screenshot with both grim and scrot.")

    # Verify the screenshot
    if not os.path.exists(screenshot_filename):
        print("line 731. Screenshot file does not exist.")
        raise RuntimeError("Screenshot file does not exist.")

    if is_black_image(screenshot_filename):
        print("Line 735. Screenshot file is black.")
        raise RuntimeError("Screenshot file is black.")

    try:
        image = Image.open(screenshot_filename)
        image.verify()  # Verify the integrity of the image
        print("line 741. Screenshot file is valid.")
    except Exception as e:
        print("line 743. Screenshot file is invalid")
        raise RuntimeError("Screenshot file is invalid.")

    # Clear the current display
    for widget in frame1.winfo_children():
        if isinstance(widget, (tk.Checkbutton, tk.Label, tk.Button, tk.Entry, tk.Radiobutton)):
            widget.destroy()

    # Continue with the rest of the GUI update logic
    transparent_frame.grid_forget()
    scraped_frame.grid_forget()
    baro_frame.grid_forget()

    frame1.grid(row=0, column=0, sticky="nsew")
    frame1.config(width=1024, height=600)

    frame1.grid_propagate(False)

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.geometry('1024x600')

    label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
    label1.grid(row=0, column=0, columnspan=20, padx=50, pady=(50,0), sticky="nw")

    instruction_text = "Please enter the email address to send the screenshot:"
    instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16), bg=tk_background_color, justify="left")
    instructions_label.grid(row=1, column=0, columnspan=20, padx=50, pady=25, sticky='nw')

    email_entry = tk.Entry(frame1, font=("Helvetica", 14), width=50)
    email_entry.grid(row=2, column=0, columnspan=20, padx=50, pady=5, sticky='nw')

    email_entry.focus_set()

    submit_button = tk.Button(frame1, text="Submit", command=submit_pic_email, font=("Helvetica", 16, "bold"))
    submit_button.grid(row=6, column=0, columnspan=20, padx=50, pady=(15,0), sticky='nw')

    cancel_button = tk.Button(frame1, text="Cancel", command=email_to_maps, font=("Helvetica", 16, "bold"))
    cancel_button.grid(row=6, column=0, columnspan=20, padx=225, pady=(15,0), sticky='nw')

    email_entry.bind("<FocusIn>", lambda e: set_current_target(email_entry))

    spacer = tk.Label(frame1, text="", bg=tk_background_color)
    spacer.grid(row=7, column=0, sticky="nsew", pady=(0, 40))

    create_virtual_keyboard(frame1, 8)

    # Load and display the screenshot image
    image_path = SCREENSHOT_PATH  # Use the fixed path
    image = Image.open(image_path)
    image = image.resize((200, 118))  # Adjusted size as per your requirement
    photo = ImageTk.PhotoImage(image)
    image_label = tk.Label(frame1, image=photo)
    image_label.image = photo  # Keep a reference!
    # Place the image at the top of the column
    image_label.grid(row=0, column=20, sticky="ne", padx=10)

    # Add a label for "Preview" text directly below the image
    preview_label = tk.Label(frame1, text="Preview", font=("Helvetica", 12), bg=tk_background_color)
    # Position it just below the image without using excessive padding or altering other widgets
    preview_label.grid(row=1, column=20, sticky="n", padx=10)

def confirm_random_sites():
    global a_town_state, b_town_state, c_town_state, aobs_only_click_flag
    global aobs_random_obs_lat, aobs_random_obs_lon, bobs_random_obs_lat, bobs_random_obs_lon, cobs_random_obs_lat, cobs_random_obs_lon

    # Check if the lat/lon variables are initialized
    try:
        #print(f"A Lat/Lon: {aobs_random_obs_lat}, {aobs_random_obs_lon}")
        #print(f"B Lat/Lon: {bobs_random_obs_lat}, {bobs_random_obs_lon}")
        #print(f"C Lat/Lon: {cobs_random_obs_lat}, {cobs_random_obs_lon}")
        pass
    except NameError as e:
        print(f"line 962. Error confirming random sites: {e}")
        return  # Exit the function if the lat/lon data isn't initialized
    
    # Construct the station dictionaries
    station_a = {'name': a_town_state, 'latitude': aobs_random_obs_lat, 'longitude': aobs_random_obs_lon}
    station_b = {'name': b_town_state, 'latitude': bobs_random_obs_lat, 'longitude': bobs_random_obs_lon}
    station_c = {'name': c_town_state, 'latitude': cobs_random_obs_lat, 'longitude': cobs_random_obs_lon}
    
    random_stations = [station_a, station_b, station_c]

    # Generate the map and then update the GUI
    create_random_map_image(random_stations)
    frame1.after(100, lambda: update_gui(random_stations))

def update_gui(random_stations):
    
    global aobs_only_click_flag

    # Collect all child widgets of frame1 to avoid destroying frame1 itself
    all_widgets = []
    widgets_to_check = frame1.winfo_children()  # Start with children of frame1
    while widgets_to_check:
        widget = widgets_to_check.pop(0)
        all_widgets.append(widget)
        widgets_to_check.extend(widget.winfo_children())  # Add children of this widget

    # Destroy all collected widgets
    for widget in all_widgets:
        widget.destroy()

    # Configure grid layout for frame1
    frame1.grid_columnconfigure(0, weight=1)
    frame1.grid_columnconfigure(9, weight=1)

    label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
    label1.grid(row=0, column=0, columnspan=9, padx=50, pady=(20,10), sticky="nw")

    announce_text = "The following 3 locations have been chosen as observation sites:"
    announce_label = tk.Label(frame1, text=announce_text, font=("Helvetica", 16), bg=tk_background_color, justify="left")
    announce_label.grid(row=1, column=0, columnspan=9, padx=50, pady=(0,15), sticky='nw')
    
    random_sites_text = f"{a_town_state}\n\n{b_town_state}\n\n{c_town_state}"
    label2 = tk.Label(frame1, text=random_sites_text, font=("Arial", 16), bg=tk_background_color, anchor='w', justify='left')
    label2.grid(row=2, column=0, columnspan=9, padx=(50,0), pady=(0, 7), sticky='w')

    # Validate that all stations have lat/lon before proceeding
    for station in random_stations:
        if 'latitude' not in station or 'longitude' not in station:
            label_error = tk.Label(frame1, text=f"Error: Missing location data for {station['name']}.", font=("Arial", 14), fg="red", bg=tk_background_color)
            label_error.grid(row=4, column=0, columnspan=20, padx=50, pady=(10,10), sticky='w')
            return
    
    # Display the map with the 3 random sites
    display_random_map_image("/home/santod/station_locations.png")

    if aobs_only_click_flag == True:
        aobs_only_click_flag = False
        next_function = forget_frame1_and_show_scraped_and_transparent_frames
    else:
        next_function = page_choose
    
    # Create the 'Back' button
    back_button = tk.Button(frame1, text=" Back ", font=("Helvetica", 16, "bold"), command=land_or_buoy)
    back_button.grid(row=3, column=0, columnspan=20, padx=(50, 0), pady=(20,0), sticky="nw")
    
    next_button = tk.Button(frame1, text="Next", command=next_function, font=("Helvetica", 16, "bold"))
    next_button.grid(row=3, column=0, columnspan=20, padx=200, pady=(20,0), sticky='nw')
    
def calculate_random_center(random_stations):
    random_latitudes = [float(station['latitude']) for station in random_stations]
    random_longitudes = [float(station['longitude']) for station in random_stations]
    return sum(random_latitudes) / len(random_latitudes), sum(random_longitudes) / len(random_longitudes)

def calculate_random_zoom_level(random_stations):
    max_random_distance = 0
    for i in range(len(random_stations)):
        for j in range(i + 1, len(random_stations)):
            point1 = (float(random_stations[i]['latitude']), float(random_stations[i]['longitude']))
            point2 = (float(random_stations[j]['latitude']), float(random_stations[j]['longitude']))
            distance = geodesic(point1, point2).kilometers
            if distance > max_random_distance:
                max_random_distance = distance
        
    if max_random_distance < 50:
        return 10
    elif max_random_distance < 100:
        return 9
    elif max_random_distance < 200:
        return 8
    elif max_random_distance < 400:
        return 7
    elif max_random_distance < 800:
        return 6
    elif max_random_distance < 1600:
        return 5
    else:
        return 4

def create_random_map_image(random_stations):
    random_center = calculate_random_center(random_stations)
    random_zoom_level = calculate_random_zoom_level(random_stations)

    # Create the map centered on the calculated center point
    m = folium.Map(location=random_center, zoom_start=random_zoom_level, width=450, height=300, control_scale=False, zoom_control=False)

    # Add markers for each station
    for station in random_stations:
        random_station_name = station['name'].split(",")[0][:9]  # Limit to 15 characters

        folium.Marker(
            location=(station['latitude'], station['longitude']),
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)
        
        # Add label with a max of 15 characters, centered, and wrapped
        folium.Marker(
            location=(station['latitude'], station['longitude']),
            icon=folium.DivIcon(
                html=f'''
                    <div style="
                        background-color: white;
                        padding: 2px 5px;
                        border-radius: 3px;
                        box-shadow: 0px 0px 2px rgba(0, 0, 0, 0.5);
                        font-size: 12px;
                        font-weight: bold;
                        text-align: center;
                        width: 70px;  /* Adjust width to fit the label */
                        word-wrap: break-word;
                        transform: translate(-40%, -130%);  /* Centering horizontally and placing above the pin */
                    ">
                        {random_station_name}
                    </div>
                '''
            )
        ).add_to(m)

    # Calculate the bounds to fit all stations, with a larger N/S buffer
    latitudes = [station['latitude'] for station in random_stations]
    longitudes = [station['longitude'] for station in random_stations]

    min_lat, max_lat = min(latitudes), max(latitudes)
    min_lon, max_lon = min(longitudes), max(longitudes)

    # Add a larger N/S buffer and a smaller E/W buffer
    ns_buffer = 0.15  # Increase N/S buffer to ensure full pin visibility
    ew_buffer = 0.1   # Keep E/W buffer smaller
    bounds = [[min_lat - ns_buffer, min_lon - ew_buffer], [max_lat + ns_buffer, max_lon + ew_buffer]]

    # Fit the map to the calculated bounds
    m.fit_bounds(bounds)

    # Save the map to an HTML file and then take a screenshot
    m.save('/home/santod/random_station_locations.html')

    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')  # Add this argument for consistency

    # Explicitly specify the chromedriver path
    driver = webdriver.Chrome(service=ChromeService(executable_path="/usr/bin/chromedriver"), options=options)
    driver.set_window_size(450, 387)

    file_path = os.path.abspath("/home/santod/random_station_locations.html")
    driver.get(f'file://{file_path}')

    time.sleep(2)  # Adjust as needed

    # Save the screenshot
    screenshot_path = '/home/santod/station_locations.png'
    driver.save_screenshot(screenshot_path)
    driver.quit()

def display_random_map_image(img_path):
    img = Image.open(img_path)
    img = img.resize((450, 300), Image.LANCZOS)
    tk_img = ImageTk.PhotoImage(img)

    label = tk.Label(frame1, image=tk_img)
    label.image = tk_img
    label.grid(row=8, column=8, rowspan=6, sticky="se", padx=(570, 10), pady=0)  

def random_geocode_location(random_site_town, random_site_state_id):
    geolocator = Nominatim(user_agent="weather_obs_locator")
    location_query = f"{random_site_town}, {random_site_state_id}, USA"
    location_data = geolocator.geocode(location_query)
    if location_data:
        return location_data.latitude, location_data.longitude
    else:
        raise ValueError("Location not found.")

def random_fetch_stations_by_state(states):
    stations = []
    max_pages = 30  # Set your desired maximum number of pages
    page_counter = 0

    for state in states:
        url = f"{RANDOM_NWS_API_STATIONS_ENDPOINT}?state={state.upper()}&limit=500"
        while url and page_counter < max_pages:
            response = requests.get(url)
            if response.status_code != 200:
                raise ValueError(f"Error retrieving stations for state {state}: {response.status_code}")
            data = response.json()
            features = data.get('features', [])
            for feature in features:
                feature['state'] = state  # Add the state to each feature
            stations.extend(features)

            if len(features) < 500:
                break  # Stop if fewer than 500 stations are retrieved in one page

            cursor = data.get('pagination', {}).get('next', None)
            url = cursor
            page_counter += 1

    return stations

def random_get_nearby_states(state):
    return neighboring_states.get(state.upper(), [])

def abbreviate_location(name, state_id, max_length=21):
    # Common abbreviations
    abbreviations = {
        "International": "Intl",
        "Municipal": "Muni",
        "Regional": "Reg",
        "Airport": "Arpt",
        "Field": "Fld",
        "National": "Natl",
        "County": "Co",
        "Boardman": "Brdmn",
        "Southern": "Sthrn",
        "Northeast": "NE",
        "Northwest": "NW",
        "Southwest": "SW",
        "Southeast": "SE",
        " North ": "N",
        " South ": "S",
        " East ": "E",
        " West ": "W",
        " And ": "&",
    }

    # Replace common words with their abbreviations
    for word, abbr in abbreviations.items():
        name = name.replace(word, abbr)

    # Truncate and add ellipsis if necessary
    if len(name) > max_length:
        return f"{name[:max_length-3]}..., {state_id}"
    else:
        return f"{name}, {state_id}"

def random_get_stations_starting_with_k_and_airport_or_jetport_within_distance(lat, lon, states, max_distance=100):
    features = random_fetch_stations_by_state(states)

    stations = []

    for feature in features:
        properties = feature.get('properties', {})
        station_id = properties.get('stationIdentifier')
        name = properties.get('name')
        coordinates = feature.get('geometry', {}).get('coordinates', [None, None])
        station_lat = coordinates[1]
        station_lon = coordinates[0]
        state_id = feature.get('state', 'Unknown')

        if station_id.startswith('K') and ('Airport' in name or 'Jetport' in name):
            distance = geopy.distance.distance((lat, lon), (station_lat, station_lon)).miles
            if distance <= max_distance:
                # Use the abbreviate_location function
                town_state = abbreviate_location(name.split(',')[0].strip(), state_id)
                stations.append((station_id, name, station_lat, station_lon, distance, town_state))

    return stations

def random_degrees_to_cardinal(deg):
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    idx = int((deg / 22.5) + 0.5) % 16
    return directions[idx]

def random_get_latest_observation(station_id):
    url = RANDOM_NWS_API_LATEST_OBSERVATION_ENDPOINT.format(station_id=station_id)
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error retrieving latest observation for station {station_id}: {response.status_code}")
        return None
    data = response.json()
    properties = data.get('properties', {})
    temp_c = properties.get('temperature', {}).get('value', None)
    wind_direction_deg = properties.get('windDirection', {}).get('value', None)
    wind_speed_kph = properties.get('windSpeed', {}).get('value', None)
    wind_gust_kph = properties.get('windGust', {}).get('value', None)
    timestamp = properties.get('timestamp', None)

    # Check if the observation is less than 2 hours old
    if timestamp:
        observation_time = parse(timestamp)
        current_time = datetime.now(pytz.timezone("America/New_York")).astimezone(timezone.utc)

        if current_time - observation_time > timedelta(hours=2):
            #print(f"Observation for station {station_id} is older than 2 hours. Skipping.")
            return None
    else:
        print(f"No timestamp for observation from station {station_id}. Skipping.")
        return None

    # Check if temperature and wind speed are valid numbers
    if temp_c is None or wind_speed_kph is None:
        #print(f"Invalid temperature or wind speed for station {station_id}. Skipping.")
        return None

    # Convert temperature from Celsius to Fahrenheit and round to the nearest hundredth
    temp_f = round((temp_c * 9/5) + 32, 2)

    # Convert wind speed from km/h to mph and round to the nearest whole number
    wind_speed_mph = round(wind_speed_kph * 0.621371)
    wind_gust_mph = round(wind_gust_kph * 0.621371) if wind_gust_kph is not None else None

    # Convert wind direction to cardinal direction
    wind_direction = random_degrees_to_cardinal(wind_direction_deg) if wind_direction_deg is not None else 'N/A'

    return temp_f, wind_direction, wind_speed_mph, wind_gust_mph

def generate_random_sites():
    global aobs_station_identifier, bobs_station_identifier, cobs_station_identifier, aobs_site, a_town_state, b_town_state, c_town_state
    global alternative_town_1, alternative_town_2, alternative_town_3
    global aobs_random_obs_lat, aobs_random_obs_lon, bobs_random_obs_lat, bobs_random_obs_lon, cobs_random_obs_lat, cobs_random_obs_lon
    global random_sites_flag
    
    random_sites_flag = True # set it back to false again as leaving staion plots function block
    
    instruction_text = f"Please wait while 3 random sites are chosen for you."
    instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 12,), bg=tk_background_color, anchor='w', justify='left')
    instructions_label.grid(row=3, column=0, padx=50, pady=5, sticky='w')
    
    # Update idle tasks to display the message immediately
    frame1.update_idletasks()
    
    random_site_state_id = aobs_site[-2:]
    random_site_town = aobs_site.split(',')[0].strip()

    try:
        lat, lon = random_geocode_location(random_site_town, random_site_state_id)
        nearby_states = [random_site_state_id] + random_get_nearby_states(random_site_state_id)
        stations = random_get_stations_starting_with_k_and_airport_or_jetport_within_distance(lat, lon, nearby_states)
        
        valid_stations = []
        remaining_stations = stations[:]
        
        while len(valid_stations) < 3 and remaining_stations:
            station_id, name, station_lat, station_lon, distance, town_state = random.choice(remaining_stations)
            remaining_stations.remove((station_id, name, station_lat, station_lon, distance, town_state))
            
            try:
                observation = random_get_latest_observation(station_id)
                if observation is not None:
                    temp_f, wind_direction, wind_speed_mph, wind_gust_mph = observation
                    # Check for valid latitude and longitude values
                    if station_lat is None or station_lon is None or not isinstance(station_lat, (int, float)) or not isinstance(station_lon, (int, float)):
                        print(f"Invalid lat/lon for station {station_id}. Skipping.")
                        continue
                    
                    valid_stations.append((station_id, name, station_lat, station_lon, distance, town_state))
                else:
                    #print(f"No valid observation data for station {station_id}. Skipping.")
                    pass
            except Exception as e:
                print(f"Error retrieving latest observation for station {station_id}: {e}. Skipping.")
        
        if len(valid_stations) < 3:
            print("Not enough valid stations found.")
        else:
            aobs_station_identifier, bobs_station_identifier, cobs_station_identifier = [station[0] for station in valid_stations[:3]]
            a_town_state, b_town_state, c_town_state = [station[5] for station in valid_stations[:3]]
            
            # Set the lat/lon global variables here
            aobs_random_obs_lat, aobs_random_obs_lon = valid_stations[0][2], valid_stations[0][3]
            bobs_random_obs_lat, bobs_random_obs_lon = valid_stations[1][2], valid_stations[1][3]
            cobs_random_obs_lat, cobs_random_obs_lon = valid_stations[2][2], valid_stations[2][3]
            
            alternative_town_1 = a_town_state
            alternative_town_2 = b_town_state
            alternative_town_3 = c_town_state
            
            confirm_random_sites()
        
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def cobs_input_land():
    global town_entry, alternative_town_3, state_entry, alternative_state_3, current_target_entry
    global cobs_only_click_flag

    # Clear the current display
    for widget in frame1.winfo_children():
        if isinstance(widget, (tk.Checkbutton, tk.Label, tk.Button, tk.Entry, tk.Radiobutton)):
            widget.destroy()

    frame1.grid(row=0, column=0, sticky="nsew")

    label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
    label1.grid(row=0, column=0, columnspan=20, padx=50, pady=(50,0), sticky="nw")

    instruction_text = "Please enter the name of the town for the third observation site:"
    instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16), bg=tk_background_color, justify="left")
    instructions_label.grid(row=1, column=0, columnspan=20, padx=50, pady=5, sticky='nw')

    town_entry = tk.Entry(frame1, font=("Helvetica", 14))
    town_entry.grid(row=2, column=0, columnspan=20, padx=50, pady=5, sticky='nw')

    # Automatically set focus to the town_entry widget
    town_entry.focus_set()

    state_instruction_text = "Please enter the 2-letter state ID for the third observation site:"
    state_instructions_label = tk.Label(frame1, text=state_instruction_text, font=("Helvetica", 16), bg=tk_background_color, justify="left")
    state_instructions_label.grid(row=3, column=0, columnspan=20, padx=50, pady=5, sticky='nw')
    
    state_entry = tk.Entry(frame1, font=("Helvetica", 14))
    state_entry.grid(row=4, column=0, columnspan=20, padx=50, pady=5, sticky='nw')

    instruction_text_2 = "After clicking SUBMIT, the system will pause while gathering a list of observation stations."
    instructions_label_2 = tk.Label(frame1, text=instruction_text_2, font=("Helvetica", 12), bg=tk_background_color, justify="left")
    instructions_label_2.grid(row=5, column=0, columnspan=20, padx=50, pady=10, sticky='nw') 

    if cobs_only_click_flag == False:
        # Create the 'Back' button
        back_button = tk.Button(frame1, text=" Back ", font=("Helvetica", 16, "bold"), command=bobs_confirm_land)
        back_button.grid(row=6, column=0, columnspan=20, padx=(50, 0), pady=5, sticky="nw")

    submit_button = tk.Button(frame1, text="Submit", command=submit_town3_and_state3, font=("Helvetica", 16, "bold"))
    submit_button.grid(row=6, column=0, columnspan=20, padx=200, pady=5, sticky='nw')

    town_entry.bind("<FocusIn>", lambda e: set_current_target(town_entry))
    state_entry.bind("<FocusIn>", lambda e: set_current_target(state_entry))
    
    # Spacer to push the keyboard to the bottom
    spacer = tk.Label(frame1, text="", bg=tk_background_color)
    spacer.grid(row=7, column=0, sticky="nsew", pady=(0, 10))  # Adjust row and pady as necessary
    
    # Display the virtual keyboard
    create_virtual_keyboard(frame1, 8)  # Adjust as necessary based on layout

    
def submit_town3_and_state3():
    global town_entry, alternative_town_3, state_entry, alternative_state_3, result, town, state

    if 'keyboard_window' in globals() and keyboard_window.winfo_exists():
        keyboard_window.destroy()

    # Get the user's input
    town = town_entry.get()
    state = state_entry.get()

    # Set the global variable alternative_town_3 to the user's input
    alternative_town_3 = town
    alternative_state_3 = state
    
    # Continue with other actions or functions as needed
    cobs_check_land()
            
def bobs_input_land():
    global town_entry, alternative_town_2, state_entry, alternative_state_2, current_target_entry

    # Clear the current display
    for widget in frame1.winfo_children():
        widget.destroy()

    frame1.grid(row=0, column=0, sticky="nsew")

    label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
    label1.grid(row=0, column=0, columnspan=20, padx=50, pady=(50,0), sticky="nw")

    instruction_text = "Please enter the name of the town for the second observation site:"
    instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16), bg=tk_background_color, justify="left")
    instructions_label.grid(row=1, column=0, columnspan=20, padx=50, pady=5, sticky='nw')

    town_entry = tk.Entry(frame1, font=("Helvetica", 14))
    town_entry.grid(row=2, column=0, columnspan=20, padx=50, pady=5, sticky='nw')

    # Automatically set focus to the town_entry widget
    town_entry.focus_set()

    state_instruction_text = "Please enter the 2-letter state ID for the second observation site:"
    state_instructions_label = tk.Label(frame1, text=state_instruction_text, font=("Helvetica", 16), bg=tk_background_color, justify="left")
    state_instructions_label.grid(row=3, column=0, columnspan=20, padx=50, pady=5, sticky='nw')

    state_entry = tk.Entry(frame1, font=("Helvetica", 14))
    state_entry.grid(row=4, column=0, columnspan=20, padx=50, pady=5, sticky='nw')

    instruction_text_2 = "After clicking SUBMIT, the system will pause while gathering a list of observation stations."
    instructions_label_2 = tk.Label(frame1, text=instruction_text_2, font=("Helvetica", 12), bg=tk_background_color, justify="left")
    instructions_label_2.grid(row=5, column=0, columnspan=20, padx=50, pady=10, sticky='nw') 

    # Create the 'Back' button
    back_button = tk.Button(frame1, text=" Back ", font=("Helvetica", 16, "bold"), command=bobs_input_land)
    back_button.grid(row=6, column=0, columnspan=20, padx=(50, 0), pady=5, sticky="nw")

    submit_button = tk.Button(frame1, text="Submit", command=submit_town2_and_state2, font=("Helvetica", 16, "bold"))
    submit_button.grid(row=6, column=0, columnspan=20, padx=200, pady=5, sticky='nw')

    town_entry.bind("<FocusIn>", lambda e: set_current_target(town_entry))
    state_entry.bind("<FocusIn>", lambda e: set_current_target(state_entry))

    # Spacer to push the keyboard to the bottom
    spacer = tk.Label(frame1, text="", bg=tk_background_color)
    spacer.grid(row=7, column=0, sticky="nsew", pady=(0, 10))  # Adjust row and pady as necessary
    
    # Display the virtual keyboard
    create_virtual_keyboard(frame1, 8)  # Adjust as necessary based on layout
    
def submit_town2_and_state2():
    global town_entry, alternative_town_2, state_entry, alternative_state_2, result, town, state

    # Get the user's input
    town = town_entry.get()
    state = state_entry.get()

    # Set the global variable alternative_town_2 to the user's input
    alternative_town_2 = town
    
    # Check if the length of alternative_town_1 is 3 characters
    if len(alternative_town_2) == 3:
        alternative_town_2 = alternative_town_2.upper()
        
    else:
        alternative_town_2 = alternative_town_2.title()
      
    alternative_state_2 = state
    
    # Continue with other actions or functions as needed
    bobs_check_land()
    
def aobs_input_land():
    global town_entry, alternative_town_1, state_entry, alternative_state_1, current_target_entry

    # Clear the current display
    for widget in frame1.winfo_children():
        widget.destroy()

    frame1.grid(row=0, column=0, sticky="nsew")

    label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
    label1.grid(row=0, column=0, columnspan=20, padx=50, pady=(50,0), sticky="nw")

    instruction_text = "Please enter the name of the town for the first observation site:"
    instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16), bg=tk_background_color, justify="left")
    instructions_label.grid(row=1, column=0, columnspan=20, padx=50, pady=5, sticky='nw')

    town_entry = tk.Entry(frame1, font=("Helvetica", 14))
    town_entry.grid(row=2, column=0, columnspan=20, padx=50, pady=5, sticky='nw')

    # Automatically set focus to the town_entry widget
    town_entry.focus_set()

    state_instruction_text = "Please enter the 2-letter state ID for the first observation site:"
    state_instructions_label = tk.Label(frame1, text=state_instruction_text, font=("Helvetica", 16), bg=tk_background_color, justify="left")
    state_instructions_label.grid(row=3, column=0, columnspan=20, padx=50, pady=5, sticky='nw')

    state_entry = tk.Entry(frame1, font=("Helvetica", 14))
    state_entry.grid(row=4, column=0, columnspan=20, padx=50, pady=5, sticky='nw')

    instruction_text_2 = "After clicking SUBMIT, the system will pause while gathering a list of observation stations."
    instructions_label_2 = tk.Label(frame1, text=instruction_text_2, font=("Helvetica", 12), bg=tk_background_color, justify="left")
    instructions_label_2.grid(row=5, column=0, columnspan=20, padx=50, pady=10, sticky='nw')

    # Create the 'Back' button
    back_button = tk.Button(frame1, text=" Back ", font=button_font, command=land_or_buoy)
    back_button.grid(row=6, column=0, columnspan=20, padx=(50, 0), pady=5, sticky="w")

    submit_button = tk.Button(frame1, text="Submit", command=submit_town1_and_state1, font=button_font)
    submit_button.grid(row=6, column=0, columnspan=20, padx=200, pady=5, sticky='nw')

    town_entry.bind("<FocusIn>", lambda e: set_current_target(town_entry))
    state_entry.bind("<FocusIn>", lambda e: set_current_target(state_entry))

    # Spacer to push the keyboard to the bottom
    spacer = tk.Label(frame1, text="", bg=tk_background_color)
    spacer.grid(row=7, column=0, sticky="nsew", pady=(0, 10))  # Adjust row and pady as necessary
    
    # Display the virtual keyboard
    create_virtual_keyboard(frame1, 8)  # Adjust as necessary based on layout

    
def submit_town1_and_state1():
    global town_entry, alternative_town_1, state_entry, alternative_state_1, result, town, state

    if 'keyboard_window' in globals() and keyboard_window.winfo_exists():
        keyboard_window.destroy()

    # Get the user's input
    town = town_entry.get()
    state = state_entry.get()

    # Set the global variable alternative_town_1 to the user's input
    alternative_town_1 = town
    alternative_state_1 = state
             
    # Continue with other actions or functions as needed
    aobs_check_land()
    
def cobs_input_buoy():
    pass

def bobs_input_buoy():
    global town_entry, alternative_town_2, state_entry, alternative_state_2, current_target_entry

    # Clear the current display
    for widget in frame1.winfo_children():
        widget.destroy()

    frame1.grid(row=0, column=0, sticky="nsew")

    label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
    label1.grid(row=0, column=0, columnspan=20, padx=50, pady=(50, 5), sticky="nw")

    instruction_text = "Please enter the 5-character code for the buoy for the second site:"
    instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16), bg=tk_background_color, justify="left")
    instructions_label.grid(row=1, column=0, columnspan=20, padx=50, pady=5, sticky='nw')

    town_entry = tk.Entry(frame1, font=("Helvetica", 14))
    town_entry.grid(row=2, column=0, columnspan=20, padx=50, pady=5, sticky='nw')
    town_entry.bind("<FocusIn>", lambda e: set_current_target(town_entry))

    # Automatically set focus to the town_entry widget
    town_entry.focus_set()

    submit_button = tk.Button(frame1, text="Submit", command=bobs_submit_buoy_code, font=("Helvetica", 16, "bold"))
    submit_button.grid(row=3, column=0, columnspan=20, padx=50, pady=5, sticky='nw')

    # Spacer to push the keyboard to the bottom
    spacer = tk.Label(frame1, text="", bg=tk_background_color)
    spacer.grid(row=4, column=0, sticky="nsew", pady=(0, 120))  # Adjust row and pady as necessary
    
    # Display the virtual keyboard
    create_virtual_keyboard(frame1, 5)  # Adjust as necessary based on layout

    
def bobs_submit_buoy_code():
    global town_entry, alternative_town_2, result, town, state

    if 'keyboard_window' in globals() and keyboard_window.winfo_exists():
        keyboard_window.destroy()

    # Get the user's input
    town = town_entry.get()

    # Set the global variable alternative_town_2 to the user's input
    alternative_town_2 = town
    
    # Continue with other actions or functions as needed
    bobs_check_buoy()            

def aobs_input_buoy():
    global town_entry, alternative_town_1, state_entry, alternative_state_1, current_target_entry

    # Clear the current display
    for widget in frame1.winfo_children():
        widget.destroy()

    frame1.grid(row=0, column=0, sticky="nsew")

    label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
    label1.grid(row=0, column=0, columnspan=20, padx=50, pady=(50,0), sticky="nw")

    instruction_text = "Please enter the 5-character code for the buoy for the first site:"
    instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16), bg=tk_background_color, justify="left")
    instructions_label.grid(row=1, column=0, columnspan=20, padx=50, pady=5, sticky='nw')

    town_entry = tk.Entry(frame1, font=("Helvetica", 14))
    town_entry.grid(row=2, column=0, columnspan=20, padx=50, pady=5, sticky='nw')
    town_entry.bind("<FocusIn>", lambda e: set_current_target(town_entry))

    # Automatically set focus to the town_entry widget
    town_entry.focus_set()

    submit_button = tk.Button(frame1, text="Submit", command=aobs_submit_buoy_code, font=("Helvetica", 16, "bold"))
    submit_button.grid(row=3, column=0, columnspan=20, padx=50, pady=5, sticky='nw')

    # Spacer to push the keyboard to the bottom
    spacer = tk.Label(frame1, text="", bg=tk_background_color)
    spacer.grid(row=4, column=0, sticky="nsew", pady=(0, 120))  # Adjust row and pady as necessary
    
    # Display the virtual keyboard
    create_virtual_keyboard(frame1, 5)  # Adjust as necessary based on layout
    
def aobs_submit_buoy_code():
    global town_entry, alternative_town_1, result, town, state, keyboard_window

    if 'keyboard_window' in globals() and keyboard_window.winfo_exists():
        keyboard_window.destroy()

    # Get the user's input
    town = town_entry.get()

    # Set the global variable alternative_town_1 to the user's input
    alternative_town_1 = town
 
    # Continue with other actions or functions as needed
    aobs_check_buoy()
           
def cobs_check_land():
    global alternative_town_3, alternative_state_3, confirmed_site_3, result, town, state, cobs_obs_site, cobs_url, cobs_selected_site, cobs_station_name

    # Define a variable to store the selected value
    cobs_api_selected = None

    NWS_API_ENDPOINT = "https://api.weather.gov"
    NWS_API_STATIONS_ENDPOINT = f"{NWS_API_ENDPOINT}/stations"
    NWS_API_LATEST_OBSERVATION_ENDPOINT = f"{NWS_API_ENDPOINT}/stations/{{station_id}}/observations/latest"

    # Set the initial value for the selected radio button (first one is chosen by default)
    cobs_selected_site = tk.IntVar(value=-1)

    def calculate_center(stations):
        latitudes = [float(station['latitude']) for station in stations]
        longitudes = [float(station['longitude']) for station in stations]
        return sum(latitudes) / len(latitudes), sum(longitudes) / len(longitudes)

    def calculate_zoom_level(stations):
        max_distance = 0
        for i in range(len(stations)):
            for j in range(i + 1, len(stations)):
                point1 = (float(stations[i]['latitude']), float(stations[i]['longitude']))
                point2 = (float(stations[j]['latitude']), float(stations[j]['longitude']))
                distance = geodesic(point1, point2).kilometers
                if distance > max_distance:
                    max_distance = distance
        
        if max_distance < 50:
            return 10
        elif max_distance < 100:
            return 9
        elif max_distance < 200:
            return 8
        elif max_distance < 400:
            return 7
        elif max_distance < 800:
            return 6
        elif max_distance < 1600:
            return 5
        else:
            return 4

    def create_map_image(stations):
        center = calculate_center(stations)
        zoom_level = calculate_zoom_level(stations)

        m = folium.Map(location=center, zoom_start=zoom_level, width=450, height=300, control_scale=False, zoom_control=False)

        for station in stations:
            # Truncate the station name to a maximum of 6 characters
            station_name = station['name'][:6]  # Truncate name to 6 characters
            
            # Place a pin on the map
            folium.Marker(
                location=(float(station['latitude']), float(station['longitude'])),
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(m)
            
            # Add a label with the truncated station name, and adjust the CSS for proper centering
            folium.Marker(
                location=(float(station['latitude']), float(station['longitude'])),
                icon=folium.DivIcon(
                    html=f'''
                        <div style="
                            background-color: white;
                            padding: 2px 5px;
                            border-radius: 3px;
                            box-shadow: 0px 0px 2px rgba(0, 0, 0, 0.5);
                            font-size: 12px;
                            font-weight: bold;
                            text-align: center;
                            width: 60px;  /* Adjust width to fit the 6-character name */
                            transform: translate(-40%, -130%); /* Centering horizontally and placing above the pin */
                        ">
                            {station_name}
                        </div>
                    '''
                )
            ).add_to(m)

        # The rest of the map generation remains unchanged
        latitudes = [float(station['latitude']) for station in stations]
        longitudes = [float(station['longitude']) for station in stations]
        
        min_lat, max_lat = min(latitudes), max(latitudes)
        min_lon, max_lon = min(longitudes), max(longitudes)

        padding_factor = 0.1
        lat_padding = (max_lat - min_lat) * padding_factor
        lon_padding = (max_lon - min_lon) * padding_factor
        
        bounds = [
            [min_lat - lat_padding, min_lon - lon_padding],
            [max_lat + lat_padding, max_lon + lon_padding]
        ]
        
        m.fit_bounds(bounds)
        m.save('station_locations.html')

        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')  # Add this argument for consistency

        # Explicitly specify the chromedriver path
        driver = webdriver.Chrome(service=ChromeService(executable_path="/usr/bin/chromedriver"), options=options)
        driver.set_window_size(450, 387)

        driver.get(f'file://{os.path.abspath("station_locations.html")}')
        time.sleep(2)  # Adjust as needed

        driver.save_screenshot('station_locations.png')
        driver.quit()

    def display_map_image():
        img_path = "/home/santod/station_locations.png"
        img = Image.open(img_path)
        img = img.resize((450, 300), Image.LANCZOS)
        tk_img = ImageTk.PhotoImage(img)

        label = tk.Label(frame1, image=tk_img)
        label.image = tk_img
        label.grid(row=8, column=8, rowspan=6, sticky="se", padx=(570, 10), pady=0)
    
    def cobs_api_capture():
        global cobs_api_selected, cobs_station_name, cobs_station_identifier, cobs_url, cobs_station_identifier
        cobs_api_selected = cobs_selected_site.get()
        
        if cobs_api_selected < len(valid_stations):
            cobs_selected_station = valid_stations[cobs_api_selected]
            cobs_station_name = cobs_selected_station["name"]
            
            cobs_station_identifier = cobs_selected_station["identifier"]
            cobs_obs_lat, cobs_obs_lon = cobs_selected_station["latitude"], cobs_selected_station["longitude"]

            def generate_cobs_url(cobs_obs_lat, cobs_obs_lon, cobs_site=''):
                cobs_url = f"https://forecast.weather.gov/MapClick.php?lon={cobs_obs_lat}&lat={cobs_obs_lon}"
                if cobs_site:
                    cobs_url += f"&site={cobs_site}"
                return cobs_url

            cobs_url = generate_cobs_url(cobs_obs_lat, cobs_obs_lon)
                        
        else:
            land_or_buoy()


    def parse_iso_timestamp(timestamp):
        match = re.match(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})', timestamp)
        if match:
            return match.group(1)
        return None

    cobs_selected_site.trace("w", lambda name, index, mode, var=cobs_selected_site: cobs_api_capture())

    alternative_town_3 = town

    if len(alternative_town_3) == 3:
        alternative_town_3 = alternative_town_3.upper()
    else:
        alternative_town_3 = alternative_town_3.title()

    alternative_state_3 = state.upper()

    try:
        geolocator = Nominatim(user_agent="town-state-locator")
        location_query = f"{alternative_town_3}, {alternative_state_3}"
        location = geolocator.geocode(location_query, exactly_one=True)

        if location is not None:
            user_lat = location.latitude
            user_lon = location.longitude

            def fetch_stations_by_state(state):
                stations = []
                page_counter = 0
                url = f"{NWS_API_STATIONS_ENDPOINT}?state={state}&limit=500"

                while url:
                    response = requests.get(url)
                    if response.status_code != 200:
                        raise ValueError(f"Error retrieving stations for state {state}: {response.status_code}")
                    data = response.json()
                    features = data.get('features', [])
                    stations.extend(features)

                    if len(features) < 500:
                        break

                    cursor = data.get('pagination', {}).get('next', None)
                    url = cursor
                    page_counter += 1

                return stations

            def fetch_all_stations_concurrently(states):
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    futures = [executor.submit(fetch_stations_by_state, state) for state in states]
                    results = []
                    for future in concurrent.futures.as_completed(futures):
                        try:
                            results.extend(future.result())
                        except Exception as e:
                            print(f"Error fetching stations: {e}")

                return results

            def get_closest_stations(lat, lon, states):
                features = fetch_all_stations_concurrently(states)
                stations = []

                for feature in features:
                    properties = feature.get('properties', {})
                    station_id = properties.get('stationIdentifier')
                    name = properties.get('name')
                    coordinates = feature.get('geometry', {}).get('coordinates', [None, None])
                    station_lat = coordinates[1]
                    station_lon = coordinates[0]

                    if station_lat is not None and station_lon is not None:
                        distance = geopy.distance.distance((lat, lon), (station_lat, station_lon)).miles
                        stations.append((station_id, name, station_lat, station_lon, distance))

                stations.sort(key=lambda x: x[4])
                return stations

            def get_latest_observation(station_id):
                mesowest_api_token = "d8c6aee36a994f90857925cea26934be"
                url = f"https://api.mesowest.net/v2/stations/timeseries?STID={station_id}&showemptystations=1&units=temp|F,speed|mph,english&recent=240&token={mesowest_api_token}&complete=1&obtimezone=local"
                response = requests.get(url)
                if response.status_code != 200:
                    print(f"Error retrieving latest observation for station {station_id}: {response.status_code}")
                    return None

                data = response.json()
                station_data = data.get('STATION', [])[0]
                observations = station_data.get('OBSERVATIONS', {})

                temp_f = observations.get('air_temp_set_1', [None])[-1]
                wind_speed_mph = observations.get('wind_speed_set_1', [None])[-1]
                wind_direction_deg = observations.get('wind_direction_set_1', [None])[-1]
                timestamp = observations.get('date_time', [None])[-1]

                if timestamp:
                    observation_time = parse(timestamp)
                    current_time = datetime.now(timezone.utc)
                    if current_time - observation_time > timedelta(hours=2):
                        print(f"Observation for station {station_id} is older than 2 hours. Skipping.")
                        return None
                else:
                    print(f"No timestamp for observation from station {station_id}. Skipping.")
                    return None

                if temp_f is None or wind_speed_mph is None:
                    #print(f"Invalid temperature or wind speed for station {station_id}. Skipping.")
                    return None

                return {
                    "name": station_data.get('NAME'),
                    "identifier": station_id,
                    "latitude": station_data.get('LATITUDE'),
                    "longitude": station_data.get('LONGITUDE'),
                    "temperature": temp_f,
                    "wind_speed": wind_speed_mph,
                    "wind_direction": wind_direction_deg
                }

            def find_valid_stations():
                initial_states = [alternative_state_3]
                valid_stations = []
                processed_stations = set()

                stations = get_closest_stations(user_lat, user_lon, initial_states)
                for station_id, name, station_lat, station_lon, distance in stations:
                    if len(valid_stations) >= 5:
                        break

                    if station_id in processed_stations:
                        continue

                    processed_stations.add(station_id)

                    try:
                        observation = get_latest_observation(station_id)
                        if observation is not None:
                            valid_stations.append(observation)
                    except Exception as e:
                        print(f"Error retrieving latest observation for station {station_id}: {e}. Skipping.")

                if len(valid_stations) < 5:
                    print(f"Fewer than 5 stations found in the initial state. Expanding to neighboring states...")
                    nearby_states = neighboring_states.get(alternative_state_3, [])
                    if nearby_states:
                        stations = get_closest_stations(user_lat, user_lon, nearby_states)
                        for station_id, name, station_lat, station_lon, distance in stations:
                            if len(valid_stations) >= 5:
                                break

                            if station_id in processed_stations:
                                continue

                            processed_stations.add(station_id)

                            try:
                                observation = get_latest_observation(station_id)
                                if observation is not None:
                                    valid_stations.append(observation)
                            except Exception as e:
                                print(f"Error retrieving latest observation for station {station_id}: {e}. Skipping.")

                return valid_stations

            valid_stations = find_valid_stations()

            if valid_stations:
                create_map_image(valid_stations)
                display_map_image()  # Display the map only once after it is generated

            if not valid_stations:
                print("No valid stations found. Falling back to Geo-Location error handling.")
                raise ValueError("No valid weather stations found.")


            cobs_button_labels = [station['name'] for station in valid_stations] + ["Change the site"]

            for widget in frame1.winfo_children():
                widget.destroy()

            # Configure grid layout for frame1
            frame1.grid_columnconfigure(0, weight=1)
            frame1.grid_columnconfigure(9, weight=1)

            label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
            label1.grid(row=0, column=0, columnspan=9, padx=50, pady=(20, 0), sticky="nw")

            instruction_text = f"Please choose a site to represent {alternative_town_3.title()}."
            instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 14), bg=tk_background_color, justify="left")
            instructions_label.grid(row=1, column=0, columnspan=9, padx=50, pady=5, sticky='nw')

            instruction_text_2 = "Due to communication issues, not every available station will list every time this list is assembled."
            instructions_label_2 = tk.Label(frame1, text=instruction_text_2, font=("Helvetica", 12), bg=tk_background_color, justify="left", wraplength=800)
            instructions_label_2.grid(row=2, column=0, columnspan=9, padx=50, pady=5, sticky='nw')

            cobs_radio_buttons = []
            max_label_length = 40

            for a, label in enumerate(cobs_button_labels):
                if len(label) > max_label_length:
                    label = label[:max_label_length] + "..."
                
                radio_button = tk.Radiobutton(frame1, text=label, value=a, font=("Helvetica", 14), bg=tk_background_color, variable=cobs_selected_site, bd=0, highlightthickness=0)
                cobs_radio_buttons.append(radio_button)
                radio_button.grid(row=3+a, column=0, columnspan=9, padx=50, pady=6, sticky='nw')

            # Create the 'Back' button
            back_button = create_button(frame1, " Back ", button_font, cobs_input_land)
            back_button.grid(row=3+len(cobs_button_labels), column=0, columnspan=9, padx=(50, 0), pady=10, sticky="nw")

            next_button = create_button(frame1, "Submit", button_font, cobs_confirm_land)
            next_button.grid(row=3+len(cobs_button_labels), column=0, columnspan=9, padx=200, pady=10, sticky="nw")

            display_map_image()
        
        else:
            raise ValueError("Geo-Location failed. Location data is None.")

    except Exception as e:
        print(f"Error encountered: {e}")
        for widget in frame1.winfo_children():
            if isinstance(widget, (tk.Checkbutton, tk.Label, tk.Button, tk.Entry)):
                widget.destroy()

        frame1.grid(row=0, column=0, sticky="nsew")

        label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
        label1.grid(row=0, column=0, padx=50, pady=10, sticky="w") 

        instruction_text = "The Geo-Location services are not available now."
        instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16), bg=tk_background_color)
        instructions_label.grid(row=1, column=0, padx=50, pady=(20, 10), sticky='w')

        instruction_text_2 = "Please try again in a few minutes."
        instructions_label_2 = tk.Label(frame1, text=instruction_text_2, font=("Helvetica", 16), bg=tk_background_color)
        instructions_label_2.grid(row=2, column=0, padx=50, pady=(20, 10), sticky='w')

        next_button = create_button(frame1, "Next", button_font, land_or_buoy)
        next_button.grid(row=10, column=0, padx=(50, 0), pady=10, sticky="w")


def bobs_check_land():
    global alternative_town_2, alternative_state_2, confirmed_site_2, result, town, state, bobs_url, bobs_selected_site

    # Define a variable to store the selected value
    bobs_api_selected = None

    NWS_API_ENDPOINT = "https://api.weather.gov"
    NWS_API_STATIONS_ENDPOINT = f"{NWS_API_ENDPOINT}/stations"
    NWS_API_LATEST_OBSERVATION_ENDPOINT = f"{NWS_API_ENDPOINT}/stations/{{station_id}}/observations/latest"

    # Set the initial value for the selected radio button (first one is chosen by default)
    bobs_selected_site = tk.IntVar(value=-1)

    def calculate_center(stations):
        latitudes = [float(station['latitude']) for station in stations]
        longitudes = [float(station['longitude']) for station in stations]
        return sum(latitudes) / len(latitudes), sum(longitudes) / len(longitudes)

    def calculate_zoom_level(stations):
        max_distance = 0
        for i in range(len(stations)):
            for j in range(i + 1, len(stations)):
                point1 = (float(stations[i]['latitude']), float(stations[i]['longitude']))
                point2 = (float(stations[j]['latitude']), float(stations[j]['longitude']))
                distance = geodesic(point1, point2).kilometers
                if distance > max_distance:
                    max_distance = distance
        
        if max_distance < 50:
            return 10
        elif max_distance < 100:
            return 9
        elif max_distance < 200:
            return 8
        elif max_distance < 400:
            return 7
        elif max_distance < 800:
            return 6
        elif max_distance < 1600:
            return 5
        else:
            return 4

    def create_map_image(stations):
        center = calculate_center(stations)
        zoom_level = calculate_zoom_level(stations)

        m = folium.Map(location=center, zoom_start=zoom_level, width=450, height=300, control_scale=False, zoom_control=False)

        for station in stations:
            # Truncate the station name to a maximum of 6 characters
            station_name = station['name'][:6]  # Truncate name to 6 characters
            
            # Place a pin on the map
            folium.Marker(
                location=(float(station['latitude']), float(station['longitude'])),
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(m)
            
            # Add a label with the truncated station name, and adjust the CSS for proper centering
            folium.Marker(
                location=(float(station['latitude']), float(station['longitude'])),
                icon=folium.DivIcon(
                    html=f'''
                        <div style="
                            background-color: white;
                            padding: 2px 5px;
                            border-radius: 3px;
                            box-shadow: 0px 0px 2px rgba(0, 0, 0, 0.5);
                            font-size: 12px;
                            font-weight: bold;
                            text-align: center;
                            width: 60px;  /* Adjust width to fit the 6-character name */
                            transform: translate(-40%, -130%); /* Centering horizontally and placing above the pin */
                        ">
                            {station_name}
                        </div>
                    '''
                )
            ).add_to(m)

        # The rest of the map generation remains unchanged
        latitudes = [float(station['latitude']) for station in stations]
        longitudes = [float(station['longitude']) for station in stations]
        
        min_lat, max_lat = min(latitudes), max(latitudes)
        min_lon, max_lon = min(longitudes), max(longitudes)

        padding_factor = 0.1
        lat_padding = (max_lat - min_lat) * padding_factor
        lon_padding = (max_lon - min_lon) * padding_factor
        
        bounds = [
            [min_lat - lat_padding, min_lon - lon_padding],
            [max_lat + lat_padding, max_lon + lon_padding]
        ]
        
        m.fit_bounds(bounds)
        m.save('station_locations.html')

        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')  # Add this argument for consistency

        # Explicitly specify the chromedriver path
        driver = webdriver.Chrome(service=ChromeService(executable_path="/usr/bin/chromedriver"), options=options)
        driver.set_window_size(450, 387)

        driver.get(f'file://{os.path.abspath("station_locations.html")}')
        time.sleep(2)  # Adjust as needed

        driver.save_screenshot('station_locations.png')
        driver.quit()

    def display_map_image():
        img_path = "/home/santod/station_locations.png"
        img = Image.open(img_path)
        img = img.resize((450, 300), Image.LANCZOS)
        tk_img = ImageTk.PhotoImage(img)

        label = tk.Label(frame1, image=tk_img)
        label.image = tk_img
        label.grid(row=8, column=8, rowspan=6, sticky="se", padx=(570, 10), pady=0)
    
    def bobs_api_capture():
        global bobs_api_selected, bobs_station_name, bobs_station_identifier, bobs_url, bobs_station_identifier
        bobs_api_selected = bobs_selected_site.get()
        
        if bobs_api_selected < len(valid_stations):
            bobs_selected_station = valid_stations[bobs_api_selected]
            bobs_station_name = bobs_selected_station["name"]
            
            bobs_station_identifier = bobs_selected_station["identifier"]
            bobs_obs_lat, bobs_obs_lon = bobs_selected_station["latitude"], bobs_selected_station["longitude"]

            def generate_bobs_url(bobs_obs_lat, bobs_obs_lon, bobs_site=''):
                bobs_url = f"https://forecast.weather.gov/MapClick.php?lon={bobs_obs_lat}&lat={bobs_obs_lon}"
                if bobs_site:
                    bobs_url += f"&site={bobs_site}"
                return bobs_url

            bobs_url = generate_bobs_url(bobs_obs_lat, bobs_obs_lon)
                        
        else:
            land_or_buoy()


    def parse_iso_timestamp(timestamp):
        match = re.match(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})', timestamp)
        if match:
            return match.group(1)
        return None

    bobs_selected_site.trace("w", lambda name, index, mode, var=bobs_selected_site: bobs_api_capture())

    alternative_town_2 = town

    if len(alternative_town_2) == 3:
        alternative_town_2 = alternative_town_2.upper()
    else:
        alternative_town_2 = alternative_town_2.title()

    alternative_state_2 = state.upper()

    try:
        geolocator = Nominatim(user_agent="town-state-locator")
        location_query = f"{alternative_town_2}, {alternative_state_2}"
        location = geolocator.geocode(location_query, exactly_one=True)

        if location is not None:
            user_lat = location.latitude
            user_lon = location.longitude

            def fetch_stations_by_state(state):
                stations = []
                page_counter = 0
                url = f"{NWS_API_STATIONS_ENDPOINT}?state={state}&limit=500"

                while url:
                    response = requests.get(url)
                    if response.status_code != 200:
                        raise ValueError(f"Error retrieving stations for state {state}: {response.status_code}")
                    data = response.json()
                    features = data.get('features', [])
                    stations.extend(features)

                    if len(features) < 500:
                        break

                    cursor = data.get('pagination', {}).get('next', None)
                    url = cursor
                    page_counter += 1

                return stations

            def fetch_all_stations_concurrently(states):
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    futures = [executor.submit(fetch_stations_by_state, state) for state in states]
                    results = []
                    for future in concurrent.futures.as_completed(futures):
                        try:
                            results.extend(future.result())
                        except Exception as e:
                            print(f"Error fetching stations: {e}")

                return results

            def get_closest_stations(lat, lon, states):
                features = fetch_all_stations_concurrently(states)
                stations = []

                for feature in features:
                    properties = feature.get('properties', {})
                    station_id = properties.get('stationIdentifier')
                    name = properties.get('name')
                    coordinates = feature.get('geometry', {}).get('coordinates', [None, None])
                    station_lat = coordinates[1]
                    station_lon = coordinates[0]

                    if station_lat is not None and station_lon is not None:
                        distance = geopy.distance.distance((lat, lon), (station_lat, station_lon)).miles
                        stations.append((station_id, name, station_lat, station_lon, distance))

                stations.sort(key=lambda x: x[4])
                return stations

            def get_latest_observation(station_id):
                mesowest_api_token = "d8c6aee36a994f90857925cea26934be"
                url = f"https://api.mesowest.net/v2/stations/timeseries?STID={station_id}&showemptystations=1&units=temp|F,speed|mph,english&recent=240&token={mesowest_api_token}&complete=1&obtimezone=local"
                response = requests.get(url)
                if response.status_code != 200:
                    print(f"Error retrieving latest observation for station {station_id}: {response.status_code}")
                    return None

                data = response.json()
                station_data = data.get('STATION', [])[0]
                observations = station_data.get('OBSERVATIONS', {})

                temp_f = observations.get('air_temp_set_1', [None])[-1]
                wind_speed_mph = observations.get('wind_speed_set_1', [None])[-1]
                wind_direction_deg = observations.get('wind_direction_set_1', [None])[-1]
                timestamp = observations.get('date_time', [None])[-1]

                if timestamp:
                    observation_time = parse(timestamp)
                    current_time = datetime.now(timezone.utc)
                    if current_time - observation_time > timedelta(hours=2):
                        print(f"Observation for station {station_id} is older than 2 hours. Skipping.")
                        return None
                else:
                    print(f"No timestamp for observation from station {station_id}. Skipping.")
                    return None

                if temp_f is None or wind_speed_mph is None:
                    #print(f"Invalid temperature or wind speed for station {station_id}. Skipping.")
                    return None

                return {
                    "name": station_data.get('NAME'),
                    "identifier": station_id,
                    "latitude": station_data.get('LATITUDE'),
                    "longitude": station_data.get('LONGITUDE'),
                    "temperature": temp_f,
                    "wind_speed": wind_speed_mph,
                    "wind_direction": wind_direction_deg
                }

            def find_valid_stations():
                initial_states = [alternative_state_2]
                valid_stations = []
                processed_stations = set()

                stations = get_closest_stations(user_lat, user_lon, initial_states)
                for station_id, name, station_lat, station_lon, distance in stations:
                    if len(valid_stations) >= 5:
                        break

                    if station_id in processed_stations:
                        continue

                    processed_stations.add(station_id)

                    try:
                        observation = get_latest_observation(station_id)
                        if observation is not None:
                            valid_stations.append(observation)
                    except Exception as e:
                        print(f"Error retrieving latest observation for station {station_id}: {e}. Skipping.")

                if len(valid_stations) < 5:
                    print(f"Fewer than 5 stations found in the initial state. Expanding to neighboring states...")
                    nearby_states = neighboring_states.get(alternative_state_2, [])
                    if nearby_states:
                        stations = get_closest_stations(user_lat, user_lon, nearby_states)
                        for station_id, name, station_lat, station_lon, distance in stations:
                            if len(valid_stations) >= 5:
                                break

                            if station_id in processed_stations:
                                continue

                            processed_stations.add(station_id)

                            try:
                                observation = get_latest_observation(station_id)
                                if observation is not None:
                                    valid_stations.append(observation)
                            except Exception as e:
                                print(f"Error retrieving latest observation for station {station_id}: {e}. Skipping.")

                return valid_stations

            valid_stations = find_valid_stations()

            if valid_stations:
                create_map_image(valid_stations)
                display_map_image()  # Display the map only once after it is generated

            if not valid_stations:
                print("No valid stations found. Falling back to Geo-Location error handling.")
                raise ValueError("No valid weather stations found.")


            bobs_button_labels = [station['name'] for station in valid_stations] + ["Change the site"]

            for widget in frame1.winfo_children():
                widget.destroy()

            # Configure grid layout for frame1
            frame1.grid_columnconfigure(0, weight=1)
            frame1.grid_columnconfigure(9, weight=1)

            label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
            label1.grid(row=0, column=0, columnspan=9, padx=50, pady=(20, 0), sticky="nw")

            instruction_text = f"Please choose a site to represent {alternative_town_2.title()}."
            instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 14), bg=tk_background_color, justify="left")
            instructions_label.grid(row=1, column=0, columnspan=9, padx=50, pady=5, sticky='nw')

            instruction_text_2 = "Due to communication issues, not every available station will list every time this list is assembled."
            instructions_label_2 = tk.Label(frame1, text=instruction_text_2, font=("Helvetica", 12), bg=tk_background_color, justify="left", wraplength=800)
            instructions_label_2.grid(row=2, column=0, columnspan=9, padx=50, pady=5, sticky='nw')

            bobs_radio_buttons = []
            max_label_length = 40

            for a, label in enumerate(bobs_button_labels):
                if len(label) > max_label_length:
                    label = label[:max_label_length] + "..."
                
                radio_button = tk.Radiobutton(frame1, text=label, value=a, font=("Helvetica", 14), bg=tk_background_color, variable=bobs_selected_site, bd=0, highlightthickness=0)
                bobs_radio_buttons.append(radio_button)
                radio_button.grid(row=3+a, column=0, columnspan=9, padx=50, pady=6, sticky='nw')

            next_button = create_button(frame1, "Submit", button_font, bobs_confirm_land)
            next_button.grid(row=3+len(bobs_button_labels), column=0, columnspan=9, padx=50, pady=0, sticky="nw")

            display_map_image()
        
        else:
            raise ValueError("Geo-Location failed. Location data is None.")

    except Exception as e:
        print(f"Error encountered: {e}")
        for widget in frame1.winfo_children():
            if isinstance(widget, (tk.Checkbutton, tk.Label, tk.Button, tk.Entry)):
                widget.destroy()

        frame1.grid(row=0, column=0, sticky="nsew")

        label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
        label1.grid(row=0, column=0, padx=50, pady=10, sticky="w") 

        instruction_text = "The Geo-Location services are not available now."
        instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16), bg=tk_background_color)
        instructions_label.grid(row=1, column=0, padx=50, pady=(20, 10), sticky='w')

        instruction_text_2 = "Please try again in a few minutes."
        instructions_label_2 = tk.Label(frame1, text=instruction_text_2, font=("Helvetica", 16), bg=tk_background_color)
        instructions_label_2.grid(row=2, column=0, padx=50, pady=(20, 10), sticky='w')

        next_button = create_button(frame1, "Next", button_font, land_or_buoy)
        next_button.grid(row=10, column=0, padx=(50, 0), pady=10, sticky="w")


def aobs_check_land(): 
    global alternative_town_1, alternative_state_1, confirmed_site_1, result, town, state, aobs_station_name, aobs_url, aobs_selected_site

    # Define a variable to store the selected value
    aobs_api_selected = None

    NWS_API_ENDPOINT = "https://api.weather.gov"
    NWS_API_STATIONS_ENDPOINT = f"{NWS_API_ENDPOINT}/stations"
    NWS_API_LATEST_OBSERVATION_ENDPOINT = f"{NWS_API_ENDPOINT}/stations/{{station_id}}/observations/latest"

    # Set the initial value for the selected radio button (first one is chosen by default)
    aobs_selected_site = tk.IntVar(value=-1)

    def calculate_center(stations):
        latitudes = [float(station['latitude']) for station in stations]
        longitudes = [float(station['longitude']) for station in stations]
        return sum(latitudes) / len(latitudes), sum(longitudes) / len(longitudes)

    def calculate_zoom_level(stations):
        max_distance = 0
        for i in range(len(stations)):
            for j in range(i + 1, len(stations)):
                point1 = (float(stations[i]['latitude']), float(stations[i]['longitude']))
                point2 = (float(stations[j]['latitude']), float(stations[j]['longitude']))
                distance = geodesic(point1, point2).kilometers
                if distance > max_distance:
                    max_distance = distance
        
        if max_distance < 50:
            return 10
        elif max_distance < 100:
            return 9
        elif max_distance < 200:
            return 8
        elif max_distance < 400:
            return 7
        elif max_distance < 800:
            return 6
        elif max_distance < 1600:
            return 5
        else:
            return 4

    def create_map_image(stations):
        center = calculate_center(stations)
        zoom_level = calculate_zoom_level(stations)

        m = folium.Map(location=center, zoom_start=zoom_level, width=450, height=300, control_scale=False, zoom_control=False)

        for station in stations:
            # Truncate the station name to a maximum of 6 characters
            station_name = station['name'][:6]  # Truncate name to 6 characters
            
            # Place a pin on the map
            folium.Marker(
                location=(float(station['latitude']), float(station['longitude'])),
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(m)
            
            # Add a label with the truncated station name, and adjust the CSS for proper centering
            folium.Marker(
                location=(float(station['latitude']), float(station['longitude'])),
                icon=folium.DivIcon(
                    html=f'''
                        <div style="
                            background-color: white;
                            padding: 2px 5px;
                            border-radius: 3px;
                            box-shadow: 0px 0px 2px rgba(0, 0, 0, 0.5);
                            font-size: 12px;
                            font-weight: bold;
                            text-align: center;
                            width: 60px;  /* Adjust width to fit the 6-character name */
                            transform: translate(-40%, -130%); /* Centering horizontally and placing above the pin */
                        ">
                            {station_name}
                        </div>
                    '''
                )
            ).add_to(m)

        # The rest of the map generation remains unchanged
        latitudes = [float(station['latitude']) for station in stations]
        longitudes = [float(station['longitude']) for station in stations]
        
        min_lat, max_lat = min(latitudes), max(latitudes)
        min_lon, max_lon = min(longitudes), max(longitudes)

        padding_factor = 0.1
        lat_padding = (max_lat - min_lat) * padding_factor
        lon_padding = (max_lon - min_lon) * padding_factor
        
        bounds = [
            [min_lat - lat_padding, min_lon - lon_padding],
            [max_lat + lat_padding, max_lon + lon_padding]
        ]
        
        m.fit_bounds(bounds)
        m.save('station_locations.html')

        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')  # Add this argument for consistency

        # Explicitly specify the chromedriver path
        driver = webdriver.Chrome(service=ChromeService(executable_path="/usr/bin/chromedriver"), options=options)
        driver.set_window_size(450, 387)

        driver.get(f'file://{os.path.abspath("station_locations.html")}')
        time.sleep(2)  # Adjust as needed

        driver.save_screenshot('station_locations.png')
        driver.quit()

    def display_map_image():
        img_path = "/home/santod/station_locations.png"
        img = Image.open(img_path)
        img = img.resize((450, 300), Image.LANCZOS)
        tk_img = ImageTk.PhotoImage(img)

        label = tk.Label(frame1, image=tk_img)
        label.image = tk_img
        label.grid(row=8, column=8, rowspan=6, sticky="se", padx=(570, 10), pady=0)

        #frame1.update_idletasks()
    
    def aobs_api_capture():
        global aobs_api_selected, aobs_station_name, aobs_station_identifier, aobs_url, aobs_station_identifier
        aobs_api_selected = aobs_selected_site.get()
        
        if aobs_api_selected < len(valid_stations):
            aobs_selected_station = valid_stations[aobs_api_selected]
            aobs_station_name = aobs_selected_station["name"]
            
            aobs_station_identifier = aobs_selected_station["identifier"]
            aobs_obs_lat, aobs_obs_lon = aobs_selected_station["latitude"], aobs_selected_station["longitude"]

            def generate_aobs_url(aobs_obs_lat, aobs_obs_lon, aobs_site=''):
                aobs_url = f"https://forecast.weather.gov/MapClick.php?lon={aobs_obs_lat}&lat={aobs_obs_lon}"
                if aobs_site:
                    aobs_url += f"&site={aobs_site}"
                return aobs_url

            aobs_url = generate_aobs_url(aobs_obs_lat, aobs_obs_lon)
                         
        else:
            land_or_buoy()


    def parse_iso_timestamp(timestamp):
        match = re.match(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})', timestamp)
        if match:
            return match.group(1)
        return None

    aobs_selected_site.trace("w", lambda name, index, mode, var=aobs_selected_site: aobs_api_capture())

    alternative_town_1 = town

    if len(alternative_town_1) == 3:
        alternative_town_1 = alternative_town_1.upper()
    else:
        alternative_town_1 = alternative_town_1.title()

    alternative_state_1 = state.upper()

    try:
        geolocator = Nominatim(user_agent="town-state-locator")
        location_query = f"{alternative_town_1}, {alternative_state_1}"
        location = geolocator.geocode(location_query, exactly_one=True)

        if location is not None:
            user_lat = location.latitude
            user_lon = location.longitude

            def fetch_stations_by_state(state):
                stations = []
                page_counter = 0
                url = f"{NWS_API_STATIONS_ENDPOINT}?state={state}&limit=500"

                while url:
                    response = requests.get(url)
                    if response.status_code != 200:
                        raise ValueError(f"Error retrieving stations for state {state}: {response.status_code}")
                    data = response.json()
                    features = data.get('features', [])
                    stations.extend(features)

                    if len(features) < 500:
                        break

                    cursor = data.get('pagination', {}).get('next', None)
                    url = cursor
                    page_counter += 1

                return stations

            def fetch_all_stations_concurrently(states):
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    futures = [executor.submit(fetch_stations_by_state, state) for state in states]
                    results = []
                    for future in concurrent.futures.as_completed(futures):
                        try:
                            results.extend(future.result())
                        except Exception as e:
                            print(f"Error fetching stations: {e}")

                return results

            def get_closest_stations(lat, lon, states):
                features = fetch_all_stations_concurrently(states)
                stations = []

                for feature in features:
                    properties = feature.get('properties', {})
                    station_id = properties.get('stationIdentifier')
                    name = properties.get('name')
                    coordinates = feature.get('geometry', {}).get('coordinates', [None, None])
                    station_lat = coordinates[1]
                    station_lon = coordinates[0]

                    if station_lat is not None and station_lon is not None:
                        distance = geopy.distance.distance((lat, lon), (station_lat, station_lon)).miles
                        stations.append((station_id, name, station_lat, station_lon, distance))

                stations.sort(key=lambda x: x[4])
                return stations

            def get_latest_observation(station_id):
                mesowest_api_token = "d8c6aee36a994f90857925cea26934be"
                url = f"https://api.mesowest.net/v2/stations/timeseries?STID={station_id}&showemptystations=1&units=temp|F,speed|mph,english&recent=240&token={mesowest_api_token}&complete=1&obtimezone=local"
                response = requests.get(url)
                if response.status_code != 200:
                    print(f"Error retrieving latest observation for station {station_id}: {response.status_code}")
                    return None

                data = response.json()
                station_data = data.get('STATION', [])[0]
                observations = station_data.get('OBSERVATIONS', {})

                temp_f = observations.get('air_temp_set_1', [None])[-1]
                wind_speed_mph = observations.get('wind_speed_set_1', [None])[-1]
                wind_direction_deg = observations.get('wind_direction_set_1', [None])[-1]
                timestamp = observations.get('date_time', [None])[-1]

                if timestamp:
                    observation_time = parse(timestamp)
                    current_time = datetime.now(timezone.utc)
                    if current_time - observation_time > timedelta(hours=2):
                        print(f"Observation for station {station_id} is older than 2 hours. Skipping.")
                        return None
                else:
                    print(f"No timestamp for observation from station {station_id}. Skipping.")
                    return None

                if temp_f is None or wind_speed_mph is None:
                    #print(f"Invalid temperature or wind speed for station {station_id}. Skipping.")
                    return None

                return {
                    "name": station_data.get('NAME'),
                    "identifier": station_id,
                    "latitude": station_data.get('LATITUDE'),
                    "longitude": station_data.get('LONGITUDE'),
                    "temperature": temp_f,
                    "wind_speed": wind_speed_mph,
                    "wind_direction": wind_direction_deg
                }

            def find_valid_stations():
                initial_states = [alternative_state_1]
                valid_stations = []
                processed_stations = set()

                stations = get_closest_stations(user_lat, user_lon, initial_states)
                for station_id, name, station_lat, station_lon, distance in stations:
                    if len(valid_stations) >= 5:
                        break

                    if station_id in processed_stations:
                        continue

                    processed_stations.add(station_id)

                    try:
                        observation = get_latest_observation(station_id)
                        if observation is not None:
                            valid_stations.append(observation)
                    except Exception as e:
                        print(f"Error retrieving latest observation for station {station_id}: {e}. Skipping.")

                if len(valid_stations) < 5:
                    print(f"Fewer than 5 stations found in the initial state. Expanding to neighboring states...")
                    nearby_states = neighboring_states.get(alternative_state_1, [])
                    if nearby_states:
                        stations = get_closest_stations(user_lat, user_lon, nearby_states)
                        for station_id, name, station_lat, station_lon, distance in stations:
                            if len(valid_stations) >= 5:
                                break

                            if station_id in processed_stations:
                                continue

                            processed_stations.add(station_id)

                            try:
                                observation = get_latest_observation(station_id)
                                if observation is not None:
                                    valid_stations.append(observation)
                            except Exception as e:
                                print(f"Error retrieving latest observation for station {station_id}: {e}. Skipping.")

                return valid_stations

            valid_stations = find_valid_stations()

            if valid_stations:
                create_map_image(valid_stations)
                display_map_image()  # Display the map only once after it is generated

            if not valid_stations:
                print("No valid stations found. Falling back to Geo-Location error handling.")
                raise ValueError("No valid weather stations found.")


            aobs_button_labels = [station['name'] for station in valid_stations] + ["Change the site"]

            for widget in frame1.winfo_children():
                widget.destroy()

            # Configure grid layout for frame1
            frame1.grid_columnconfigure(0, weight=1)
            frame1.grid_columnconfigure(9, weight=1)

            label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
            label1.grid(row=0, column=0, columnspan=9, padx=50, pady=(20, 0), sticky="nw")

            instruction_text = f"Please choose a site to represent {alternative_town_1.title()}."
            instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 14), bg=tk_background_color, justify="left")
            instructions_label.grid(row=1, column=0, columnspan=9, padx=50, pady=5, sticky='nw')

            instruction_text_2 = "Due to communication issues, not every available station will list every time this list is assembled."
            instructions_label_2 = tk.Label(frame1, text=instruction_text_2, font=("Helvetica", 12), bg=tk_background_color, justify="left", wraplength=800)
            instructions_label_2.grid(row=2, column=0, columnspan=9, padx=50, pady=5, sticky='nw')

            aobs_radio_buttons = []
            max_label_length = 40

            for a, label in enumerate(aobs_button_labels):
                if len(label) > max_label_length:
                    label = label[:max_label_length] + "..."
                
                radio_button = tk.Radiobutton(frame1, text=label, value=a, font=("Helvetica", 14), bg=tk_background_color, variable=aobs_selected_site, bd=0, highlightthickness=0)
                aobs_radio_buttons.append(radio_button)
                radio_button.grid(row=3+a, column=0, columnspan=9, padx=50, pady=6, sticky='nw')

            # Create the 'Back' button
            back_button = create_button(frame1, " Back ", button_font, aobs_input_land)
            back_button.grid(row=3+len(aobs_button_labels), column=0, columnspan=9, padx=(50, 0), pady=0, sticky="nw")
                       
            next_button = create_button(frame1, "Submit", button_font, aobs_confirm_land)
            next_button.grid(row=3+len(aobs_button_labels), column=0, columnspan=9, padx=200, pady=0, sticky="nw")

            display_map_image()
        
        else:
            raise ValueError("Geo-Location failed. Location data is None.")

    except Exception as e:
        print(f"Error encountered: {e}")
        for widget in frame1.winfo_children():
            if isinstance(widget, (tk.Checkbutton, tk.Label, tk.Button, tk.Entry)):
                widget.destroy()

        frame1.grid(row=0, column=0, sticky="nsew")

        label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
        label1.grid(row=0, column=0, padx=50, pady=10, sticky="w") 

        instruction_text = "The Geo-Location services are not available now."
        instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16), bg=tk_background_color)
        instructions_label.grid(row=1, column=0, padx=50, pady=(20, 10), sticky='w')

        instruction_text_2 = "Please try again in a few minutes."
        instructions_label_2 = tk.Label(frame1, text=instruction_text_2, font=("Helvetica", 16), bg=tk_background_color)
        instructions_label_2.grid(row=2, column=0, padx=50, pady=(20, 10), sticky='w')

        next_button = create_button(frame1, "Next", button_font, land_or_buoy)
        next_button.grid(row=10, column=0, padx=(50, 0), pady=10, sticky="w")




def bobs_check_buoy():
    global alternative_town_2, town_entry, result, bobs_url, bobs_only_click_flag
    
    # Clear the current display
    for widget in frame1.winfo_children():
        widget.destroy()

    # Assuming existing setup for frame1, bobs_api, and other variables
    frame1.grid(row=0, column=0, sticky="nsew")

    # Create and display the updated labels
    label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
    label1.grid(row=0, column=0, padx=50, pady=(50,0), sticky="w")
    
    # Build the URL using the buoy code
    bobs_url = f"https://www.ndbc.noaa.gov/station_page.php?station={alternative_town_2}"
    response = requests.get(bobs_url)
    
    if response.status_code == 200:
        confirmed_site_2 = True

        # Define the URL with the correct station ID for the MesoWest API
        b_station_url = f"https://api.mesowest.net/v2/stations/timeseries?STID={alternative_town_2}&showemptystations=1&units=temp|F,speed|mph,english&recent=240&token=d8c6aee36a994f90857925cea26934be&complete=1&obtimezone=local"
        b_response = requests.get(b_station_url)
        b_data = b_response.json()

        try:
            station_data = b_data["STATION"][0]
            if "OBSERVATIONS" in station_data and "date_time" in station_data["OBSERVATIONS"]:
                last_observation_time_str = station_data["OBSERVATIONS"]["date_time"][-1]
                last_observation_time = datetime.strptime(last_observation_time_str, '%Y-%m-%dT%H:%M:%S%z')
                current_time = datetime.now(timezone.utc)
                time_difference = current_time - last_observation_time

                if time_difference > timedelta(hours=2):
                    raise ValueError("Data from buoy {} is more than 2 hours old. Please select a different site.".format(alternative_town_2))

                # If data is recent
                accept_text = f"Buoy {alternative_town_2} will be used for the second observation site."
                accept_label = tk.Label(frame1, text=accept_text, font=("Helvetica", 16,), bg=tk_background_color)
                accept_label.grid(row=1, column=0, padx=50, pady=(20,10))
                next_function = cobs_input_land if not bobs_only_click_flag else forget_frame1_and_show_scraped_and_transparent_frames
                bobs_only_click_flag = False

            else:
                raise ValueError("No recent data available for buoy {}. Please select a different site.".format(alternative_town_2))

        except Exception as e:
            print(f"Error processing data: {e}")
            error_message = "Data from buoy {} is more than 2 hours old or missing. Please select a different site.".format(alternative_town_2)
            error_label = tk.Label(frame1, text=error_message, font=("Helvetica", 16,), bg=tk_background_color)
            error_label.grid(row=1, column=0, padx=50, pady=(20,10))
            next_function = bobs_land_or_buoy

        # Create the 'Next' button
        next_button = create_button(frame1, "Next", button_font, next_function)
        next_button.grid(row=3, column=0, padx=(50, 0), pady=10, sticky="w")

    else:
        deny_text = f"Not able to find a buoy with that code. Please choose another site."
        deny_label = tk.Label(frame1, text=deny_text, font=("Helvetica", 16,), bg=tk_background_color)
        deny_label.grid(row=1, column=0, padx=50, pady=(20,10))
        next_function = bobs_land_or_buoy
        # Create the 'Next' button
        next_button = create_button(frame1, "Next", button_font, next_function)
        next_button.grid(row=3, column=0, padx=(50, 0), pady=10, sticky="w")



def aobs_check_buoy():
    global alternative_town_1, town_entry, result, aobs_url, aobs_only_click_flag

    # Clear the current display
    for widget in frame1.winfo_children():
        widget.destroy()

    # Assuming existing setup for frame1, aobs_api, and other variables
    frame1.grid(row=0, column=0, sticky="nsew")

    # Create and display the updated labels
    label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
    label1.grid(row=0, column=0, padx=50, pady=(50,0), sticky="w")

    # Build the URL using the buoy code
    aobs_url = f"https://www.ndbc.noaa.gov/station_page.php?station={alternative_town_1}"
    response = requests.get(aobs_url)

    if response.status_code == 200:
        confirmed_site_1 = True

        # Define the URL with the correct station ID
        a_station_url = f"https://api.mesowest.net/v2/stations/timeseries?STID={alternative_town_1}&showemptystations=1&units=temp|F,speed|mph,english&recent=240&token=d8c6aee36a994f90857925cea26934be&complete=1&obtimezone=local"
        a_response = requests.get(a_station_url)
        a_data = a_response.json()

        try:
            station_data = a_data["STATION"][0]
            if "OBSERVATIONS" in station_data and "date_time" in station_data["OBSERVATIONS"]:
                last_observation_time_str = station_data["OBSERVATIONS"]["date_time"][-1]
                last_observation_time = datetime.strptime(last_observation_time_str, '%Y-%m-%dT%H:%M:%S%z')
                current_time = datetime.now(timezone.utc)
                time_difference = current_time - last_observation_time

                if time_difference > timedelta(hours=2):
                    raise ValueError("Data from buoy {} is more than 2 hours old. Please select a different site.".format(alternative_town_1))

                # If data is recent
                accept_text = f"Buoy {alternative_town_1} will be used for the first observation site."
                accept_label = tk.Label(frame1, text=accept_text, font=("Helvetica", 16,), bg=tk_background_color)
                accept_label.grid(row=1, column=0, padx=50, pady=(20,10))
                next_function = bobs_land_or_buoy if not aobs_only_click_flag else forget_frame1_and_show_scraped_and_transparent_frames
                aobs_only_click_flag = False

            else:
                raise ValueError("No recent data available for buoy {}. Please select a different site.".format(alternative_town_1))

        except Exception as e:
            print(f"Error processing data: {e}")
            error_message = "Data from buoy {} is more than 2 hours old or missing. Please select a different site.".format(alternative_town_1)
            error_label = tk.Label(frame1, text=error_message, font=("Helvetica", 16,), bg=tk_background_color)
            error_label.grid(row=1, column=0, padx=50, pady=(20,10))
            next_function = land_or_buoy
                       
        # Create the 'Next' button
        next_button = create_button(frame1, " Next ", button_font, next_function)
        next_button.grid(row=3, column=0, padx=(200, 0), pady=10, sticky="w")

    else:
        deny_text = f"Not able to find a buoy with that code. Please choose another site."
        deny_label = tk.Label(frame1, text=deny_text, font=("Helvetica", 16,), bg=tk_background_color)
        deny_label.grid(row=1, column=0, padx=50, pady=(20,10))
        next_function = land_or_buoy
        # Create the 'Next' button
        next_button = create_button(frame1, "Next", button_font, next_function)
        next_button.grid(row=3, column=0, padx=(50, 0), pady=10, sticky="w")    
                
def cobs_confirm_land():
    global town_entry, alternative_town_3, state_entry, alternative_state_3, result, cobs_site, cobs_obs_site, cobs_only_click_flag, random_sites_flag
    
    selected_value = cobs_selected_site.get()
        
    if selected_value == -1:
        # Reset the input variables to empty strings
        alternative_town_3 = ""
        alternative_state_3 = ""
        town_entry.delete(0, 'end')
        state_entry.delete(0, 'end')

    # Collect all child widgets of frame1 to avoid destroying frame1 itself
    all_widgets = []
    widgets_to_check = frame1.winfo_children()  # Start with children of frame1
    while widgets_to_check:
        widget = widgets_to_check.pop(0)
        all_widgets.append(widget)
        widgets_to_check.extend(widget.winfo_children())  # Add children of this widget

    # Destroy all collected widgets
    for widget in all_widgets:
        widget.destroy()

    # Reset clean position for frame1
    frame1.grid(row=0, column=0, sticky="nsew") 

    # Create and display the updated labels
    label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
    label1.grid(row=0, column=0, padx=50, pady=(50,0), sticky="w")

    instruction_text = f"{cobs_station_name}"
    instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,), bg=tk_background_color)
    instructions_label.grid(row=1, column=0, padx=50, pady=(20, 5), sticky='w')
    
    instruction_text = f"will be used for the third observation site."
    instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,), bg=tk_background_color)
    instructions_label.grid(row=2, column=0, padx=50, pady=(5, 10), sticky='w')
    
    # handle condition when user is here to just change the 3rd observation
    if cobs_only_click_flag == True:
        cobs_only_click_flag = False
        next_function = forget_frame1_and_show_scraped_and_transparent_frames
        
    else:
        next_function = page_choose
    
    # Create the 'Back' button
    back_button = create_button(frame1, " Back ", button_font, cobs_check_land)
    back_button.grid(row=4, column=0, padx=(50, 0), pady=10, sticky="w")
    
    # Create the 'Next' button
    next_button = create_button(frame1, " Next ", button_font, next_function)
    next_button.grid(row=4, column=0, padx=(200, 0), pady=10, sticky="w")     
                
def bobs_confirm_land():
    global town_entry, alternative_town_2, state_entry, alternative_state_2, result, bobs_selected_site, bobs_only_click_flag

    selected_value = bobs_selected_site.get()
    
    if selected_value == -1:
        # Reset the input variables to empty strings
        alternative_town_2 = ""
        alternative_state_2 = ""
        town_entry.delete(0, 'end')
        state_entry.delete(0, 'end')

    # Clear the current display
    for widget in frame1.winfo_children():
        if isinstance(widget, (tk.Checkbutton, tk.Label, tk.Button, tk.Entry, tk.Radiobutton)):
            widget.destroy()

    frame1.grid(row=0, column=0, sticky="nsew")

    # Create and display the updated labels
    label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
    label1.grid(row=0, column=0, padx=50, pady=10, sticky="w")

    instruction_text = f"{bobs_station_name}"
    instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,), bg=tk_background_color)
    instructions_label.grid(row=1, column=0, padx=50, pady=(50, 5), sticky='w')
    
    instruction_text = f"will be used for the second observation site."
    instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,), bg=tk_background_color)
    instructions_label.grid(row=2, column=0, padx=50, pady=(5, 10), sticky='w')
    
    # handle condition when user is here to just change the 2nd observation
    if bobs_only_click_flag == True:
        bobs_only_click_flag = False
        next_function = forget_frame1_and_show_scraped_and_transparent_frames
        
    else:
        next_function = cobs_input_land
    
    # Create the 'Back' button
    back_button = create_button(frame1, " Back ", button_font, bobs_check_land)
    back_button.grid(row=4, column=0, padx=(50, 0), pady=10, sticky="w")
    
    # Create the 'Next' button
    next_button = create_button(frame1, "Next", button_font, next_function)
    next_button.grid(row=4, column=0, padx=(200, 0), pady=10, sticky="w")       

def aobs_confirm_land():
    global town_entry, alternative_town_1, state_entry, alternative_state_1, result, aobs_station_name, aobs_selected_site, aobs_only_click_flag

    selected_value = aobs_selected_site.get()
    
    if selected_value == -1:
        #print("line 1244 code gets here. selected value equal to -1")
        
        # Reset the input variables to empty strings
        alternative_town_1 = ""
        alternative_state_1 = ""
        town_entry.delete(0, 'end')
        state_entry.delete(0, 'end')
        
        # A radio button has not been selected, proceed with the next function                    
        #aobs_input_land()
        
    # Clear the current display
    for widget in frame1.winfo_children():
        if isinstance(widget, (tk.Checkbutton, tk.Label, tk.Button, tk.Radiobutton)):
            widget.destroy()

    frame1.grid(row=0, column=0, sticky="nsew")

    # Create and display the updated labels
    label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
    label1.grid(row=0, column=0, padx=50, pady=50, sticky="w")

    instruction_text = f"{aobs_station_name} "
    instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,), bg=tk_background_color)
    instructions_label.grid(row=1, column=0, padx=50, pady=(20, 5), sticky='w')
    
    instruction_text = f"will be used for the first observation site."
    instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,), bg=tk_background_color)
    instructions_label.grid(row=2, column=0, padx=50, pady=(5, 10), sticky='w')

    # handle condition when user is here to just change the 1st observation
    if aobs_only_click_flag == True:
        aobs_only_click_flag = False
        next_function = forget_frame1_and_show_scraped_and_transparent_frames
        
    else:
        next_function = bobs_land_or_buoy
    
    # Create the 'Back' button
    back_button = create_button(frame1, " Back ", button_font, aobs_check_land)
    back_button.grid(row=4, column=0, padx=(50, 0), pady=10, sticky="w")
    
    # Create the 'Next' button
    next_button = create_button(frame1, " Next ", button_font, next_function)
    next_button.grid(row=4, column=0, padx=(200, 0), pady=10, sticky="w")            
    

def create_button(frame1, text, font, command_func):
    button = tk.Button(frame1, text=text, font=font, command=command_func)
    return button

def remove_checkbox():
    choice_check_button.destory()
    
    
def choose_lcl_radar():
    global box_variables

    if box_variables[2] == 0:
        lightning_center_input()

    # Clear the current display
    for widget in frame1.winfo_children():
        widget.destroy()

    # Reset clean position for frame1
    frame1.grid(row=0, column=0, sticky="nsew")

    # Check if the radar map website is available
    url = "https://weather.ral.ucar.edu/radar/"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("Website is down")
    except Exception as e:
        # Display the message and the Next button
        unavailable_message = "The map showing local radar stations is temporarily unavailable, so you can't make a local radar choice now. Please try again later."
        message_label = tk.Label(frame1, text=unavailable_message, font=("Arial", 16), justify='left', bg=tk_background_color, wraplength=500)
        message_label.grid(row=0, column=0, padx=50, pady=100, sticky='nw')

        box_variables[2] = 0

        next_button = tk.Button(frame1, text="Next", command=lightning_center_input, font=("Helvetica", 16, "bold"))
        next_button.grid(row=1, column=0, padx=50, pady=20, sticky="nw")

        return

    # Configure Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    # Use the system-installed ChromeDriver executable
    driver = webdriver.Chrome(service=Service("chromedriver"), options=chrome_options)

    # Maximize the browser window
    driver.maximize_window()

    # Navigate to the URL
    driver.get(url)

    # Wait for the radar map to be visible and ensure the page is fully loaded
    time.sleep(1)  # Give some time for the page to load
    map_element = driver.find_element(By.XPATH, "/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/form/table/tbody/tr[2]/td/img")

    # Scroll to ensure the map is fully visible
    driver.execute_script("arguments[0].scrollIntoView(true);", map_element)
    time.sleep(1)  # Wait for the scroll to finish

    # Capture a screenshot of the map
    map_screenshot = map_element.screenshot_as_png

    # Extract active links using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    active_links = soup.find('map', {'name': 'rad_imap'}).find_all('area')

    # Extract radar site code and coordinates from each link
    radar_sites = []
    for link in active_links:
        match = re.search(r"getRad\('(\w+)'\)", str(link))
        if match:
            lcl_radar_site_code = match.group(1)
            coordinates = tuple(map(int, re.findall(r"\d+", str(link['coords']))))
            radar_sites.append({"site_code": lcl_radar_site_code, "coordinates": coordinates})

    # Close the WebDriver
    driver.quit()

    # Display the screenshot using PIL
    map_screenshot_image = Image.open(BytesIO(map_screenshot))

    # Calculate the scale factor
    target_width, target_height = 800, 444
    scale_factor = target_width / map_screenshot_image.width

    # Resize the radar sites map
    map_screenshot_image = map_screenshot_image.resize((target_width, target_height), Image.LANCZOS)

    # Resize the radar site coordinates
    for site in radar_sites:
        site['coordinates'] = tuple(int(coord * scale_factor) for coord in site['coordinates'])

    # Function to draw radar site links on the label
    def lcl_radar_draw_links():
        for site in radar_sites:
            site_x, site_y, site_radius = site['coordinates']
            # label.create_oval(site_x - site_radius, site_y - site_radius, site_x + site_radius, site_y + site_radius, outline="red")

    # Function to capture mouse clicks on the map
    def lcl_radar_on_click(event):
        global closest_site, lcl_radar_site_code, radar_identifier, lcl_radar_zoom_clicks

        lcl_radar_zoom_clicks = tk.IntVar(value=0)  # re-establish variable when user changes maps

        # Get the mouse coordinates relative to the map image
        x, y = event.x, event.y

        # Find the radar site closest to the clicked coordinates
        closest_site = lcl_radar_find_closest_site(x, y)

        # Output the coordinates and radar site
        radar_identifier = closest_site['site_code']

        confirm_text = f"You chose\nradar site:\n{closest_site['site_code']}"
        confirm_label = tk.Label(frame1, text=confirm_text, font=("Arial", 16), justify='left', bg=tk_background_color)
        confirm_label.grid(row=0, column=0, padx=50, pady=210, sticky='nw')

        # while switched to ucar radar, don't display zoom option
        lcl_radar_zoom_text = f"Select the\nzoom"
        lcl_radar_zoom_label = tk.Label(frame1, text=lcl_radar_zoom_text, font=("Arial", 16), justify='left', bg=tk_background_color)
        lcl_radar_zoom_label.grid(row=0, column=0, padx=(50, 0), pady=(300, 0), sticky='nw')

        # Create and place the OptionMenu widget
        lcl_radar_choices = [0, 1, 2, 3, 4]
        lcl_radar_dropdown = tk.OptionMenu(frame1, lcl_radar_zoom_clicks, *lcl_radar_choices)
        lcl_radar_dropdown.grid(row=0, column=0, padx=(50, 0), pady=(350, 0), sticky="nw")

        # Create a submit button to process the user's input
        submit_button = tk.Button(frame1, text="Submit", command=confirm_radar_site, font=("Helvetica", 16, "bold"))
        submit_button.grid(row=0, column=0, padx=50, pady=(500, 0), sticky="nw")

    # Function to find the closest radar site to the clicked coordinates
    def lcl_radar_find_closest_site(x, y):
        min_distance = float('inf')
        closest_site = None

        for site in radar_sites:
            site_x, site_y, site_radius = site['coordinates']
            distance = ((x - site_x) ** 2 + (y - site_y) ** 2) ** 0.5 - site_radius
            if distance < min_distance:
                min_distance = distance
                closest_site = site

        return closest_site

    # Reset clean position for frame1
    root.grid_rowconfigure(0, weight=0)  # Reset to default which doesn't expand the row
    root.grid_columnconfigure(0, weight=0)  # Reset to default which doesn't expand the column
    frame1.grid_propagate(True)

    # Create a label to display the map with radar sites
    label = tk.Label(frame1, width=target_width, height=target_height)

    # Display the resized radar sites map on the label
    photo = ImageTk.PhotoImage(map_screenshot_image)
    label.configure(image=photo)
    label.image = photo  # Keep a reference to the image to prevent it from being garbage-collected

    # Set the grid placement for the map
    label.grid(row=0, column=0, sticky="nsew", padx=200, pady=70)

    # Draw radar site links on the label
    lcl_radar_draw_links()

    # Bind the click function to the label click event
    label.bind("<Button-1>", lcl_radar_on_click)

    # Create a label widget for the title
    label_text = "The Weather Observer"
    title_label = tk.Label(frame1, text=label_text, font=("Arial", 18, "bold"), bg=tk_background_color)
    title_label.grid(row=0, column=0, padx=50, pady=10, sticky='nw')

    # Corrected instruction text with original formatting
    instructions_text = "Please\nchoose the\nradar site you\nwish to\ndisplay"
    instructions_label = tk.Label(frame1, text=instructions_text, font=("Arial", 16), justify='left', bg=tk_background_color)
    instructions_label.grid(row=0, column=0, padx=50, pady=70, sticky='nw')

    # Create the 'Back' button
    back_button = tk.Button(frame1, text=" Back ", font=("Helvetica", 16, "bold"), command=page_choose)
    back_button.grid(row=0, column=0, padx=(50, 0), pady=(550,0), sticky="nw")


# begin block for radiosonde choice

def get_most_recent_gmt():
    global sonde_report_from_time, most_recent_sonde_time, sonde_letter_identifier, box_variables

    def check_url_exists(url):
        try:
            response = requests.head(url)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def format_time(gmtime_struct, hour):
        return time.strftime(f"%y%m%d{hour:02d}_OBS", gmtime_struct)

    current_time = time.gmtime()
    hour = current_time.tm_hour

    # Determine if we should start with 12Z or 00Z
    if hour >= 12:
        most_recent_hour = 12
    else:
        most_recent_hour = 0

    # Initialize the starting time
    adjusted_time = time.mktime((
        current_time.tm_year, current_time.tm_mon, current_time.tm_mday,
        most_recent_hour, 0, 0, current_time.tm_wday,
        current_time.tm_yday, current_time.tm_isdst
    ))

    while True:
        gmt_struct = time.gmtime(adjusted_time)
        most_recent_sonde_time = format_time(gmt_struct, most_recent_hour)
        url = f"https://www.spc.noaa.gov/exper/soundings/{most_recent_sonde_time}/"
        #print(f"Testing URL: {url}")  # Debug print
        if check_url_exists(url):
            break
        
        # Adjust time to the previous 12-hour period
        adjusted_time -= 12 * 3600
        if most_recent_hour == 12:
            most_recent_hour = 0
        else:
            most_recent_hour = 12

    match = re.search(r'(\d{2})_OBS$', most_recent_sonde_time)
    if match:
        sonde_report_from_time = match.group(1)
    else:
        print("Could not pull 2 digits out of most_recent_sonde_time.")
        
    return most_recent_sonde_time

def draw_radiosonde_links(active_links, scale_factor):
    global sonde_letter_identifier, box_variables
    for link in active_links:
        coords = link['coords'].split(',')
        if len(coords) == 3:
            x, y, radius = map(int, coords)
            x_scaled, y_scaled = int(x * scale_factor), int(y * scale_factor)
            radius = int(radius * 2)
            #label.create_oval(x_scaled - radius, y_scaled - radius, x_scaled + radius, y_scaled + radius, outline="red")

def handle_click(event, active_links, scale_factor, confirm_label, submit_button):
    global sonde_letter_identifier, match, confirm_text
    for link in active_links:
        coords = link['coords'].split(',')
        if len(coords) == 3:
            x, y, radius = map(int, coords)
            x_scaled, y_scaled = int(x * scale_factor), int(y * scale_factor)
            radius = int(radius * 2)
            distance = ((event.x - x_scaled) ** 2 + (event.y - y_scaled) ** 2) ** 0.5
            if distance <= radius:
                match = re.search(r'"([A-Z]{3})"', link['href'])
                if match:
                    sonde_letter_identifier = match.group(1)
                    confirm_text = f"You chose radiosonde site:\n{sonde_letter_identifier}"
                    confirm_label.config(text=confirm_text)
                    submit_button.config(state=tk.NORMAL)  # Enable submit button
                else:
                    print("No match found")

def choose_radiosonde_site():
        
    global box_variables, sonde_letter_identifier, most_recent_sonde_time, refresh_flag, has_submitted_choice
    
    sonde_letter_identifier = ""
    
    if box_variables[8] == 1:        
        
        for widget in frame1.winfo_children():
            widget.destroy()
        
#         # Clear the current display
#         for widget in frame1.winfo_children():
#             if isinstance(widget, (tk.Checkbutton, tk.Label, tk.Button, tk.Entry, tk.Radiobutton)):
#                 widget.destroy()
        
        # Reset clean position for frame1
        frame1.grid(row=0, column=0, sticky="nsew")
        #inserted 3/28/24
        # Before displaying the map, temporarily adjust the configuration
        frame1.master.grid_rowconfigure(0, weight=0)  # Reset to default which doesn't expand the row
        frame1.master.grid_columnconfigure(0, weight=0)  # Reset to default which doesn't expand the column 
        #frame1.grid_propagate(False)
        frame1.grid_propagate(True)
                
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        
        driver = webdriver.Chrome(service=Service("chromedriver"), options=chrome_options)
        
        # trying to change this line as an experiment 4/3/24 - problem 00z-1z
        url = "https://www.spc.noaa.gov/exper/soundings/{}/".format(get_most_recent_gmt())        
        #url = "https://www.spc.noaa.gov/exper/soundings/{}/".format(most_recent_sonde_time()) 
        
        driver.get(url)

        try:
            map_element = driver.find_element("xpath", "/html/body/table/tbody/tr/td[1]/center/img")
            valid_page_found = True
        except Exception as e:
            print(f"Line 2124. Error: {e}")
            current_time = time.gmtime(time.mktime(time.gmtime()) - 43200)  # Subtract 12 hours in seconds
            url = "https://www.spc.noaa.gov/exper/soundings/{}/".format(get_most_recent_gmt())
            print("Going back to the most recent URL because new sondes aren't out yet:", url)            
            driver.quit()

        map_image_url = map_element.get_attribute("src")
        map_response = requests.get(map_image_url, stream=True)
        original_map_image = Image.open(BytesIO(map_response.content))

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        active_links = soup.find('map', {'name': 'stations'}).find_all('area')

        target_width, target_height = 600, 450
        scale_factor = target_width / original_map_image.width
        enlarged_map_image = original_map_image.resize((target_width, target_height), Image.LANCZOS)

        label = tk.Label(frame1)
        label.grid(row=0, column=1, padx=0, pady=85)

        enlarged_map_photo = ImageTk.PhotoImage(enlarged_map_image)
        label.configure(image=enlarged_map_photo)
        label.image = enlarged_map_photo

        draw_radiosonde_links(active_links, scale_factor)

        overlay_label = tk.Label(frame1, text="Sounding Stations", font=("Arial", 18, "bold"), bg="white", fg="black")
        overlay_label.grid(row=0, column=1, pady=(400,0))

        match = re.search(r'<span class="style5">Observed Radiosonde Data<br>\s*([^<]+)\s*</span>', driver.page_source)
        if match:
            date_str = match.group(1)
            overlay_label["text"] += f" {date_str}"
        
        #frame1.grid(row=0, column=0, sticky="nw") 
        
        label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), justify="left", bg=tk_background_color)
        label1.grid(row=0, column=0, padx=50, pady=10, sticky="nw") 

        instruction_text = f"These are the\nradiosonde sites that are\navailable as of {sonde_report_from_time} GMT."
        instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,), justify='left', bg=tk_background_color)
        instructions_label.grid(row=0, column=0, padx=50, pady=(60, 10), sticky='nw')

        instruction_text = "Click on the location\nof a station,\nthen click submit."
        instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,), justify='left', bg=tk_background_color)
        instructions_label.grid(row=0, column=0, padx=50, pady=(150, 10), sticky='nw')

        confirm_text = f"You chose radiosonde site:\n{sonde_letter_identifier}"
        confirm_label = tk.Label(frame1, text=confirm_text, font=("Arial", 16), justify='left', bg=tk_background_color)
        confirm_label.grid(row=0, column=0, padx=50, pady=250, sticky='nw')

        if box_variables[5] == 1:
            #refresh_flag = True # this allows back button on choose_radiosonde_site to go back to choose_reg_sat, but prevents program from displaying
            # need to toggle refresh_flag back to False at some point
            has_submitted_choice = False
            back_function = choose_reg_sat
            
        elif box_variables[3] == 1:
            back_function = lightning_center_input
            
        elif box_variables[2] == 1:
            back_function = choose_lcl_radar
            
        else:
            back_function = page_choose

        # Create the 'Back' button
        back_button = tk.Button(frame1, text=" Back ", font=("Helvetica", 16, "bold"), command=back_function)
        back_button.grid(row=0, column=0, padx=(50, 0), pady=(400,0), sticky="nw")

        submit_button = tk.Button(frame1, text="Submit", command=station_center_input, font=("Helvetica", 16, "bold"), state=tk.DISABLED)
        submit_button.grid(row=0, column=0, padx=50, pady=(350,0), sticky="nw")            

        label.bind("<Button-1>", lambda event: handle_click(event, active_links, scale_factor, confirm_label, submit_button))
        
    else:
        station_center_input()
    
def choose_reg_sat():
    global reg_sat_choice_variables, box_variables, reg_sat, has_submitted_choice, refresh_flag
    
    reg_sat_choice_variable = tk.IntVar(value=-1)  # Single IntVar for all radio buttons
    reg_sat_choice_variables = [0] * 12  # Ensure this is initialized correctly
    
    if refresh_flag == True:
        has_submitted_choice = False
        
    if box_variables[5] != 1:
        choose_radiosonde_site()

    elif not has_submitted_choice:
        frame1.grid(row=0, column=0, sticky="nsew")
        for widget in frame1.winfo_children():
            if isinstance(widget, (tk.Checkbutton, tk.Label, tk.Button, tk.Entry, tk.Radiobutton)):
                widget.destroy()

        reg_sat_label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
        reg_sat_label1.grid(row=0, column=0, padx=50, pady=(50,10), sticky="w")

        instruction_text = "Please select your regional satellite view:"
        instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 14, "bold"), bg=tk_background_color)
        instructions_label.grid(row=1, column=0, padx=50, pady=(0, 25), sticky='w') 

        choices = ['Pacific NW', 'Pacific SW', 'Northern Rockies', 'Southern Rockies', 'Upper Miss. Valley',
                   'Southern Miss. Valley', 'Great Lakes', 'Southern Plains', 'Northeast', 'Southeast',
                   'US Pacific Coast', 'US Atlantic Coast']

        column1_frame = tk.Frame(frame1, bg=tk_background_color)
        column2_frame = tk.Frame(frame1, bg=tk_background_color)
        column3_frame = tk.Frame(frame1, bg=tk_background_color)

        column1_frame.grid(row=2, column=0, padx=(50, 0), sticky='w')
        column2_frame.grid(row=2, column=0, padx=(310, 0), sticky='w')
        column3_frame.grid(row=2, column=0, padx=(610, 0), pady=(20, 20), sticky='w')

        def update_sat_radio_buttons():
            # Enable submit button if any radio button is selected
            submit_button['state'] = tk.NORMAL if reg_sat_choice_variable.get() != -1 else tk.DISABLED

        for index, choice in enumerate(choices):
            choice_radio_button = tk.Radiobutton(
                column1_frame if index < 4 else column2_frame if index < 8 else column3_frame,
                text=choice, variable=reg_sat_choice_variable, value=index,
                font=("Arial", 14, "bold"),
                bg=tk_background_color,
                command=update_sat_radio_buttons,
                highlightthickness=0,  # Remove the wireframe
                borderwidth=0          # Remove the border
            )
            choice_radio_button.grid(row=index % 4, column=0, padx=10, pady=(5, 55), sticky='w')

        def submit_sat_choice():
            global reg_sat_choice_variables, has_submitted_choice
            selected_index = reg_sat_choice_variable.get()
            if selected_index != -1:
                reg_sat_choice_variables = [1 if i == selected_index else 0 for i in range(12)]
                has_submitted_choice = True
                # Clear the current display
                for widget in frame1.winfo_children():
                    widget.destroy()
                frame1.grid(row=0, column=0, sticky="nsew")
                frame1.config(width=1024, height=600)
                column1_frame.destroy()
                column2_frame.destroy()
                column3_frame.destroy()
                if box_variables[8] == 1:                
                    choose_radiosonde_site()                        
                else:
                    station_center_input()

        if box_variables[3] == 1:
            back_function = lightning_center_input
            
        elif box_variables[2] == 1:
            back_function = choose_lcl_radar
            
        else:
            back_function = page_choose

        # Create the 'Back' button
        back_button = tk.Button(frame1, text=" Back ", font=("Arial", 16, "bold"), command=back_function)
        back_button.grid(row=3, column=0, padx=(600,0), pady=0, sticky="s")

        submit_button = tk.Button(frame1, text="Submit", command=submit_sat_choice, font=("Arial", 16, "bold"), state=tk.DISABLED)
        submit_button.grid(row=3, column=3, padx=0, pady=0, sticky='s')  # Check padding here to match original specifications


def submit_choices():
    global box_variables, hold_box_variables
    box_variables = [var.get() for var in page_choose_choice_vars]
    hold_box_variables = []

    # Set each hold_box_variable individually
    for value in box_variables:
        hold_box_variables.append(value)

    # Apply conditional changes to box_variables
    for index, value in enumerate(box_variables):
        if value == 1:
            box_variables[index] = 2 if index in {10, 11} else 1

#     # Loop through each value in hold_box_variables and print it inside submit_choices
#     for index, value in enumerate(hold_box_variables):
#         print(f"submit_choices: hold_box_variables[{index}] = {value}")

    # Clear the current display and choose the next action based on choices
    for widget in frame1.winfo_children():
        widget.destroy()

    if box_variables[2] == 1:
        choose_lcl_radar()  
    else:
        lightning_center_input()  


def page_choose():
    global page_choose_choice_vars, hold_box_variables, xs  # Declare these global to modify
    global random_sites_flag
    # Clear the current display
    for widget in frame1.winfo_children():
        widget.destroy()
    
    frame1.grid(row=0, column=0, sticky="nsew")
    frame1.master.grid_rowconfigure(0, weight=1)
    frame1.master.grid_columnconfigure(0, weight=1)
    frame1.config(width=1024, height=600)
    
    label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 22, "bold"), bg=tk_background_color, justify="left")
    label1.grid(row=0, column=0, columnspan=3, padx=50, pady=(50,10), sticky="w")
    
    instructions_label = tk.Label(frame1, text="Please select your display choices:", font=("Helvetica", 20), bg=tk_background_color)
    instructions_label.grid(row=1, column=0, columnspan=3, padx=50, pady=(0, 15), sticky='w')
    
    # Initialize the global variable for this page's choice variables
    page_choose_choice_vars = []

    choices = ['Barograph', 'National Radar', 'Local Radar', 'Lightning', 'GOES16 East Satellite',
               'Regional Satellite', 'National Surface Analysis', 'Local Station Plots', 'Radiosonde', '500mb Vorticity',
               'Next Idea', 'Next Idea']

    # Create a custom style for the check buttons with the learned attributes
    custom_style = ttk.Style()
    custom_style.configure("Custom.TCheckbutton", font=("Arial", 14, "bold"))  # Set the font properties
    custom_style.map("Custom.TCheckbutton",
                     background=[("disabled", "lightblue"), ("!disabled", "lightblue")],
                     foreground=[("disabled", "gray"), ("!disabled", "black")])
    
    column_frames = [tk.Frame(frame1, bg=tk_background_color) for _ in range(3)]
    for i, col_frame in enumerate(column_frames):
        col_frame.grid(row=2, column=i, padx=(50, 20), pady=10, sticky='nw')
        frame1.grid_columnconfigure(i, weight=1)
        
    for index, choice in enumerate(choices):
        var = tk.IntVar()
        page_choose_choice_vars.append(var)
        col_index = index // 4
        check_button = ttk.Checkbutton(column_frames[col_index], text=choice, variable=var, style="Custom.TCheckbutton")
        check_button.grid(row=index % 4, column=0, padx=10, pady=30, sticky='w')

        # Set the checkbox based on hold_box_variables if available, handle special cases
        if index == 0:
            var.set(1)
            check_button.state(["disabled"])
        elif index >= 10:
            var.set(0)
            check_button.state(["disabled"])
        else:
            if hold_box_variables and index < len(hold_box_variables):
                var.set(hold_box_variables[index])

    if random_sites_flag:
        next_function = confirm_random_sites
    else:
        next_function = cobs_confirm_land
    
    if len(xs) == 0: # only show this back button for set up, not during operation       
        back_button = tk.Button(frame1, text=" Back ", font=("Arial", 16, "bold"), command=next_function)
        back_button.grid(row=4, column=2, padx=(30,0), pady=(15, 10), sticky="s")

    submit_button = tk.Button(frame1, text="Submit", command=submit_choices, font=("Arial", 16, "bold"), bg="light gray", foreground="black")
    submit_button.grid(row=4, column=3, padx=0, pady=(15, 10), sticky='s')

def submit_lightning_center():
    global submit_lightning_town, submit_lightning_state, lightning_town, lightning_state, lightning_lat, lightning_lon 

    # Get the user's input
    submit_lightning_town = lightning_town.get()
    submit_lightning_state = lightning_state.get()

    # Clear the current display
    for widget in frame1.winfo_children():
        if isinstance(widget, (tk.Checkbutton, tk.Label, tk.Button, tk.Entry)):
            widget.destroy()

    if 'keyboard_window' in globals() and keyboard_window.winfo_exists():
        keyboard_window.destroy()

    lightning_geolocator = Nominatim(user_agent="lightning_map")
        
    # Combine town and state into a search query
    lightning_query = f"{submit_lightning_town}, {submit_lightning_state}"

    # Use geocoder to get coordinates of lightning map center
    lightning_location = lightning_geolocator.geocode(lightning_query)

    if lightning_location:
        lightning_lat = lightning_location.latitude
        lightning_lon = lightning_location.longitude
        choose_reg_sat()
        #break
    else:
        # Clear the current display
        for widget in frame1.winfo_children():
            if isinstance(widget, (tk.Checkbutton, tk.Label, tk.Button, tk.Entry)):
                widget.destroy()
                
        instruction_text = "Not able to use that location as center."
        instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,), bg=tk_background_color)
        instructions_label.grid(row=1, column=0, padx=50, pady=(20, 10))
        
        # Create the 'Next' button
        next_button = create_button(frame1, "Next", button_font, lightning_center_input)
        next_button.grid(row=3, column=0, padx=(90, 0), pady=10, sticky="w")  
              
def lightning_center_input():
    global box_variables, lightning_town, lightning_state

    if box_variables[3] == 1:
        # Clear the current display
        for widget in frame1.winfo_children():
            widget.destroy()

        frame1.grid(row=0, column=0, sticky="nsew")
        frame1.grid_propagate(False)
        
        # Create and display the updated labels
        label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
        label1.grid(row=0, column=0, columnspan=20, padx=50, pady=(50,0), sticky="nw")

        instruction_text = "Please enter the name of the town for the center of the lightning map:"
        instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16), bg=tk_background_color, justify="left")
        instructions_label.grid(row=1, column=0, columnspan=20, padx=50, pady=5, sticky='nw')

        lightning_town = tk.Entry(frame1, font=("Helvetica", 14))
        lightning_town.grid(row=2, column=0, columnspan=20, padx=50, pady=5, sticky='nw')
        lightning_town.focus_set()  # Set focus to the first entry widget
        
        state_instruction_text = "Please enter the 2-letter state ID for the center of the lightning map:"
        state_instructions_label = tk.Label(frame1, text=state_instruction_text, font=("Helvetica", 16), bg=tk_background_color, justify="left")
        state_instructions_label.grid(row=3, column=0, columnspan=20, padx=50, pady=5, sticky='nw')

        lightning_state = tk.Entry(frame1, font=("Helvetica", 14))
        lightning_state.grid(row=4, column=0, columnspan=20, padx=50, pady=5, sticky='nw')

        lightning_town.bind("<FocusIn>", lambda e: set_current_target(lightning_town))
        lightning_state.bind("<FocusIn>", lambda e: set_current_target(lightning_state))

        if box_variables[2] == 1:
            back_function = choose_lcl_radar
            
        else:
            back_function = page_choose

        # Create the 'Back' button
        back_button = tk.Button(frame1, text=" Back ", font=("Helvetica", 16, "bold"), command=back_function)
        back_button.grid(row=5, column=0, columnspan=20, padx=(50, 0), pady=5, sticky="nw")

        submit_button = tk.Button(frame1, text="Submit", command=submit_lightning_center, font=("Helvetica", 16, "bold"))
        submit_button.grid(row=5, column=0, columnspan=20, padx=200, pady=5, sticky='nw')

        # Spacer to ensure layout consistency
        spacer = tk.Label(frame1, text="", bg=tk_background_color)
        spacer.grid(row=6, column=0, columnspan=20, sticky="nsew", pady=(0, 50))  # Adjust this to fit the layout
        
        # Display the virtual keyboard, assuming row 7 is correctly positioned below the submit button and spacer
        create_virtual_keyboard(frame1, 7)
           
    else:
        
        choose_reg_sat()

import tkinter as tk
from tkinter import ttk

def station_center_input():
    global box_variables, refresh_flag, station_plot_town, station_plot_state, zoom_plot, random_sites_flag
    random_sites_flag = False
    zoom_plot = None
    if box_variables[7] == 1:

        # Clear the current display
        for widget in frame1.winfo_children():
            widget.destroy()

        frame1.grid(row=0, column=0, sticky="nsew")
        frame1.grid_propagate(False)  # another line later in this function 2533

        zoom_plot = tk.StringVar(value="9")

        def submit_station_plot_center():
            global submit_station_plot_town, submit_station_plot_state, station_plot_town, station_plot_state, station_plot_lat, station_plot_lon, zoom_plot
            global refresh_flag

            try:
                station_plot_geolocator = Nominatim(user_agent="station_plot_map")

                # Get the user's input
                submit_station_plot_town = station_plot_town.get()
                submit_station_plot_state = station_plot_state.get()

                # Retrieve user's zoom choice
                zoom_plot = zoom_plot.get()

                # Combine town and state into a search query
                station_plot_query = f"{submit_station_plot_town}, {submit_station_plot_state}"

                # Use geocoder to get coordinates of lightning map center
                station_plot_location = station_plot_geolocator.geocode(station_plot_query)

                if station_plot_location:
                    station_plot_lat = station_plot_location.latitude
                    station_plot_lon = station_plot_location.longitude

                    if len(xs) == 0:
                        frame1.grid_forget()
                        start_animation()
                    else:
                        frame1.grid_forget()
                        refresh_flag = False
                        show_transparent_frame()
                        
                        scraped_frame.grid(row=0, column=0, sticky="nsew")
                        check_widgets_and_show_frame(scraped_frame, transparent_frame, [transparent_frame, scraped_to_frame1, maps_only_button, pic_email_button, reboot_button], timeout=30000, interval=500)
                else:
                    # Clear the current display
                    for widget in frame1.winfo_children():
                        if isinstance(widget, (tk.Checkbutton, tk.Label, tk.Button, tk.Entry, tk.Radiobutton)):
                            widget.destroy()

                    instruction_text = "Not able to use that location as center."
                    instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16), bg=tk_background_color)
                    instructions_label.grid(row=1, column=0, padx=50, pady=(20, 10))

                    # Create the 'Next' button
                    next_button = create_button(frame1, "Next", button_font, station_center_input)
                    next_button.grid(row=3, column=0, padx=(90, 0), pady=10, sticky="w")

                    station_center_input()

            except Exception as e:
                # Clear the current display
                for widget in frame1.winfo_children():
                    if isinstance(widget, (tk.Checkbutton, tk.Label, tk.Button, tk.Entry, tk.Radiobutton)):
                        widget.destroy()

                # Create and display the updated labels
                label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
                label1.grid(row=0, column=0, padx=50, pady=5, sticky="w")

                #print("line 3747. problem with choosing that town. Choose another.")
                instruction_text = "Not able to use that location as center."
                instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16), bg=tk_background_color)
                instructions_label.grid(row=1, column=0, padx=50, pady=(20, 10))

                # Create the 'Next' button
                next_button = create_button(frame1, "Next", button_font, station_center_input)
                next_button.grid(row=3, column=0, padx=(90, 0), pady=10, sticky="w")

        label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
        label1.grid(row=0, column=0, columnspan=20, padx=50, pady=(50, 0), sticky="nw")

        instructions_label = tk.Label(frame1, text="Please enter the name of the town for the center of the station plot map:", font=("Helvetica", 16), bg=tk_background_color)
        instructions_label.grid(row=1, column=0, columnspan=20, padx=50, pady=5, sticky='nw')

        station_plot_town = tk.Entry(frame1, font=("Helvetica", 14))
        station_plot_town.grid(row=2, column=0, columnspan=20, padx=50, pady=5, sticky='nw')
        station_plot_town.focus_set()

        state_instructions_label = tk.Label(frame1, text="Please enter the 2-letter state ID for the center of the station plot map:", font=("Helvetica", 16), bg=tk_background_color)
        state_instructions_label.grid(row=3, column=0, columnspan=20, padx=50, pady=5, sticky='nw')

        station_plot_state = tk.Entry(frame1, font=("Helvetica", 14))
        station_plot_state.grid(row=4, column=0, columnspan=20, padx=50, pady=(5, 25), sticky='nw')

        station_plot_town.bind("<FocusIn>", lambda e: set_current_target(station_plot_town))
        station_plot_state.bind("<FocusIn>", lambda e: set_current_target(station_plot_state))

        # Manually set the grid placement for each radio button
        radio_buttons_info = [
            ("Few small\ncounties", "10"),
            ("Several\ncounties", "9"),
            ("States", "6"),
            ("Continents", "4"),
            ("Almost a\nhemisphere", "3")
        ]

        # Button 1
        radio_button1 = tk.Radiobutton(frame1, text=radio_buttons_info[0][0], variable=zoom_plot, value=radio_buttons_info[0][1],
                                       font=("Helvetica", 11), bg=tk_background_color, bd=0, highlightthickness=0, justify="left")
        radio_button1.grid(row=6, column=0, columnspan=2, sticky="w", padx=(30, 0))

        # Button 2
        radio_button2 = tk.Radiobutton(frame1, text=radio_buttons_info[1][0], variable=zoom_plot, value=radio_buttons_info[1][1],
                                       font=("Helvetica", 11), bg=tk_background_color, bd=0, highlightthickness=0, justify="left")
        radio_button2.grid(row=6, column=2, columnspan=2, sticky="w", padx=(0, 0))

        # Button 3
        radio_button3 = tk.Radiobutton(frame1, text=radio_buttons_info[2][0], variable=zoom_plot, value=radio_buttons_info[2][1],
                                       font=("Helvetica", 11), bg=tk_background_color, bd=0, highlightthickness=0, justify="left")
        radio_button3.grid(row=6, column=4, columnspan=3, sticky="w", padx=(0, 0))

        # Button 4
        radio_button4 = tk.Radiobutton(frame1, text=radio_buttons_info[3][0], variable=zoom_plot, value=radio_buttons_info[3][1],
                                       font=("Helvetica", 11), bg=tk_background_color, bd=0, highlightthickness=0, justify="left")
        radio_button4.grid(row=6, column=6, columnspan=3, sticky="w", padx=(0, 10))

        # Button 5
        radio_button5 = tk.Radiobutton(frame1, text=radio_buttons_info[4][0], variable=zoom_plot, value=radio_buttons_info[4][1],
                                       font=("Helvetica", 11), bg=tk_background_color, bd=0, highlightthickness=0, justify="left")
        radio_button5.grid(row=6, column=8, columnspan=3, sticky="w", padx=(10, 20))

        if box_variables[8] == 1:
            back_function = choose_radiosonde_site
        
        elif box_variables[5] == 1:
            #refresh_flag = True # when commented out, still can click back button from station plots to get radiosonde site
            back_function = choose_reg_sat
            
        elif box_variables[3] == 1:
            back_function = lightning_center_input
            
        elif box_variables[2] == 1:
            back_function = choose_lcl_radar
            
        else:
            back_function = page_choose
        
        # Create the 'Back' button
        back_button = tk.Button(frame1, text=" Back ", font=("Helvetica", 16, "bold"), command=back_function)
        back_button.grid(row=7, column=0, columnspan=20, padx=(50, 0), pady=15, sticky="nw")

        submit_button = tk.Button(frame1, text="Submit", command=submit_station_plot_center, font=("Helvetica", 16, "bold"))
        submit_button.grid(row=7, column=0, columnspan=20, padx=200, pady=15, sticky='nw')

        # Spacer to push the keyboard to the bottom
        # vertical_spacer = tk.Label(frame1, text="", bg=tk_background_color)
        # vertical_spacer.grid(row=8, column=0, sticky="nsew", pady=(0, 0))  # Adjust row and pady as necessary

        frame1.grid_propagate(False)  # prevent keyboard from skipping at refresh?

        # Display the virtual keyboard, ensuring it appears below all widgets
        create_virtual_keyboard(frame1, 8)  # Adjust the row based on your layout needs

    else:
        if len(xs) == 0:
            frame1.grid_forget()
            start_animation()
        else:
            frame1.grid_forget()
            refresh_flag = False
            show_transparent_frame()

            scraped_frame.grid(row=0, column=0, sticky="nsew")
            # Assuming the buttons are created somewhere else in the code
            
# Code isn't set up to ever come here because we're not offering buoy obs with cobs yet.
def cobs_land_or_buoy():
    global cobs_only_click_flag
    # Clear the current display
    for widget in frame1.winfo_children():
        if isinstance(widget, (tk.Checkbutton, tk.Label, tk.Button, tk.Radiobutton)):
            widget.destroy()
    
    frame1.grid(row=0, column=0, sticky="nsew")
    
    # Create and display the updated labels
    label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
    label1.grid(row=0, column=0, padx=50, pady=(50,0), sticky="w")
    
    instruction_text = "Do you want the third observation site to be on land or a buoy?"
    instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,), bg=tk_background_color)
    instructions_label.grid(row=1, column=0, padx=50, pady=10)
    
    if cobs_only_click_flag == False:
        # Create the 'Back' button
        back_button = create_button(frame1, " Back ", button_font, bobs_confirm_land)
        back_button.grid(row=2, column=0, padx=(50, 0), pady=30, sticky="w")
    
    # Create "Land" button
    land_button = create_button(frame1, " Land ", button_font, cobs_input_land)
    land_button.grid(row=2, column=0, padx=200, pady=30, sticky="w")

    # Create "Buoy" button
    buoy_button = create_button(frame1, " Buoy ", button_font, cobs_input_buoy)
    buoy_button.grid(row=2, column=0, padx=350, pady=30, sticky="w")
    
def bobs_land_or_buoy():
    global bobs_only_click_flag
    # Clear the current display
    for widget in frame1.winfo_children():
        if isinstance(widget, (tk.Checkbutton, tk.Label, tk.Button, tk.Radiobutton)):
            widget.destroy()
    
    frame1.grid(row=0, column=0, sticky="nsew")
    
    # Create and display the updated labels
    label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
    label1.grid(row=0, column=0, padx=50, pady=(50,0), sticky="w")
    
    instruction_text = "Do you want the second observation site to be on land or a buoy?"
    instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,), bg=tk_background_color)
    instructions_label.grid(row=1, column=0, padx=50, pady=10, sticky="w")
    
    if bobs_only_click_flag == False:
        # Create the 'Back' button
        back_button = create_button(frame1, " Back ", button_font, aobs_confirm_land)
        back_button.grid(row=2, column=0, padx=(50, 0), pady=30, sticky="w")
    
    # Create "Land" button
    land_button = create_button(frame1, " Land ", button_font, bobs_input_land)
    land_button.grid(row=2, column=0, padx=200, pady=30, sticky="w")

    # Create "Buoy" button
    buoy_button = create_button(frame1, " Buoy ", button_font, bobs_input_buoy)
    buoy_button.grid(row=2, column=0, padx=350, pady=30, sticky="w")
        
def land_or_buoy():
    global aobs_only_click_flag
    # Clear the current display
    for widget in frame1.winfo_children():
        if isinstance(widget, (tk.Checkbutton, tk.Label, tk.Button, tk.Radiobutton, tk.Entry)):
            widget.destroy()

    frame1.grid(row=0, column=0, sticky="nsew")

    # Create and display the updated labels
    label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
    label1.grid(row=0, column=0, padx=50, pady=(50,0), sticky="w")
    
    instruction_text = f"Do you want the first observation site to be on land or a buoy?\n\nOr\n\nYou can have 3 random sites chosen for you."
    instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,), bg=tk_background_color, anchor='w', justify='left')
    instructions_label.grid(row=1, column=0, padx=50, pady=10, sticky='w')
    
    if aobs_only_click_flag == False:        
        # Create the 'Back' button
        back_button = create_button(frame1, " Back ", button_font, confirm_calibration_site)
        back_button.grid(row=2, column=0, padx=(50, 0), pady=30, sticky="w")
    
    # Create "Land" button
    land_button = create_button(frame1, " Land ", button_font, aobs_input_land)
    land_button.grid(row=2, column=0, padx=(200,0), pady=30, sticky="w")

    # Create "Buoy" button
    buoy_button = create_button(frame1, " Buoy ", button_font, aobs_input_buoy)
    buoy_button.grid(row=2, column=0, padx=(350,0), pady=30, sticky="w")
    
    # Create "Random" button
    random_button = create_button(frame1, "Random", button_font, generate_random_sites)
    random_button.grid(row=2, column=0, padx=(500,0), pady=30, sticky="w")

def confirm_radar_site():
    
    global radar_identifier, lcl_radar_zoom_clicks

    lcl_radar_zoom_clicks = lcl_radar_zoom_clicks.get()
    
    # Clear the current display
    for widget in frame1.winfo_children():
        widget.destroy()
        
    lightning_center_input()

def confirm_calibration_site():
    global submit_calibration_town, show_baro_input, baro_input
    
    # Clear the current display
    for widget in frame1.winfo_children():
        widget.destroy()

    frame1.grid(row=0, column=0, sticky="nesw")
    
    # Create and display the updated labels
    label1 = tk.Label(frame1, text="The Weather Observer\n", font=("Arial", 18, "bold"), bg=tk_background_color)
    label1.grid(row=0, column=0, padx=50, pady=(50, 0), sticky="w")
    
    updated_text = f"{aobs_site}"
    label2 = tk.Label(frame1, text=updated_text, font=("Arial", 16), bg=tk_background_color)
    label2.grid(row=1, column=0, padx=(50,0), pady=(0, 10), sticky='w')
    
    updated_text = f"will be used as the calibration site."
    label2 = tk.Label(frame1, text=updated_text, font=("Arial", 16), bg=tk_background_color)
    label2.grid(row=2, column=0, padx=(50,0), pady=(20, 30), sticky='w') 
    
    # Create the 'Next' button
    next_button = create_button(frame1, "Next", button_font, land_or_buoy)
    next_button.grid(row=3, column=0, padx=(200, 0), pady=5, sticky="w")
    
    # Create the 'Back' button
    back_button = create_button(frame1, "Back", button_font, welcome_screen)
    back_button.grid(row=3, column=0, padx=(50, 0), pady=5, sticky="w")
    
def pascals_to_inches_hg(pascals):
    """Converts pressure in Pascals to inches of mercury."""
    return pascals / 3386.389

def submit_calibration_input():
    global submit_calibration_town, submit_calibration_state, calibration_town, calibration_state, calibration_lat, calibration_lon, aobs_site
    global show_baro_input, baro_input
    
    submit_calibration_town = calibration_town.get()
    submit_calibration_state = calibration_state.get()

    submit_calibration_town = submit_calibration_town.title()
    submit_calibration_state = submit_calibration_state.upper()

    aobs_site = submit_calibration_town + ", " + submit_calibration_state

    for widget in frame1.winfo_children():
        widget.destroy()

    label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
    label1.grid(row=0, column=0, padx=50, pady=(50,10), sticky="w")

    geolocator = Nominatim(user_agent="geocoder_app")
    location = geolocator.geocode(f"{submit_calibration_town}, {submit_calibration_state}", country_codes="us")
    if location is not None:
        calibration_lat = location.latitude
        calibration_lon = location.longitude

        response = requests.get(f'https://api.weather.gov/points/{calibration_lat},{calibration_lon}')
        if response.status_code == 200:
            data = response.json()
            stations_url = data['properties']['observationStations']
            stations_response = requests.get(stations_url)
            if stations_response.status_code == 200:
                stations_data = stations_response.json()

                for station_url in stations_data['observationStations']:
                    obs_response = requests.get(f"{station_url}/observations/latest")
                    if obs_response.status_code == 200:
                        obs_data = obs_response.json()
                        if 'barometricPressure' in obs_data['properties'] and obs_data['properties']['barometricPressure']['value'] is not None:
                            baro_input = pascals_to_inches_hg(obs_data['properties']['barometricPressure']['value'])
                            show_baro_input = f'{baro_input:.2f}'
                            #aobs_site = submit_calibration_town.title()
                            instruction_text = f"The barometric pressure at {aobs_site} is {show_baro_input} inches.\nDo you want to keep this as the calibration site,\nchange the site again or,\nenter your own barometric presure?"
                            display_calibration_results(instruction_text)
                            return

        display_calibration_error("No usable barometric pressure reading was found.")
    else:
        display_calibration_error("Could not match that location with a barometric pressure reading.")

def display_calibration_results(instruction_text):
    """Displays the calibration results on the GUI."""
    instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16), bg=tk_background_color, justify="left")
    instructions_label.grid(row=1, column=0, padx=(50,0), pady=(10, 20), sticky="w")

    # Create the 'Back' button
    back_button = tk.Button(frame1, text=" Back ", font=button_font, command=change_calibration_site)
    back_button.grid(row=2, column=0, padx=(50, 0), pady=20, sticky="w")
    
    keep_button = tk.Button(frame1, text=" Keep ", font=button_font, command=confirm_calibration_site)
    keep_button.grid(row=2, column=0, padx=(200,0), pady=20, sticky="w")
    change_button = tk.Button(frame1, text="Change", font=button_font, command=change_calibration_site)
    change_button.grid(row=2, column=0, padx=(350,0), pady=20, sticky="w")
    enter_own_button = tk.Button(frame1, text=" Own ", font=button_font, command=own_calibration_site)
    enter_own_button.grid(row=2, column=0, padx=(500,0), pady=20, sticky="w")

def display_calibration_error(message):
    """Displays an error message on the GUI."""
    instructions_label = tk.Label(frame1, text=message, font=("Helvetica", 16), bg=tk_background_color)
    instructions_label.grid(row=1, column=0, padx=(50,0), pady=(20, 10))
    change_button = tk.Button(frame1, text="Change", font=button_font, command=change_calibration_site)
    change_button.grid(row=2, column=0, padx=(50,0), pady=5, sticky="w")
        
        
def change_calibration_site():
    global calibration_town, calibration_state, current_target_entry

    # Clear the current display
    for widget in frame1.winfo_children():
        widget.destroy()

    frame1.grid(row=0, column=0, sticky="nsew")
    frame1.grid_propagate(False)

    label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
    label1.grid(row=0, column=0, columnspan=20, padx=50, pady=(50,5), sticky="nw")
    
    instructions_label = tk.Label(frame1, text="Please enter the name of the town to be used for calibration:", font=("Helvetica", 16), bg=tk_background_color, justify="left")
    instructions_label.grid(row=1, column=0, columnspan=20, padx=(50,0), pady=5, sticky='nw')
    
    calibration_town = tk.Entry(frame1, font=("Helvetica", 14), justify="left")
    calibration_town.grid(row=2, column=0, columnspan=20, padx=(50,0), pady=5, sticky='nw')
    calibration_town.bind("<FocusIn>", lambda e: set_current_target(calibration_town))
    calibration_town.focus_set()
        
    state_instructions_label = tk.Label(frame1, text="Please enter the 2-letter state ID for the calibration site:", font=("Helvetica", 16), bg=tk_background_color, justify="left")
    state_instructions_label.grid(row=3, column=0, columnspan=20, padx=(50,0), pady=5, sticky='nw')
    
    calibration_state = tk.Entry(frame1, font=("Helvetica", 14))
    calibration_state.grid(row=4, column=0, columnspan=20, padx=(50,0), pady=5, sticky='nw')
    calibration_state.bind("<FocusIn>", lambda e: set_current_target(calibration_state))

    # Create the 'Back' button
    back_button = tk.Button(frame1, text=" Back ", font=("Helvetica", 16, "bold"), command=welcome_screen)
    back_button.grid(row=5, column=0, columnspan=20, padx=(50, 0), pady=5, sticky="nw")

    submit_button = tk.Button(frame1, text="Submit", command=submit_calibration_input, font=("Helvetica", 16, "bold"))
    submit_button.grid(row=5, column=0, columnspan=20, padx=(200,0), pady=5, sticky='nw')
    
    # Spacer to push the keyboard to the bottom
    spacer = tk.Label(frame1, text="", bg=tk_background_color)
    spacer.grid(row=6, column=0, sticky="nsew", pady=(0, 50))  # Adjust row and pady as necessary
    
    # Display the virtual keyboard
    create_virtual_keyboard(frame1, 7) 

def set_current_target(entry_widget):
    global current_target_entry
    current_target_entry = entry_widget
    
    
def own_calibration_site():
    global baro_input_box, current_target_entry

    # Clear the current display
    for widget in frame1.winfo_children():
        widget.destroy()

    frame1.grid(row=0, column=0, sticky="nsew")
    frame1.grid_propagate(False)

    label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
    label1.grid(row=0, column=0, columnspan=20, padx=50, pady=(50,5), sticky="nw")

    instruction_text = "Please enter the current barometric pressure reading in inches from your own source.\n\nEnter in the form XX.XX"
    instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16), bg=tk_background_color, justify="left")
    instructions_label.grid(row=1, column=0, columnspan=20, padx=50, pady=5, sticky="nw")

    # Create an Entry widget for the user to input the barometric pressure
    baro_input_box = tk.Entry(frame1, font=("Helvetica", 14), width=10)  # Adjust width as necessary
    baro_input_box.grid(row=2, column=0, columnspan=20, padx=50, pady=5, sticky="nw")
    baro_input_box.bind("<FocusIn>", lambda e: set_current_target(baro_input_box))

    label_text = "inches of mercury"
    label = tk.Label(frame1, text=label_text, font=("Helvetica", 14), bg=tk_background_color)
    label.grid(row=2, column=4, columnspan=20, padx=(150, 0), pady=5, sticky="w")  # Minor adjustment for positioning next to the entry
    
    # Create the 'Back' button
    back_button = tk.Button(frame1, text=" Back ", font=("Helvetica", 16, "bold"), command=welcome_screen)
    back_button.grid(row=3, column=0, columnspan=20, padx=(50, 0), pady=20, sticky="nw")
    
    # Create a submit button to process the user's input
    submit_button = tk.Button(frame1, text="Submit", command=submit_own_calibration, font=("Helvetica", 16, "bold"))
    submit_button.grid(row=3, column=0, columnspan=20, padx=200, pady=20, sticky="nw")

    # Spacer to push the keyboard to the bottom
    spacer = tk.Label(frame1, text="", bg=tk_background_color)
    spacer.grid(row=4, column=0, sticky="nsew", pady=(0, 45))  # Adjust row and pady as necessary

    # Display the virtual keyboard
    create_virtual_keyboard(frame1, 5)  # Adjust as necessary based on layout
    
def submit_own_calibration():
    global baro_input 

    # Get the user's input
    baro_input = float(baro_input_box.get())
 
    # Continue with other actions or functions as needed
    land_or_buoy()
                                
def welcome_screen():
    
    # Clear the current display
    for widget in frame1.winfo_children():
        widget.destroy()

    frame1.grid(row=0, column=0, sticky="nsew")

    # First line (bold)
    label1 = tk.Label(frame1, text=f'Welcome to The Weather Observer v{VERSION}', font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
    label1.grid(row=0, column=0, padx=50, pady=(50, 10), sticky="w")

    if baro_input is None:
        own_calibration_site()

    # Main block of text including the question
    info_text = f'''
    In order to begin, your new instrument needs to be calibrated,
    and you need to make choices about which weather to observe.

    Information from your router indicates that the nearest NWS Observation site found is:
    {aobs_site}

    This site should be close to your current location. If it isn't, click change and
    enter your town and two-letter state ID.
    
    The site will be used to calibrate the first barometric pressure reading.
    The current barometric pressure reading at {aobs_site} is: {baro_input:.2f} inches.

    Do you want to keep the default calibration site,
    change to another site, or
    enter your own barometric pressure?
    '''

    label2 = tk.Label(frame1, text=info_text, font=("Arial", 16), bg=tk_background_color, justify="left")
    label2.grid(row=1, column=0, padx=50, pady=(0, 10), sticky='w')

    # Define frame_question
    frame_question = tk.Frame(frame1, bg=tk_background_color)
    frame_question.grid(row=2, column=0, pady=(0, 5), sticky="w")

    # Create the 'Keep' button
    keep_button = create_button(frame_question, "Keep", button_font, confirm_calibration_site)
    keep_button.grid(row=0, column=0, padx=50, pady=0, sticky="w")

    # Create the 'Change' button
    change_button = create_button(frame_question, "Change", button_font, change_calibration_site)
    change_button.grid(row=0, column=0, padx=190, pady=0, sticky="w")

    # Create the 'Enter Your Own' button
    enter_own_button = create_button(frame_question, "Own", button_font, own_calibration_site)
    enter_own_button.grid(row=0, column=0, padx=350, pady=0, sticky="w")

welcome_screen()

gold = 30.75
yellow = 30.35
gainsboro = 29.65
darkgrey = 29.25

ax.axhline(gold, color='gold', lw=81, alpha=.5)
ax.axhline(yellow, color='yellow', lw=49, alpha=.2)
ax.axhline(gainsboro, color='gainsboro', lw=49, alpha=.5)    
ax.axhline(darkgrey, color='darkgrey', lw=81, alpha=.5)

# Lines on minor ticks
for t in np.arange(29, 31, 0.05):
    ax.axhline(t, color='black', lw=.5, alpha=.2)
for u in np.arange(29, 31, 0.25):
    ax.axhline(u, color='black', lw=.7)

ax.tick_params(axis='x', direction='inout', length=5, width=1, color='black')
plt.grid(True, color='.01')  # Draws default horiz and vert grid lines
ax.yaxis.set_minor_locator(AutoMinorLocator(5))
ax.yaxis.set_major_formatter(FormatStrFormatter('%2.2f'))

# Add annotation for day of the week - this defines it
day_label = ax.annotate('', xy=(0, 0), xycoords='data', ha='center', va='center',
                         fontsize=10, fontstyle='italic', color='blue')

# Set major and minor ticks format for midnight label and other vertical lines
ax.xaxis.set(
    major_locator=mdates.HourLocator(byhour=[0, 4, 8, 12, 16, 20]),
    major_formatter=mdates.DateFormatter('%-I%P'),
    minor_locator=mdates.HourLocator(interval=1),
    minor_formatter=ticker.FuncFormatter(lambda x, pos: '\n%a,%-m/%-d' if (isinstance(x, datetime) and x.hour == 0) else '')
)

ax.xaxis.set(
    minor_locator=mdates.DayLocator(),
    minor_formatter=mdates.DateFormatter("\n%a,%-m/%-d"),
)

# This line seems responsible for vertical lines
ax.grid(which='major', axis='both', linestyle='-', linewidth=1, color='black', alpha=1, zorder=10)

# Disable removing overlapping locations
ax.xaxis.remove_overlapping_locs = False

# Copying this over from daysleanbaro2-5-24. Not sure it's necessary
# This gets midnight of the current day, then figures the x value for 12 pm
now = datetime.now()
date_time = pd.to_datetime(now.strftime("%m/%d/%Y, %H:%M:%S"))
midnight = datetime.combine(date_time.date(), datetime.min.time())
x_value_12pm = mdates.date2num(midnight.replace(hour=12))

y_value_day_label = 30.92

# Add annotation for day of the week - this defines it
day_label = ax.annotate('', xy=(0,0), xycoords='data', ha='center', va='center',
                         fontsize=10, fontstyle='italic', color='blue')

# Set axis limits and labels
now = datetime.now()
time_delta = timedelta(minutes=3600)
start_time = now - time_delta

ax.set_xlim(start_time, now)
ax.set_ylim(29, 31)

ax.set_yticks([29, 29.5, 30, 30.5, 31])

# Create empty xs and ys arrays
xs = []
ys = []

# Create a line plot
line, = ax.plot([], [], 'r-')

# Get I2C bus
bus = smbus.SMBus(1)

yesterday_annotation = None
before_yesterday_annotation = None
today_annotation_flag = False
today_inHg_annotation_flag = False
#_day_3050_annotation = None

# Initialize a dictionary to keep track of annotations
annotations_created = {
    "before_yesterday": False,
    "bday_3050": False,
    "bday_3000": False,
    "bday_2950": False
}

# This function is called periodically from FuncAnimation
#@profile
def animate(i):
    try:
        global xs, ys, line, yesterday_annotation, before_yesterday_annotation, threshold_x_value
        global inHg_correction_factor, refresh_flag, iterate_flag, day_label
        global today_annotation_flag, today_inHg_annotation_flag
        
        if iterate_flag == False and len(xs) >= 1:            
            return
        
        # Set a threshold x value below which the before_yesterday_annotation should be removed
        threshold_left_x_value = mdates.date2num(datetime.now() - timedelta(days=2.4))

        # Set a threshold x value beyond which the x_value_12pm annotation should not be added on the right
        threshold_right_x_value = mdates.date2num(datetime.now() - timedelta(days=.125))
        
        # HP203B address, 0x77(118)
        # Send OSR and channel setting command, 0x44(68)
        bus.write_byte(0x77, 0x44 | 0x00)

        time.sleep(0.5)

        # HP203B address, 0x77(118)
        # Read data back from 0x10(16), 6 bytes
        # cTemp MSB, cTemp CSB, cTemp LSB, pressure MSB, pressure CSB, pressure LSB
        data = bus.read_i2c_block_data(0x77, 0x10, 6)

        # Convert the data to 20-bits
        # Correct for 160 feet above sea level
        # cpressure is pressure corrected for elevation
        cTemp = (((data[0] & 0x0F) * 65536) + (data[1] * 256) + data[2]) / 100.00
        fTemp = (cTemp * 1.8) + 32
        pressure = (((data[3] & 0x0F) * 65536) + (data[4] * 256) + data[5]) / 100.00
        cpressure = (pressure * 1.0058)
        inHg = (cpressure * .029529)
        
        if i == 0:        
            # calculate a correction factor only when i == 0
            inHg_correction_factor = (baro_input / inHg)
        # apply correct factor to each reading from sensor
        inHg = round(inHg * inHg_correction_factor, 3)

        # Define a flag to track if day names have been reassigned
        midnight_reassigned = False
       
        # Initialize the flag outside of the loop
        previous_day_annotations_created = False
       
        # Get time stamp
        now = datetime.now()
        date_time = pd.to_datetime(now.strftime("%m/%d/%Y, %H:%M:%S"))
        
        yesterday_name = now - timedelta(days=1)
        yesterday_name = yesterday_name.strftime('%A')
        
        before_yesterday_name = now - timedelta(days=2)
        before_yesterday_name = before_yesterday_name.strftime('%A')

        # Check if it's within the 5-minute window around midnight to reassign day names
        if 0 <= now.hour < 1 and 0 <= now.minute <= 5 and not midnight_reassigned:
            # Update day labels at midnight
            previous_annotation = datetime.now().strftime('%A')
            
            # not sure the following line is needed
            _day_label_annotation =  datetime.now().strftime('%A')
          
            yesterday_name = date_time - timedelta(days=1)
            yesterday_name = yesterday_name.strftime('%A')

            before_yesterday_name = date_time - timedelta(days=2)
            before_yesterday_name = before_yesterday_name.strftime('%A')

            # Set the flag to True to indicate that reassignment has occurred
            midnight_reassigned = True
            
            today_annotation_flag = False
            today_inHg_annotation_flag = False 

        # Build xs and ys arrays
        xs.append(date_time)
        ys.append(inHg)

        xs = xs[-1200:]
        ys = ys[-1200:]

        # Update day of the week label
        day_label.set_text(date_time.strftime('%A'))

        # This gets midnight of the current day, then figures the x value for 12 pm
        midnight = datetime.combine(date_time.date(), datetime.min.time())
        x_value_12pm = mdates.date2num(midnight.replace(hour=12))

        # noon_time = x_value_12pm
        x_value_yesterday = x_value_12pm - 1
        x_value_day_before = x_value_12pm - 2
        y_value_day_label = 30.92

        # Update day label position based on the x value for 12 pm
        previous_annotation = getattr(ax, "_day_label_annotation", None)
        
        if x_value_12pm < threshold_right_x_value and today_annotation_flag == False:  
            
            ax._day_label_annotation = ax.annotate(date_time.strftime('%A'), (x_value_12pm, y_value_day_label),
                                        ha='center', fontsize=10, fontstyle='italic', fontfamily='DejaVu Serif', fontweight='bold')
            
            today_annotation_flag = True
            
        if x_value_12pm < threshold_right_x_value + .08 and today_inHg_annotation_flag == False:
            # Your existing code with translucent box properties as arguments
            ax._day_3050_annotation = ax.annotate('30.50', (x_value_12pm - .001, 30.475),
                                                  ha='center', fontsize=10, fontfamily='DejaVu Serif')
                                                  

            # Your existing code with translucent box properties as arguments
            ax._day_3000_annotation = ax.annotate('30.00', (x_value_12pm - .001, 29.975),
                                                  ha='center', fontsize=10, fontfamily='DejaVu Serif')
                                                  

            # Your existing code with translucent box properties as arguments
            ax._day_2950_annotation = ax.annotate('29.50', (x_value_12pm - .001, 29.475),
                                                  ha='center', fontsize=10, fontfamily='DejaVu Serif')

            today_inHg_annotation_flag = True 

        # Annotate 'yesterday' at the specified coordinates if not removed
        if yesterday_annotation is None and x_value_yesterday < threshold_right_x_value + 0.2:
            yesterday_annotation = ax.annotate(f'{yesterday_name}', xy=(x_value_yesterday, y_value_day_label), xytext=(0, 0),
                        textcoords='offset points', ha='center',
                        fontsize=10, fontstyle='italic', fontfamily='DejaVu Serif', fontweight='bold', color='black')

            # Your existing code with translucent box properties as arguments
            ax._day_3050_annotation = ax.annotate('30.50', (x_value_yesterday - 0.001, 30.475),
                                                  ha='center', fontsize=10, fontfamily='DejaVu Serif')
                                                  

            # Your existing code with translucent box properties as arguments
            ax._day_3000_annotation = ax.annotate('30.00', (x_value_yesterday - 0.001, 29.975),
                                                  ha='center', fontsize=10, fontfamily='DejaVu Serif')
                                                  

            # Your existing code with translucent box properties as arguments
            ax._day_2950_annotation = ax.annotate('29.50', (x_value_yesterday - 0.001, 29.475),
                                                  ha='center', fontsize=10, fontfamily='DejaVu Serif')
                                                  


        # Check if x value is below the threshold, and remove before_yesterday_annotation if needed
        if before_yesterday_annotation and x_value_day_before < threshold_left_x_value:
            # If the before_yesterday label has already been created, skip updating it
            before_yesterday_annotation.remove()
            before_yesterday_annotation = None  # Set to None to indicate it has been removed 
            annotations_created["before_yesterday"] = False  # Reset the flag

        # Annotate 'day before yesterday' at the specified coordinates if not removed
        # Increase what's added to the threshold_left_x_value to make day before label disappear sooner
        if not annotations_created["before_yesterday"] and x_value_day_before > threshold_left_x_value + 0.027:
            before_yesterday_annotation = ax.annotate(
                f'{before_yesterday_name}', xy=(x_value_day_before, y_value_day_label), xytext=(0, 0),
                textcoords='offset points', ha='center',
                fontsize=10, fontstyle='italic', fontfamily='DejaVu Serif', fontweight='bold', color='black')
            annotations_created["before_yesterday"] = True  # Set the flag to True to indicate that the annotation has been created

        # Check if x value is within the range to display other annotations
        if x_value_day_before > threshold_left_x_value - 0.044:
            # Check if the annotations have not been created yet
            if not annotations_created["bday_3050"]:
                ax._bday_3050_annotation = ax.annotate('30.50', (x_value_day_before - 0.001, 30.475),
                                                        ha='center', fontsize=10, fontfamily='DejaVu Serif')
                annotations_created["bday_3050"] = True  # Set the flag to True to indicate that the annotation has been created
                
            if not annotations_created["bday_3000"]:
                ax._bday_3000_annotation = ax.annotate('30.00', (x_value_day_before - 0.001, 29.975),
                                                        ha='center', fontsize=10, fontfamily='DejaVu Serif')
                annotations_created["bday_3000"] = True
                
            if not annotations_created["bday_2950"]:
                ax._bday_2950_annotation = ax.annotate('29.50', (x_value_day_before - 0.001, 29.475),
                                                        ha='center', fontsize=10, fontfamily='DejaVu Serif')
                annotations_created["bday_2950"] = True
                
                
        else:            
            pass

        # Update the line data here so the line plots on top of labels
        line.set_data(xs, ys)

        ax.set_xlim(datetime.now() - timedelta(minutes=3600), datetime.now())

        print(i)
        
        fig.savefig("baro_trace.png")
        # changed if condition when making obs buttons
        if refresh_flag == False and aobs_only_click_flag == False and bobs_only_click_flag == False and cobs_only_click_flag == False:
            
            show_transparent_frame()
    
            iterate_flag = False
            
            if len(xs) <= 1:
                show_scraped_frame()
            else:
                return
        
        else:            
            return
        
    except Exception as e:
        print("Display Baro Trace. line 3722", e)

# Create a function to start the animation
#@profile
def start_animation(): # code goes here once when the user starts barograph
    #show_transparent_frame()
    #transparent_frame.lift()
    frame1.grid_forget()
    baro_frame.grid_forget()
    clear_frame(frame1)
    
    ani = animation.FuncAnimation(fig, animate, interval=180000, save_count=1500)
    canvas.draw()

# Function to show the transparent frame
#@profile
def show_transparent_frame():
    global alternative_town_1, alternative_state_1, alternative_town_2, alternative_state_2, alternative_town_3, alternative_state_3
    global left_site_label, aobs_only_click_flag, bobs_only_click_flag, cobs_only_click_flag
    
    # don't forget frame1 if user is still making choices in
    if aobs_only_click_flag == False and bobs_only_click_flag == False and cobs_only_click_flag == False:
        frame1.grid_forget() 
    
    if ".ndbc." in aobs_url:
        try:
            
            #Scrape for buoy data
            aurl = aobs_url
            ahtml = requests.get(aurl)# requests instance    
            time.sleep(5)    
            asoup = BeautifulSoup(ahtml.text,'html.parser')   
        
            awd = asoup.find(class_="dataTable").find_all('td')[0]
            awd = awd.string.split()[0]
        
            aws = asoup.find(class_="dataTable").find_all('td')[1]
            aws = float(aws.string) * 1.15078
            aws = round(aws)
            aws = " at {} mph".format(aws)

            awg = asoup.find(class_="dataTable").find_all('td')[2]
            awg = round(float(awg.string) * 1.15078)
            awg = " G{}".format(awg)

            awind = awd + aws + awg
        
            awt = asoup.find(class_="dataTable")
            awt = awt.find_all('td')[10]
            awt = awt.string
        
            if not "-" in awt:
                awtemp = "Water Temp: " + str(round(float(awt.string))) + chr(176)
            
            else:
                awtemp = "Water Temp: -"
                pass
            aat = asoup.find(class_="dataTable")
            aat = aat.find_all('td')[9]

            if aat.string == '-':
                atemp = "Air Temp: N/A"
                pass
            else:
                atemp = "Air Temp: " + str(round(float(aat.string))) + chr(176)

        except Exception as e:
            print("Scrape buoy data", e)
            pass
    
    else:
        
        # get data for aobs land
        try:
            
            # Define the URL
            a_station_url = "https://api.mesowest.net/v2/stations/timeseries?STID={}&showemptystations=1&units=temp|F,speed|mph,english&recent=240&token=d8c6aee36a994f90857925cea26934be&complete=1&obtimezone=local".format(aobs_station_identifier)
            
            # Send a GET request to the URL
            a_response = requests.get(a_station_url)

            # Check if the request was successful
            if a_response.status_code == 200:
                # Parse the JSON response to get the keys
                a_data = a_response.json()
                
                try:
                
                    # Check if all the necessary keys exist before attempting to access them
                    if "STATION" in a_data and isinstance(a_data["STATION"], list) and a_data["STATION"]:
                        station_data = a_data["STATION"][0]
                        if "OBSERVATIONS" in station_data and isinstance(station_data["OBSERVATIONS"], dict):
                            obs_data = station_data["OBSERVATIONS"]
                            
                            # Check if "wind_cardinal_direction_set_1d" exists and is a list with values
                            if "wind_cardinal_direction_set_1d" in obs_data and isinstance(obs_data["wind_cardinal_direction_set_1d"], list) and obs_data["wind_cardinal_direction_set_1d"]:
                                a_wind_direction = obs_data["wind_cardinal_direction_set_1d"][-1]
                                
                                # Check if a_wind_direction is a string
                                if isinstance(a_wind_direction, str):
                                    # You mentioned no rounding or modification, so we keep it as is
                                    pass
                                else:
                                    a_wind_direction = "N/A"
                            else:
                                a_wind_direction = "N/A"
                        else:
                            a_wind_direction = "N/A"
                    else:
                        a_wind_direction = "N/A"
                    
                except Exception as e:
                    print("wind direction station a", e)
                    a_wind_direction = "N/A"
                
                try:
                    
                    # Check if all the necessary keys exist before attempting to access them
                    if "STATION" in a_data and isinstance(a_data["STATION"], list) and a_data["STATION"]:
                        station_data = a_data["STATION"][0]
                        if "OBSERVATIONS" in station_data and isinstance(station_data["OBSERVATIONS"], dict):
                            obs_data = station_data["OBSERVATIONS"]
                            
                            # Check if "wind_speed_set_1" exists and is a list with values
                            if "wind_speed_set_1" in obs_data and isinstance(obs_data["wind_speed_set_1"], list) and obs_data["wind_speed_set_1"]:
                                a_wind_speed = obs_data["wind_speed_set_1"][-1]
                                
                                # Check if a_wind_speed is a valid numeric value
                                if isinstance(a_wind_speed, (int, float)):
                                    a_wind_speed = str(round(a_wind_speed))
                                else:
                                    a_wind_speed = "N/A"
                            else:
                                a_wind_speed = "N/A"
                        else:
                            a_wind_speed = "N/A"
                    else:
                        a_wind_speed = "N/A"
                    
                except Exception as e:
                    print("wind speed station a", e)
                    a_wind_speed = "N/A"
                    
                try:
                    
                    # Check if all the necessary keys exist before attempting to access them
                    if "STATION" in a_data and isinstance(a_data["STATION"], list) and a_data["STATION"]:
                        station_data = a_data["STATION"][0]
                        if "OBSERVATIONS" in station_data and isinstance(station_data["OBSERVATIONS"], dict):
                            obs_data = station_data["OBSERVATIONS"]
                            
                            # Check if "wind_gust_set_1" exists and is a list with values
                            if "wind_gust_set_1" in obs_data and isinstance(obs_data["wind_gust_set_1"], list) and obs_data["wind_gust_set_1"]:
                                a_wind_gust = obs_data["wind_gust_set_1"][-1]
                                
                                # Check if a_wind_gust is a valid numeric value
                                if isinstance(a_wind_gust, (int, float)):
                                    a_wind_gust = "G" + str(round(a_wind_gust))
                                else:
                                    a_wind_gust = ""
                            else:
                                a_wind_gust = ""
                        else:
                            a_wind_gust = ""
                    else:
                        a_wind_gust = ""

                    
                except Exception as e:
                    print("a_wind_gust", e)
                    a_wind_gust = ""
                    
                awind = a_wind_direction + " at " + a_wind_speed + " mph " + a_wind_gust 
                
                try:
                    # Check if all the necessary keys exist before attempting to access them
                    if "STATION" in a_data and isinstance(a_data["STATION"], list) and a_data["STATION"]:
                        station_data = a_data["STATION"][0]
                        if "OBSERVATIONS" in station_data and isinstance(station_data["OBSERVATIONS"], dict):
                            obs_data = station_data["OBSERVATIONS"]
                            
                            # Check if "air_temp_set_1" exists and is a list with values
                            if "air_temp_set_1" in obs_data and isinstance(obs_data["air_temp_set_1"], list) and obs_data["air_temp_set_1"]:
                                atemp = str(obs_data["air_temp_set_1"][-1])
                                atemp = atemp + chr(176)
                            else:
                                atemp = "N/A"
                        else:
                            atemp = "N/A"
                    else:
                        atemp = "N/A"

                except Exception as e:
                    atemp = "N/A"
                    print("air temperature station a", e)
                            
            else:
                atemp = "N/A"
                awind = "N/A"
        
        except Exception as e:
            atemp = "N/A"
            awind = "N/A"

    if ".ndbc." in bobs_url:
        try:
                        #Scrape for buoy data
            burl = bobs_url        
            bhtml = requests.get(burl)# requests instance    
            time.sleep(5)    
            bsoup = BeautifulSoup(bhtml.text,'html.parser')   
        
            bwd = bsoup.find(class_="dataTable").find_all('td')[0]
            bwd = bwd.string.split()[0]
            
            bws = bsoup.find(class_="dataTable").find_all('td')[1]
            bws = float(bws.string) * 1.15078
            bws = round(bws)
            bws = " at {} mph".format(bws)

            bwg = bsoup.find(class_="dataTable").find_all('td')[2]
            bwg = round(float(bwg.string) * 1.15078)
            bwg = " G{}".format(bwg)

            bwind = bwd + bws + bwg
        
            bwt = bsoup.find(class_="dataTable")
            bwt = bwt.find_all('td')[10]
            bwt = bwt.string
            
            if not "-" in bwt:
                bwtemp = "Water Temp: " + str(round(float(bwt.string))) + chr(176)
            
            else:
                bwtemp = "Water Temp: -"
                pass
            
            bat = bsoup.find(class_="dataTable")
            bat = bat.find_all('td')[9]
            
            if bat.string == '-':
                btemp = "Air Temp: N/A"
                pass
            else:
                btemp = "Air Temp: " + str(round(float(bat.string))) + chr(176)
            
        except Exception as e:
            print("Scrape buoy data for burl", e)
            pass
    
    else:
        
        try:

            # Define the URL
            b_station_url = "https://api.mesowest.net/v2/stations/timeseries?STID={}&showemptystations=1&units=temp|F,speed|mph,english&recent=240&token=d8c6aee36a994f90857925cea26934be&complete=1&obtimezone=local".format(bobs_station_identifier)

            # Send a GET request to the URL
            b_response = requests.get(b_station_url)

            # Check if the request was successful
            if b_response.status_code == 200:
                # Parse the JSON response
                b_data = b_response.json()

                try:
                    # Check if all the necessary keys exist before attempting to access them
                    if "STATION" in b_data and isinstance(b_data["STATION"], list) and b_data["STATION"]:
                        station_data = b_data["STATION"][0]
                        if "OBSERVATIONS" in station_data and isinstance(station_data["OBSERVATIONS"], dict):
                            obs_data = station_data["OBSERVATIONS"]
                            
                            # Check if "wind_cardinal_direction_set_1d" exists and is a list with values
                            if "wind_cardinal_direction_set_1d" in obs_data and isinstance(obs_data["wind_cardinal_direction_set_1d"], list) and obs_data["wind_cardinal_direction_set_1d"]:
                                b_wind_direction = obs_data["wind_cardinal_direction_set_1d"][-1]
                                
                                # Check if b_wind_direction is a string
                                if isinstance(b_wind_direction, str):
                                    # You mentioned no rounding or modification, so we keep it as is
                                    pass
                                else:
                                    b_wind_direction = "N/A"
                            else:
                                b_wind_direction = "N/A"
                        else:
                            b_wind_direction = "N/A"
                    else:
                        b_wind_direction = "N/A"
                    
                except Exception as e:
                    print("b_wind_direction", e)
                    b_wind_direction = "N/A"

                try:
                    # Check if all the necessary keys exist before attempting to access them
                    if "STATION" in b_data and isinstance(b_data["STATION"], list) and b_data["STATION"]:
                        station_data = b_data["STATION"][0]
                        if "OBSERVATIONS" in station_data and isinstance(station_data["OBSERVATIONS"], dict):
                            obs_data = station_data["OBSERVATIONS"]
                            
                            # Check if "wind_speed_set_1" exists and is a list with values
                            if "wind_speed_set_1" in obs_data and isinstance(obs_data["wind_speed_set_1"], list) and obs_data["wind_speed_set_1"]:
                                b_wind_speed = obs_data["wind_speed_set_1"][-1]
                                
                                # Check if b_wind_speed is a valid numeric value
                                if isinstance(b_wind_speed, (int, float)):
                                    b_wind_speed = str(round(b_wind_speed))
                                else:
                                    b_wind_speed = "N/A"
                            else:
                                b_wind_speed = "N/A"
                        else:
                            b_wind_speed = "N/A"
                    else:
                        b_wind_speed = "N/A"
                    
                except Exception as e:
                    print("b_wind_speed", e)
                    b_wind_speed = "N/A"
                    
                try:
                    # Check if all the necessary keys exist before attempting to access them
                    if "STATION" in b_data and isinstance(b_data["STATION"], list) and b_data["STATION"]:
                        station_data = b_data["STATION"][0]
                        if "OBSERVATIONS" in station_data and isinstance(station_data["OBSERVATIONS"], dict):
                            obs_data = station_data["OBSERVATIONS"]
                            
                            # Check if "wind_gust_set_1" exists and is a list with values
                            if "wind_gust_set_1" in obs_data and isinstance(obs_data["wind_gust_set_1"], list) and obs_data["wind_gust_set_1"]:
                                b_wind_gust = obs_data["wind_gust_set_1"][-1]
                                
                                # Check if b_wind_gust is a valid numeric value or "null"
                                if isinstance(b_wind_gust, (int, float)):
                                    b_wind_gust = "G" + str(round(b_wind_gust))
                                else:
                                    b_wind_gust = ""
                            else:
                                b_wind_gust = ""
                        else:
                            b_wind_gust = ""
                    else:
                        b_wind_gust = ""
                    
                except Exception as e:
                    print("b_wind_gust", e)
                    b_wind_gust = ""
                    
                bwind = b_wind_direction + " at " + b_wind_speed + " mph " + b_wind_gust
                
                try:
                    # Check if all the necessary keys exist before attempting to access them
                    if "STATION" in b_data and isinstance(b_data["STATION"], list) and b_data["STATION"]:
                        station_data = b_data["STATION"][0]
                        if "OBSERVATIONS" in station_data and isinstance(station_data["OBSERVATIONS"], dict):
                            obs_data = station_data["OBSERVATIONS"]
                            
                            # Check if "air_temp_set_1" exists and is a list with values
                            if "air_temp_set_1" in obs_data and isinstance(obs_data["air_temp_set_1"], list) and obs_data["air_temp_set_1"]:
                                btemp = str(obs_data["air_temp_set_1"][-1])
                                btemp = btemp + chr(176)
                            else:
                                btemp = "N/A"
                        else:
                            btemp = "N/A"
                    else:
                        btemp = "N/A"
                    
                except Exception as e:
                    btemp = "N/A"
                    print("air temperature station b", e)
                    
            else:
                btemp = "N/A"
                bwind = "N/A"
        
        except Exception as e:
            btemp = "N/A"
            bwind = "N/A"        
    
    try: 

        # Define the URL
        c_station_url = "https://api.mesowest.net/v2/stations/timeseries?STID={}&showemptystations=1&units=temp|F,speed|mph,english&recent=240&token=d8c6aee36a994f90857925cea26934be&complete=1&obtimezone=local".format(cobs_station_identifier)
        
        # Send a GET request to the URL
        c_response = requests.get(c_station_url)
        
        # Check if the request was successful
        if c_response.status_code == 200:
            # Parse the JSON response
            c_data = c_response.json()
                
            try:    
            
                # Check if all the necessary keys exist before attempting to access them
                if "STATION" in c_data and isinstance(c_data["STATION"], list) and c_data["STATION"]:
                    station_data = c_data["STATION"][0]
                    if "OBSERVATIONS" in station_data and isinstance(station_data["OBSERVATIONS"], dict):
                        obs_data = station_data["OBSERVATIONS"]
                        
                        # Check if "wind_cardinal_direction_set_1d" exists and is a list with values
                        if "wind_cardinal_direction_set_1d" in obs_data and isinstance(obs_data["wind_cardinal_direction_set_1d"], list) and obs_data["wind_cardinal_direction_set_1d"]:
                            c_wind_direction = obs_data["wind_cardinal_direction_set_1d"][-1]
                            
                            # Check if c_wind_direction is a string
                            if isinstance(c_wind_direction, str):
                                # You mentioned no rounding or modification, so we keep it as is
                                pass
                            else:
                                c_wind_direction = "N/A"
                        else:
                            c_wind_direction = "N/A"
                    else:
                        c_wind_direction = "N/A"
                else:
                    c_wind_direction = "N/A"
             
            except Exception as e:
                print("c_wind_direction", e)
                c_wind_direction = "N/A"
            
            try:
                # Check if all the necessary keys exist before attempting to access them
                if "STATION" in c_data and isinstance(c_data["STATION"], list) and c_data["STATION"]:
                    station_data = c_data["STATION"][0]
                    if "OBSERVATIONS" in station_data and isinstance(station_data["OBSERVATIONS"], dict):
                        obs_data = station_data["OBSERVATIONS"]
                        
                        # Check if "wind_speed_set_1" exists and is a list with values
                        if "wind_speed_set_1" in obs_data and isinstance(obs_data["wind_speed_set_1"], list) and obs_data["wind_speed_set_1"]:
                            c_wind_speed = obs_data["wind_speed_set_1"][-1]
                            
                            # Check if c_wind_speed is a valid numeric value
                            if isinstance(c_wind_speed, (int, float)):
                                c_wind_speed = str(round(c_wind_speed))
                            else:
                                c_wind_speed = "N/A"
                        else:
                            c_wind_speed = "N/A"
                    else:
                        c_wind_speed = "N/A"
                else:
                    c_wind_speed = "N/A"
                
            except Exception as e:
                print("c_wind_speed", e)
                c_wind_speed = "N/A"
            
            try:
                # Check if all the necessary keys exist before attempting to access them
                if "STATION" in c_data and isinstance(c_data["STATION"], list) and c_data["STATION"]:
                    station_data = c_data["STATION"][0]
                    if "OBSERVATIONS" in station_data and isinstance(station_data["OBSERVATIONS"], dict):
                        obs_data = station_data["OBSERVATIONS"]
                        
                        # Check if "wind_gust_set_1" exists and is a list with values
                        if "wind_gust_set_1" in obs_data and isinstance(obs_data["wind_gust_set_1"], list) and obs_data["wind_gust_set_1"]:
                            c_wind_gust = obs_data["wind_gust_set_1"][-1]
                            
                            # Check if c_wind_gust is a valid numeric value
                            if isinstance(c_wind_gust, (int, float)):
                                c_wind_gust = "G" + str(round(c_wind_gust))
                            else:
                                c_wind_gust = ""
                        else:
                            c_wind_gust = ""
                    else:
                        c_wind_gust = ""
                else:
                    c_wind_gust = ""
                
            except Exception as e:
                c_wind_gust = ""
                print("c_wind_gust is: ", c_wind_gust, "and the error is: ", e)
            
            cwind = c_wind_direction + " at " + c_wind_speed + " mph " + c_wind_gust 
            
            try:
                # Check if all the necessary keys exist before attempting to access them
                if "STATION" in c_data and isinstance(c_data["STATION"], list) and c_data["STATION"]:
                    station_data = c_data["STATION"][0]
                    if "OBSERVATIONS" in station_data and isinstance(station_data["OBSERVATIONS"], dict):
                        obs_data = station_data["OBSERVATIONS"]
                        
                        # Check if "air_temp_set_1" exists and is a list with values
                        if "air_temp_set_1" in obs_data and isinstance(obs_data["air_temp_set_1"], list) and obs_data["air_temp_set_1"]:
                            ctemp = str(obs_data["air_temp_set_1"][-1])
                            ctemp = ctemp + chr(176)
                        else:
                            ctemp = "N/A"
                    else:
                        ctemp = "N/A"
                else:
                    ctemp = "N/A"
            
            except Exception as e:
                ctemp = "N/A"
                print("air temperature station c", e)
            
        else:
            ctemp = "N/A"
            cwind = "N/A"
    
    except Exception as e:
        ctemp = "N/A"
        cwind = "N/A"

    
    now = datetime.now() # current date and time 
    hourmin_str = now.strftime("%-I:%M %P")    
    
    transparent_frame.grid(row=0, column=0, sticky="nw")
    transparent_frame.lift() #need this to show transparent frame
    
    # Add text to the transparent frame with custom font and styling
    logo_font = font.Font(family="Helvetica", size=16, weight="bold")  # Customize the font
    text_label = tk.Label(transparent_frame, text="The\nWeather\nObserver", fg="black", bg=tk_background_color, font=logo_font, anchor="w", justify="left")
    text_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')
     
    # enter code for time stamp
    time_stamp = font.Font(family="Helvetica", size=8, weight="normal", slant="italic")
    time_stamp_label = tk.Label(transparent_frame, text=f'Version {VERSION}\nLast Updated\n{now.strftime("%A")}\n{hourmin_str}', fg="black", bg=tk_background_color, font=time_stamp, anchor="w", justify="left")
    time_stamp_label.grid(row=0, column=0, padx=120, pady=(17, 5), sticky='w')

    if ".ndbc." in aobs_url:
        
        try:
            def aobs_buoy_on_click():
                
                global aobs_only_click_flag
                
                scraped_frame.grid_forget() 
                baro_frame.grid_forget()
                transparent_frame.grid_forget()
                
                for widget in transparent_frame.winfo_children():        
                    widget.destroy()
                
                aobs_only_click_flag = True
                
                land_or_buoy()
                
            # Combine text into one StringVar with four lines
            left_combined_text = tk.StringVar()
            left_combined_text.set(f"Buoy: {alternative_town_1}\n{atemp}\n{awtemp}\nWind: {awind}")

            # Define a single button with the combined text
            left_combined_button = tk.Button(
                transparent_frame, 
                textvariable=left_combined_text, 
                fg="black", 
                bg=tk_background_color, 
                font=buoy_font, 
                anchor="w", 
                justify="left", 
                command=aobs_buoy_on_click, 
                relief=tk.RAISED, 
                bd=1, 
                highlightthickness=0,
                width=29  # Adjust width to ensure it fits all text nicely
            )
            left_combined_button.grid(row=0, column=0, padx=200, pady=(5, 10), sticky='w')

        except Exception as e:
            print("printing a buoy", e)

    else:
                       
        def aobs_on_click():
            
            global aobs_only_click_flag
    
            scraped_frame.grid_forget() 
            baro_frame.grid_forget()
            transparent_frame.grid_forget()
            
            for widget in transparent_frame.winfo_children():        
                widget.destroy()
            
            aobs_only_click_flag = True
            
            land_or_buoy()

        # Combine text into one StringVar
        left_combined_text = tk.StringVar()
        left_combined_text.set(f"{alternative_town_1}\nTemp: {atemp}\nWind: {awind}")

        try:
            
            # Define a single button with the combined text
            left_combined_button = tk.Button(transparent_frame, textvariable=left_combined_text, fg="black", bg=tk_background_color, font=obs_font, anchor="w", justify="left", command=aobs_on_click, relief=tk.RAISED, bd=1, highlightthickness=0, width=23)
            left_combined_button.grid(row=0, column=0, padx=200, pady=(5, 10), sticky='w')

        except Exception as e:
            print("printing a land", e)
        
    if ".ndbc." in bobs_url:
        try:
            def bobs_buoy_on_click():                
                global bobs_only_click_flag
                
                scraped_frame.grid_forget() 
                baro_frame.grid_forget()
                transparent_frame.grid_forget()
                
                for widget in transparent_frame.winfo_children():        
                    widget.destroy()
                
                bobs_only_click_flag = True
                
                bobs_land_or_buoy()
                
            # Combine text into one StringVar with four lines
            middle_combined_text = tk.StringVar()
            middle_combined_text.set(f"Buoy: {alternative_town_2}\n{btemp}\n{bwtemp}\nWind: {bwind}")

            # Define a single button with the combined text
            middle_combined_button = tk.Button(
                transparent_frame, 
                textvariable=middle_combined_text, 
                fg="black", 
                bg=tk_background_color, 
                font=buoy_font, 
                anchor="w", 
                justify="left", 
                command=bobs_buoy_on_click, 
                relief=tk.RAISED, 
                bd=1, 
                highlightthickness=0,
                width=29  # Adjust width to ensure it fits all text nicely
            )
            middle_combined_button.grid(row=0, column=0, padx=475, pady=(5, 10), sticky='w')

        except Exception as e:
            print("printing b buoy", e)
        
    else:
        
        def bobs_on_click():
            global bobs_only_click_flag
                
            scraped_frame.grid_forget() 
            baro_frame.grid_forget()
            transparent_frame.grid_forget()
            
            for widget in transparent_frame.winfo_children():        
                widget.destroy()
            
            bobs_only_click_flag = True
            
            bobs_land_or_buoy()

        # Combine text into one StringVar
        middle_combined_text = tk.StringVar()
        middle_combined_text.set(f"{alternative_town_2}\nTemp: {btemp}\nWind: {bwind}")

        try:
            
            # Define a single button with the combined text
            middle_combined_button = tk.Button(transparent_frame, textvariable=middle_combined_text, fg="black", bg=tk_background_color, font=obs_font, anchor="w", justify="left", command=bobs_on_click, relief=tk.RAISED, bd=1, highlightthickness=0, width=23)
            middle_combined_button.grid(row=0, column=0, padx=475, pady=(5, 10), sticky='w')

        except Exception as e:
            print("printing b land", e)

    def cobs_on_click():
        global cobs_only_click_flag
        
        scraped_frame.grid_forget() 
        baro_frame.grid_forget()
        transparent_frame.grid_forget()            
        
        for widget in transparent_frame.winfo_children():        
            widget.destroy()
        
        cobs_only_click_flag = True
        
        cobs_input_land()

    # Combine text into one StringVar
    right_combined_text = tk.StringVar()
    right_combined_text.set(f"{alternative_town_3}\nTemp: {ctemp}\nWind: {cwind}")

    try:
        # Define a single button with the combined text
        right_combined_button = tk.Button(transparent_frame, textvariable=right_combined_text, fg="black", bg=tk_background_color, font=obs_font, anchor="w", justify="left", command=cobs_on_click, relief=tk.RAISED, bd=1, highlightthickness=0, width=23)
        right_combined_button.grid(row=0, column=0, padx=750, pady=(5, 10), sticky='w')

    except Exception as e:
        print("printing c land", e)

#@profile
# Code for national radar
def convert_gif_to_jpg_national_radar(gif_data):
    # Open the gif using PIL
    gif = Image.open(BytesIO(gif_data))

    # Convert to RGB mode
    gif = gif.convert('RGB')

    # Save the image as a new jpg image
    output = BytesIO()
    gif.save(output, format="JPEG", quality=95, optimize=True)

    # Explicitly close the image
    gif.close()

    return output.getvalue()

#@profile
def display_national_radar():
    try:
        global last_national_radar_scrape_time, baro_img_label
        global img_label_national_radar, img_tk_national_radar, national_radar_hidden

        # _forget baro image if it's been saved for lcl radar, but lcl radar not used
        if baro_img_label and baro_img_label.winfo_exists():
            baro_img_label.grid_forget()
        
        # Showing scraped frame
        scraped_frame.grid(row=0, column=0, sticky="nsew")
        
        # Check if 10 minutes have passed since the last scrape or if it's the first time
        current_time = datetime.now()
        if last_national_radar_scrape_time is None or (current_time - last_national_radar_scrape_time).total_seconds() >= 600:
            #print("Getting new national radar. time ", current_time)
            radar_url = 'https://radar.weather.gov/ridge/standard/CONUS_0.gif'
            response = requests.get(radar_url)

            if response.status_code == 200:
                try:
                    # Convert the gif to jpg
                    jpg_data = convert_gif_to_jpg_national_radar(response.content)
                    img_national_radar = Image.open(BytesIO(jpg_data))

                    # Resize the image to fit the window
                    img_national_radar = img_national_radar.resize((870, 515), Image.LANCZOS)

                    # Keep a reference to the image to prevent garbage collection
                    img_tk_national_radar = ImageTk.PhotoImage(img_national_radar)

                    # Set the last scrape time to the current time
                    last_national_radar_scrape_time = current_time

                    img_label_national_radar = tk.Label(scraped_frame, image=img_tk_national_radar)
                    img_label_national_radar.image = img_tk_national_radar
                    img_label_national_radar.grid(row=1, column=0, padx=130, pady=80, sticky="se")

                    # Right after resizing and before or after setting it to the label
                    img_national_radar.save('displayed_national_radar.png')

                    root.update()  # Update the tkinter window to show the image
                    # setting national_radar_hidden to false because it's being shown
                    national_radar_hidden = False
                    
                    # Use after() to schedule hiding the image after some seconds
                    root.after(12000, lambda: hide_national_radar())
                    
                except Exception as img_err:
                    print("display_national_radar error:", img_err)
                    #show_local_radar_loop()
                    hide_national_radar()

        else:
            # If less than 10 minutes have passed, still display the most recently scraped image
            img_label_national_radar = tk.Label(scraped_frame, image=img_tk_national_radar)
            img_label_national_radar.image = img_tk_national_radar
            img_label_national_radar.grid(row=1, column=0, padx=130, pady=80, sticky="se")

            root.update()  # Update the tkinter window to show the image
            
            # setting national_radar_hidden to false because it's being shown
            national_radar_hidden = False
            
            # Use after() to schedule hiding the image after some seconds
            root.after(12000, lambda: hide_national_radar())

    except Exception as e:
        print("Scrape, Save, and Display national radar", e)
        #show_local_radar_loop()
        hide_national_radar()
        
#@profile
def hide_national_radar():
    global img_label_national_radar, national_radar_hidden
    global img_tk_national_radar  # Declare img_tk_national_radar as a global variable

    if img_label_national_radar and box_variables[2] != 1 and box_variables [3] != 1 and img_label_national_radar.winfo_exists():
        # flag established to track whether img_label_national_radar is forgotten to smooth displays
        national_radar_hidden = True

        img_label_national_radar.grid_forget()

    show_local_radar_loop()
    
#@profile
def show_national_radar():
    global img_tk_national_radar, img_label_national_radar, last_forget_clock, last_national_radar_scrape_time, last_national_sfc_map_scrape_time, last_station_model_scrape_time, last_sounding_scrape_time, last_vorticity_scrape_time, last_national_satellite_scrape_time  # Declare global variables
    global baro_img_label
    # Code to forget images every set amount of time
    current_time = datetime.now()

    # Ensure last_forget_clock is initialized
    if last_forget_clock is None:
        last_forget_clock = current_time

    if (current_time - last_forget_clock).total_seconds() >= 10800:
        print("clearing frames", current_time)
        # Clear frames
        transparent_frame.grid_forget()
        for widget in transparent_frame.winfo_children():
            widget.destroy()

        scraped_frame.grid_forget()
        for widget in scraped_frame.winfo_children():
            widget.destroy()

        baro_frame.grid_forget()

        # Update last_forget_clock
        last_forget_clock = current_time

        # Reset other time variables
        last_national_radar_scrape_time = None
        last_national_sfc_map_scrape_time = None
        last_station_model_scrape_time = None
        last_sounding_scrape_time = None
        last_vorticity_scrape_time = None

        # Print disk usage before cleanup
        # Clean APT cache
        clean_apt_cache()

        # Directories to clean
        directories_to_clean = [
            '/home/santod/',
            '/home/santod/myprojectenv/lib/python3.11/site-packages/'
        ]

        # Clean up specific directories if free space is below threshold
        for directory in directories_to_clean:
            clean_up_directory(directory, free_up_threshold=100 * 1024 * 1024)

        # Additional cleanup
        additional_cleanup()
        
    # Showing scraped frame
    scraped_frame.grid(row=0, column=0, sticky="nsew")

    # Buttons for user to refresh maps and observation site choices
    scraped_to_frame1 = ttk.Button(scraped_frame, text="   Change\nObservation\n    Sites &\n     Maps", command=refresh_choices)
    scraped_to_frame1.grid(row=1, column=0, padx=15, pady=(174,0), sticky='nw')
    
    # Buttons for user to refresh map choices
    maps_only_button = ttk.Button(scraped_frame, text=" \n    Change\n  Maps Only \n", command=change_maps_only)
    maps_only_button.grid(row=1, column=0, padx=15, pady=(265,0), sticky='nw') 
    
    # Buttons for screenshot and email
    pic_email_button = ttk.Button(scraped_frame, text=" \n    Email a \n Screenshot \n", command=pic_email)
    pic_email_button.grid(row=1, column=0, padx=15, pady=(355,0), sticky='nw') 
    
    reboot_button = ttk.Button(scraped_frame, text="  Reboot \n  System \n", command=reboot_system)
    reboot_button.grid(row=1, column=0, padx=15, pady=(500,0), sticky='nw')

    if box_variables[1] == 1 and refresh_flag == False:
        # Clear previous image label
        if img_label_national_radar and img_label_national_radar.winfo_exists():
            img_label_national_radar.grid_forget() # changed to forgot 7/25/24
        
        if baro_img_label and baro_img_label.winfo_exists():
            baro_img_label.grid_forget() # changed to forget 7/25/24
        
        # Showing scraped frame
        scraped_frame.grid(row=0, column=0, sticky="nsew")

        # show_national_satellite()
        display_national_radar()
    else:
        show_local_radar_loop()

# Code begins for nws lcl radar loop
def lcl_radar_selenium(max_retries=2, initial_delay=1):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    for attempt in range(max_retries):
        try:
            driver = webdriver.Chrome(service=Service("chromedriver"), options=chrome_options)
            driver.set_window_size(900, 600)  # Set the browser window size to be wider
            driver.set_script_timeout(30)  # Increase script timeout
            return driver
        except (SessionNotCreatedException, TimeoutException, WebDriverException) as e:
            print(f"Attempt {attempt + 1}: Failed to initialize the Selenium WebDriver in lcl radar: {e}")
        except Exception as e:
            print(f"Attempt {attempt + 1}: Unexpected error: Failed to initialize the Selenium WebDriver in lcl radar: {e}")

        # Exponential backoff
        time.sleep(initial_delay * (2 ** attempt))

    hide_local_radar_loop()
    return None

def adjust_slider(driver, xpath_1, xpath_2):
    try:
        slider_dot = find_slider_element(driver, xpath_1, xpath_2)
        if slider_dot and slider_dot.get_attribute('aria-valuenow') is not None:
            move_slider_to_ten(driver, slider_dot)
            return True
        else:
            return False
    except Exception as e:
        print(f"Error adjusting slider with xpaths {xpath_1} or {xpath_2}: {e}")
        return False

def move_slider_to_ten(driver, slider_dot):
    initial_value = float(slider_dot.get_attribute('aria-valuenow'))
    while True:
        remaining_value = float(slider_dot.get_attribute('aria-valuenow'))
        if remaining_value <= 10:
            break
        ActionChains(driver).click_and_hold(slider_dot).move_by_offset(-remaining_value, 0).release().perform()
        time.sleep(0.1)
        current_value = slider_dot.get_attribute('aria-valuenow')
        if float(current_value) <= 10:
            break

def find_slider_element(driver, xpath_1, xpath_2):
    try:
        slider_dot = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath_1))
        )
        if slider_dot.get_attribute('aria-valuenow') is not None:
            return slider_dot
    except Exception as e:
        print(f"Error locating slider element with xpath: {xpath_1}: {e}")
    
    try:
        slider_dot = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath_2))
        )
        if slider_dot.get_attribute('aria-valuenow') is not None:
            return slider_dot
    except Exception as e:
        print(f"Error locating slider element with xpath: {xpath_2}: {e}")

    return None

def capture_lcl_radar_screenshots(driver, num_images=10):
    images = {}
    attempts = 0
    max_attempts = 20  # Maximum number of attempts to capture all frames
    captured_times = set()
    wait = WebDriverWait(driver, 10)

    while len(images) < num_images and attempts < max_attempts:
        try:
            frame_time = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/main/div/div/div[2]/div[2]/div[1]/div[1]/div[2]'))
            ).text
            frame_number = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/main/div/div/div[2]/div[2]/div[1]/div[1]/div[3]'))
            ).text
            frame_index = int(frame_number.split('/')[0])

            # Ensure the timestamp is unique
            if frame_time not in captured_times:
                # Hide the VCR controls and legend
                vcr_controls = driver.find_element(By.XPATH, '//*[@id="app"]/main/div/div/div[2]/div[2]/div[2]')
                legend = driver.find_element(By.XPATH, '//*[@id="app"]/main/div/div/div[2]/div[2]/div[3]')
                driver.execute_script("arguments[0].style.display='none'", vcr_controls)
                driver.execute_script("arguments[0].style.display='none'", legend)

                # Capture the screenshot
                png = driver.get_screenshot_as_png()
                image = Image.open(BytesIO(png))
                images[frame_index] = {'image': image, 'time': frame_time}
                captured_times.add(frame_time)

                # Show the VCR controls and legend
                driver.execute_script("arguments[0].style.display='block'", vcr_controls)
                driver.execute_script("arguments[0].style.display='block'", legend)
            
            # Move to the next frame by clicking the step forward button
            step_fwd_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/main/div/div/div[2]/div[2]/div[2]/div[6]'))
            )
            step_fwd_button.click()
            time.sleep(1.5)  # Wait for the next frame to load
            attempts += 1
        except Exception as e:
            print(f"Error capturing frame: {e}")
            break

    # Ensure images are in order by their timestamps
    ordered_images = [images[i]['image'] for i in sorted(images.keys())]
    return ordered_images

def fetch_lcl_radar_coordinates(identifier):
    url = f"https://api.weather.gov/radar/stations/{identifier}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Will raise an exception for HTTP errors
        data = response.json()
        lat = data['geometry']['coordinates'][1]
        lon = data['geometry']['coordinates'][0]
        return lon, lat
    except requests.RequestException as e:
        print(f"Network-related error fetching data for radar site {identifier}: {e}")
        return None

def generate_lcl_radar_url(radar_site, center_coordinates, zoom_level):
    settings = {
        "agenda": {
            "id": "local",
            "center": center_coordinates,  # [longitude, latitude]
            "location": None,
            "zoom": zoom_level,
            "filter": None,
            "layer": "sr_bref",
            "station": radar_site
        },
        "animating": False,
        "base": "standard",
        "artcc": False,
        "county": False,
        "cwa": False,
        "rfc": False,
        "state": False,
        "menu": True,
        "shortFusedOnly": True,
        "opacity": {
            "alerts": 0.8,
            "local": 0.6,
            "localStations": 0.8,
            "national": 0.6
        }
    }
    
    settings_str = json.dumps(settings)
    encoded_settings = base64.b64encode(settings_str.encode('utf-8')).decode('utf-8')
    url = f"https://radar.weather.gov/?settings=v1_{encoded_settings}"
    return url

def fetch_lcl_radar_images(driver, num_images=10):
    global lcl_radar_zoom_clicks
    try:
        coordinates = fetch_lcl_radar_coordinates(radar_identifier)
        if not coordinates:
            print("Failed to fetch radar coordinates.")
            return []

        lon, lat = coordinates
        url = generate_lcl_radar_url(radar_identifier, [lon, lat], 7.6 + lcl_radar_zoom_clicks)
        
        driver.get(url)
        time.sleep(4)  # Allow page to load

        # Set up the UI for screenshot (including hiding non-relevant UI elements)
        if not setup_ui_for_screenshot(driver):
            print("Failed to setup UI for screenshots.")
            return []

        # Now hide additional UI elements that could interfere with screenshots
        if not hide_additional_ui_elements(driver):
            print("Failed to hide UI elements.")
            return []

        images = capture_lcl_radar_screenshots(driver, num_images=num_images)
        return images if images else []

    except TimeoutException as e:
        print(f"TimeoutException: Failed to fetch lcl radar images: {e}")
        driver.save_screenshot('debug_screenshot_navigation.png')
        return []

    except Exception as e:
        print(f"Unexpected error during image fetching: {e}")
        return []

def setup_ui_for_screenshot(driver):
    try:
        # Click the three dots button to open additional settings
        three_dots_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/main/div/div/div[1]/div[2]/div/div[2]/div[4]/span'))
        )
        three_dots_button.click()
        time.sleep(2)

        # Adjust the first slider
        if not adjust_slider(driver, '//*[@id="app"]/main/div/div/div[1]/div[3]/div/div[3]/div[2]/div[2]/div/div/div/div[1]', '//*[@id="app"]/main/div/div/div[1]/div[3]/div/div[3]/div[2]/div[2]/div/div/div/div[2]'):
            return False

        # Adjust the second slider
        if not adjust_slider(driver, '//*[@id="app"]/main/div/div/div[1]/div[3]/div/div[3]/div[5]/div[2]/div/div/div/div[1]', '//*[@id="app"]/main/div/div/div[1]/div[3]/div/div[3]/div[5]/div[2]/div/div/div/div[2]'):
            return False

        # Click the close button
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/main/div/div/div[1]/div[4]/input'))
        )
        close_button.click()
        time.sleep(2)

        return True
    except Exception as e:
        print(f"Failed UI interaction setup: {e}")
        return False

def hide_additional_ui_elements(driver):
    wait = WebDriverWait(driver, 10)
    try:
        # Hide the menu agendas
        header_element = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/main/div/div/div[1]/div[2]/div'))
        )
        driver.execute_script("arguments[0].style.display='none'", header_element)

        # Hide the primary menu
        primary_menu = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/main/div/div/div[1]'))
        )
        driver.execute_script("arguments[0].style.display='none'", primary_menu)

        # Hide the two buttons in the banner
        buttons_to_hide = driver.find_element(By.XPATH, '//*[@id="app"]/header/div/div[3]')
        driver.execute_script("arguments[0].style.display='none'", buttons_to_hide)
        return True
    except Exception as e:
        print(f"Could not hide additional UI elements: {e}")
        return False

def display_lcl_radar_images(images):
    global label_lcl_radar
    # Ensure previous label is removed
    if label_lcl_radar and label_lcl_radar.winfo_exists():
        label_lcl_radar.grid_forget()

    label_lcl_radar = tk.Label(scraped_frame)
    label_lcl_radar.grid(row=1, column=0, padx=130, pady=80, sticky="se")

    cycle_count = 0
    max_cycles = 3

    def update_frame(index):
        global img_label_national_radar, baro_img_label, national_radar_hidden
        nonlocal cycle_count

        if not national_radar_hidden and img_label_national_radar and img_label_national_radar.winfo_exists():
            img_label_national_radar.grid_forget()
            national_radar_hidden = True

        if baro_img_label and baro_img_label.winfo_exists():
            baro_img_label.grid_forget()

        frame = images[index]
        resized_image = frame.resize((850, 515), Image.LANCZOS)
        photo = ImageTk.PhotoImage(resized_image)
        label_lcl_radar.config(image=photo)
        label_lcl_radar.image = photo
        next_index = (index + 1) % len(images)

        if next_index == 0:
            cycle_count += 1
            if cycle_count < max_cycles:
                scraped_frame.after(1000, update_frame, next_index)
            elif cycle_count == max_cycles:
                scraped_frame.after(5000, lambda: hide_local_radar_loop(label_lcl_radar))
        else:
            scraped_frame.after(1000, update_frame, next_index)

    update_frame(0)

def hide_local_radar_loop(label_lcl_radar=None):
    global box_variables

    if label_lcl_radar and box_variables[3] != 1 and box_variables[5] != 1 and label_lcl_radar.winfo_exists():
        label_lcl_radar.grid_forget()

    show_lightning()

def display_local_radar_loop(queue):
    driver = lcl_radar_selenium()
    if driver is None:
        print("Failed to start Selenium WebDriver in lcl radar. Skipping lcl radar image.")
        hide_local_radar_loop()
        return

    try:
        images = fetch_lcl_radar_images(driver, num_images=10)
        if not images:
            print("No valid frames captured in lcl radar.")
            hide_local_radar_loop()

        else:
            queue.put(images)
    except Exception as e:
        print(f"Error during lcl radar image fetch: {e}")
        hide_local_radar_loop()
    finally:
        driver.quit()

def lcl_radar_process_queue(queue):
    try:
        images = queue.get_nowait()
        if images:
            display_lcl_radar_images(images)
        else:
            #show_lightning()
            hide_local_radar_loop()
    except Empty:
        scraped_frame.after(100, lcl_radar_process_queue, queue)

def lcl_radar_start_scraping(queue):
    driver = lcl_radar_selenium()
    if driver:
        try:
            images = fetch_lcl_radar_images(driver, num_images=10)
            if images:
                queue.put(images)
        finally:
            driver.quit()

def show_local_radar_loop():
    global label_lcl_radar, box_variables

    # Ensure previous label is removed
    if label_lcl_radar and label_lcl_radar.winfo_exists():
        label_lcl_radar.grid_forget()

    if box_variables[2] == 1 and not refresh_flag:
        image_queue = Queue()
        scraping_thread = threading.Thread(target=display_local_radar_loop, args=(image_queue,))
        scraping_thread.start()
        scraped_frame.after(100, lcl_radar_process_queue, image_queue)
    else:
        show_lightning()

# Code for lightning
#@profile
def capture_screenshot(lightning_url):
    global img_tk_lightning, label_lcl_radar, img_label_national_radar, lightning_max_retries, baro_img_label

    img_label = None  # Initialize img_label to avoid UnboundLocalError

    try:
        driver = None  # Ensure driver is initialized as None
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            driver = webdriver.Chrome(service=Service("chromedriver"), options=chrome_options)
            driver.get(lightning_url)

            wait = WebDriverWait(driver, 15)
            got_it_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='cc-btn cc-dismiss']")))
            got_it_button.click()
            time.sleep(5)

            lightning_screenshot = driver.get_screenshot_as_png()

            try:
                lightning_screenshot_image = Image.open(BytesIO(lightning_screenshot))
                crop_box = (46, 0, lightning_screenshot_image.width, lightning_screenshot_image.height - 90)
                lightning_screenshot_crop = lightning_screenshot_image.crop(crop_box)
                target_width, target_height = 800, 515
                lightning_screenshot_resized = lightning_screenshot_crop.resize((target_width, target_height), Image.LANCZOS)

                del lightning_screenshot_image
                del lightning_screenshot_crop
                del lightning_screenshot

                if box_variables[2] == 1 and label_lcl_radar and label_lcl_radar.winfo_exists():
                    label_lcl_radar.grid_forget()
                if img_label_national_radar and img_label_national_radar.winfo_exists():
                    img_label_national_radar.grid_forget()
                if baro_img_label and baro_img_label.winfo_exists():
                    baro_img_label.grid_forget()

                img_tk_lightning = ImageTk.PhotoImage(lightning_screenshot_resized)
                img_label = tk.Label(scraped_frame, image=img_tk_lightning)
                img_label.image = img_tk_lightning
                img_label.grid(row=1, column=0, padx=150, pady=80, sticky="se")
                root.update()
                root.after(15000, lambda: hide_lightning(img_label))

            except Exception as img_e:
                print(f"Image processing failed for lightning: {img_e}")
                cleanup_lightning_display(img_label)
        
        except (TimeoutException, NoSuchElementException, WebDriverException, urllib3.exceptions.ProtocolError) as e:
            print(f"Selenium operation or network failed for lightning: {e}")
            cleanup_lightning_display(img_label)
        
        finally:
            if driver:
                driver.quit()

    except Exception as e:
        print(f"Unexpected error in capture_screenshot: {e}")
        cleanup_lightning_display(img_label)

def cleanup_lightning_display(img_label):
    """
    A function to handle all cleanup tasks when there's an error or when the image cannot be displayed.
    """
    if img_label and img_label.winfo_exists():
        img_label.grid_forget()
    if box_variables[2] == 1 and label_lcl_radar and label_lcl_radar.winfo_exists():
        label_lcl_radar.grid_forget()
    if img_label_national_radar and img_label_national_radar.winfo_exists():
        img_label_national_radar.grid_forget()
    if baro_img_label and baro_img_label.winfo_exists():
        baro_img_label.grid_forget()

    # Call the function to hide the lightning image and proceed to the next one.
    hide_lightning(img_label)


def display_lightning():
    lightning_url = (
        "https://www.lightningmaps.org/?lang=en#m=oss;t=1;s=200;o=0;b=0.00;ts=0;d=2;dl=2;dc=0;y=" +
        str(lightning_lat) + ";x=" + str(lightning_lon) + ";z=6;"
    )
    capture_screenshot(lightning_url)

def hide_lightning(img_label):
    global img_tk_lightning  
    img_tk_lightning = None  
    
    if img_label and img_label.winfo_exists():
        img_label.grid_forget()

    show_national_satellite()

def show_lightning():
    if box_variables[3] == 1 and not refresh_flag:
        lightning_thread = threading.Thread(target=display_lightning)
        lightning_thread.start()
    else:
        show_national_satellite()
        
# Code for national satellite
#@profile
def display_national_satellite():
    global img_tk_satellite, last_national_satellite_scrape_time, resized_image, img_label_national_satellite
    global label_lcl_radar
    # Initialize img_label_national_satellite as None
    img_label_national_satellite = None

    try:
        current_time = time.time()
        if last_national_satellite_scrape_time is None or (current_time - last_national_satellite_scrape_time) >= 600:

            # URL to scrape
            #us_sat_url = "https://cdn.star.nesdis.noaa.gov/GOES16/ABI/CONUS/GEOCOLOR/625x375.jpg"
            # supposedly this code can properly scrape and adjust an image with higher resolution
            us_sat_url = "https://cdn.star.nesdis.noaa.gov/GOES16/ABI/CONUS/GEOCOLOR/1250x750.jpg"
            
            # Set the desired width and height for the tkinter window
            window_width = 800
            window_height = 518

            # Configure Chrome options for headless mode
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")

            # Use the system-installed ChromeDriver executable
            driver = webdriver.Chrome(service=Service("chromedriver"), options=chrome_options)

            # Navigate to the URL
            driver.get(us_sat_url)

            # Capture a screenshot of the entire page
            satellite_screenshot = driver.get_screenshot_as_png()

            # Close the WebDriver
            driver.quit()

            # Open the screenshot using PIL
            satellite_screenshot_image = Image.open(BytesIO(satellite_screenshot))

            # Define a dark color threshold (adjust this value if needed)
            dark_color_threshold = 50

            # Convert the image to grayscale
            gray_image = satellite_screenshot_image.convert('L')

            # Find bounding box of non-dark region
            non_dark_region = gray_image.point(lambda x: 0 if x < dark_color_threshold else 255, '1').getbbox()

            # Crop the image to the non-dark region
            cropped_image = satellite_screenshot_image.crop(non_dark_region)

            # Resize the cropped image to fit the tkinter window
            resized_image = cropped_image.resize((window_width, window_height), Image.LANCZOS)
            
            # Set the last scrape time to the current time
            last_national_satellite_scrape_time = current_time

            # Explicitly set the reference to None before creating a new PhotoImage
            img_tk_satellite = None

            # get rid of saved images intended to fill gaps
                
            if label_lcl_radar and label_lcl_radar.winfo_exists():
                label_lcl_radar.grid_forget()

            # Create a new PhotoImage object
            img_tk_satellite = ImageTk.PhotoImage(resized_image)

            # Check if the label already exists, if not, create it
            if img_label_national_satellite is None:
                img_label_national_satellite = tk.Label(scraped_frame, image=img_tk_satellite)
                img_label_national_satellite.grid(row=1, column=0, padx=150, pady=75, sticky="se")
            else:
                # Update the image on the existing label
                img_label_national_satellite.config(image=img_tk_satellite)
                img_label_national_satellite.image = img_tk_satellite

            root.update()  # Update the tkinter window to show the image

            # Use after() to schedule hiding the image after some seconds
            root.after(16000, lambda: hide_image(img_label_national_satellite))

        else:
            # If less than 10 minutes have passed, still display the most recently scraped image

            # Check if the label already exists, if not, create it
            if img_label_national_satellite is None:
                img_label_national_satellite = tk.Label(scraped_frame, image=img_tk_satellite)
                img_label_national_satellite.grid(row=1, column=0, padx=150, pady=75, sticky="se")
            else:
                # Update the image on the existing label
                img_label_national_satellite.config(image=img_tk_satellite)
                img_label_national_satellite.image = img_tk_satellite

            root.update()  # Update the tkinter window to show the image

            # Use after() to schedule hiding the image after some seconds
            root.after(16000, lambda: hide_image(img_label_national_satellite))

    except Exception as e:
        print(f"An error occurred: {e}")
        # Ensure cleanup on error
        if img_label_national_satellite and img_label_national_satellite.winfo_exists() and box_variables[5] != 1:
            img_label_national_satellite.grid_forget()
            #img_label_national_satellite = None
        hide_image(img_label_national_satellite)

def hide_image(img_label_national_satellite):
    
    if img_label_national_satellite and box_variables[5] != 1 and img_label_national_satellite.winfo_exists():
        img_label_national_satellite.grid_forget()
        img_label_national_satellite = None
    show_reg_sat_loop()
    
#@profile
def show_national_satellite():
    global label_lcl_radar, img_label_national_radar, baro_img_label
    #global refresh_flag
    if box_variables[4] == 1 and refresh_flag == False:
        # added this block 7/25/24 to ensure fillers are _forget
        if label_lcl_radar and label_lcl_radar.winfo_exists():
            label_lcl_radar.grid_forget()
            
        if img_label_national_radar and img_label_national_radar.winfo_exists():
            img_label_national_radar.grid_forget()
        
        if baro_img_label and baro_img_label.winfo_exists():
            baro_img_label.grid_forget()
                    
        display_national_satellite()
    else:
        show_reg_sat_loop()

# Code for regional radar loop
def get_reg_sat_settings():
    selected_index = reg_sat_choice_variables.index(1)
    
    sat_goes = 16  # Default value
    sat_reg = 'unknown'  # Default value

    if selected_index == 0:
        sat_goes = 18
        sat_reg = 'pnw'
    elif selected_index == 1:
        sat_goes = 18
        sat_reg = 'psw'
    elif selected_index == 2:
        sat_goes = 16
        sat_reg = 'nr'
    elif selected_index == 3:
        sat_goes = 16
        sat_reg = 'sr'
    elif selected_index == 4:
        sat_goes = 16
        sat_reg = 'umv'
    elif selected_index == 5:
        sat_goes = 16
        sat_reg = 'smv'
    elif selected_index == 6:
        sat_goes = 16
        sat_reg = 'cgl'
    elif selected_index == 7:
        sat_goes = 16
        sat_reg = 'sp'
    elif selected_index == 8:
        sat_goes = 16
        sat_reg = 'ne' 
    elif selected_index == 9:
        sat_goes = 16
        sat_reg = 'se'
    elif selected_index == 10:
        sat_goes = 18
        sat_reg = 'wus' 
    elif selected_index == 11:
        sat_goes = 16
        sat_reg = 'eus'

    return sat_goes, sat_reg


# Function to generate URLs with different time codes
def generate_sat_reg_urls(base_url, num_images, sat_goes, sat_reg):
    urls = []
    current_time_utc = datetime.utcnow()

    for _ in range(num_images):
        if reg_sat_choice_variables[10] == 1:
            time_offset = 20
            time_format = "%H%M"
            image_suffix = "500x500.jpg"
            valid_minutes = {0}
        elif reg_sat_choice_variables[11] == 1:
            time_offset = 10
            time_format = "%H%M"
            image_suffix = "500x500.jpg"
            valid_minutes = {6}
        else:
            time_offset = 10
            time_format = "%H%M"
            image_suffix = "600x600.jpg"
            valid_minutes = {6}

        current_time_utc -= timedelta(minutes=time_offset)
        while current_time_utc.minute % 10 not in valid_minutes:
            current_time_utc -= timedelta(minutes=1)

        year = current_time_utc.year
        day_of_year = current_time_utc.timetuple().tm_yday
        time_code = current_time_utc.strftime(time_format)

        url = f"{base_url}{year}{day_of_year:03d}{time_code}_GOES{sat_goes}-ABI-{sat_reg}-GEOCOLOR-{image_suffix}"
        urls.append(url)
        current_time_utc -= timedelta(minutes=5)

    return urls

def trim_near_black_borders_reg_sat(img, threshold=30):
    try:
        grayscale_img = img.convert("L")
    except Exception as e:
        print(f"Error converting image to grayscale in reg_sat: {e}")
        return img

    try:
        binary_img = grayscale_img.point(lambda p: 255 if p > threshold else 0, '1')
    except Exception as e:
        print(f"Error creating binary image in reg_sat: {e}")
        return img

    try:
        bbox = binary_img.getbbox()
        if bbox:
            return img.crop(bbox)
    except Exception as e:
        print(f"Error cropping the image in reg_sat: {e}")

    return img

def scrape_reg_sat_images(urls, sat_goes, sat_reg):
    global img_label_satellite
    images = []

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
        
    try:
        driver = webdriver.Chrome(service=Service("chromedriver"), options=chrome_options)
    except Exception as e:
        print(f"Failed to initialize the driver in reg sat: {e}")
        return

    try:
        for url in reversed(urls):
            try:
                driver.get(url)
                if "404 Not Found" in driver.title:
                    print(f"No image found for URL in reg sat: {url}")
                    continue

                screenshot = driver.get_screenshot_as_png()
                screenshot = Image.open(BytesIO(screenshot))
                screenshot = trim_near_black_borders_reg_sat(screenshot)
                target_size = (515, 515)
                screenshot = screenshot.resize(target_size, Image.LANCZOS)
                image = ImageTk.PhotoImage(screenshot)
                images.append(image)
            except Exception as e:
                print(f"Error processing image from URL {url} in reg sat: {e}")

    finally:
        driver.quit()

    display_reg_sat_loop(images)

tkinter_lock = threading.Lock()

def display_reg_sat_loop(images):
    global img_label_satellite, img_label_national_satellite, label_lcl_radar, img_label_national_radar, baro_img_label

    def cleanup_labels():
        
        if img_label_national_satellite and img_label_national_satellite.winfo_exists():
            img_label_national_satellite.grid_forget()
            
        if label_lcl_radar and label_lcl_radar.winfo_exists():
            label_lcl_radar.grid_forget()
            
        if img_label_national_radar and img_label_national_radar.winfo_exists():
            img_label_national_radar.grid_forget()
        
        if baro_img_label and baro_img_label.winfo_exists():
            baro_img_label.grid_forget()

    cleanup_labels()

    try:
        if img_label_satellite is None or not img_label_satellite.winfo_exists():
            img_label_satellite = tk.Label(scraped_frame)
            img_label_satellite.grid(row=1, column=0, padx=250, pady=80, sticky='se')

        idx = 0
        reg_sat_num_cycles = 0

        def update_image():
            nonlocal idx, reg_sat_num_cycles
            try:
                if idx < len(images):
                    tkinter_lock.acquire()
                    try:
                        img_label_satellite.config(image=images[idx])
                    finally:
                        tkinter_lock.release()
                    idx += 1
                    scraped_frame.after(100, update_image)
                elif reg_sat_num_cycles == 5:
                    scraped_frame.after(2000, hide_reg_sat_loop)
                else:
                    scraped_frame.after(2000, reset_and_continue)

            except Exception as e:
                print(f"Error updating image in reg sat: {e}")
                cleanup_labels()
                #scraped_frame.after(1000, show_national_sfc_map)
                scraped_frame.after(1000, hide_reg_sat_loop)

        def reset_and_continue():
            nonlocal idx, reg_sat_num_cycles
            idx = 0
            reg_sat_num_cycles += 1
            update_image()

        if images:
            scraped_frame.after(0, update_image)
        else:
            print("No images to display for regional satellite.")
            cleanup_labels()
            #show_national_sfc_map()
            hide_reg_sat_loop()

    except Exception as e:
        print(f"Error setting up image loop in reg sat: {e}")
        cleanup_labels()
        #show_national_sfc_map()
        hide_reg_sat_loop()

def hide_reg_sat_loop():
    global img_label_satellite
    if img_label_satellite:
        img_label_satellite.grid_forget()
        img_label_satellite = None
                
    show_national_sfc_map()

def threaded_satellite_scraping():
    base_url = "https://cdn.star.nesdis.noaa.gov/GOES{}/ABI/SECTOR/{}/GEOCOLOR/"
    num_images_to_scrape = 12
    sat_goes, sat_reg = get_reg_sat_settings()
    urls_to_scrape = generate_sat_reg_urls(base_url.format(sat_goes, sat_reg), num_images_to_scrape, sat_goes, sat_reg)

    scrape_reg_sat_images(urls_to_scrape, sat_goes, sat_reg)

def show_reg_sat_loop():
    if box_variables[5] == 1 and not refresh_flag:
        scraping_thread = threading.Thread(target=threaded_satellite_scraping)
        scraping_thread.start()
    else:
        show_national_sfc_map()

#@profile
def display_national_sfc_map():
    try:
        global last_national_sfc_map_scrape_time
        global img_tk_sfc_map  # Declare img_tk_sfc_map as a global variable
        global img_label_sfc_map  # Declare img_label_sfc_map as a global variable

        # Check if an hour has passed since the last scrape or if it's the first time
        current_time = datetime.now()
        if last_national_sfc_map_scrape_time is None or (current_time - last_national_sfc_map_scrape_time).total_seconds() >= 3600:

            sfc_url = 'https://www.wpc.ncep.noaa.gov/basicwx/92fndfd.jpg'
            response = requests.get(sfc_url)

            if response.status_code == 200:
                img_data = response.content
                img = Image.open(BytesIO(img_data))
                img = img.resize((850, 520))
                img_tk = ImageTk.PhotoImage(img)

                # Set the last scrape time to the current time
                last_national_sfc_map_scrape_time = current_time

                # Explicitly set the reference to None before creating a new PhotoImage
                img_tk_sfc_map = None
                
                # Create a new PhotoImage object
                img_tk_sfc_map = img_tk
                
                img_label_sfc_map = tk.Label(scraped_frame, image=img_tk_sfc_map)
                img_label_sfc_map.image = img_tk_sfc_map
                img_label_sfc_map.grid(row=1, column=0, padx=150, pady=70, sticky="se")

                root.update()

                # Use after() to schedule hiding the image after some seconds
                root.after(12000, lambda: hide_national_sfc_map(img_label_sfc_map))

        else:
            # If less than an hour has passed, still display the most recently scraped image
            img_label_sfc_map = tk.Label(scraped_frame, image=img_tk_sfc_map)
            img_label_sfc_map.image = img_tk_sfc_map
            img_label_sfc_map.grid(row=1, column=0, padx=150, pady=70, sticky="se")

            root.update()

            # Use after() to schedule hiding the image after some seconds
            root.after(12000, lambda: hide_national_sfc_map(img_label_sfc_map))

    except Exception as e:
        print("National surface map scrape error:", e, "on way to show_station_models")
        #show_station_models()
        hide_national_sfc_map(img_label_sfc_map)
#@profile
def hide_national_sfc_map(img_label_sfc_map):
    
    if img_label_sfc_map and box_variables[7] != 1 and img_label_sfc_map.winfo_exists():
        img_label_sfc_map.grid_forget()

    show_station_models()
    
#@profile
def show_national_sfc_map():
    global img_label_national_satellite, label_lcl_radar, img_label_national_radar, baro_img_label 
    #global refresh_flag
    if box_variables[6] == 1 and refresh_flag == False:
        # Move the variable assignment here
        
        if img_label_national_satellite and img_label_national_satellite.winfo_exists():
            img_label_national_satellite.grid_forget()
    
        if label_lcl_radar and label_lcl_radar.winfo_exists():
            label_lcl_radar.grid_forget()
            
        if img_label_national_radar and img_label_national_radar.winfo_exists():
            img_label_national_radar.grid_forget()
        
        if baro_img_label and baro_img_label.winfo_exists():
            baro_img_label.grid_forget()
        
        last_national_sfc_map_scrape_time = None

        display_national_sfc_map()
    else:
        show_station_models()
        
#@profile        
def display_station_models():
    global station_model_url, zoom_plot, img_tk_station_model, last_station_model_scrape_time
    global img_label_sfc_map, img_label_national_satellite, label_lcl_radar, img_label_national_radar, baro_img_label

    timeout_seconds = 30
    current_timestamp = datetime.now()
    current_time = time.time()

    # Initialize img_label to None to prevent UnboundLocalError
    img_label = None

    try:
        # Check if 3 minutes have passed since the last scrape or if it's the first time
        if last_station_model_scrape_time is None or (current_time - last_station_model_scrape_time) >= 180:
            # URL of the website to capture the station model map
            base_url = f"http://www.wrh.noaa.gov/map/?&zoom={zoom_plot}&scroll_zoom=false"
            other_params = "&boundaries=false,false,false,false,false,false,false,false,false,false,false&tab=observation&obs=true&obs_type=weather&elements=temp,dew,wind,gust,slp"
            lat_lon_params = "&center=" + str(station_plot_lat) + "," + str(station_plot_lon)
            station_model_url = base_url + lat_lon_params + other_params

            # Configure Chrome options for headless mode
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")

            # Set desired aspect ratio and window size
            desired_aspect_ratio = 1.72
            desired_width = 900
            desired_height = int(desired_width / desired_aspect_ratio)
            chrome_options.add_argument(f"--window-size={desired_width},{desired_height}")

            driver = webdriver.Chrome(service=Service("chromedriver"), options=chrome_options)
            driver.get(station_model_url)

            # Wait and click the close button
            close_button_locator = (By.CSS_SELECTOR, "a.panel-close")
            wait = WebDriverWait(driver, timeout_seconds)
            wait.until(EC.element_to_be_clickable(close_button_locator)).click()

            time.sleep(10)

            # Capture screenshot and process image
            station_model_screenshot = driver.get_screenshot_as_png()
            driver.quit()

            station_model_image = Image.open(io.BytesIO(station_model_screenshot))
            station_model_image_crop = station_model_image.crop((42, 0, station_model_image.width, station_model_image.height))

            # Set the last scrape time
            last_station_model_scrape_time = current_time

            # Cleanup previous images
            cleanup_previous_station_models_images()

            # Create the new PhotoImage object and assign to img_label
            img_tk_station_model = ImageTk.PhotoImage(station_model_image_crop)
            img_label = tk.Label(scraped_frame, image=img_tk_station_model)
            img_label.image = img_tk_station_model
            img_label.grid(row=1, column=0, padx=150, pady=73, sticky="se")

            root.update()
            root.after(20000, lambda: hide_station_models(img_label))

        else:
            # If less than 3 minutes have passed, reuse the existing image
            cleanup_previous_station_models_images()

            img_label = tk.Label(scraped_frame, image=img_tk_station_model)
            img_label.image = img_tk_station_model
            img_label.grid(row=1, column=0, padx=150, pady=73, sticky="se")

            root.update()
            root.after(20000, lambda: hide_station_models(img_label))

    except Exception as e:
        print("Error displaying station models:", e)
        cleanup_previous_station_models_images()

        # Gracefully proceed even after an error
        if img_label:
            hide_station_models(img_label)

def cleanup_previous_station_models_images():
    """Helper function to clean up any previously displayed station models images."""
    if img_label_sfc_map and img_label_sfc_map.winfo_exists():
        img_label_sfc_map.grid_forget()
    if img_label_national_satellite and img_label_national_satellite.winfo_exists():
        img_label_national_satellite.grid_forget()
    if label_lcl_radar and label_lcl_radar.winfo_exists():
        label_lcl_radar.grid_forget()
    if img_label_national_radar and img_label_national_radar.winfo_exists():
        img_label_national_radar.grid_forget()
    if baro_img_label and baro_img_label.winfo_exists():
        baro_img_label.grid_forget()

def hide_station_models(img_label):
    """Function to hide the station model image after a delay."""
    if img_label and img_label.winfo_exists():
        img_label.grid_forget()
        if hasattr(img_label, 'image'):
            img_label.image = None  # Clear image reference

    show_sounding()

def show_station_models():
    """Starts the display of station models in a new thread to avoid blocking the GUI."""
    if box_variables[7] == 1 and not refresh_flag:
        threading.Thread(target=display_station_models).start()
    else:
        cleanup_previous_station_models_images()
        show_sounding()

def display_sounding():
    
    import datetime
    from datetime import timedelta
    
    global last_sounding_scrape_time, sonde_letter_identifier, img_tk_sounding

    try:
        # Get current UTC time and date
        scrape_now = datetime.datetime.utcnow()  # Corrected usage of datetime here

        # Check if 10 min has passed since the last scrape or if it's the first time
        if last_sounding_scrape_time is None or (scrape_now - last_sounding_scrape_time).total_seconds() >= 600:

            # Determine the most recent significant time
            if scrape_now.hour < 12:
                hour_str = "00"
                date = scrape_now.replace(hour=0, minute=0, second=0, microsecond=0)
            else:
                hour_str = "12"
                date = scrape_now.replace(hour=12, minute=0, second=0, microsecond=0)

            date_str = date.strftime('%y%m%d')
            month_str = scrape_now.strftime("%b").capitalize()
            day_str = str(scrape_now.day)

            # Construct initial image URL
            sonde_sound_url = f"https://www.spc.noaa.gov/exper/soundings/{date_str}{hour_str}_OBS/{sonde_letter_identifier}.gif"

            # Attempt to fetch the image
            sonde_sound_response = requests.get(sonde_sound_url)

            # Retry with a different time if the initial attempt fails
            if sonde_sound_response.status_code != 200:
                if hour_str == "00":
                    date -= timedelta(days=1)
                    hour_str = "12"
                else:
                    date = date.replace(hour=0)
                    hour_str = "00"
                date_str = date.strftime('%y%m%d')
                sonde_sound_url = f"https://www.spc.noaa.gov/exper/soundings/{date_str}{hour_str}_OBS/{sonde_letter_identifier}.gif"
                print("Retry. sonde_sound_url: ", sonde_sound_url)
                sonde_sound_response = requests.get(sonde_sound_url)

            # Continue processing the image if it was successfully retrieved
            if sonde_sound_response.status_code == 200:
                sonde_sound_img = Image.open(BytesIO(sonde_sound_response.content))
                crop_box = (0, 250, sonde_sound_img.width, sonde_sound_img.height)
                sonde_sound_img = sonde_sound_img.crop(crop_box)
                sonde_sound_img.save('sonde_sound.png', 'PNG')
                sonde_sound_img = Image.open('sonde_sound.png')
                sonde_sound_img = sonde_sound_img.convert('RGBA')
                aspect_ratio = sonde_sound_img.width / sonde_sound_img.height
                desired_width = 880
                desired_height = int(desired_width / aspect_ratio * 1.18)
                sonde_sound_img = sonde_sound_img.resize((desired_width, desired_height), Image.LANCZOS)
                sonde_sound_img_with_white_bg = Image.new('RGBA', (int(sonde_sound_img.width), int(sonde_sound_img.height)), (255, 255, 255, 255))
                sonde_sound_img_with_white_bg.paste(sonde_sound_img, (0, 0), sonde_sound_img)
                draw = ImageDraw.Draw(sonde_sound_img_with_white_bg)
                font_size = 48
                font = ImageFont.load_default()
                text = f'{sonde_letter_identifier}\n{month_str} {day_str} {hour_str} GMT'
                text_position = (300, 70)
                draw.text(text_position, text, fill=(0, 0, 0), font=font)
                img_tk_sonde_sounding = ImageTk.PhotoImage(sonde_sound_img_with_white_bg)
                last_sonde_sounding_scrape_time = scrape_now
                img_label_sounding = tk.Label(scraped_frame, image=img_tk_sonde_sounding)
                img_label_sounding.image = img_tk_sonde_sounding
                img_label_sounding.grid(row=1, column=0, padx=120, pady=90, sticky="se")
                root.update()
                root.after(20000, lambda: hide_sounding(img_label_sounding))
        else:
            img_label_sounding = tk.Label(scraped_frame, image=img_tk_sonde_sounding)
            img_label_sounding.image = img_tk_sonde_sounding
            img_label_sounding.grid(row=1, column=0, padx=115, pady=90, sticky="se")
            root.update()
            root.after(20000, lambda: hide_sounding(img_label_sounding))

    except Exception as e:
        print("Scrape, Save and Display sonde sounding error:", e)
        show_vorticity()  # Assuming show_vorticity is another function you want to fallback to


def hide_sounding(img_label_sounding):
    if img_label_sounding and img_label_sounding.winfo_exists():
        img_label_sounding.grid_forget()

    show_vorticity()

def show_sounding():
    #global refresh_flag
    # Is the sounding a user choice?
    
    #on 7/14/24 include block to _forget labels used as gaps fillers to try to eliminate double imaging
    # will include this before baro is displayed too
    global img_label_national_satellite, label_lcl_radar, img_label_national_radar, img_label_sfc_map, bar_img_label
    
    if img_label_national_satellite and img_label_national_satellite.winfo_exists():
        img_label_national_satellite.grid_forget() 
    
    if label_lcl_radar and label_lcl_radar.winfo_exists():
        label_lcl_radar.grid_forget()
        
    if img_label_national_radar and img_label_national_radar.winfo_exists():
        img_label_national_radar.grid_forget()
    
    if baro_img_label and baro_img_label.winfo_exists():
        baro_img_label.grid_forget()
        
    if img_label_sfc_map and img_label_sfc_map.winfo_exists():
        img_label_sfc_map.grid_forget()
        
    if box_variables[8] == 1 and refresh_flag == False:
        display_sounding()
    else:
        show_vorticity()

def display_vorticity():
    try:
        global vort_img_tk  # Declare vort_img_tk as a global variable
        global last_vorticity_scrape_time

        current_time = datetime.utcnow()

        # Check if an hour has passed since the last scrape or if it's the first time
        if last_vorticity_scrape_time is None or (current_time - last_vorticity_scrape_time).total_seconds() >= 3600:

            times_intervals = [(2, 8), (8, 14), (14, 20), (20, 26)]
            XX_values = ['00', '06', '12', '18']
            XX = ''

            for count, (start_hour, end_hour) in enumerate(times_intervals):
                if start_hour <= current_time.hour < end_hour:
                    XX = XX_values[count]
                    break

            if not XX:
                XX = '18'

            vort_url = f'https://mag.ncep.noaa.gov/data/nam/{XX}/nam_namer_000_500_vort_ht.gif'
            vort_response = requests.get(vort_url)
            vort_content = vort_response.content

            def convert_gif_to_jpg(gif_data):
                gif = Image.open(BytesIO(gif_data))
                gif = gif.convert('RGB')
                output = BytesIO()
                gif.save(output, format="JPEG", quality=95, optimize=True)
                return output.getvalue()

            jpg_data = convert_gif_to_jpg(vort_content)
            vort_img = Image.open(BytesIO(jpg_data))
            vort_img = vort_img.resize((820, 510), Image.LANCZOS)
            new_vort_img_tk = ImageTk.PhotoImage(vort_img)

            # Set the last scrape time to the current time
            last_vorticity_scrape_time = current_time

            # Explicitly set the reference to None before creating a new PhotoImage
            vort_img_tk = None

            # Create a new PhotoImage object
            vort_img_tk = new_vort_img_tk

            vort_img_label = tk.Label(scraped_frame, image=vort_img_tk)
            vort_img_label.image = vort_img_tk
            vort_img_label.grid(row=1, column=0, padx=150, pady=85, sticky="se")

            root.update()
            root.after(12000, lambda: hide_vorticity(vort_img_label))

        else:
            # If less than an hour has passed, still display the most recently scraped image
            vort_img_label = tk.Label(scraped_frame, image=vort_img_tk)
            vort_img_label.image = vort_img_tk
            vort_img_label.grid(row=1, column=0, padx=150, pady=85, sticky="se")

            root.update()  # Update the tkinter window to show the image

            # Use after() to schedule hiding the image after some seconds
            root.after(12000, lambda: hide_vorticity(vort_img_label))

    except Exception as e:
        print("Scrape, Save, and Display 500mb vort analysis", e, "on way to display_baro_trace")
        #display_baro_trace()
        hide_vorticity(vort_img_label)

def hide_vorticity(vort_img_label):
    global iterate_flag  # Declare iterate_flag as global 
    if vort_img_label and vort_img_label.winfo_exists():
        vort_img_label.grid_forget()

    display_baro_trace()

def show_vorticity():
    #global refresh_flag  # Declare refresh_flag as global
    if box_variables[9] == 1 and refresh_flag == False:
        display_vorticity()
    else:        
        display_baro_trace()

def display_baro_trace():
    global baro_img_tk  # Declare baro_img_tk as a global variable
    global baro_img_label #to manage transition from baro to lcl radar
    
    #on 7/14/24 include block to _forget labels used as gaps fillers to try to eliminate double imaging
    # will include this before sounding is displayed too
    
    global img_label_national_satellite, label_lcl_radar, img_label_national_radar, img_label_sfc_map
    
    if img_label_national_satellite and img_label_national_satellite.winfo_exists():
        img_label_national_satellite.grid_forget() 
    
    if label_lcl_radar and label_lcl_radar.winfo_exists():
        label_lcl_radar.grid_forget()
        
    if img_label_national_radar and img_label_national_radar.winfo_exists():
        img_label_national_radar.grid_forget()
    
    if baro_img_label and baro_img_label.winfo_exists():
        baro_img_label.grid_forget()
        
    if img_label_sfc_map and img_label_sfc_map.winfo_exists():
        img_label_sfc_map.grid_forget()
    
    # destroy previous baro_img_label
    if baro_img_label and baro_img_label.winfo_exists():
        baro_img_label.destroy() # why destroy and not _forget? wondering on 7/25/24
    
    try:
        # Path to the image on the Raspberry Pi
        image_path = '/home/santod/baro_trace.png'

        # Open the image using PIL
        img = Image.open(image_path)

        # Crop the left side of the image
        left_crop_width = 100  # Adjust this value based on your requirements
        img = img.crop((left_crop_width, 0, img.width, img.height))

        # Resize the image to fit the window
        img = img.resize((1000, 560), Image.LANCZOS)

        # Keep a reference to the image to prevent garbage collection
        baro_img_tk = ImageTk.PhotoImage(img)

        # Create a label to display the image
        baro_img_label = tk.Label(scraped_frame, image=baro_img_tk, bd=0)  # Set the background color to white
        baro_img_label.image = baro_img_tk
        baro_img_label.grid(row=1, column=0, padx=110, pady=30, sticky="se")

        root.update()  # Update the tkinter window to show the image

        # Use after() to schedule hiding the image after some seconds
        root.after(20000, lambda: hide_baro_trace(baro_img_label))

    except Exception as e:
        print("Display Baro Trace. Line 4343", e, "on way to show_national_radar")
        #show_national_radar() took this out on 8/10
        hide_baro_trace(baro_img_label)
        
def hide_baro_trace(baro_img_label):
    global baro_img_tk, iterate_flag  # Declare baro_img_tk as a global variable

    # experimenting with trying to extend baro while lcl radar or lightning loads
    if baro_img_label and box_variables[2] != 1 and box_variables[3] != 1 and baro_img_label.winfo_exists():
    #if baro_img_label and baro_img_label.winfo_exists():
        baro_img_label.grid_forget() # why destroy, and not _forget? wondering on 7/25/24

    # Reference set to None to allow for garbage collection
    baro_img_tk = None
    
    iterate_flag = True
    
    root.update_idletasks()  # Explicitly update the layout 
    
    show_national_radar()
     
# # Function to show scraped frame and hide the other frames1
def show_scraped_frame():
    #baro_frame.grid_forget()
        
    frame1.grid_forget()
    scraped_frame.grid(row=0, column=0, sticky="nsew")
    
    if len(xs) > 1 and refresh_flag == False:        
        show_transparent_frame()
        # Raise the transparent frame to the top of the stacking order
        transparent_frame.lift()
#         
    show_national_radar()

# Start the tkinter main loop
root.mainloop()

