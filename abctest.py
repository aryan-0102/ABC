#!/usr/bin/env python3
import pandas as pd
import numpy as np
import osmnx as ox
import networkx as nx
import time
from datetime import datetime
import folium
from folium.plugins import MarkerCluster
import webbrowser
import os
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import time
import os
start_time = time.time()


customer_data = pd.read_csv('customer_data_old.csv')

hubs = {
    'A': (30.724913, 76.787800),
    'B': (30.746120, 76.769660),
    'C': (30.727379, 76.725188),
    'D': (30.700463, 76.755896)
}

print("Fetching Chandigarh map...")
G = ox.graph_from_place('Chandigarh, India', network_type='drive')


# Helper function to find nearest node on the graph given coordinates
def nearest_node(lat, lon):
    return ox.distance.nearest_nodes(G, lon, lat)


# Precompute hub nodes for efficiency
hub_nodes = {hub: nearest_node(*coords) for hub, coords in hubs.items()}

# Initialize distance matrix and routes dictionary
distance_matrix = []
routes_dict = {}

print("Calculating distances and routes from customers to hubs...")
for idx, row in customer_data.iterrows():
    cust_node = nearest_node(row['Latitude'], row['Longitude'])
    distances_to_hubs = {}
    routes_to_hubs = {}

    for hub_name, hub_node in hub_nodes.items():
        try:
            distance = nx.shortest_path_length(G, source=hub_node, target=cust_node, weight='length')
            route = nx.shortest_path(G, source=hub_node, target=cust_node, weight='length')
        except nx.NetworkXNoPath:
            distance = np.inf
            route = []

        distances_to_hubs[hub_name] = distance
        routes_to_hubs[hub_name] = route

    distance_matrix.append(distances_to_hubs)
    routes_dict[row['Location']] = routes_to_hubs

distance_df = pd.DataFrame(distance_matrix)
distance_df.insert(0, 'Location', customer_data['Location'])


# Artificial Bee Colony Algorithm implementation
class ABCAlgorithm:
    def __init__(self, distance_df, n_bees=50, max_iter=1000):
        self.distance_df = distance_df.set_index('Location')
        self.locations = self.distance_df.index.tolist()
        self.hubs = self.distance_df.columns.tolist()
        self.n_customers = len(self.locations)
        self.n_bees = n_bees
        self.max_iter = max_iter
        self.best_solution = None
        self.best_cost = np.inf

    def initialize_population(self):
        return [np.random.choice(self.hubs, self.n_customers) for _ in range(self.n_bees)]

    def evaluate_fitness(self, solution):
        total_distance = sum(
            self.distance_df.loc[self.locations[i], solution[i]] for i in range(self.n_customers)
        )
        return total_distance

    def run(self):
        print("Running ABC optimization...")
        population = self.initialize_population()

        for iteration in range(self.max_iter):
            fitness_values = [self.evaluate_fitness(sol) for sol in population]

            # Update best solution found so far
            min_idx = np.argmin(fitness_values)
            if fitness_values[min_idx] < self.best_cost:
                self.best_cost = fitness_values[min_idx]
                self.best_solution = population[min_idx].copy()
                if iteration%100 == 0:
                    print(f"Iteration {iteration + 1}: Best total distance so far: {self.best_cost:.2f} meters")

            # Employed bees phase (local search)
            for i in range(self.n_bees):
                new_sol = population[i].copy()
                idx_change = np.random.randint(0, self.n_customers)
                new_sol[idx_change] = np.random.choice(self.hubs)
                if self.evaluate_fitness(new_sol) < fitness_values[i]:
                    population[i] = new_sol

            # Onlooker bees phase (probabilistic selection based on fitness)
            fitness_inv = [1 / f if f > 0 else 0 for f in fitness_values]
            probs_sum = np.sum(fitness_inv)
            probs = fitness_inv / probs_sum if probs_sum > 0 else np.ones(self.n_bees) / self.n_bees

            for i in range(self.n_bees):
                selected_idx = np.random.choice(range(self.n_bees), p=probs)
                new_sol = population[selected_idx].copy()
                idx_change = np.random.randint(0, self.n_customers)
                new_sol[idx_change] = np.random.choice(self.hubs)
                if self.evaluate_fitness(new_sol) < fitness_values[selected_idx]:
                    population[selected_idx] = new_sol

            # Scout bees phase (replace worst solution randomly)
            worst_idx = np.argmax(fitness_values)
            population[worst_idx] = np.random.choice(self.hubs, self.n_customers)

        print("ABC optimization completed.")
        return dict(zip(self.locations, self.best_solution))


