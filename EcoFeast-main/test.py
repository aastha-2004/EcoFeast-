import streamlit as st
from matcher import match_donor_to_best_receiver
import pandas as pd
import folium
from streamlit_folium import folium_static
from utils import haversine_distance

# Set page config
st.set_page_config(
    page_title="Food Waste Management System",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for improved theme
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #f1f8e9 0%, #dcedc8 100%);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #33691e !important;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #1b5e20 !important;
        font-weight: 600 !important;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #2e7d32 !important;
        color: white !important;
        border: none !important;
        border-radius: 5px !important;
        padding: 0.5rem 1rem !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        background-color: #1b5e20 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
    }
    
    /* Input fields */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select {
        background-color: #ffffff !important;
        border: 2px solid #81c784 !important;
        border-radius: 5px !important;
        padding: 0.5rem !important;
        color: #2e7d32 !important;
    }
    
    /* Form containers */
    .stForm {
        background-color: rgba(255, 255, 255, 0.95) !important;
        padding: 2rem !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        border: 1px solid #81c784 !important;
    }
    
    /* Dataframes */
    .stDataFrame {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 10px !important;
        padding: 1rem !important;
        border: 1px solid #81c784 !important;
    }
    
    /* Success messages */
    .stAlert {
        background-color: #e8f5e9 !important;
        border-left: 4px solid #2e7d32 !important;
        color: #1b5e20 !important;
    }
    
    /* Warning messages */
    .stWarning {
        background-color: #fff3e0 !important;
        border-left: 4px solid #ff9800 !important;
        color: #e65100 !important;
    }
    
    /* Error messages */
    .stError {
        background-color: #ffebee !important;
        border-left: 4px solid #f44336 !important;
        color: #c62828 !important;
    }
    
    /* Map container */
    .folium-map {
        border-radius: 10px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        border: 1px solid #81c784 !important;
    }
    
    /* Radio buttons */
    .stRadio > div {
        background-color: rgba(255, 255, 255, 0.95) !important;
        padding: 1rem !important;
        border-radius: 10px !important;
        border: 1px solid #81c784 !important;
    }
    
    /* Sidebar title */
    .css-1d391kg h1 {
        color: white !important;
    }
    
    /* Labels */
    .stMarkdown p {
        color: #2e7d32 !important;
        font-weight: 500 !important;
    }
    
    /* Text input labels */
    .stTextInput label, .stNumberInput label {
        color: #2e7d32 !important;
        font-weight: 500 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("🍽️ Food Waste Management System")
st.markdown("""
    <div style='background-color: rgba(255, 255, 255, 0.95); padding: 1.5rem; border-radius: 10px; 
    box-shadow: 0 4px 6px rgba(0,0,0,0.1); border: 1px solid #81c784;'>
        <p style='color: #2e7d32; font-size: 1.1rem;'>
            This system helps match food donors with the most suitable receivers based on various factors 
            including location, quantity, and dietary requirements. Together, we can reduce food waste and 
            make a positive impact on our environment.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Donor Form", "Receiver List", "Matching Results"])

if page == "Donor Form":
    st.header("Food Donor Information")
    
    # Donor form
    with st.form("donor_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            food_category = st.text_input("Food Category")
            quantity = st.number_input("Quantity (in portions)", min_value=1, step=1)
            ingredients = st.text_input("Ingredients (comma-separated)")
            contact_number = st.text_input("Contact Number")
        
        with col2:
            st.subheader("Location")
            latitude = st.number_input("Latitude", format="%.6f")
            longitude = st.number_input("Longitude", format="%.6f")
            pickup_time = st.time_input("Preferred Pickup Time")
        
        submit_donor = st.form_submit_button("Submit Donor Information")
        
        if submit_donor:
            donor = {
                "Food_Category": food_category,
                "Quantity": quantity,
                "latitude": latitude,
                "longitude": longitude,
                "Ingredients": [ing.strip() for ing in ingredients.split(",")],
                "Contact_Number": contact_number,
                "Pickup_Time": pickup_time
            }
            st.session_state.donor = donor
            st.success("Donor information submitted successfully!")

elif page == "Receiver List":
    st.header("Food Receiver Information")
    
    if 'receivers' not in st.session_state:
        st.session_state.receivers = []
    
    with st.form("receiver_form"):
        st.subheader("Add New Receiver")
        col1, col2 = st.columns(2)
        
        with col1:
            rec_latitude = st.number_input("Latitude", format="%.6f")
            rec_longitude = st.number_input("Longitude", format="%.6f")
            required_portions = st.number_input("Required Portions", min_value=1, step=1)
            contact_number = st.text_input("Contact Number")
        
        with col2:
            allergies = st.text_input("Allergies (comma-separated)")
            children = st.number_input("Number of children", min_value=0, step=1)
            elderly = st.number_input("Number of elderly", min_value=0, step=1)
            preferred_delivery_time = st.time_input("Preferred Delivery Time")
        
        submit_receiver = st.form_submit_button("Add Receiver")
        
        if submit_receiver:
            receiver = {
                "latitude": rec_latitude,
                "longitude": rec_longitude,
                "required_portions": required_portions,
                "allergies": [a.strip() for a in allergies.split(",")],
                "people": {
                    "children": children,
                    "elderly": elderly
                },
                "Contact_Number": contact_number,
                "Preferred_Delivery_Time": preferred_delivery_time
            }
            st.session_state.receivers.append(receiver)
            st.success("Receiver added successfully!")
    
    # Display current receivers
    if st.session_state.receivers:
        st.subheader("Current Receivers")
        receiver_data = []
        for i, rec in enumerate(st.session_state.receivers):
            receiver_data.append({
                "Receiver #": i+1,
                "Location": f"({rec['latitude']}, {rec['longitude']})",
                "Required Portions": rec['required_portions'],
                "Children": rec['people']['children'],
                "Elderly": rec['people']['elderly'],
                "Contact": rec['Contact_Number']
            })
        st.dataframe(pd.DataFrame(receiver_data))

elif page == "Matching Results":
    st.header("Matching Results")
    
    if 'donor' not in st.session_state or not st.session_state.receivers:
        st.warning("Please complete both donor and receiver information first!")
    else:
        if st.button("Find Best Match"):
            best_receiver, score, distance = match_donor_to_best_receiver(
                st.session_state.donor,
                st.session_state.receivers
            )
            
            if best_receiver:
                st.success("Best match found!")
                
                # Create a map
                m = folium.Map(
                    location=[st.session_state.donor['latitude'], st.session_state.donor['longitude']],
                    zoom_start=12
                )
                
                # Add donor marker
                folium.Marker(
                    [st.session_state.donor['latitude'], st.session_state.donor['longitude']],
                    popup="Donor",
                    icon=folium.Icon(color='green', icon='info-sign')
                ).add_to(m)
                
                # Add receiver marker
                folium.Marker(
                    [best_receiver['latitude'], best_receiver['longitude']],
                    popup="Best Match Receiver",
                    icon=folium.Icon(color='red', icon='info-sign')
                ).add_to(m)
                
                # Display map
                folium_static(m)
                
                # Display match details
                st.subheader("Match Details")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Donor Information**")
                    st.write(f"Food Category: {st.session_state.donor['Food_Category']}")
                    st.write(f"Quantity: {st.session_state.donor['Quantity']} portions")
                    st.write(f"Location: ({st.session_state.donor['latitude']}, {st.session_state.donor['longitude']})")
                    st.write(f"Contact: {st.session_state.donor['Contact_Number']}")
                    st.write(f"Pickup Time: {st.session_state.donor['Pickup_Time']}")
                
                with col2:
                    st.write("**Best Match Receiver**")
                    st.write(f"Location: ({best_receiver['latitude']}, {best_receiver['longitude']})")
                    st.write(f"Required Portions: {best_receiver['required_portions']}")
                    st.write(f"Children: {best_receiver['people']['children']}")
                    st.write(f"Elderly: {best_receiver['people']['elderly']}")
                    st.write(f"Contact: {best_receiver['Contact_Number']}")
                    st.write(f"Preferred Delivery Time: {best_receiver['Preferred_Delivery_Time']}")
                
                st.write(f"**Match Score:** {score:.2f}")
                st.write(f"**Distance:** {distance:.2f} km")
            else:
                st.error("No suitable receiver found.") 