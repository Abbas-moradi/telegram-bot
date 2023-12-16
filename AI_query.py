from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_most_similar_question(user_input, database, vectorizer, tfidf_matrix):
    user_vector = vectorizer.transform([user_input])

    # Calculate cosine similarity between user input and database questions
    similarities = cosine_similarity(user_vector, tfidf_matrix)

    # Get the index of the most similar question
    most_similar_index = similarities.argmax()

    most_similar_question = list(database.keys())[most_similar_index]
    return most_similar_question, database[most_similar_question]

def result(user_input, database):
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Fit and transform the database questions
    tfidf_matrix = vectorizer.fit_transform(database.keys())
    
    most_similar_question, answer = get_most_similar_question(user_input, database, vectorizer, tfidf_matrix)
    return most_similar_question, answer

