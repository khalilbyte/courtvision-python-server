# CourtVision

The NBA regular season is spans across 7 months and over 1200 games. For NBA Fantasy team owners, this means staying on top of your game day-in and day-out. CourtVision gives you an all-in-one place to keep up-to-date with players on your teams.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Dependencies](#dependencies)

## Features

- See all players available in NBA Fantasy
- Search for specific players
- Add players to your watchlist
- Create and manage custom fantasy teams

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Local Setup

Clone the repository:

```
git clone https://github.com/fullstackkg/courtvision-fastapi.git
```

Create and activate virtual Python environment:

```
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On Unix or MacOS:
source venv/bin/activate
```

Install FastAPI and the required dependencies:

```
pip install "fastapi[standard]"
```

## Core Dependencies

The project uses FastAPI framework with the following key dependencies:

FastAPI: Modern web framework for building APIs
Uvicorn: Fast ASGI server
Pydantic: Data validation using Python type annotations

To install all dependencies, simply run:

```
pip install -r requirements.txt
```

## Running the Application

Start the FastAPI development server:

```
uvicorn main:app --reload
```

Application runs on http://localhost:8000

### Production Build

Create JAR

```
mvn clean package
```

Run JAR

```
java -jar target/courtvision-server-0.0.1-SNAPSHOT.jar
```

## External API Integration

This project utilizes the [NBA_API](https://github.com/swar/nba_api) for retrieving NBA statistics and player data.

## API Documentation

The API documentation is automatically generated and can be accessed at:

Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc

#### Players

- GET /players?page={page}&players_per_page={players_per_page} - List all players
- GET /players/categories?number_of_players={number_of_players}&category={category} - Show category leaders
- GET /players/search?keyword={keyword} - Search by player name
- GET /players/{player_id} - Get single player details

#### Teams

- GET /teams - List all teams
- GET /teams/{team_id}/players - Get all players on a team
