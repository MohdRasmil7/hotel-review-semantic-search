from flask import Flask, render_template, request, jsonify
import pandas as pd
import spacy
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
import pickle

app = Flask(__name__)
CACHE_FILE = 'embeddings_cache.pkl'
BATCH_SIZE = 1000

def load_data():
    """Load and preprocess the dataset."""
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'hotel_reviews.csv')  # Ensure this path is correct

    # Check if the file exists
    if not os.path.exists(data_path):
        raise FileNotFoundError("Dataset not found.")

    # Attempt to load the data with different encodings
    encodings_to_try = ['utf-8', 'ISO-8859-1', 'utf-8-sig', 'Windows-1252']
    for encoding in encodings_to_try:
        try:
            df = pd.read_csv(data_path, encoding=encoding)
            print(f"Successfully loaded data with encoding: {encoding}")
            break  # Exit the loop if loading succeeds
        except Exception as e:
            print(f"Failed to load with encoding {encoding}: {e}")
    else:
        raise ValueError("All encoding attempts failed.")

    # Process reviews
    df['cleaned_reviews'] = df['Review'].str.lower().dropna()
    
    return df

def load_model():
    """Load the spaCy model."""
    return spacy.load('en_core_web_md', disable=['ner', 'parser', 'tagger'])

def create_embeddings(df, nlp):
    """Create embeddings for the cleaned reviews."""
    embeddings = []
    for review in df['cleaned_reviews']:
        embeddings.append(nlp(review).vector)
    return embeddings

def cache_embeddings(embeddings):
    """Cache the embeddings for future use."""
    with open(CACHE_FILE, 'wb') as f:
        pickle.dump(embeddings, f)

def load_cached_embeddings():
    """Load embeddings from cache if available."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'rb') as f:
            return pickle.load(f)
    return None

def initialize_app():
    """Initialize the app by loading data and models."""
    nlp = load_model()
    df = load_data()
    cached_embeddings = load_cached_embeddings()
    
    if cached_embeddings is not None and len(cached_embeddings) == len(df):
        df['embeddings'] = cached_embeddings
    else:
        df['embeddings'] = create_embeddings(df, nlp)
        cache_embeddings(df['embeddings'].tolist())
    
    df.drop('cleaned_reviews', axis=1, inplace=True)
    return df, nlp

def search_reviews(query, df, nlp, top_k=5):
    """Find the most similar reviews to the query."""
    query_embedding = nlp(query.lower()).vector
    similarities = cosine_similarity([query_embedding], np.vstack(df['embeddings'].values))[0]
    
    # Get the top k indices
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    results = [{'review': df.iloc[idx]['Review'], 'sentiment': df.iloc[idx]['Feedback'], 'similarity': float(similarities[idx])} for idx in top_indices]
    
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_endpoint():
    query = request.form.get('query', '').strip()
    if not query:
        return jsonify({'error': 'Please provide a search query'}), 400

    try:
        results = search_reviews(query, df, nlp)
        return jsonify({'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stats')
def stats():
    """Get dataset statistics."""
    stats = {
        'total_reviews': len(df),
        'positive_reviews': len(df[df['Feedback'] == 'Pos']),
        'negative_reviews': len(df[df['Feedback'] == 'Neg'])
    }
    return jsonify(stats)

if __name__ == "__main__":
    df, nlp = initialize_app()
    app.run(debug=False, host='0.0.0.0', port=5000)
