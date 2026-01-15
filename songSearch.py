import pandas as pd
import streamlit as st

df = pd.read_csv("song_data.csv")
df.index += 1

st.title("Songs")

menu = st.sidebar.selectbox("Select Action", 
                            ["Search by Song Name", 
                            "Search by Artist Name", 
                            "Display All Songs"])

if "search_done" not in st.session_state:
    st.session_state.search_done = False

if "search_result" not in st.session_state:
    st.session_state.search_result = pd.DataFrame()

if "selected_song" not in st.session_state:
    st.session_state.selected_song = "-- Select a song --"


if menu == "Search by Song Name":
    st.header("Search Song")
    song_name = st.text_input("Enter Song Name:", key="song_input").strip()

    if st.button("Search"):

        st.session_state.search_done = True
        st.session_state.selected_song = "-- Select a song --"

        if not song_name.strip():
            st.session_state.search_result = pd.DataFrame()
        else:
            st.session_state.search_result = df.loc[df["Song Name"].str.contains(song_name, case=False, na=False)]

    if not st.session_state.search_done:
        st.info("search for a song")
    else:
        result = st.session_state.search_result

        if result.empty:
            st.error("song not found")
        else:
            st.dataframe(result)
            song_options = ["-- Select a song --"] + result["Song Name"].tolist()
            selected_song = st.selectbox("select a song", song_options, key="selected_song")
            play_disabled = st.session_state.selected_song == "-- Select a song --"

            if not play_disabled:
                song_row = result[result["Song Name"] == st.session_state.selected_song].iloc[0]

            if st.button("Play on YouTube", disabled=play_disabled):
                st.markdown(f"""<a href="{song_row['YouTube Link']}" 
                            target="_blank">Open YouTube</a>""", 
                            unsafe_allow_html=True)

elif menu == "Search by Artist Name":
    st.header("Artist Name")

    artist_name = st.text_input("Enter Artist's Name:", key="artist_input")

    if st.button("Search Artist"):

        st.session_state.search_done = True
        st.session_state.selected_song = "-- Select a song --"

        if not artist_name.strip():
                st.warning("artist does not exist")
                st.session_state.search_result = pd.DataFrame()
        else:
            st.session_state.search_result = df.loc[df["Artist"].str.contains(artist_name, case=False, na=False)]

            result = st.session_state.search_result

    if not st.session_state.search_done:
        st.info("search for an artist")
    else:
        result = st.session_state.search_result

        if result.empty:
                st.error("artist not found")
        else:
            st.dataframe(result)
            song_options = ["-- Select a song --"] + result["Song Name"].tolist()

            selected_artist = st.selectbox("Select a song", song_options, key="selected_song")
            play_disabled = (st.session_state.selected_song == "-- Select a song --")

            if not play_disabled:
                song_row = result[result["Song Name"] == st.session_state.selected_song].iloc[0]

            if st.button("Play on YouTube", disabled=play_disabled):
                st.markdown(f"""<a href="{song_row['YouTube Link']}" 
                            target="_blank">Open YouTube</a>""", 
                            unsafe_allow_html=True)
            
elif menu == "Display All Songs":
    st.dataframe(df)