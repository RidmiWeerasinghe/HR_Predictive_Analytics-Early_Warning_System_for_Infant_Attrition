# # app/tab_dashboard.py

# import os
# import streamlit as st
# import database

# def render():
#     st.write("### 📈 Executive Analytics Dashboard")
#     st.write("Overview of the latest batch predictions and historical factory attrition trends.")

#     # --- 1. LATEST BATCH METRICS ---
#     st.markdown("#### Latest Prediction Batch Results")
#     latest_run = database.get_latest_batch_run()

#     if latest_run:
#         timestamp, total, high, med, low = latest_run
#         st.caption(f"Last run: {timestamp}")
        
#         col1, col2, col3, col4 = st.columns(4)
#         col1.metric("Total Evaluated", total)
#         col2.metric("High Risk 🚨", high, delta="Action Required", delta_color="inverse")
#         col3.metric("Medium Risk ⚠️", med)
#         col4.metric("Low Risk ✅", low, delta="Stable", delta_color="normal")
#     else:
#         st.info("No bulk predictions have been run yet. Upload a CSV in the Batch Upload tab to populate these metrics.")

#     st.divider()

#     # --- 2. HISTORICAL INSIGHTS (EDA) ---
#     st.markdown("#### Historical Factory Attrition Insights")
#     st.write("Key vulnerabilities identified during the baseline exploratory data analysis.")

#     # Map the paths to your new assets folder
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     assets_dir = os.path.join(current_dir, "assets")
    
#     col_img1, col_img2 = st.columns(2)
    
#     with col_img1:
#         st.markdown("**1. Geographic Risk Profile**")
#         try:
#             st.image(os.path.join(assets_dir, "district_risk.png"), use_container_width=True)
#         except:
#             st.warning("Missing image: assets/district_risk.png")

#         st.markdown("**3. Demographic Vulnerability**")
#         try:
#             st.image(os.path.join(assets_dir, "heatmap_risk.png"), use_container_width=True)
#         except:
#             st.warning("Missing image: assets/heatmap_risk.png")   
        

#     # with col_img2:
#     #     st.markdown("**2. Team Hotspots**")
#     #     try:
#     #         st.image(os.path.join(assets_dir, "team_risk.png"), use_container_width=True)
#     #     except:
#     #         st.warning("Missing image: assets/team_risk.png")

# app/tab_dashboard.py

import streamlit as st
import plotly.express as px
import pandas as pd
import database

def render(df):
    st.write("### 📈 Executive Analytics Dashboard")
    st.write("Overview of the latest batch predictions and historical factory attrition trends.")

    # --- 1. LATEST BATCH METRICS ---
    st.markdown("#### Latest Prediction Batch Results")
    
    # Use the new MySQL function which returns a Pandas DataFrame
    df_metrics = database.get_historical_metrics()

    if not df_metrics.empty:
        # Extract the very first row (the most recent run)
        latest_run = df_metrics.iloc[0]
        
        timestamp = latest_run['upload_date']
        total = latest_run['total_records']
        high = latest_run['high_risk_count']
        low = latest_run['stable_count']
        
        st.caption(f"Last run: {timestamp}")
        
        # We use 3 columns because the Random Forest model is strictly binary (0 or 1)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Evaluated", total)
        col2.metric("High Risk 🚨", high, delta="Action Required", delta_color="inverse")
        col3.metric("Low Risk ✅", low, delta="Stable", delta_color="normal")
    else:
        st.info("No bulk predictions have been run yet. Upload a CSV in the Batch Upload tab to populate these metrics.")

    st.divider()

    # --- 2. DYNAMIC HISTORICAL INSIGHTS (EDA) ---
    st.markdown("#### Historical Factory Attrition Insights")
    st.write("Interactive vulnerabilities identified from the baseline factory dataset.")

    # In your previous phase, you mentioned creating the 'Early_Attrition' column.
    # We will use this to calculate the risk probabilities dynamically.
    target_col = 'Early_Attrition'
    
    if target_col not in df.columns:
        st.warning(f"⚠️ Could not find the '{target_col}' column in the dataset to generate charts. Ensure the processed CSV contains this target variable.")
        return

    # --- Chart 1: Geographic Risk (Probability by District) ---
    # We group by District and get the mean of Early_Attrition (which equals the % probability)
    district_risk = df.groupby('District')[target_col].mean().reset_index()
    district_risk = district_risk.sort_values(by=target_col, ascending=False)
    
    fig_district = px.bar(
        district_risk, 
        x='District', 
        y=target_col, 
        title='Early Attrition Risk by District',
        labels={target_col: 'Probability of Quitting < 1 Year'},
        color=target_col, 
        color_continuous_scale='Reds'
    )
    fig_district.update_layout(xaxis_tickangle=-45) # Tilt the labels so they fit nicely
    
    # --- Chart 2: Team Hotspots (Volume of Early Resignations) ---
    # We filter only the people who quit (1), group by Team, and count them
    team_risk = df[df[target_col] == 1].groupby('Team').size().reset_index(name='Resignations')
    team_risk = team_risk.sort_values(by='Resignations', ascending=False).head(10)
    
    fig_team = px.bar(
        team_risk, 
        x='Resignations', 
        y='Team', 
        orientation='h',
        title='Top 10 High-Risk Production Teams',
        color='Resignations', 
        color_continuous_scale='Reds'
    )
    fig_team.update_layout(yaxis={'categoryorder':'total ascending'}) # Put the highest at the top

    # --- Display the Interactive Charts Side-by-Side ---
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.plotly_chart(fig_district, use_container_width=True)
        
    with col_chart2:
        st.plotly_chart(fig_team, use_container_width=True)