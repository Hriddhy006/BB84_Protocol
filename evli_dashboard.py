import streamlit as st
import requests

st.set_page_config(page_title="Interference Panel", layout="wide")
st.title("😈 Targeted Link Sabotage")

cities = ["London", "Paris", "Berlin", "Brussels", "Amsterdam", "Munich", "Prague", "Vienna", "Madrid", "Lyon"]
all_links = [f"{cities[i]}-{cities[j]}" for i in range(len(cities)) for j in range(i+1, len(cities))]

noise_map = {}
cols = st.columns(3)
for idx, link in enumerate(all_links):
    with cols[idx % 3]:
        noise_map[link] = st.slider(f"{link}", 0.0, 1.0, 0.1, key=link)

# Push updates instantly
requests.post("http://127.0.0.1:5000/update_evil", json={
    "noise_map": noise_map,
    "eves": [k for k,v in noise_map.items() if v > 0.4]
})