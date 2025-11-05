import altair as alt
import pandas as pd
import streamlit as st

# Streamlit page setup
st.set_page_config(page_title="🎵 Album Ratings Dashboard", page_icon="🎶")
st.title("🎶 Album Ratings Dashboard")

st.write("""
Explore your album ratings interactively!
Select artists or albums, and visualize how your ratings compare across categories.
""")

# --- Load data ---
@st.cache_data
def load_data():
    df = pd.read_csv("Album Ratings - Album Ratings.csv")
    return df

df = load_data()

# --- Inspect the dataset ---
st.subheader("Data Preview")
st.dataframe(df.head())

# --- Basic checks ---
st.write("Columns detected:", list(df.columns))

# --- Filters (based on your likely columns) ---
if "Artist" in df.columns:
    artists = st.multiselect("Select Artist(s)", sorted(df["Artist"].unique()))
    if artists:
        df = df[df["Artist"].isin(artists)]

if "Album" in df.columns:
    albums = st.multiselect("Select Album(s)", sorted(df["Album"].unique()))
    if albums:
        df = df[df["Album"].isin(albums)]

# --- Rating visualization ---
rating_col = None
for c in df.columns:
    if "Score" in c or "Rating" in c:
        rating_col = c
        break

if rating_col:
    st.subheader("Average Album Ratings")
    avg_ratings = (
        df.groupby("Artist")[rating_col]
        .mean()
        .reset_index()
        .sort_values(by=rating_col, ascending=False)
    )

    chart = (
        alt.Chart(avg_ratings)
        .mark_bar()
        .encode(
            x=alt.X(rating_col, title="Average Rating"),
            y=alt.Y("Artist", sort="-x", title="Artist"),
            tooltip=["Artist", rating_col],
        )
        .properties(height=400)
    )
    st.altair_chart(chart, use_container_width=True)
else:
    st.warning("Couldn’t find a rating column (something like 'Score' or 'Rating').")

# --- Optional: Album art display if there's an image/URL column ---
img_cols = [c for c in df.columns if "art" in c.lower() or "cover" in c.lower()]
if img_cols:
    st.subheader("Album Covers")
    for _, row in df.iterrows():
        st.image(row[img_cols[0]], caption=f"{row.get('Album', '')} by {row.get('Artist', '')}")