# Run ABC algorithm to get optimal assignments
abc_solver = ABCAlgorithm(distance_df)
optimal_assignment = abc_solver.run()

# Save final results including route details to CSV file
final_results = []

print("Saving results to abc_new.csv...")
for idx, row in customer_data.iterrows():
    loc_name = row['Location']
    assigned_hub = optimal_assignment[loc_name]
    final_results.append({
        'Location': loc_name,
        'Latitude': row['Latitude'],
        'Longitude': row['Longitude'],
        'NearestHub': assigned_hub,
        'Distance(meters)': distance_df.loc[distance_df.Location == loc_name, assigned_hub].values[0],
        'Route(nodes)': routes_dict[loc_name][assigned_hub]
    })

final_results_df = pd.DataFrame(final_results)
final_results_df.to_csv('abc_new.csv', index=False)

# Create a Folium map centered on Chandigarh
print("Creating map visualization...")
chandigarh_center = [30.7333, 76.7794]
m = folium.Map(location=chandigarh_center, zoom_start=13, tiles='OpenStreetMap')

# Define colors for different hubs
hub_colors = {
    'A': 'red',
    'B': 'blue',
    'C': 'green',
    'D': 'purple'
}

# Add hub markers
for hub_name, (lat, lon) in hubs.items():
    folium.Marker(
        location=[lat, lon],
        popup=f"Hub {hub_name}",
        icon=folium.Icon(color=hub_colors[hub_name], icon='home', prefix='fa'),
    ).add_to(m)

# Create marker clusters for customers grouped by assigned hub
hub_clusters = {hub: MarkerCluster(name=f"Customers assigned to Hub {hub}") for hub in hubs.keys()}
for cluster in hub_clusters.values():
    cluster.add_to(m)

# Add customer markers and routes
for result in final_results:
    hub_name = result['NearestHub']
    customer_location = [result['Latitude'], result['Longitude']]

    # Add customer marker to appropriate cluster
    folium.Marker(
        location=customer_location,
        popup=f"Customer: {result['Location']}<br>Assigned to Hub {hub_name}<br>Distance: {result['Distance(meters)']:.2f} meters",
        icon=folium.Icon(color=hub_colors[hub_name], icon='user', prefix='fa'),
    ).add_to(hub_clusters[hub_name])

    # Get route coordinates
    route_nodes = result['Route(nodes)']
    if route_nodes and len(route_nodes) > 1:
        route_coords = []
        for node in route_nodes:
            # Get node coordinates from graph
            y, x = G.nodes[node]['y'], G.nodes[node]['x']
            route_coords.append([y, x])

        # Plot route line
        folium.PolyLine(
            locations=route_coords,
            color=hub_colors[hub_name],
            weight=2,
            opacity=0.7,
            popup=f"Route from Hub {hub_name} to {result['Location']}"
        ).add_to(m)

# Add layer control
folium.LayerControl().add_to(m)

# Save the map to an HTML file
map_file = 'chandigarh_routes_map.html'
m.save(map_file)



print("All tasks completed successfully!")
end_time = time.time()
execution_time = end_time - start_time

print(f"Execution time: {execution_time} seconds")

def save_html_as_image(html_file_path, output_image_name):
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1200,800")  # adjust resolution as needed

    driver = webdriver.Chrome(options=options)
    driver.get(f"file://{os.path.abspath(html_file_path)}")

    time.sleep(5)  # wait for the page and tiles to load
    driver.save_screenshot(output_image_name)
    driver.quit()

save_html_as_image("chandigarh_routes_map.html", "chandigarh_routes_map.jpg")
