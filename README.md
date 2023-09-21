# Spotify Info API

Spotify Info API is a Flask-based web service that allows users to access information about their Spotify account, including top tracks, followed artists, followed playlists, and top artists.

## Features

- Retrieve user's account info such as username, email, Spotify Id and Subscription
- Retrieve user's top tracks.
- Get a list of followed artists.
- Get a list of followed playlists.
- Discover top artists in user's Spotify profile.

## Getting Started

These instructions will help you set up and run the SpotiInfo API on your local machine.

### Prerequisites

- Python 3.7+
- Flask
- Spotify Developer Account (for API credentials)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/spotiinfo-api.git
   ```
   
2. Navigate to the Project Directory
    ```bash
    cd spotify-info-api
    ```

3. Install the required dependencies
    ```bash
    pip install -r requirements.txt
    ```

4. Create a Spotify Developer App and obtain your `CLIENT_ID` and `CLIENT_SECRET`
5. Create a `.env` file in project directory and set the values for `SECRET_KEY`, `CLIENT_ID`, `CLIENT_SECRET` and `REDIRECT_URI`. Set `REDIRECT_URI`to `http://localhost:8080/callback`
6. Run the Application
7. Access the API in your web browser or via HTTP requests. The API will be available at `http://localhost:8080`

### Endpoints

- `/login`: login to your Spotify Account
- `/logout`: log out of your Spotify Account
- `/profile`: get user account information like username, email, spotify Id and Subscription
- `/artists/followed`: get a list of followed artists
- `/playlists/followed`: get a list of followed playlists
- `/tracks/top`: get user's top 20 tracks
- `/artists/top`: get user's top 20 artists
