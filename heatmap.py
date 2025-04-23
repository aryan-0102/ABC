'''import pandas as pd
import folium
from folium.plugins import HeatMap
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file
try:
    data = pd.read_csv('customer_data.csv')

    # Extract the latitude and longitude columns
    locations = data[['Latitude', 'Longitude']]

    # Create a folium map centered at the mean of the coordinates
    map_center = [locations['Latitude'].mean(), locations['Longitude'].mean()]
    mymap = folium.Map(location=map_center, zoom_start=12)

    # Add a heatmap layer
    HeatMap(locations.values, radius=15).add_to(mymap)

    # Save the map to an HTML file
    mymap.save('customer_heatmap.html')
    print("Heatmap created successfully and saved as 'customer_heatmap.html'")

    # Alternative: Create a static heatmap using seaborn
    plt.figure(figsize=(10, 8))
    sns.kdeplot(x=data['Longitude'], y=data['Latitude'], cmap='Reds', fill=True)
    plt.title('Customer Location Heatmap')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.savefig('customer_static_heatmap.png')
    print("Static heatmap also saved as 'customer_static_heatmap.png'")

except FileNotFoundError:
    print("Error: The file 'customer_data.csv' was not found.")
    print("Please ensure the file exists in the current directory.")
except Exception as e:
    print(f"An error occurred: {e}")

import webbrowser
webbrowser.open('customer_static_heatmap.png')'''

import pandas as pd
import folium
from folium.plugins import HeatMap
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import time
import os

# Load the CSV file
data = pd.read_csv('customer_data.csv')

# Extract the latitude and longitude columns
locations = data[['Latitude', 'Longitude']]

# Define the center of the map (Chandigarh coordinates)
chandigarh_center = [30.7333, 76.7794]

# Create a folium map centered at Chandigarh
mymap = folium.Map(location=chandigarh_center, zoom_start=13)

# Add a heatmap layer
HeatMap(locations.values, radius=15).add_to(mymap)

# Save the map to an HTML file

mymap.save('chandigarh_customer_heatmap.html')
html_file = 'chandigarh_customer_heatmap.html'
mymap.save(html_file)

def save_html_as_image(html_file_path, output_image_name):
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1200,800")  # adjust resolution as needed

    driver = webdriver.Chrome(options=options)
    driver.get(f"file://{os.path.abspath(html_file_path)}")

    time.sleep(5)  # wait for the page and tiles to load
    driver.save_screenshot(output_image_name)
    driver.quit()

save_html_as_image("chandigarh_customer_heatmap.html", "chandigarh_customer_heatmap.png")