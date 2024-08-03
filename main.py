from flask import Flask, jsonify
from bs4 import BeautifulSoup
import os
import requests
import random

app = Flask(__name__)

# List of terms
terms = [
    "Anime", "Gaming", "Meme", "Animated", "Egirl", "Drill", "Cat", "Cartoon", 
    "Matching", "Grunge", "Rapper", "Kpop", "Vtuber", "Cool", "Car", "Genshin", 
    "Discord", "Twitter", "Steam", "Instagram", "Demon slayer", "One piece", 
    "Elden ring", "Jujutsu kaisen", "Travis scott", "Ken carson", "E girl", 
    "Tokyo ghoul", "Chainsaw man", "Juice wrld", "Solo leveling", "Hello kitty", 
    "Attack on titan", "Dragon ball", "Playboi carti", "Lil peep", "Death note", 
    "League of legends"
]

def scrape_pfps():
    # Choose a random term and page number
    term = random.choice(terms).replace(' ', '-').lower()
    page_number = random.randint(1, 10)  # Assuming each term has at least 10 pages
    url = f'https://pfps.gg/pfps/{term}?page={page_number}&sort=recent'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    pfps = []
    for item in soup.find_all('div', class_='col-md-2 mb-4 pfp item'):
        img_tag = item.find('img', class_='img lazy')
        img_src = img_tag['src']
        alt_text = img_tag['alt']
        details_link = item.find('a', class_='h5')['href']
        pfps.append({
            'image': img_src,
            'alt': alt_text,
            'details_link': f"{details_link}"
        })
    
    return pfps

@app.route('/api/pfp', methods=['GET'])
def get_pfp():
    pfps = scrape_pfps()
    if pfps:
        pfp = random.choice(pfps)
        return jsonify(pfp)
    else:
        return jsonify({'error': 'No PFPs found'}), 404


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
