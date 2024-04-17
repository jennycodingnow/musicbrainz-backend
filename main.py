import requests
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['musicbrainzdb']

def store_artist_mongodb(artist_name,db):

    artist_url = "https://musicbrainz.org/ws/2/artist"
    params = {
        "query" : f"name:{artist_name}",
        "fmt": "json"
    }
    response = requests.get(artist_url, params=params)
    artist_data = response.json()

    if artist_data.get('artists'):
        first_artist = artist_data["artists"][0]
        artist_info = {
            "MBID": first_artist.get("id", None),
            "Name": first_artist.get("name", None),
            "Country": first_artist.get("country", None),
            "Type": first_artist.get("type", None),
        }
    else:
        print("No artist data found")

    
    collection = db['Artist']
    
    id_exist = collection.find_one({"MBID": artist_info["MBID"]})

    if id_exist:
        print("Artist already exists in the database")
        return artist_info["MBID"],artist_info["Name"]
    try: 
        result = collection.insert_one(artist_info)
        print("successful:", result.inserted_id)
        return artist_info["MBID"],artist_info["Name"]
    except Exception as e:
        print("An error occurred storing the artist:", e)
        return None, None


def retrieve_coverart_url(release_id):
    coverart_url = f"https://coverartarchive.org/release/{release_id}"
    params = {
        "fmt": "json"
    }
    response = requests.get(coverart_url, params=params)
    if response.status_code == 200:
        coverart_data = response.json()
        if "images" in coverart_data and coverart_data["images"]:
            image_url = coverart_data["images"][0]["image"]
            print("Cover Art URL:", image_url)
            return image_url
        else:
            print("No cover art images found for this release.")
    else:
        print("Unsucessful.", response.status_code)


def store_release_mongodb(artist_id, artist_name, db):

    album_url = "https://musicbrainz.org/ws/2/release"
    params = {
        "artist": artist_id,
        "fmt": "json"
    }
    response = requests.get(album_url, params=params)
    album_data = response.json()

    
    if album_data.get("releases"):
        albums = []
        for release in album_data["releases"]:
            # cover_art_url = retrieve_coverart_url(release.get("id"))
            album_info = {
                "MBID": release.get("id", None),
                "Artist": artist_name,
                "ArtistId": artist_id,
                "Country": release.get("country", None),
                "Title": release.get("title", None),
                "Date": release.get("date", None),
                "Status": release.get("status", None),
                # "CoverArtUrl": cover_art_url
            }
            albums.append(album_info)
    else:
        print("No album data found")

    collection = db['Release']
    for album in albums:
        id_exist = collection.find_one({"MBID": album_info["MBID"]})
        if not id_exist:
            try: 
                cover_art_url = retrieve_coverart_url(album["MBID"])
                album["CoverArtUrl"] = cover_art_url
                result = collection.insert_one(album)
                print("Successful:", result.inserted_id)
            except Exception as e:
                print("An error occurred storing the release albums:", e)
        else:
            print("Album already in database:", album["MBID"])


artist_name = input("Please enter in artist: ")
artist_id, artist_name = store_artist_mongodb(artist_name, db)
store_release_mongodb(artist_id, artist_name, db)






