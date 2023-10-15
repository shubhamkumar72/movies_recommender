import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    try:
        response = requests.get(
            'https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(
                movie_id))
        response.raise_for_status()  # Check for HTTP request errors
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            st.warning(f"No poster found for movie {movie_id}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching poster for movie {movie_id}: {str(e)}")
        return None


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for j in movies_list:
        movie_id = movies.iloc[j[0]].movie_id
        poster_url = fetch_poster(movie_id)
        if poster_url:
            recommended_movies.append(movies.iloc[j[0]].title)
            recommended_movies_posters.append(poster_url)

    return recommended_movies, recommended_movies_posters


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')
selected_movie_name = st.selectbox(
    'Select a movie:',
    movies['title'].values)
if st.button('Recommend'):
    recommendations, posters = recommend(selected_movie_name)
    for i in range(len(recommendations)):
        st.text(recommendations[i])
        if posters[i]:  # Check if the poster URL is not None
            st.image(posters[i])
