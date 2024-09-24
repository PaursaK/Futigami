# FUTIGAMI

## Table of Contents
1. [Introduction](#introduction)
2. [Screenshots](#screenshots)
3. [Installation](#installation)
4. [Methods](#methods)
5. [Technologies Used](#technologies-used)
6. [File Structure](#file-structure)
7. [Future Improvements](#future-improvements)

## Introduction

**Futigami** is a dashboard that shows all the unique scorelines in Europes Top 5 futbol leagues. It is based on **Scorigami** which is the American Football version depicting all the unique scores ever recorded in a official game in the NFL.

## Screenshots
Here’s a video of a local session in action:

![Gameplay Screenshot](./assets/GUI.png)

## Installation
```
git clone https://github.com/PaursaK/Futigami.git
cd Futigami
```
## Methods

using data science packages and webscraping tools I gathered information from https://fbref.com/en/ on Europes Top 5 leagues (Premier League, La Liga, Bundesliga, Ligue 1, Serie A)


## Technologies Used

Python, Pandas, Plotly, Dash, BeautifulSoup, requests, re (regular expression), numpy

## File Structure
```
FUTIGAMI/               # Project root
│
├── dataManagement/      # Package for data handling and scraping
│   ├── __pycache__/     # Python cache files
│   ├── __init__.py      # Init file to treat this directory as a package
│   ├── LeagueStorage.py # Manages league data storage
│   └── WebScraper.py    # Handles web scraping tasks
│
├── processing/          # Package for processing data
│   ├── __pycache__/     # Python cache files
│   ├── __init__.py      # Init file for processing package
│   └── Processor.py     # Handles computations and request processing
│
├── tests/               # Package for unit tests
│   ├── __pycache__/     # Python cache files
│   ├── __init__.py      # Init file for test package
│   ├── testRequestProcessor.py  # Tests for request processing functionality
│   └── testWebscraper.py        # Tests for web scraping functionality
│
├── userInterface/       # Package for the user interface
│   ├── __pycache__/     # Python cache files
│   ├── __init__.py      # Init file for user interface package
│   └── UserInterface.py # Handles interaction with the user (e.g., front-end logic)
│
├── utility/             # Package for utility classes
│   ├── __pycache__/     # Python cache files
│   ├── __init__.py      # Init file for utility package
│   ├── LeagueHistory.py # Utility for managing league history
│   ├── Match.py         # Utility for match data
│   ├── Season.py        # Utility for season data
│
└── main.py              # Entry point for the application
```

## Future Improvements
- **XXXXX**: 
- **XXXXX**: 