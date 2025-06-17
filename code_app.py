import pandas as pd
import numpy as np
import streamlit as st
import pickle
import requests
from numpy.f2py.crackfortran import true_intent_list

def fetch_poster(movie_id):
   response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=d892942b107b9eb7ee0545a4819c6fcf&language=en-US'.format(movie_id))
   data=response.json()
   return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
import requests

'''def fetch_poster(movie_id):
    try:
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=d892942b107b9eb7ee0545a4819c6fcf&language=en-US'
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster for movie ID {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=No+Image"'''

def recommend(movie):
    movie_index= movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]

    movies_list=sorted(list(enumerate(distances)),reverse=True , key=lambda x: x[1])[1:6] #enumerate() har element ko uske index ke saath pair karta hai.
    # enumerate ka output hoga........ like this # Output: [(0, 0.1), (1, 0.9), (2, 0.3), (3, 0.8), (4, 0.5)]  here second values are the similarity scores

    print(movies_list)

    recommended_movies=[]
    recommended_movies_posters=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].id ## iloc ka matlab hota hai: integer-location based indexing
                                             # Yaani dataframe ke 3rd row ka pura data milega.

        # print(movie_id)
        recommended_movies.append(movies.iloc[i[0]].title)
        ## fetch movie posters
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters


st.title("Movies Recommender System ...")
movies_dict=pickle.load(open(r'C:\Users\wwwan\PycharmProjects\movie_recommander_sysyem\movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity=pickle.load(open("similarity.pkl",'rb'))


selected_movie_name=st.selectbox(
    "How would you like to be contacted ?",
    movies['title'].values
)
if st.button("Recommended"):
    names,posters=recommend(selected_movie_name)
    col1, col2, col3, col4,col5= st.columns(5)

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