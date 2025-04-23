#!/bin/bash

if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install Python3 first."
    exit 1
fi

if ! command -v pip &> /dev/null; then
    echo "pip not found. Installing pip..."
    python3 -m ensurepip --upgrade
fi

pip install matplotlib seaborn numpy osmnx networkx pandas folium scikit-learn selenium webdriver-manager
