import database


# app/tab_bulk.py

def render(st, pd, model, model_columns):
    st.write("### 📂 Batch Risk Assessment")
    st.write("Upload a CSV file containing Day-1 data. Must match the exact column names of the training data.")
    
    uploaded_file = st.file_uploader("Upload CSV", type=['csv'])
    
    if uploaded_file is not None:
        df_bulk = pd.read_csv(uploaded_file)
        
        if len(df_bulk) > 100:
            st.error(f"File contains {len(df_bulk)} rows. Please upload a maximum of 100 employees at a time to prevent system timeout.")
        else:
            st.success(f"Successfully loaded {len(df_bulk)} employee records.")
            
            with st.expander("View Uploaded Data Preview"):
                st.dataframe(df_bulk)
            
            if st.button("🚀 Run Bulk Predictions"):
                with st.spinner('Running Random Forest Inference on all records...'):
                    
                    # 1. Secure the Employee Number
                    if 'Emp Number' in df_bulk.columns:
                        emp_numbers = df_bulk['Emp Number']
                        inference_data = df_bulk.drop(columns=['Emp Number'])
                    else:
                        st.warning("Warning: 'Emp Number' column not found in CSV. Generating generic IDs.")
                        emp_numbers = pd.Series([f"EMP_{i}" for i in range(1, len(df_bulk) + 1)])
                        inference_data = df_bulk.copy()
                        
                    # 2. Validate strict schema adherence before inference
                    required_cols = ['Age_Numeric', 'Gender', 'Marial Status', 'Race', 'District', 'Transport mode', 'Level', 'Team', 'Designation', 'Grade']
                    missing_cols = [col for col in required_cols if col not in inference_data.columns]
                    
                    if missing_cols:
                        st.error(f"Error: Missing required feature columns: {', '.join(missing_cols)}")
                        st.stop()
                        
                    # 3. Convert & Encode the entire batch
                    bulk_encoded = pd.get_dummies(inference_data)
                    
                    # 3. Align with training columns
                    bulk_aligned = bulk_encoded.reindex(columns=model_columns, fill_value=0)
                    
                    # 4. Make Predictions for all rows
                    bulk_probabilities = model.predict_proba(bulk_aligned)[:, 1]
                    risk_scores = (bulk_probabilities * 100).round(1)
                    
                    # Apply the exact same custom business thresholds as Tab 1
                    # statuses = []
                    # for score in risk_scores:
                    #     if score > 60:
                    #         statuses.append("🚨 High Risk")
                    #     elif score > 35:
                    #         statuses.append("⚠️ Medium Risk")
                    #     else:
                    #         statuses.append("✅ Low Risk")


                    #         # --- NEW: SAVE TO DATABASE ---
                    # high_count = statuses.count("🚨 High Risk")
                    # med_count = statuses.count("⚠️ Medium Risk")
                    # low_count = statuses.count("✅ Low Risk")
                    # database.insert_batch_run(len(df_bulk), high_count, med_count, low_count)
                    # -----------------------------
                    
                    # Apply strictly binary business thresholds (High Risk vs Stable) to match the model and DB
                    statuses = []
                    for score in risk_scores:
                        if score >= 50:
                            statuses.append("🚨 High Risk")
                        else:
                            statuses.append("✅ Low/Stable Risk")

                    # --- SAVE TO MYSQL DATABASE ---
                    high_count = statuses.count("🚨 High Risk")
                    low_count = statuses.count("✅ Low/Stable Risk")
                    
                    # Use the new MySQL function name and pass the 3 required metrics
                    database.log_batch_prediction(len(df_bulk), high_count, low_count)
                    # -----------------------------

                    # 5. Compile the Final Output Table
                    results_df = pd.DataFrame({
                        'Emp Number': emp_numbers,
                        'Risk Score (%)': risk_scores,
                        'Status': statuses
                    })
                    
                    # 5. Compile the Final Output Table
                    results_df = pd.DataFrame({
                        'Emp Number': emp_numbers,
                        'Risk Score (%)': risk_scores,
                        'Status': statuses
                    })
                    
                    # 6. Display the results
                    st.subheader("📊 Batch Prediction Results")
                    st.dataframe(results_df, use_container_width=True)
                    
                    # 7. Offer a Download Button
                    csv_output = results_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="⬇️ Download Results as CSV",
                        data=csv_output,
                        file_name='hela_bulk_attrition_predictions.csv',
                        mime='text/csv',
                    )