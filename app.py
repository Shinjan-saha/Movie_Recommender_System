# Import necessary libraries
import streamlit as st          # For creating the web app interface
import pickle                   # For loading pre-saved Python objects (like models or data)
import pandas as pd             # For data manipulation and analysis
import requests                 # For making HTTP requests to web APIs
import zipfile                  # For unzipping model files
import os                       # For checking file existence

# Function to load custom CSS for styling the Streamlit app
def add_custom_css():
    with open("style.css") as f:  # Open the CSS file
        # Inject the CSS into the app using markdown and allow HTML
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

add_custom_css()  # Call the function to apply custom styles

# Function to fetch a movie poster image from the TMDB API using the movie's ID
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'
    )  # Send a GET request to the TMDB API for movie details
    data = response.json()  # Parse the response as JSON
    # Return the full URL to the movie's poster image
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

# Load the movie data from pickled file
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))  # Load movie dictionary
movies = pd.DataFrame(movies_dict)                       # Convert to DataFrame

# Unzip and load similarity.pkl at runtime
if not os.path.exists("similarity.pkl"):
    with zipfile.ZipFile("similarityPKL.zip", "r") as zip_ref:
        zip_ref.extract("similarity.pkl")  # Only extract similarity.pkl

similarity = pickle.load(open('similarity.pkl', 'rb'))   # Load similarity matrix

# Function to recommend similar movies based on the selected movie
def recommend(movie):
    # Find the index of the selected movie in the DataFrame
    movie_index = movies[movies['title'] == movie].index[0]
    # Get the similarity scores for that movie
    distances = similarity[movie_index]
    # Pair each movie index with its similarity score, sort by score (descending), skip the first (itself), pick next 5
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []           # List to store recommended movie titles
    recommended_movies_posters = []   # List to store recommended movie poster URLs
    for i in movie_list:              # For each recommended movie
        movie_id = movies.iloc[i[0]].movie_id      # Get the movie ID
        recommended_movies.append(movies.iloc[i[0]].title)  # Add the movie title to the list
        recommended_movies_posters.append(fetch_poster(movie_id))  # Fetch and add the poster image URL
    # Return both lists
    return recommended_movies, recommended_movies_posters

# Set the title of the Streamlit app
st.title('🎥 Movie Recommender System')

# Create a dropdown for the user to select a movie
selected_movie_name = st.selectbox(
    "Select a movie to get recommendations:",
    movies['title'].values  # Populate dropdown with movie titles from DataFrame
)

# When the 'Recommend' button is clicked
if st.button("Recommend"):
    # Call the recommend function and get recommended movie titles and posters
    names, posters = recommend(selected_movie_name)

    # Create 5 columns to display the recommendations side by side
    col1, col2, col3, col4, col5 = st.columns(5)

    # Display each recommended movie's title and poster in its respective column
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])





import streamlit as st

# Your main content
# st.markdown("<h1 style='text-align: center; font-weight: bold;'>Movie Recommender System</h1>", unsafe_allow_html=True)

# Your recommendation logic and UI components here...

# Footer
st.markdown("""<hr style="margin-top: 50px;"/>
<div style='text-align: center; font-size: 0.9em; color: gray;'>
    Copyright ©2025 <b>Sourav Louha</b>. All Rights Reserved.
</div>
""", unsafe_allow_html=True)
