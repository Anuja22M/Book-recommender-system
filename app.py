from flask import Flask, jsonify, render_template, request
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
from openai import OpenAI
import re 

# Load environment variables
load_dotenv()

# Load data files
popular1_df = pd.read_csv(r'popular1_df.csv')
pt = pd.read_csv(r'pt.csv', index_col=0)
books = pd.read_csv(r'books.csv')
similarity_scores_df = pd.read_csv(r'similarity_score.csv', index_col=0)
similarity_score = similarity_scores_df.to_numpy()

app = Flask(__name__)

@app.route('/')
def index():
    """Home page with popular books"""
    return render_template('index.html',
                           book_name=list(popular1_df['Book-Title'].values),
                           author=list(popular1_df['Book-Author'].values),
                           image=list(popular1_df['Image-URL-M'].values),
                           votes=list(popular1_df['num_ratings'].values),
                           rating=list(popular1_df['avg_ratings'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    """Recommendation page UI"""
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    """Handle book recommendations based on collaborative filtering"""
    user_input = request.form.get('user_input')
    index_array = np.where(pt.index == user_input)[0]
    if len(index_array) == 0:
        print("Book not found in pt.index")
        return render_template('recommend.html', message="Book not found. Please try another title.", form_action="/recommend_books")

    index = index_array[0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    return render_template('recommend.html', data=data)

@app.route('/gpt_recommends', methods=['GET', 'POST'])
def gpt_recommends():
    """GPT AI book recommendations"""
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        if not user_input:
            return render_template('gpt.html', message="Please enter a book title or description.", user_input="")
            
        # Get recommendations using external function
        from gpt_search import get_book_recommendations
        recommendations_text, error = get_book_recommendations(f"Provide similar books to {user_input}")
        
        if error:
            return render_template('gpt.html', message=f"Error: {error}",
                                     user_input=user_input)
            
        try:
            data = []
            
            # Split by book entries (assume they're separated by newlines)
            books_text = recommendations_text.split("\n\n")
            for book_text in books_text:
                if not book_text.strip():
                    continue
                    
                lines = book_text.strip().split("\n")
                if len(lines) >= 3:  # Basic validation
                    # Extract information (very basic parsing)
                    # title = lines[0].replace("1.", "").replace("Title:", "").strip()
                    title = re.sub(r'^\d+\.\s*', '', lines[0]).replace("Title:", "").strip().strip('"*')
                    author = lines[1].replace("Author:", "").strip()
                    genre = lines[2].replace("Genre:", "").strip() if len(lines) > 2 else "Unknown"
                    
                    # Placeholder image URL - in production, you might want to search for book covers
                    # image_url = "https://images.google.com/"
                    
                    data.append({
                        "title": title,
                        "author": author,
                        "genre": genre,
                        # "image_url": image_url
                    })
            
            if not data:
                return render_template('gpt.html', message="No recommendations found. Try a different title.",user_input=user_input)
                
            return render_template('gpt.html', data=data,user_input=user_input)
            
        except Exception as e:
            return render_template('gpt.html', message=f"Error processing recommendations: {str(e)}", user_input="")
    
    # GET request
    return render_template('gpt.html', user_input="")

@app.route('/gpt_search')
def gpt_search_ui():
    """GPT Search page UI"""
    return render_template('gpt_search.html')

@app.route('/search', methods=['POST'])
def search():
    """Handle the book recommendation search request using AI"""
    try:
        data = request.form
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({
                'success': False,
                'error': 'Please provide a search prompt'
            })
        
        # Import and use the function from gpt_search.py
        from gpt_search import get_book_recommendations
        recommendations, error = get_book_recommendations(prompt)
        
        if error:
            return jsonify({
                'success': False,
                'error': error
            })
        
        return jsonify({
            'success': True,
            'recommendations': recommendations
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"An unexpected error occurred: {str(e)}"
        })

if __name__ == '__main__':
    # Make sure templates directory exists
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Create a basic gpt_search.html if it doesn't exist
    if not os.path.exists('templates/gpt_search.html'):
        with open('templates/gpt_search.html', 'w') as f:
            f.write('''
<!DOCTYPE html>
<html>
<head>
    <title>Book Recommendation System - AI Search</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css">
    <style>
        body {
            background-color: #121212;
            color: #e0e0e0;
            font-family: Arial, sans-serif;
            line-height: 1.6;
        }
        .navbar {
            background-color: #5c0013;
            overflow: hidden;
            box-shadow: 0 2px 5px rgba(0,0,0,0.5);
            margin-bottom: 0;
        }
        .navbar a {
            float: left;
            color: white;
            padding: 14px 20px;
            text-align: center;
            text-decoration: none;
            font-weight: 500;
            transition: background-color 0.3s;
        }
        .navbar a:hover {
            background-color: #6e0018;
        }
        .navbar .active {
            background-color: #8a0020;
        }
        h1 {
            color: #f5f5f5;
            text-align: center;
            margin: 30px 0;
        }
        .search-container {
            max-width: 600px;
            margin: 30px auto;
            background-color: #1e1e1e;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        #prompt {
            width: 100%;
            padding: 12px;
            margin-bottom: 15px;
            font-size: 16px;
            background-color: #2a2a2a;
            border: 1px solid #444;
            color: #e0e0e0;
            border-radius: 4px;
        }
        button {
            padding: 10px 20px;
            background-color: #ff6b35;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            display: block;
            margin: 0 auto;
            transition: background-color 0.3s;
        }
        button:hover {
            background-color: #e55a2b;
        }
        #results {
            margin-top: 30px;
            white-space: pre-line;
            background-color: #1e1e1e;
            padding: 20px;
            border-radius: 4px;
            border: 1px solid #333;
            max-width: 800px;
            margin: 30px auto;
        }
        .loading {
            text-align: center;
            display: none;
        }
        .loader {
            border: 5px solid #2a2a2a;
            border-top: 5px solid #ff6b35;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 2s linear infinite;
            margin: 20px auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .error {
            color: #e74c3c;
            font-weight: bold;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="navbar">
        <a href="/">Home</a>
        <a href="/recommend">Recommend</a>
        <a href="/gpt_recommends">Deepseek</a>
        <a href="/gpt_search" class="active">AI Search</a>
    </div>

    <div class="container">
        <h1>AI Book Recommendations</h1>
        
        <div class="search-container">
            <form id="search-form" onsubmit="searchBooks(event)">
                <input type="text" id="prompt" name="prompt" placeholder="Example: Provide similar books to Harry Potter" required>
                <button type="submit">Search</button>
            </form>
        </div>
        
        <div class="loading" id="loading">
            <div class="loader"></div>
            <p>Finding the perfect books for you...</p>
        </div>
        
        <div id="results"></div>
    </div>
    
    <script>
        function searchBooks(event) {
            event.preventDefault();
            
            const prompt = document.getElementById('prompt').value;
            const results = document.getElementById('results');
            const loading = document.getElementById('loading');
            
            // Clear previous results and show loading
            results.innerHTML = '';
            loading.style.display = 'block';
            
            // Send request to server
            fetch('/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    'prompt': prompt
                })
            })
            .then(response => response.json())
            .then(data => {
                loading.style.display = 'none';
                
                if (data.success) {
                    results.innerHTML = data.recommendations;
                } else {
                    results.innerHTML = `<div class="error">Error: ${data.error}</div>`;
                }
            })
            .catch(error => {
                loading.style.display = 'none';
                results.innerHTML = `<div class="error">Error: ${error.message}</div>`;
            });
        }
    </script>
</body>
</html>
            ''')
    
    app.run(debug=True)