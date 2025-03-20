import streamlit as st
import pandas as pd


@st.cache_data
def load_data():
    df = pd.read_csv("airbnb.csv")
    return df


data = load_data()


data['minimum_nights'] = pd.to_numeric(data['minimum_nights'], errors='coerce')
data = data.dropna(subset=['minimum_nights'])

st.title("Carolina Gasalla")


st.sidebar.header("Filters")
neighborhoods = st.sidebar.multiselect(
    "Select Neighborhoods", 
    data['neighbourhood'].unique(), 
    default=data['neighbourhood'].unique()
)

room_types = st.sidebar.multiselect(
    "Select Room Type", 
    data['room_type'].unique(), 
    default=data['room_type'].unique()
)


data_filtered = data[
    (data['neighbourhood'].isin(neighborhoods)) & 
    (data['room_type'].isin(room_types))
]


tab1, tab2 = st.tabs(["Analysis", "Simulator"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Room Type vs Price")
        table1 = data_filtered.groupby('room_type')['price'].describe()
        st.dataframe(table1)
    
    with col2:
        st.subheader("Number of Reviews by Room Type")
        table2 = data_filtered.groupby('room_type')['number_of_reviews'].describe()
        st.dataframe(table2)
    
    st.subheader("Top Reviewed Apartments by Neighborhood")
    top_reviews = data_filtered.groupby(['neighbourhood', 'room_type']).agg({'reviews_per_month': 'sum'}).reset_index()
    st.dataframe(top_reviews)


with tab2:
    st.header("Price Recommendation Simulator")
    
    sim_neighborhood = st.selectbox("Select Neighborhood", data['neighbourhood'].unique())
    sim_type = st.selectbox("Select Room Type", data['room_type'].unique())
    
  
    max_nights = int(data['minimum_nights'].max()) 
    sim_people = st.slider("Minimum Nights", 1, max_nights, 2)
    
    
    filtered_price = data[
        (data['neighbourhood'] == sim_neighborhood) & 
        (data['room_type'] == sim_type)
    ]
    recommended_price = filtered_price['price'].median() if not filtered_price.empty else "Not enough data"
    
    st.subheader(f"Recommended Price: ${recommended_price}")
