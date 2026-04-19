import streamlit as st
import pandas as pd
import folium
import requests
import time
from streamlit_folium import folium_static
from streamlit_lottie import st_lottie
from matcher import match_donor_to_best_receiver
from utils import haversine_distance

# Utility: Load Lottie Animations
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Set page config
st.set_page_config(
    page_title="EcoFeast | Food Waste Management",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced Custom CSS: Modern green theme with improved styling and animations
st.markdown("""
    <style>
    /* Overall App Styling: Elegant Green Gradient */
    .stApp {
        background: linear-gradient(135deg, #1B5E20, #2E7D32, #388E3C);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        font-family: 'Poppins', 'Segoe UI', sans-serif;
        color: #f1f1f1;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Typography Improvements */
    h1, h2, h3, h4, h5, h6 {
        font-weight: 600 !important;
        color: #E8F5E9 !important;
    }
    
    h1 {
        font-size: 2.5rem !important;
        letter-spacing: -0.5px !important;
    }
    
    h2 {
        font-size: 2rem !important;
    }
    
    h3 {
        font-size: 1.5rem !important;
    }
    
    p, li, div {
        font-weight: 400;
        line-height: 1.6;
    }
    
    /* Hero Section with Parallax Effect */
    .hero-container {
        background-image: url("https://images.unsplash.com/photo-1542838132-92c53300491e?q=80&w=2670&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        position: relative;
        border-radius: 16px;
        margin-bottom: 2.5rem;
        padding: 5rem 2rem;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        transition: all 0.5s ease;
    }
    
    .hero-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
    }
    
    .hero-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(27, 94, 32, 0.85), rgba(46, 125, 50, 0.85));
        border-radius: 16px;
    }
    
    .hero-content {
        position: relative;
        text-align: center;
        color: #ffffff;
        z-index: 1;
        animation: fadeInUp 1s ease-out;
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .hero-content h1 {
        font-size: 4.5rem !important;
        margin-bottom: 0.5rem;
        background: linear-gradient(90deg, #E8F5E9, #A5D6A7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .hero-content p {
        font-size: 1.8rem;
        font-weight: 300;
        margin-top: 1rem;
        opacity: 0;
        animation: fadeIn 1s ease-out 0.5s forwards;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Enhanced Carousel Styling */
    .carousel-container {
        max-width: 100%;
        margin: 2.5rem auto;
        overflow: hidden;
        border-radius: 16px;
        box-shadow: 0 15px 30px rgba(0,0,0,0.3);
        position: relative;
    }
    
    .carousel-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(to bottom, 
                                  rgba(27, 94, 32, 0.2), 
                                  rgba(27, 94, 32, 0));
        z-index: 1;
        pointer-events: none;
    }
    
    .slides {
        display: flex;
        width: 300%;
        animation: slideAnimation 20s infinite ease-in-out;
    }
    
    .slides img {
        width: 100%;
        height: 500px;
        object-fit: cover;
        border: 0;
        transition: transform 0.5s ease;
    }
    
    .slides:hover {
        animation-play-state: paused;
    }
    
    @keyframes slideAnimation {
        0%   { transform: translateX(0%); }
        28%  { transform: translateX(0%); }
        33%  { transform: translateX(-33.33%); }
        61%  { transform: translateX(-33.33%); }
        66%  { transform: translateX(-66.66%); }
        94%  { transform: translateX(-66.66%); }
        100% { transform: translateX(0%); }
    }
    
    /* Feature Cards with Hover Effects */
    .feature-card {
        background: linear-gradient(135deg, #2E7D32, #388E3C);
        padding: 2.5rem;
        margin: 1.5rem 0;
        border-radius: 16px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.15);
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid rgba(255,255,255,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
                                  rgba(255,255,255,0), 
                                  rgba(255,255,255,0.1), 
                                  rgba(255,255,255,0));
        transition: left 0.7s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.25);
    }
    
    .feature-card:hover::before {
        left: 100%;
    }
    
    .feature-card h3 {
        color: #A5D6A7 !important;
        margin-bottom: 1rem;
        position: relative;
        display: inline-block;
    }
    
    .feature-card h3::after {
        content: '';
        position: absolute;
        width: 50%;
        height: 3px;
        background: #A5D6A7;
        bottom: -10px;
        left: 25%;
        border-radius: 2px;
    }
    
    .feature-card p {
        color: #f1f1f1;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1.5rem;
        color: #A5D6A7;
    }
    
    /* Enhanced Button Styling with Animation */
    .stButton>button {
        background: linear-gradient(135deg, #2e7d32, #388E3C) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.9rem 1.8rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.15) !important;
        position: relative;
        overflow: hidden;
        z-index: 1;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
                                  transparent, 
                                  rgba(255,255,255,0.2), 
                                  transparent);
        transition: left 0.7s ease;
        z-index: -1;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 20px rgba(0,0,0,0.2) !important;
    }
    
    .stButton>button:hover::before {
        left: 100%;
    }
    
    .stButton>button:active {
        transform: translateY(1px);
    }
    
    /* Enhanced Form Inputs with Focus Effects */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select,
    .stTimeInput>div>div>input {
        background-color: rgba(55, 71, 79, 0.8) !important;
        border: 2px solid rgba(96, 125, 139, 0.5) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        font-size: 1.1rem !important;
        color: #ffffff !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
    }
    
    .stTextInput>div>div>input:focus,
    .stNumberInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus,
    .stTimeInput>div>div>input:focus {
        border-color: #81C784 !important;
        box-shadow: 0 0 0 3px rgba(129, 199, 132, 0.3) !important;
        transform: translateY(-2px);
    }
    
    /* Label Styling */
    .stTextInput label, 
    .stNumberInput label, 
    .stSelectbox label,
    .stTimeInput label {
        color: #A5D6A7 !important;
        font-weight: 500 !important;
        font-size: 1.05rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Enhanced Form and DataFrame Containers */
    .stForm, .stDataFrame {
        background: linear-gradient(135deg, rgba(69, 90, 100, 0.9), rgba(55, 71, 79, 0.9)) !important;
        padding: 2.5rem !important;
        border-radius: 16px !important;
        box-shadow: 0 15px 30px rgba(0,0,0,0.2) !important;
        margin-bottom: 2.5rem;
        color: #ffffff;
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .stForm:hover, .stDataFrame:hover {
        box-shadow: 0 20px 40px rgba(0,0,0,0.25) !important;
        transform: translateY(-5px);
    }
    
    /* Form Section Headers */
    .form-section-header {
        color: #A5D6A7 !important;
        font-size: 1.5rem !important;
        margin-bottom: 1.5rem !important;
        padding-bottom: 0.8rem;
        border-bottom: 2px solid rgba(165, 214, 167, 0.3);
    }
    
    /* Enhanced Sidebar Styling with Animation */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1B5E20, #2E7D32) !important;
        color: #ffffff;
        border-right: 1px solid rgba(255,255,255,0.1);
        box-shadow: 5px 0 15px rgba(0,0,0,0.2);
    }
    
    [data-testid="stSidebar"] * {
        color: #ffffff;
    }
    
    [data-testid="stSidebar"] .sidebar-content {
        padding: 2rem 1rem;
    }
    
    [data-testid="stSidebar"] h1 {
        font-size: 2rem !important;
        text-align: center;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid rgba(255,255,255,0.2);
    }
    
    /* Enhanced Map Container Styling */
    .folium-map {
        border-radius: 16px !important;
        box-shadow: 0 15px 30px rgba(0,0,0,0.25) !important;
        border: 2px solid rgba(96, 125, 139, 0.5) !important;
        overflow: hidden !important;
        transition: all 0.3s ease;
    }
    
    .folium-map:hover {
        box-shadow: 0 20px 40px rgba(0,0,0,0.3) !important;
        transform: translateY(-5px);
    }
    
    /* Success and Error Messages */
    .stSuccess, .stInfo, .stWarning, .stError {
        border-radius: 12px !important;
        padding: 1rem !important;
        animation: slideInRight 0.5s ease-out;
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* Dataframe Styling */
    .dataframe {
        font-family: 'Poppins', sans-serif !important;
    }
    
    .dataframe th {
        background-color: rgba(46, 125, 50, 0.7) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 12px 15px !important;
        text-transform: uppercase;
        font-size: 0.9rem;
        letter-spacing: 0.5px;
    }
    
    .dataframe td {
        padding: 12px 15px !important;
        border-bottom: 1px solid rgba(255,255,255,0.1) !important;
    }
    
    .dataframe tr:nth-child(even) {
        background-color: rgba(255,255,255,0.05) !important;
    }
    
    .dataframe tr:hover {
        background-color: rgba(129, 199, 132, 0.1) !important;
    }
    
    /* Card Layout for Match Details */
    .match-card {
        background: linear-gradient(135deg, rgba(69, 90, 100, 0.9), rgba(55, 71, 79, 0.9));
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 10px 20px rgba(0,0,0,0.15);
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.3s ease;
    }
    
    .match-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.2);
    }
    
    .match-card h4 {
        color: #A5D6A7 !important;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(165, 214, 167, 0.3);
    }
    
    .match-card p {
        margin-bottom: 0.5rem;
        display: flex;
        justify-content: space-between;
    }
    
    .match-card p strong {
        color: #A5D6A7;
    }
    
    /* Loading Animation */
    .loading-animation {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 2rem 0;
    }
    
    .loading-spinner {
        width: 50px;
        height: 50px;
        border: 5px solid rgba(165, 214, 167, 0.3);
        border-radius: 50%;
        border-top-color: #A5D6A7;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Progress Bar Animation */
    .progress-container {
        width: 100%;
        height: 10px;
        background-color: rgba(255,255,255,0.1);
        border-radius: 5px;
        margin: 1.5rem 0;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #2E7D32, #81C784);
        border-radius: 5px;
        animation: progressAnimation 2s ease-out;
    }
    
    @keyframes progressAnimation {
        from { width: 0%; }
        to { width: 100%; }
    }
    
    /* Entrance Animation for Main Content */
    .main .block-container {
        animation: fadeInUp 0.8s ease-out;
    }
    
    /* Tooltip Styling */
    .tooltip {
        position: relative;
        display: inline-block;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background-color: rgba(46, 125, 50, 0.9);
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 10px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .tooltip .tooltiptext::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -5px;
        border-width: 5px;
        border-style: solid;
        border-color: rgba(46, 125, 50, 0.9) transparent transparent transparent;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    
    /* Responsive Adjustments */
    @media (max-width: 768px) {
        .hero-content h1 {
            font-size: 3rem !important;
        }
        
        .hero-content p {
            font-size: 1.4rem;
        }
        
        .feature-card {
            padding: 1.5rem;
        }
        
        .slides img {
            height: 300px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Load Lottie Animations
lottie_food = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_dgjKx3.json")
lottie_location = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_UJjaUv.json")
lottie_community = load_lottieurl("https://assets8.lottiefiles.com/private_files/lf30_f0fhps1k.json")

# Enhanced Hero Section with Animated Text
st.markdown("""
    <div class="hero-container">
      <div class="hero-overlay"></div>
      <div class="hero-content">
        <h1>EcoFeast</h1>
        <p>Reduce Food Waste • Empower Communities • Save the Planet</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

# Enhanced Carousel with Smooth Transitions
st.markdown("""
    <div class="carousel-container">
      <div class="slides">
        <img src="https://images.unsplash.com/photo-1534533983688-c7b8e13fd3b6?q=80&w=2670&auto=format&fit=crop&ixlib=rb-4.0.3" alt="Sustainable Food">
        <img src="https://images.unsplash.com/photo-1542624771497-851f77d79349?q=80&w=2666&auto=format&fit=crop&ixlib=rb-4.0.3" alt="Community Garden">
        <img src="https://images.unsplash.com/photo-1490818387583-1baba5e638af?q=80&w=2664&auto=format&fit=crop&ixlib=rb-4.0.3" alt="Fresh Produce">
      </div>
    </div>
    """, unsafe_allow_html=True)

# Feature Cards with Icons
st.markdown("""
    <div style="display: flex; flex-wrap: wrap; gap: 20px; margin: 2rem 0;">
        <div class="feature-card" style="flex: 1; min-width: 250px;">
            <div class="feature-icon">🌱</div>
            <h3>Reduce Waste</h3>
            <p>Help reduce the 1.3 billion tons of food wasted globally each year by connecting surplus food with those who need it most.</p>
        </div>
        <div class="feature-card" style="flex: 1; min-width: 250px;">
            <div class="feature-icon">🤝</div>
            <h3>Build Community</h3>
            <p>Create meaningful connections between donors and receivers, strengthening community bonds and support networks.</p>
        </div>
        <div class="feature-card" style="flex: 1; min-width: 250px;">
            <div class="feature-icon">🌍</div>
            <h3>Environmental Impact</h3>
            <p>Reduce greenhouse gas emissions and conserve resources by preventing food from ending up in landfills.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main Content with Lottie Animation
col1, col2 = st.columns((2,1))
with col1:
    st.markdown("<h1 style='margin-top: 0;'>🍽️ Food Waste Management System</h1>", unsafe_allow_html=True)
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(69, 90, 100, 0.9), rgba(55, 71, 79, 0.9)); 
             padding: 1.8rem; border-radius: 16px; box-shadow: 0 10px 20px rgba(0,0,0,0.15); 
             border: 1px solid rgba(255,255,255,0.1);'>
            <p style='color: #ffffff; font-size: 1.3rem; line-height: 1.7;'>
                Our intelligent system matches food donors with the perfect receivers based on location, 
                quantity, and dietary needs. Join our growing community of environmentally conscious 
                individuals and organizations making a real difference.
            </p>
        </div>
        """, unsafe_allow_html=True)
with col2:
    if lottie_food:
        st_lottie(lottie_food, height=300, key="hero_anim")

# Enhanced Sidebar Navigation
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.title("Navigation")
    
    # Add a small animation to sidebar
    if lottie_community:
        st_lottie(lottie_community, height=180, key="sidebar_anim")
    
    # Enhanced radio buttons for navigation
    page = st.radio("", ["Donor Form", "Receiver List", "Matching Results", "Admin Panel"])
    
    # Add impact statistics
    st.markdown("---")
    st.markdown("<h3 style='text-align: center; margin-bottom: 1rem;'>Impact Stats</h3>", unsafe_allow_html=True)
    
    # Sample stats - these would be calculated from your actual data
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div style='background: rgba(255,255,255,0.1); border-radius: 10px; padding: 10px; text-align: center;'>
                <h3 style='margin: 0; font-size: 1.8rem;'>1,250</h3>
                <p style='margin: 0; font-size: 0.8rem; opacity: 0.8;'>Meals Shared</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div style='background: rgba(255,255,255,0.1); border-radius: 10px; padding: 10px; text-align: center;'>
                <h3 style='margin: 0; font-size: 1.8rem;'>350</h3>
                <p style='margin: 0; font-size: 0.8rem; opacity: 0.8;'>CO₂ Reduced</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Donor Form Tab with Enhanced UI
if page == "Donor Form":
    st.markdown("<h2>🥗 Food Donor Information</h2>", unsafe_allow_html=True)
    
    # Add location animation
    if lottie_location:
        st_lottie(lottie_location, height=200, key="location_anim")
    
    with st.form("donor_form"):
        st.markdown("<p class='form-section-header'>Share Your Surplus Food</p>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<p style='color: #A5D6A7; font-weight: 500; margin-bottom: 1rem;'>Food Details</p>", unsafe_allow_html=True)
            
            food_category = st.selectbox(
                "Food Category",
                ["Prepared Meals", "Fresh Produce", "Bakery Items", "Canned Goods", "Dairy", "Other"],
                help="Select the category that best describes your food donation"
            )
            
            quantity = st.number_input(
                "Quantity (in portions)", 
                min_value=1, 
                step=1,
                help="Estimate how many individual portions your donation could provide"
            )
            
            ingredients = st.text_area(
                "Ingredients (comma-separated)",
                help="List main ingredients to help identify potential allergens"
            )
            
            contact_number = st.text_input(
                "Contact Number",
                help="Your phone number for coordination purposes"
            )
            
        with col2:
            st.markdown("<p style='color: #A5D6A7; font-weight: 500; margin-bottom: 1rem;'>Location & Timing</p>", unsafe_allow_html=True)
            
            latitude = st.number_input(
                "Latitude", 
                format="%.6f",
                help="Your location coordinates (latitude)"
            )
            
            longitude = st.number_input(
                "Longitude", 
                format="%.6f",
                help="Your location coordinates (longitude)"
            )
            
            pickup_time = st.time_input(
                "Preferred Pickup Time",
                help="When would you prefer the food to be collected?"
            )
            
            # Additional field for better UX
            pickup_window = st.slider(
                "Pickup Window (hours)", 
                min_value=1, 
                max_value=24, 
                value=2,
                help="How long is your pickup window around the preferred time?"
            )
        
        # Visual progress indicator
        st.markdown("""
            <div class="progress-container">
                <div class="progress-bar" style="width: 100%;"></div>
            </div>
            <p style='text-align: right; color: #A5D6A7; font-size: 0.9rem; margin-top: 0.5rem;'>
                Form complete - ready to submit!
            </p>
        """, unsafe_allow_html=True)
        
        submit_donor = st.form_submit_button("Submit Donation")
        
        if submit_donor:
            # Show loading animation
            with st.spinner("Processing your donation..."):
                time.sleep(1)  # Simulate processing
                
                donor = {
                    "Food_Category": food_category,
                    "Quantity": quantity,
                    "latitude": latitude,
                    "longitude": longitude,
                    "Ingredients": [ing.strip() for ing in ingredients.split(",")],
                    "Contact_Number": contact_number,
                    "Pickup_Time": pickup_time,
                    "Pickup_Window": pickup_window
                }
                st.session_state.donor = donor
                
                # Success message with animation
                st.success("🎉 Thank you for your donation! Your contribution will make a difference.")
                
                # Show impact visualization
                st.markdown("<h4 style='color: #A5D6A7; margin-top: 1.5rem;'>Your Donation Impact</h4>", unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"""
                        <div class="match-card" style="text-align: center;">
                            <div style="font-size: 2.5rem; color: #A5D6A7; margin-bottom: 0.5rem;">{quantity}</div>
                            <p style="margin: 0;">Meals Provided</p>
                        </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                        <div class="match-card" style="text-align: center;">
                            <div style="font-size: 2.5rem; color: #A5D6A7; margin-bottom: 0.5rem;">{quantity * 2.5:.1f}</div>
                            <p style="margin: 0;">kg CO₂ Saved</p>
                        </div>
                    """, unsafe_allow_html=True)
                with col3:
                    st.markdown(f"""
                        <div class="match-card" style="text-align: center;">
                            <div style="font-size: 2.5rem; color: #A5D6A7; margin-bottom: 0.5rem;">{quantity * 100:.0f}</div>
                            <p style="margin: 0;">L Water Conserved</p>
                        </div>
                    """, unsafe_allow_html=True)

# Receiver List Tab with Enhanced UI
elif page == "Receiver List":
    st.markdown("<h2>🏠 Food Receiver Registration</h2>", unsafe_allow_html=True)
    
    # Add community animation
    if lottie_community:
        st_lottie(lottie_community, height=200, key="community_anim")
    
    # Introduction text
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(69, 90, 100, 0.9), rgba(55, 71, 79, 0.9)); 
             padding: 1.8rem; border-radius: 16px; box-shadow: 0 10px 20px rgba(0,0,0,0.15); 
             border: 1px solid rgba(255,255,255,0.1); margin-bottom: 2rem;'>
            <p style='color: #ffffff; font-size: 1.2rem; line-height: 1.6;'>
                Register as a food receiver to be matched with suitable donations. Our system considers your location,
                dietary needs, and preferences to find the perfect match.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    if 'receivers' not in st.session_state:
        st.session_state.receivers = []
    
    with st.form("receiver_form"):
        st.markdown("<p class='form-section-header'>Register as a Receiver</p>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<p style='color: #A5D6A7; font-weight: 500; margin-bottom: 1rem;'>Location & Contact</p>", unsafe_allow_html=True)
            
            receiver_name = st.text_input(
                "Organization/Individual Name",
                help="Name of the receiving organization or individual"
            )
            
            rec_latitude = st.number_input(
                "Latitude", 
                format="%.6f", 
                key="lat",
                help="Your location coordinates (latitude)"
            )
            
            rec_longitude = st.number_input(
                "Longitude", 
                format="%.6f", 
                key="lon",
                help="Your location coordinates (longitude)"
            )
            
            contact_number = st.text_input(
                "Contact Number", 
                key="cnt",
                help="Your phone number for coordination purposes"
            )
            
        with col2:
            st.markdown("<p style='color: #A5D6A7; font-weight: 500; margin-bottom: 1rem;'>Requirements & Preferences</p>", unsafe_allow_html=True)
            
            required_portions = st.number_input(
                "Required Portions", 
                min_value=1, 
                step=1,
                help="How many portions do you need?"
            )
            
            allergies = st.text_input(
                "Allergies (comma-separated)",
                help="List any food allergies or restrictions"
            )
            
            children = st.number_input(
                "Number of children", 
                min_value=0, 
                step=1,
                help="How many children will be served?"
            )
            
            elderly = st.number_input(
                "Number of elderly", 
                min_value=0, 
                step=1,
                help="How many elderly people will be served?"
            )
            
            preferred_delivery_time = st.time_input(
                "Preferred Delivery Time",
                help="When would you prefer to receive food?"
            )
        
        # Visual progress indicator
        st.markdown("""
            <div class="progress-container">
                <div class="progress-bar" style="width: 100%;"></div>
            </div>
            <p style='text-align: right; color: #A5D6A7; font-size: 0.9rem; margin-top: 0.5rem;'>
                Form complete - ready to submit!
            </p>
        """, unsafe_allow_html=True)
        
        submit_receiver = st.form_submit_button("Register as Receiver")
        
        if submit_receiver:
            # Show loading animation
            with st.spinner("Processing your registration..."):
                time.sleep(1)  # Simulate processing
                
                receiver = {
                    "name": receiver_name,
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
                
                # Success message with animation
                st.success("✅ Registration successful! You're now in our system to receive food donations.")
    
    # Display current receivers with enhanced styling
    if st.session_state.receivers:
        st.markdown("<h3 style='color: #A5D6A7; margin-top: 2rem;'>📋 Registered Receivers</h3>", unsafe_allow_html=True)
        
        # Create a more visual representation of receivers
        receiver_cols = st.columns(min(3, len(st.session_state.receivers)))
        
        for i, rec in enumerate(st.session_state.receivers):
            col_index = i % len(receiver_cols)
            with receiver_cols[col_index]:
                st.markdown(f"""
                    <div class="match-card">
                        <h4>{rec.get('name', f'Receiver #{i+1}')}</h4>
                        <p><strong>Location:</strong> ({rec['latitude']:.4f}, {rec['longitude']:.4f})</p>
                        <p><strong>Portions:</strong> {rec['required_portions']}</p>
                        <p><strong>People:</strong> {rec['people']['children']} children, {rec['people']['elderly']} elderly</p>
                        <p><strong>Contact:</strong> {rec['Contact_Number']}</p>
                    </div>
                """, unsafe_allow_html=True)
        
        # Add a map showing all receivers
        st.markdown("<h4 style='color: #A5D6A7; margin-top: 1.5rem;'>📍 Receiver Locations</h4>", unsafe_allow_html=True)
        
        # Create a map centered on the average location
        if len(st.session_state.receivers) > 0:
            avg_lat = sum(r['latitude'] for r in st.session_state.receivers) / len(st.session_state.receivers)
            avg_lon = sum(r['longitude'] for r in st.session_state.receivers) / len(st.session_state.receivers)
            
            m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12, 
                          tiles="CartoDB dark_matter")
            
            # Add markers for all receivers
            for i, rec in enumerate(st.session_state.receivers):
                popup_html = f"""
                <div style='font-family: Arial, sans-serif; min-width: 180px;'>
                    <h4 style='margin: 0 0 5px 0; color: #2e7d32;'>{rec.get('name', f'Receiver #{i+1}')}</h4>
                    <p style='margin: 5px 0;'><b>Portions needed:</b> {rec['required_portions']}</p>
                    <p style='margin: 5px 0;'><b>People:</b> {rec['people']['children']} children, {rec['people']['elderly']} elderly</p>
                    <p style='margin: 5px 0;'><b>Contact:</b> {rec['Contact_Number']}</p>
                </div>
                """
                
                folium.Marker(
                    [rec['latitude'], rec['longitude']],
                    popup=folium.Popup(popup_html, max_width=300),
                    tooltip=rec.get('name', f"Receiver #{i+1}"),
                    icon=folium.Icon(color='red', icon='home')
                ).add_to(m)
            
            # Display the map
            folium_static(m)

# Matching Results Tab with Enhanced UI
elif page == "Matching Results":
    st.markdown("<h2>🔄 Smart Matching System</h2>", unsafe_allow_html=True)
    
    # Add location animation
    if lottie_location:
        st_lottie(lottie_location, height=200, key="matching_anim")
    
    # Introduction text
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(69, 90, 100, 0.9), rgba(55, 71, 79, 0.9)); 
             padding: 1.8rem; border-radius: 16px; box-shadow: 0 10px 20px rgba(0,0,0,0.15); 
             border: 1px solid rgba(255,255,255,0.1); margin-bottom: 2rem;'>
            <p style='color: #ffffff; font-size: 1.2rem; line-height: 1.6;'>
                Our intelligent algorithm finds the optimal match between food donors and receivers based on multiple factors
                including location, quantity, and dietary requirements.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    if 'donor' not in st.session_state or not st.session_state.receivers:
        st.warning("⚠️ Please complete both donor and receiver information first!")
        
        # Add helpful guidance
        st.markdown("""
            <div style='background-color: rgba(255, 236, 179, 0.2); padding: 1.5rem; border-radius: 16px; 
            border-left: 5px solid #FFC107; margin-top: 1.5rem;'>
                <h4 style='color: #FFC107; margin-top: 0;'>Getting Started</h4>
                <p style='color: #E0E0E0; margin-bottom: 1rem;'>To use the matching system, you need to:</p>
                <ol style='color: #E0E0E0; margin-bottom: 0;'>
                    <li>First, go to the <b>Donor Form</b> page and submit donation details</li>
                    <li>Then, go to the <b>Receiver List</b> page and add at least one receiver</li>
                    <li>Return to this page to find the best match!</li>
                </ol>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Add a visually appealing button to find matches
        if st.button("Find Best Match", key="find_match_button"):
            # Show a loading animation with progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Simulate the matching process with steps
            status_text.text("Analyzing donor information...")
            progress_bar.progress(20)
            time.sleep(0.5)
            
            status_text.text("Evaluating receiver requirements...")
            progress_bar.progress(40)
            time.sleep(0.5)
            
            status_text.text("Calculating distances and logistics...")
            progress_bar.progress(60)
            time.sleep(0.5)
            
            status_text.text("Optimizing matching algorithm...")
            progress_bar.progress(80)
            time.sleep(0.5)
            
            status_text.text("Finalizing best match...")
            progress_bar.progress(100)
            time.sleep(0.5)
            
            # Clear the progress indicators
            status_text.empty()
            progress_bar.empty()
            
            # Get the actual match
            best_receiver, score, distance = match_donor_to_best_receiver(
                st.session_state.donor,
                st.session_state.receivers
            )
            
            if best_receiver:
                # Success message with animation
                st.success("✅ Best match found! The algorithm has identified the optimal receiver for this donation.")
                
                # Create a map with improved styling
                st.markdown("<h3 style='color: #A5D6A7; margin-top: 2rem;'>🗺️ Match Location Map</h3>", unsafe_allow_html=True)
                
                m = folium.Map(
                    location=[st.session_state.donor['latitude'], st.session_state.donor['longitude']],
                    zoom_start=12,
                    tiles="CartoDB dark_matter"
                )
                
                # Add donor marker with custom popup
                donor_popup_html = f"""
                <div style='font-family: Arial, sans-serif; min-width: 200px;'>
                    <h4 style='margin: 0 0 5px 0; color: #2e7d32;'>Food Donor</h4>
                    <p style='margin: 5px 0;'><b>Food:</b> {st.session_state.donor['Food_Category']}</p>
                    <p style='margin: 5px 0;'><b>Quantity:</b> {st.session_state.donor['Quantity']} portions</p>
                    <p style='margin: 5px 0;'><b>Pickup:</b> {st.session_state.donor['Pickup_Time']}</p>
                    <p style='margin: 5px 0;'><b>Contact:</b> {st.session_state.donor['Contact_Number']}</p>
                </div>
                """
                
                folium.Marker(
                    [st.session_state.donor['latitude'], st.session_state.donor['longitude']],
                    popup=folium.Popup(donor_popup_html, max_width=300),
                    tooltip="Food Donor",
                    icon=folium.Icon(color='green', icon='cutlery', prefix='fa')
                ).add_to(m)
                
                # Add receiver marker with custom popup
                receiver_popup_html = f"""
                <div style='font-family: Arial, sans-serif; min-width: 200px;'>
                    <h4 style='margin: 0 0 5px 0; color: #e53935;'>Best Match Receiver</h4>
                    <p style='margin: 5px 0;'><b>Portions needed:</b> {best_receiver['required_portions']}</p>
                    <p style='margin: 5px 0;'><b>People:</b> {best_receiver['people']['children']} children, {best_receiver['people']['elderly']} elderly</p>
                    <p style='margin: 5px 0;'><b>Delivery:</b> {best_receiver['Preferred_Delivery_Time']}</p>
                    <p style='margin: 5px 0;'><b>Contact:</b> {best_receiver['Contact_Number']}</p>
                </div>
                """
                
                folium.Marker(
                    [best_receiver['latitude'], best_receiver['longitude']],
                    popup=folium.Popup(receiver_popup_html, max_width=300),
                    tooltip="Best Match Receiver",
                    icon=folium.Icon(color='red', icon='home', prefix='fa')
                ).add_to(m)
                
                # Add a line connecting the two points
                folium.PolyLine(
                    locations=[
                        [st.session_state.donor['latitude'], st.session_state.donor['longitude']],
                        [best_receiver['latitude'], best_receiver['longitude']]
                    ],
                    color='#81C784',
                    weight=3,
                    opacity=0.7,
                    dash_array='5, 10'
                ).add_to(m)
                
                # Add distance marker
                midpoint = [
                    (st.session_state.donor['latitude'] + best_receiver['latitude']) / 2,
                    (st.session_state.donor['longitude'] + best_receiver['longitude']) / 2
                ]
                
                folium.Marker(
                    midpoint,
                    tooltip=f"{distance:.2f} km",
                    icon=folium.DivIcon(
                        html=f"""
                        <div style="
                            background-color: #2e7d32;
                            border: 2px solid #81C784;
                            border-radius: 50px;
                            text-align: center;
                            padding: 5px 10px;
                            font-weight: bold;
                            color: white;
                            font-size: 12px;
                        ">{distance:.2f} km</div>
                        """
                    )
                ).add_to(m)
                
                # Display map
                folium_static(m)
                
                # Display match details with improved styling
                st.markdown("<h3 style='color: #A5D6A7; margin-top: 2rem;'>📊 Match Details</h3>", unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                        <div class="match-card">
                            <h4>🥗 Donor Information</h4>
                            <p><strong>Food Category:</strong> {st.session_state.donor['Food_Category']}</p>
                            <p><strong>Quantity:</strong> {st.session_state.donor['Quantity']} portions</p>
                            <p><strong>Location:</strong> ({st.session_state.donor['latitude']:.4f}, {st.session_state.donor['longitude']:.4f})</p>
                            <p><strong>Contact:</strong> {st.session_state.donor['Contact_Number']}</p>
                            <p><strong>Pickup Time:</strong> {st.session_state.donor['Pickup_Time']}</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                        <div class="match-card">
                            <h4>🏠 Best Match Receiver</h4>
                            <p><strong>Location:</strong> ({best_receiver['latitude']:.4f}, {best_receiver['longitude']:.4f})</p>
                            <p><strong>Required Portions:</strong> {best_receiver['required_portions']}</p>
                            <p><strong>Children:</strong> {best_receiver['people']['children']}</p>
                            <p><strong>Elderly:</strong> {best_receiver['people']['elderly']}</p>
                            <p><strong>Delivery Time:</strong> {best_receiver['Preferred_Delivery_Time']}</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Match score visualization
                st.markdown("<h4 style='color: #A5D6A7; margin-top: 1.5rem;'>🎯 Match Quality</h4>", unsafe_allow_html=True)
                
                # Create a visual score indicator
                score_percentage = min(score * 100, 100)  # Convert score to percentage, max 100%
                
                st.markdown(f"""
                    <div style="background: rgba(69, 90, 100, 0.5); border-radius: 16px; padding: 1.5rem; margin-top: 1rem;">
                        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                            <div style="font-size: 2.5rem; font-weight: bold; color: #A5D6A7; margin-right: 1rem;">{score_percentage:.1f}%</div>
                            <div style="flex-grow: 1;">
                                <div style="font-weight: 500; margin-bottom: 0.5rem;">Match Score</div>
                                <div style="background: rgba(255,255,255,0.1); height: 10px; border-radius: 5px; overflow: hidden;">
                                    <div style="background: linear-gradient(90deg, #2E7D32, #81C784); height: 100%; width: {score_percentage}%;"></div>
                                </div>
                            </div>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-top: 0.5rem;">
                            <div style="font-size: 0.9rem; color: #A5D6A7;">Distance: {distance:.2f} km</div>
                            <div style="font-size: 0.9rem; color: #A5D6A7;">Portion Match: {100 - abs(st.session_state.donor['Quantity'] - best_receiver['required_portions']) * 5:.0f}%</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Next steps section
                st.markdown("<h3 style='color: #A5D6A7; margin-top: 2rem;'>🚀 Next Steps</h3>", unsafe_allow_html=True)
                
                st.markdown("""
                    <div style='background: linear-gradient(135deg, rgba(69, 90, 100, 0.9), rgba(55, 71, 79, 0.9)); 
                         padding: 1.8rem; border-radius: 16px; box-shadow: 0 10px 20px rgba(0,0,0,0.15); 
                         border: 1px solid rgba(255,255,255,0.1); margin-bottom: 1.5rem;'>
                        <p style='color: #ffffff; margin-top: 0;'>Now that we've found the best match, here's what happens next:</p>
                        <ol style='color: #ffffff; margin-bottom: 0;'>
                            <li><b>Notification:</b> Both the donor and receiver will be notified about this match</li>
                            <li><b>Confirmation:</b> Both parties need to confirm the arrangement</li>
                            <li><b>Coordination:</b> Our system will help coordinate pickup and delivery times</li>
                            <li><b>Feedback:</b> After completion, both parties can provide feedback on the experience</li>
                        </ol>
                    </div>
                """, unsafe_allow_html=True)
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.button("📱 Contact Parties", key="contact_button")
                
                with col2:
                    st.button("📝 Generate Report", key="report_button")
                
                with col3:
                    st.button("📅 Schedule Delivery", key="schedule_button")
            else:
                st.error("❌ No suitable receiver found. Please try adding more receivers or adjusting the donor information.")

# Admin Panel Tab
elif page == "Admin Panel":
    st.markdown("<h2>Admin Panel</h2>", unsafe_allow_html=True)
    
    # Summary counts
    donor_exists = 'donor' in st.session_state
    receivers = st.session_state.get("receivers", [])
    st.info(f"**Total Donors Registered:** {1 if donor_exists else 0}")
    st.info(f"**Total Receivers Registered:** {len(receivers)}")
    
    # Display donor details if available
    if donor_exists:
        st.subheader("Donor Details")
        donor_df = pd.DataFrame([st.session_state.donor])
        st.dataframe(donor_df)
        csv_donor = donor_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Donor Data as CSV",
            data=csv_donor,
            file_name='donor_data.csv',
            mime='text/csv'
        )
    else:
        st.warning("No donor details available.")
    
    # Display receiver details if available
    if receivers:
        st.subheader("Receiver Details")
        receiver_df = pd.DataFrame(receivers)
        st.dataframe(receiver_df)
        csv_receiver = receiver_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Receiver Data as CSV",
            data=csv_receiver,
            file_name='receiver_data.csv',
            mime='text/csv'
        )
    else:
        st.warning("No receiver details available.")
    
    # (Optional) You could also generate a combined CSV report
    if donor_exists or receivers:
        combined = {}
        if donor_exists:
            combined["donor"] = st.session_state.donor
        if receivers:
            combined["receivers"] = receivers
        combined_df = pd.json_normalize(combined, sep='_')
        st.subheader("Combined Details")
        st.dataframe(combined_df)
        csv_combined = combined_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Combined Data as CSV",
            data=csv_combined,
            file_name='combined_data.csv',
            mime='text/csv'
        )

# Add a footer
st.markdown("""
    <div style="background: rgba(27, 94, 32, 0.3); padding: 1.5rem; border-radius: 16px; margin-top: 3rem; text-align: center;">
        <p style="margin: 0; color: #A5D6A7;">EcoFeast © 2023 | Reducing Food Waste, One Meal at a Time</p>
    </div>
    """, unsafe_allow_html=True)