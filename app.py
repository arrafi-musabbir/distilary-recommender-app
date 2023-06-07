'''
Author: Bappy Ahmed
Email: entbappy73@gmail.com
Date: 2021-Nov-15
'''

import pickle
import streamlit as st
import requests
from rapidfuzz import process, fuzz
import pandas as pd
import py7zr
import base64
import os


# st.set_page_config(layout="wide")
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('background.png')  


def recommend(alcohol):
    # print(alcohol)
    result_df = pd.DataFrame(columns = alcohols.columns[:-1])
    try:
        index = alcohols[alcohols['tags'] == alcohol].index[0]
    except:
        most_similar = process.extract(alcohol, alcohols['product'], scorer=fuzz.WRatio, limit=1)
        index = most_similar[0][2]
        # print("jere")
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key = lambda x: x[1])
    recommended_alcohol_names = []
    
    for i in distances[0:5]:
        recommended_alcohol_names.append(alcohols.iloc[i[0]].product)
        for i in distances[0:5]:
            if i[0]>=9096:
                result_df.loc[len(result_df)] = alcohols.iloc[i[0]-9096]
            else:
                result_df.loc[len(result_df)] = alcohols.iloc[i[0]]
    result_df = result_df.drop_duplicates()
        # result_df.loc[len(result_df)] = alcohols.iloc[i[0]]
    # return recommended_alcohol_names
    result_df = result_df[result_df['price/bottle (€)'] >= 0]
    return result_df

def _max_width_():
    max_width_str = f"max-width: 2000px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )

def recommendAlcohls(selected_alcohol):
    recommended_alcohol_names = recommend(selected_alcohol)
    # recommended_alcohol_names = recommended_alcohol_names.sort_values(by=['price/case (€)'], ascending=True, ignore_index=True)

    # Display a static table       
    
    recommended_alcohol_names.rename(columns = {'alcohol (%)':'alc(%)'}, inplace = True)
    st.dataframe(recommended_alcohol_names, _max_width_())  

st.header('Alcohol Recommender System')
archive = py7zr.SevenZipFile('similarity.7z', mode='r')
archive.extractall(path=os.getcwd())
archive.close()

alcohols = pickle.load(open('artifacts/alcohol_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
import numpy as np



alcohol_list = alcohols['tags'].values
selected_alcohol = st.selectbox(
    "Type or select a alcohol from the dropdown",
    alcohol_list
    # on_change=recommendAlcohls(selected_alcohol)
)



with st.container():
    _max_width_()
    if st.button('Show Recommendation'):
        
        recommendAlcohls(selected_alcohol)

# if st.button('Show Recommendation'):
    
#     recommendAlcohls(selected_alcohol)

footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Developed by <a style='display: block; text-align: center;' href="https://www.upwork.com/freelancers/~01e67fa858ee6db637" target="_blank">Musabbir Arrafi</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)