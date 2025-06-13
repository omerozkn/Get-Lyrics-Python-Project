# Get Lyrics

#### Video Demo: https://youtu.be/txGAvxUfg78
# Project title: Get Lyrics
# Name: Ömer Faruk Özkan
# github: omerozkn
# edx:omerozkn
# city/country: Istanbul/Turkey
# Date 26.05.2025
#### Description:
This project is a Python application that asks the user for a song, then retrieves the lyrics URL for that song from an online lyrics website called Lyrical Nonsense. It is designed to simplify the process of finding and saving song lyrics for later reference. The program accepts user input, processes it using custom functions—such as parsing the query to extract the artist and song title, fetching the appropriate lyrics URL via an HTTP request, and saving the results to a text file. Additionally, it includes a sorting feature that organizes the saved entries alphabetically by artist name and song title. This small project demonstrates key programming skills including user input handling, HTTP requests, error handling, file management, and automated testing with pytest.

## Project Structure

- **project.py**  
  Contains the main function and at least three custom functions:
  - `query_parser`: Parses the user input.
  - `find_song_by_direct_url`: Fetches a lyrics URL based on the artist and song title.
  - `save_songs_to_file`: Saves the lyrics URL, artist, and song title to a text file.
  - `sort_entries_in_file`: Sorts the entries in the saved songs file.
  
- **test_project.py**  
  Contains test functions for the custom functions. Tests are executed using pytest.  
  The tests ensure:
  - `query_parser` works correctly for various input formats.
  - `find_song_by_direct_url` raises errors or returns correct URLs based on input.
  - `save_songs_to_file` and `sort_entries_in_file` behave as expected.

- **requirements.txt**  
  Lists the Python libraries required to run this project.

## How to Run the Project

1. **Install Dependencies:**  
   Run the following command to install all necessary libraries:
   ```bash
   pip install -r requirements.txt
