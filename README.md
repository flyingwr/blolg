# BLOLG

This tool is designed to provide statistics and history of League of Legends tournaments using the [Leaguepedia](https://lol.fandom.com/wiki/League_of_Legends_Esports_Wiki) API, where it's possible to fetch the most up-to-date statistical data of players, teams and leagues from around the world, and put up good knowledge and assistance on finding probabilities for betting.

## Features
- **Player Search**: Enter the name of a professional player to retrieve their match history with detailed statistics including champion played, KDA, match date, tournament name and match result. Filtering the results by specific champions is possible.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/flyingwr/blolg.git
   cd blolg
   ```
2. Install dependencies:
    ```bash
    python -m pip install -r requirements.txt
    ```

3. Run the application:
    ```bash
    python server.py
    ```

## Usage

Open your browser and navigate to `http://localhost:8080/players` to start using the application