import requests
import re
import os
from datetime import datetime

def main():
    """
    Main function that gets user input, parses it, fetches the lyrics URL, and saves the result.
    
    This function repeatedly prompts the user until valid input is provided and the lyrics URL is successfully retrieved.
    Errors in parsing or fetching are handled here, allowing for appropriate user feedback.
    """

    #This project is a python application that asks the user for a song and then seaches for the song Lyrics URL and saves the song Lyrics URL to a text file.
    
    while True:
        try:
            query = input("Enter song name and artist  (e.g., ' Fujii Kaze - Hana')(Formats accepted: artist - song or song by artist ): ")
            artist, song_title = query_parser(query)
            if artist is None or song_title is None:
                print("\nInvalid format. Please use one of the following formats:")
                print("  1. Artist - Song")
                print("  2. Song by Artist")
                print("Also, check for spelling mistakes, remove any special characters,")
                print("or use only English characters if possible.\n")
            else:
                #this print is for testing purposes remove it after code is finished  
                print(f"\nParsed successfully: Artist: '{artist}', Song Title: '{song_title}'\n")
                print(f"Searching for: {re.sub(r'\s+', ' ', query).strip()}")
            
                try:
                    lyrics_url = (find_song_by_direct_url(artist, song_title))
                except Exception as e:
                    print(f"An error occurred: {e}")
                else:
                    print(f"Lyrics URL found: {lyrics_url}")
                    save_songs_to_file(artist, song_title, lyrics_url)
                    print(f"Song lyrics saved successfully to 'songs_lyrics_collection.txt'")
                    break               
        except Exception as e:
            # Log the exception and prompt again.
            print(f"\nAn error occurred input: {e}")
            

def query_parser(query):
    """
    Parses the input query to extract the artist and song title.

    """
    # Remove extra spaces
    normalized_query = re.sub(r'\s+', ' ', query).strip()

    # Pattern for "Artist - Title"
    pattern1 = re.compile(r'^(?P<artist>.+)\s*-\s*(?P<song_title>.+)$', re.IGNORECASE)
    # Pattern for "Title by Artist"
    pattern2 = re.compile(r'^(?P<song_title>.+)\s+by\s+(?P<artist>.+)$', re.IGNORECASE)

    # check if the query matches the pattern and #check if the query is in the format of "Artist - Title"
    match1 = pattern1.match(normalized_query)
    if match1:
        artist = match1.group("artist").strip()
        song_title = match1.group("song_title").strip()
        return artist, song_title
    # check if the query matches the pattern and #check if the query is in the format of "Title by Artist"
    match2 = pattern2.match(normalized_query)
    if match2:
        artist = match2.group("artist").strip()
        song_title = match2.group("song_title").strip()
        return artist, song_title  
    return None, None
    
def find_song_by_direct_url(artist, song_title):
    """
    Constructs a URL for the given artist and song title.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Cookie": "language=en; ln_global=1"
    }
    url = "https://www.lyrical-nonsense.com/global/"
    lyrics_url = f"{url}lyrics/{artist.replace(' ', '-').lower()}/{song_title.replace(' ','-').lower()}/"
    
    response = requests.get(lyrics_url, headers=headers, timeout=10)
    if response.status_code == 200:
        return lyrics_url
    else:        
        raise ValueError(f"Failed to fetch lyrics URL for {artist} - {song_title} with status code {response.status_code}")
         
def save_songs_to_file(artist, song_title,lyrics_url):    
    """
    saves the song lyrics URL, artist name and song title  to a text file

    This function ensures that the target directory exists, writes a header if the file is new,
    and appends the new entry with the current date and time. 

    """
    # Create a new text file and write the songs lyrics to it.
    folder = "saved_songs_lyrics_folder"
    filename = "songs_lyrics_collection.txt"
    file_path = os.path.join(folder, filename)
    os.makedirs(folder, exist_ok=True)

    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("Artist|Song Title|Lyrics URL|Date\n")
    with open(file_path, "a" , encoding="utf-8") as file:
        file.write(f"{artist} | {song_title} | {lyrics_url} | {datetime.now()}\n")

def sort_entries_in_file(file_path):
    """
    Reads the text file, sorts the entries alphabetically (first by Artist, then by Song Title),
    and rewrites the file with the header followed by sorted entries.
    
    Parameters:
        file_path (str): The full path to the text file to be sorted.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()       
    if not lines:
        return  # Empty file
    header = lines[0]
    entries = lines[1:]
    
    # Remove any empty lines (if present)
    '''
    new_entries = []
    for line in entries:
        if line.strip():  # If line is not empty after stripping whitespace
            new_entries.append(line)
    entries = new_entries
    code below is all the above code in one line
    '''
    entries = [line for line in entries if line.strip()]

    
    # Sort entries by Artist (first field) and then by Song Title (second field)
    entries.sort(key=lambda line: (
        line.split(" | ")[0].strip().lower(), 
        line.split(" | ")[1].strip().lower()
    ))
    
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(header)
        file.writelines(entries)

if __name__ == "__main__":
    main()
