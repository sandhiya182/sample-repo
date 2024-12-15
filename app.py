import streamlit as st
import pandas as pd
import pymysql
import datetime


def fetch_data_from_db():
    """
    Connects to the MySQL database and fetches data from the 'bus_routes' table.

    Returns:
        pd.DataFrame: DataFrame containing the data from the 'bus_routes' table.
    """
    # Establish a connection to the MySQL database
    conn = pymysql.connect(host='localhost', user='root', passwd='Santhi@18', database='redbus_data_scraping')
    
    # Define the SQL query to fetch all data from the bus_routes table
    query = "SELECT * FROM bus_routes"
    
    # Execute the query and store the result in a DataFrame
    df = pd.read_sql(query, conn)
    
    # Close the database connection
    conn.close()
    
    return df

def display_bus_data(df):
    """
    Displays the bus data in a Streamlit app with various filtering options.

    Args:
        df (pd.DataFrame): DataFrame containing bus route data to display.
    """
    # Apply custom styling to the Streamlit app
    st.markdown(
        """
        <style>
        body {
            background-color: #FFFFFF;
        }
        .header {
            text-align: center;
            font-size: 32px;
            font-weight: bold;
            color: #003366;
            padding: 20px 0;
        }
        .filter-section {
            margin-bottom: 20px;
        }
        .filter-label {
            font-weight: bold;
            color: #003366;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Add a header for the page
    st.markdown('<div class="header">Red Bus Routes</div>', unsafe_allow_html=True)

    # Create a section for filter options
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)

    # Create columns for various filter options
    col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 2, 2])

    with col1:
        # Filter by state name
        state_options = df['state_name'].unique()
        selected_state = st.selectbox("State Name", ["All"] + list(state_options))

    with col2:
        # Filter by bus route
        route_options = df['route_name'].unique()
        selected_route = st.selectbox("Bus Route", ["All"] + list(route_options))

    with col3:
        # Filter by bus type
        bustype_options = df['bustype'].unique()
        selected_bustype = st.selectbox("Bus Type", ["All"] + list(bustype_options))

    with col4:
        # Filter by star rating
        rating_min = st.number_input("Min Rating", min_value=0.0, max_value=5.0, value=0.0, step=0.1)

    with col5:
        # Filter by price
        price_min = st.number_input("Min Price", min_value=0, value=0)
        price_max = st.number_input("Max Price", min_value=0, value=10000)

    with col6:
        # Filter by departure time
        dep_time_min = st.time_input("Min Departure Time", value=datetime.time(0, 0)) 
        dep_time_max = st.time_input("Max Departure Time", value=datetime.time(23, 59, 59))

    st.markdown('</div>', unsafe_allow_html=True)

    # Ensure 'departing_time' column is in datetime format for filtering
    df['departing_time'] = pd.to_datetime(df['departing_time'], format='%H:%M:%S', errors='coerce').dt.time

    # Apply filters to the DataFrame based on user inputs
    if selected_state != "All":
        df = df[df['state_name'] == selected_state]
    if selected_route != "All":
        df = df[df['route_name'] == selected_route]
    if selected_bustype != "All":
        df = df[df['bustype'] == selected_bustype]
    df = df[(df['price'] >= price_min) & (df['price'] <= price_max)]
    df = df[df['star_rating'] >= rating_min]
    df = df[(df['departing_time'] >= dep_time_min) & (df['departing_time'] <= dep_time_max)]

    # Display the filtered data in a table
    st.write("### Bus Routes")
    st.dataframe(df, use_container_width=True, hide_index=True)

def main():
    """
    Main function to set up and run the Streamlit application.

    Sets the page layout to wide and initiates the data fetching and display functions.
    """
    st.set_page_config(layout="wide")  # Maximize window width

    # Fetch data from the database
    df = fetch_data_from_db()
    
    # Display the fetched data with filters
    display_bus_data(df)

if __name__ == "__main__":
    main()
