import altair as alt
import pandas as pd
import streamlit as st

# Show the page title and description.
st.set_page_config(page_title="Albums Dataset", page_icon="🎵")
st.title("🎶 Albums dataset")
st.write(
    """
    This app visualizes data from [The Movie Database (TMDB)](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata).
    It shows which movie Genre performed best at the box office over the Years. Just 
    click on the widgets below to explore!
    """
)


# Load the data from a CSV. We're caching this so it doesn't reload every time the app
# reruns (e.g. if the user interacts with the widgets).
@st.cache_data
def load_data():
    df = pd.read_csv("data/Album Ratings - Album Ratings.csv")
    return df


df = load_data()

# Show a multiselect widget with the Genres using `st.multiselect`.
Genres = st.multiselect(
    "Genres",
    df.Genre.unique(),
    ["Action", "Adventure", "Biography", "Comedy", "Drama", "Horror"],
)

# Show a slider widget with the Years using `st.slider`.
Years = st.slider("Years", 1986, 2006, (2000, 2016))

# Filter the dataframe based on the widget input and reshape it.
df_filtered = df[(df["Genre"].isin(Genres)) & (df["Year"].between(Years[0], Years[1]))]
df_reshaped = df_filtered.pivot_table(
    index="Year", columns="Genre", values="Score", aggfunc="sum", fill_value=0
)
df_reshaped = df_reshaped.sort_values(by="Year", ascending=False)


# Display the data as a table using `st.dataframe`.
st.dataframe(
    df_reshaped,
    use_container_width=True,
    column_config={"Year": st.column_config.TextColumn("Year")},
)

# Display the data as an Altair chart using `st.altair_chart`.
df_chart = pd.melt(
    df_reshaped.reset_index(), id_vars="Year", var_name="Genre", value_name="Score"
)
chart = (
    alt.Chart(df_chart)
    .mark_line()
    .encode(
        x=alt.X("Year:N", title="Year"),
        y=alt.Y("Score:Q", title="Score earnings ($)"),
        color="Genre:N",
    )
    .properties(height=320)
)
st.altair_chart(chart, use_container_width=True)
