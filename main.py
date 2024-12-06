import os
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
GOOGLE_BOOKS_API_KEY = os.getenv('GOOGLE_BOOKS_API_KEY')
OMDB_API_KEY = os.getenv('OMDB_API_KEY')

app = Flask(__name__)
def get_books_by_genre(genre):
    url = f'https://www.googleapis.com/books/v1/volumes?q=subject:{genre}&maxResults=10&key={GOOGLE_BOOKS_API_KEY}'
    try:
        response = requests.get(url)
        data = response.json()
        return data['items'] if 'items' in data else []
    except Exception as e:
        print(f'Error fetching books: {e}')
        return []


def get_movies_by_genre(genre):
    url = f"http://www.omdbapi.com/?s={genre}&type=movie&apikey={OMDB_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()

        if data.get('Response') == 'True':  
            return data['Search']  
        else:
            return []  
    except Exception as e:
        print(f"Error fetching movies: {e}")
        return []  


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    content_type = request.form['content_type'] 
    genre = request.form['genre'].lower() 

    recommendations = []

    if content_type == 'movie':
        recommendations = get_movies_by_genre(genre)  
    elif content_type == 'book':
        recommendations = get_books_by_genre(genre)

    return render_template('recommendation.html', recommendations=recommendations, content_type=content_type)

if __name__ == '__main__':
    app.run(debug=True)
