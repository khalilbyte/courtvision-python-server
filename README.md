# CourtVision

The NBA regular season spans across 7 months and over 1200 games. For NBA Fantasy team owners, this means staying on top of your game day-in and day-out. CourtVision gives you an all-in-one place to keep up-to-date with players on your teams.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [API Documentation](#api-documentation)
- [External API Integration](#external-api-integration)

## Features

- See all players available in NBA Fantasy
- Search for specific players
- View category leaders (points, rebounds, assists, etc.)
- Browse team rosters
- Fast response times with Redis caching

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Redis server

### Local Setup

Clone the repository:

```bash
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

Install required dependencies:

```
pip install -r requirements.txt
```

## Running the Application

Start the FastAPI development server:

```
uvicorn main:app --reload
```

Application runs on http://localhost:8000

## Core Dependencies

The project is built with modern Python tools and frameworks:

FastAPI: High-performance web framework for building APIs
Uvicorn: Lightning-fast ASGI server
Pydantic: Data validation using Python type annotations
Redis: In-memory caching for improved performance
NBA_API: Python client for accessing NBA statistics

## API Documentation

Interactive API documentation is automatically generated and available at:

Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc

### Available Endpoints

#### Players

- GET /players?page={page}&players_per_page={players_per_page} - List all players
- GET /players/categories?number_of_players={number_of_players}&category={category} - Show category leaders
- GET /players/search?keyword={keyword} - Search by player name
- GET /players/{player_id} - Get single player details

#### Teams

- GET /teams - List all teams
- GET /teams/{team_id}/players - Get all players on a team

## External API Integration

This project utilizes the [NBA_API](https://github.com/swar/nba_api) for retrieving NBA statistics and player data.
