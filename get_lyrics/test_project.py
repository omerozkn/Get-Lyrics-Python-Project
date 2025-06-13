import pytest
import os
from project import query_parser, find_song_by_direct_url, save_songs_to_file, sort_entries_in_file

def test_query_parser():
    assert query_parser("Fujii Kaze - Hana") == ("Fujii Kaze", "Hana")
    assert query_parser("Hana by Fujii Kaze") == ("Fujii Kaze", "Hana")
    assert query_parser("fujii kaze / hana") == (None, None)
    assert query_parser("Hana") == (None, None)

def test_find_song_by_direct_url():
    assert find_song_by_direct_url("Fujii Kaze", "Hana") ==("https://www.lyrical-nonsense.com/global/lyrics/fujii-kaze/hana/")
    with pytest.raises(ValueError) as exc_info:
        find_song_by_direct_url("Fuji Kaze", "Hana")
    assert str(exc_info.value) == "Failed to fetch lyrics URL for Fuji Kaze - Hana with status code 404"

def test_save_songs_to_file():

    # Attention: This test will add new test entry to the  the existing songs_lyrics_collection.txt file remove the test entry after the test.

    folder = "saved_songs_lyrics_folder"
    filename = "songs_lyrics_collection.txt"
    file_path = os.path.join(folder, filename)
    
    test_artist = "Test Artist Unique 123"
    test_song = "Test Song Unique 123"
    test_url = "https://www.example.com/lyrics/test-artist-unique/test-song-unique/"
    
    save_songs_to_file(test_artist, test_song, test_url)
    
    # Read the file and verify the new entry is present.
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    assert test_artist in content
    assert test_song in content
    assert test_url in content

def test_sort_entries_in_file():
    # Used a dedicated test file to avoid modifying the main file.
    folder = "saved_songs_lyrics_folder"
    test_filename = "test_sort.txt"
    file_path = os.path.join(folder, test_filename)
    
    os.makedirs(folder, exist_ok=True)
    # Write an unsorted test file.
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("Artist|Song Title|Lyrics URL|Date\n")
        f.write("Beta | Song2 | URL2 | 2023-01-02\n")
        f.write("alpha | Song1 | URL1 | 2023-01-01\n")
        f.write("Charlie | Song3 | URL3 | 2023-01-03\n")
    
    sort_entries_in_file(file_path)
    
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
    
    # Verify the header remains intact.
    assert lines[0] == "Artist|Song Title|Lyrics URL|Date"
    
    # Verify that the entries are sorted (alphabetically by artist then song title).
    expected_entries = [
        "alpha | Song1 | URL1 | 2023-01-01",
        "Beta | Song2 | URL2 | 2023-01-02",
        "Charlie | Song3 | URL3 | 2023-01-03"
    ]
    assert lines[1:] == expected_entries

