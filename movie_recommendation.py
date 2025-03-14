import redis
import json

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Sample movies
movies = {
    "1": {"title": "The Matrix", "genre": "Sci-Fi"},
    "2": {"title": "The Godfather", "genre": "Drama"},
    "3": {"title": "Inception", "genre": "Sci-Fi"},
    "4": {"title": "Titanic", "genre": "Romance"}
}

# Store movies in Redis
for movie_id, details in movies.items():
    r.set(f"movie:{movie_id}", json.dumps(details))

# Function to add user ratings
def rate_movie(user_id, movie_id, rating):
    key = f"user:{user_id}:ratings"
    r.hset(key, movie_id, rating)

# Function to get recommendations
def recommend_movies(user_id):
    key = f"user:{user_id}:ratings"
    user_ratings = r.hgetall(key)
    
    # Find preferred genre
    genre_count = {}
    for movie_id, rating in user_ratings.items():
        if int(rating) >= 4:  # Consider only high ratings
            movie = json.loads(r.get(f"movie:{movie_id}"))
            genre = movie["genre"]
            genre_count[genre] = genre_count.get(genre, 0) + 1

    if not genre_count:
        return "Not enough ratings to recommend movies."

    favorite_genre = max(genre_count, key=genre_count.get)
    
    # Recommend movies from the favorite genre
    recommendations = []
    for movie_id, details in movies.items():
        if details["genre"] == favorite_genre and movie_id not in user_ratings:
            recommendations.append(details["title"])

    return recommendations if recommendations else "No new recommendations."

# Simulate user interactions
rate_movie("1", "1", 5)  # User 1 rates "The Matrix" 5 stars
rate_movie("1", "3", 4)  # User 1 rates "Inception" 4 stars
print(recommend_movies("1"))  # Should recommend "Sci-Fi" movies
