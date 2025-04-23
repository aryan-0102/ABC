# Drone Delivery Route Optimization in Chandigarh 🚁💨

**Optimizing Last-Mile Delivery using Artificial Bee Colony (ABC), Dijkstra, and A* with FCFS Scheduling**

---

## 🚀 Overview

This project addresses the complex problem of optimizing last-mile drone delivery routes within the specific urban landscape of **Chandigarh, India**. It leverages customer location data (coordinates), incorporates order details (value, priority, timestamp), and utilizes **four strategically chosen central hubs** to ensure effective city coverage.

The primary innovation lies in applying the **Artificial Bee Colony (ABC) algorithm** to discover highly efficient delivery routes, demonstrating a significant potential reduction in delivery times compared to conventional methods[3]. The performance of ABC is systematically benchmarked against established pathfinding algorithms: **Dijkstra's** and **A***.

Beyond route optimization, the system implements **First-Come, First-Served (FCFS)** scheduling to manage the sequence of deliveries. It also analyzes drone resource allocation, concluding through simulation that deploying **two drones per hub** strikes an effective balance for handling typical demand in this scenario, aligning with findings in drone logistics research which show diminishing returns when adding too many drones to a limited area [5][6].

The entire simulation and analysis workflow – from data ingestion and algorithm execution to comparison and visualization – is automated via a central `runner.py` script. The project culminates in a comprehensive **PDF report** detailing the methodologies, comparative results, and key findings.

## 📚 Related Research Paper

This codebase implements the methodology and experiments detailed in the following research paper:

*   **[Link to Paper](https://drive.google.com/file/d/1OeOcCFwjQrK_eCuH9Qn3P73KdsmQT0cT/view?usp=drive_link)** *(Note: Access may require appropriate permissions)*

## 🎯 Project Goals

*   Optimize drone delivery routes specifically for Chandigarh using the ABC algorithm.
*   Quantitatively compare ABC's efficiency (e.g., total delivery time, route cost) against Dijkstra and A*.
*   Implement and evaluate FCFS scheduling for processing drone delivery orders.
*   Determine an operationally sound number of drones required per hub based on simulated demand (identified as 2 per hub).
*   Develop a reusable simulation framework for drone delivery logistics in urban environments.
*   Generate a consolidated report summarizing the findings.

## ✨ Key Features

*   **Advanced Algorithm Implementation:**
    *   **Artificial Bee Colony (ABC):** For sophisticated route optimization, shown to be effective for vehicle routing problems[3].
    *   **Dijkstra's Algorithm:** Classic shortest path algorithm for baseline comparison.
    *   **A* Search Algorithm:** Informed search algorithm for baseline comparison.
*   **Context-Specific Data Handling:** Processes geographic coordinates for Chandigarh, uses 4 central hubs, and incorporates order attributes (value, priority, time).
*   **FCFS Scheduling:** Manages order dispatch sequence based on arrival time.
*   **Drone Fleet Optimization:** Analysis leading to the recommendation of 2 drones per hub for balanced throughput[5][6].
*   **Performance Benchmarking:** Compares algorithms based on metrics like route efficiency and computation time.
*   **Result Visualization:** Includes tools for generating graphs and potentially heatmaps (`comparision_time_graph.py`, `heatmap.py`).
*   **Automated PDF Reporting:** `report.py` generates a final document summarizing the simulation results and conclusions.

## 🏙️ Problem Context & Data

*   **Scenario:** Optimizing last-mile drone deliveries originating from 4 central hubs in Chandigarh.
*   **Data Source:** Customer coordinates and order details (value, priority, timestamp) collected via methods like Google Forms.
*   **Objective:** Minimize delivery time/cost through intelligent routing (ABC) and scheduling (FCFS).

## 🛠️ Setup and Installation

Get the project running on your local machine.

### Prerequisites

*   **Python:** Version 3.x is required.
*   **pip:** Python package installer (typically included with Python).
*   **Git:** For cloning the repository.
*   **Bash:** Or a compatible shell to execute the setup script.

### Installation Steps

1.  **Clone the Repository:**
    ```
    git clone https://github.com/aryan-0102/ABC.git
    cd ABC
    ```

2.  **Install All Dependencies:**
    Execute the `requirement.sh` script **first**. This script uses `pip` to install all necessary Python libraries defined within it (e.g., pandas, numpy, matplotlib, libraries for PDF generation).
    ```
    bash requirement.sh
    ```

## ⚙️ How to Run

The project is designed to be run via a single command:

1.  **Execute the Main Runner Script:**
    ```
    python runner.py
    ```
    *This command initiates the entire process:*
    *   Loads Chandigarh map data, hub locations, and customer order data.
    *   Executes ABC, Dijkstra, and A* algorithms to find routes.
    *   Applies FCFS scheduling logic and simulates deliveries with 2 drones per hub.
    *   Performs comparative analysis of the algorithms' performance.
    *   Generates visualizations (graphs, etc.).
    *   **Crucially, it produces a final `report.pdf` file** in the project directory, containing a detailed summary of the findings.

*Review `runner.py` if you need to understand the specific sequence or pass any configuration parameters.*



## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature suggestions.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request


---

*This README incorporates the specific details from the project description and related research context. Ensure data file names and any specific configurations are accurate.*
