# app/app.py

import os
import streamlit as st
import pandas as pd
import joblib
import numpy as np
import shap  
import matplotlib.pyplot as plt 

# Import our modular files
import tab_single
import tab_bulk
import database  # <--- Our new DB module
import tab_dashboard
import tab_user_management

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Hela HR Analytics", page_icon="🏭", layout="wide")

# --- 2. INITIALIZE DATABASE & STATE ---
# Run database setup and inject a default admin user
# database.init_db()
database.initialize_admin()
# database.create_default_user("admin", "Hela123!") 

# Set up the login memory state
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'role' not in st.session_state:
    st.session_state['role'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = None

# --- 3. THE LOGIN SCREEN ---
if not st.session_state['logged_in']:
    # Use columns to center the login box nicely
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        st.markdown("<h1 style='text-align: center;'>Login</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Please log in to access the Predictive HR Analytics system.</p>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password") # Hides the text!
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                if not username.strip() or not password.strip():
                    st.error("Please enter your credentials.")
                else:
                    result = database.verify_login(username, password)
                    if result and result.get("status") == "success":
                        user_data = result["user_data"]
                        st.session_state['logged_in'] = True
                        st.session_state['role'] = user_data['role']
                        st.session_state['username'] = user_data['username']
                        st.success("Login successful!")
                        st.rerun() # Refresh the page instantly to show the dashboard
                    elif result and result.get("status") == "error":
                        st.error(result["message"])
                    else:
                        st.error("An unknown error occurred during login.")

# --- 4. THE MAIN APPLICATION (Only runs if logged in) ---
else:
    # --- Sidebar Navigation & Logout ---
    with st.sidebar:
        st.write(f"👤 **Logged in as:** {st.session_state['username']} ({st.session_state['role']})")
        
        st.markdown("---")
        # st.subheader("Navigation")
        
        # Custom CSS to make radio buttons look like a modern interactive menu
        st.markdown("""
        <style>
        /* Hide the radio button circles */
        div[role="radiogroup"] > label > div:first-of-type {
            display: none !important;
        }
        /* Style the labels to look like buttons */
        div[role="radiogroup"] > label {
            padding: 10px 15px;
            margin-bottom: 5px;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s;
            width: 100%;
            border-left: 4px solid transparent;
        }
        /* Hover state */
        div[role="radiogroup"] > label:hover {
            background-color: rgba(150, 150, 150, 0.1);
        }
        /* Selected state */
        div[role="radiogroup"] > label:has(input:checked) {
            background-color: rgba(29, 131, 248, 0.15) !important;
            border-left: 4px solid #1d83f8;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)

        nav_options = ["Executive Dashboard", "Single Employee Assessment", "Bulk Batch Upload"]
        if st.session_state.get('role') == 'ADMIN':
            nav_options.append("User Management")
            
        selected_page = st.radio("Navigation", nav_options, label_visibility="collapsed")
        
        st.markdown("---")
        if st.button("Logout", use_container_width=True):
            st.session_state['logged_in'] = False
            st.session_state['role'] = None
            st.session_state['username'] = None
            st.rerun()

    # --- App Header ---
    st.title("🏭 Predictive HR Analytics")
    st.subheader("Early Warning System: Infant Attrition Risk (0-12 Months)")
    
    # --- Load Assets ---
    @st.cache_resource
    def load_assets():
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        
        model_path = os.path.join(parent_dir, 'models', 'rf_churn_model.pkl')
        columns_path = os.path.join(parent_dir, 'models', 'model_columns.pkl')
        data_path = os.path.join(parent_dir, 'data', 'processed', 'Hela_ML_Ready.csv')
        
        model = joblib.load(model_path)
        model_columns = joblib.load(columns_path) 
        df = pd.read_csv(data_path)
        return model, model_columns, df

    try:
        model, model_columns, df = load_assets()
    except FileNotFoundError as e:
        st.error(f"Assets not found! Check your file paths. Error details: {e}")
        st.stop()

    districts = sorted(df['District'].dropna().unique().tolist())
    transports = sorted(df['Transport mode'].dropna().unique().tolist())
    marital_statuses = sorted(df['Marial Status'].dropna().unique().tolist())
    races = sorted(df['Race'].dropna().unique().tolist())
    genders = sorted(df['Gender'].dropna().unique().tolist())
    levels = sorted(df['Level'].dropna().unique().tolist())
    teams = sorted(df['Team'].dropna().unique().tolist())
    designations = sorted(df['Designation'].dropna().unique().tolist())
    grades = sorted(df['Grade'].dropna().unique().tolist())

    # --- RENDER THE SELECTED PAGE ---
    if selected_page == "Executive Dashboard":
        tab_dashboard.render(df)
    elif selected_page == "Single Employee Assessment":
        tab_single.render(st, pd, shap, plt, model, model_columns, districts, transports, marital_statuses, races, genders, levels, teams, designations, grades)
    elif selected_page == "Bulk Batch Upload":
        tab_bulk.render(st, pd, model, model_columns)
    elif selected_page == "User Management" and st.session_state.get('role') == 'ADMIN':
        tab_user_management.render()