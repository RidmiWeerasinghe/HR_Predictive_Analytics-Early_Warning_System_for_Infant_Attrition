# app/tab_single.py

def render(st, pd, shap, plt, model, model_columns, districts, transports, marital_statuses, races, genders, levels, teams, designations, grades):
    with st.form("employee_form"):
        st.write("### 👤 Employee Profile")
        
        col1, col2, col3 = st.columns(3) 
        
        with col1:
            st.markdown("**Personal Details**")
            age = st.number_input("Age (Years)", min_value=18, max_value=60, value=22)
            gender = st.selectbox("Gender", genders)
            marital_status = st.selectbox("Marital Status", marital_statuses)
            race = st.selectbox("Race", races)
            
        with col2:
            st.markdown("**Logistics**")
            district = st.selectbox("District (Residence)", districts)
            transport = st.selectbox("Transport Mode", transports)
            
        with col3:
            st.markdown("**Job Role**")
            level = st.selectbox("Job Level", levels)
            team = st.selectbox("Production Team", teams) 
            designation = st.selectbox("Designation", designations) 
            grade = st.selectbox("Grade", grades)
        
        st.markdown("---")
        submit_button = st.form_submit_button("🔍 Calculate Risk Score", use_container_width=True)

    # if submit_button:
    #     with st.spinner("Analyzing profile patterns through Random Forest Algorithm..."):
            
    #         # 1. Capture input
    #         input_data = {
    #             'Age_Numeric': age,
    #             'Gender': gender,
    #             'Marial Status': marital_status,
    #             'Race': race,
    #             'District': district,
    #             'Transport mode': transport,
    #             'Level': level,
    #             'Team': team,
    #             'Designation': designation,
    #             'Grade': grade
    #         }
            
    #         # 2. Convert & Encode
    #         input_df = pd.DataFrame([input_data])
    #         input_encoded = pd.get_dummies(input_df)
            
    #         # 3. Align with training columns
    #         input_aligned = input_encoded.reindex(columns=model_columns, fill_value=0)
            
    #         # 4. Make the Prediction
    #         probabilities = model.predict_proba(input_aligned)[0]
    #         risk_score = round(probabilities[1] * 100, 1)
            
    #         # --- 5. EXPLAINABLE AI (SHAP) ---
    #         input_aligned = input_aligned.astype(float)
    #         explainer = shap.TreeExplainer(model)
    #         shap_values = explainer.shap_values(input_aligned, check_additivity=False)
            
    #         if isinstance(shap_values, list):
    #             employee_shap_values = shap_values[1][0] 
    #         else:
    #             if len(shap_values.shape) == 3:
    #                 employee_shap_values = shap_values[0, :, 1]
    #             else:
    #                 employee_shap_values = shap_values[0]

    #         feature_impact = pd.DataFrame({
    #             'Feature': input_aligned.columns,
    #             'Impact': employee_shap_values,
    #             'Input_Value': input_aligned.iloc[0].values
    #         })
    #         feature_impact = feature_impact[feature_impact['Input_Value'] != 0]
    #         feature_impact['Abs_Impact'] = feature_impact['Impact'].abs()
    #         top_factors = feature_impact.sort_values(by='Abs_Impact', ascending=False).head(5)
            
    #         # --- 6. DISPLAY RESULTS ---
    #         st.markdown("### 📊 Prediction Results")
            
    #         col_res1, col_res2 = st.columns([1, 1])
            
    #         with col_res1:
    #             if risk_score > 60:
    #                 st.error(f"🚨 **HIGH RISK**: **{risk_score}%** probability of Early Attrition (< 12 Months).")
    #                 st.warning("**Action:** Assign a floor mentor. Verify boarding/transport.")
    #             elif risk_score > 35:
    #                 st.warning(f"⚠️ **MEDIUM RISK**: **{risk_score}%** probability of Early Attrition (< 12 Months).")
    #                 st.info("**Action:** Standard onboarding. Schedule 30-day check-in.")
    #             else:
    #                 st.success(f"✅ **LOW RISK**: **{risk_score}%** probability of Early Attrition (< 12 Months).")
    #                 st.info("**Action:** Highly stable match. Proceed with standard integration.")
                    
    #         with col_res2:
    #             st.markdown("**Explainable AI: Why did the model give this score?**")
                
    #             fig, ax = plt.subplots(figsize=(5, 3))
    #             colors = ['#ff9999' if val > 0 else '#99ff99' for val in top_factors['Impact']]
                
    #             ax.barh(top_factors['Feature'], top_factors['Impact'], color=colors)
    #             ax.set_xlabel("Impact on Risk Score")
    #             ax.set_title("Top 5 Driving Factors", fontsize=10)
    #             ax.invert_yaxis() 
                
    #             ax.spines['top'].set_visible(False)
    #             ax.spines['right'].set_visible(False)
                
    #             st.pyplot(fig)

    if submit_button:
        with st.spinner("Analyzing profile patterns through Random Forest Algorithm..."):
            
            # 1. Capture input (Reverting to the reliable dictionary approach)
            input_data = {
                'Age_Numeric': age,
                'Gender': gender,
                'Marial Status': marital_status,
                'Race': race,
                'District': district,
                'Transport mode': transport,
                'Level': level,
                'Team': team,
                'Designation': designation,
                'Grade': grade
            }
            
            # 2. Convert & Encode (Using pandas' native encoder)
            input_df = pd.DataFrame([input_data])
            input_encoded = pd.get_dummies(input_df)
            
            # 3. Align with training columns
            input_aligned = input_encoded.reindex(columns=model_columns, fill_value=0)
            
            # 4. Make the Prediction
            probabilities = model.predict_proba(input_aligned)[0]
            risk_score = round(probabilities[1] * 100, 1)
            
            # --- 5. EXPLAINABLE AI (SHAP) ---
            # Force everything to float for SHAP compatibility
            input_aligned = input_aligned.astype(float)
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(input_aligned, check_additivity=False)
            
            if isinstance(shap_values, list):
                employee_shap_values = shap_values[1][0] 
            else:
                if len(shap_values.shape) == 3:
                    employee_shap_values = shap_values[0, :, 1]
                else:
                    employee_shap_values = shap_values[0]

            # Bind the impact scores to the actual input values
            feature_impact = pd.DataFrame({
                'Feature': input_aligned.columns,
                'Impact': employee_shap_values,
                'Input_Value': input_aligned.iloc[0].values
            })
            
            # THE FIX: Only keep features where the employee actually possesses the trait (> 0)
            # This perfectly filters out all the 0.0 "ghost" columns but keeps Age (which is > 0)
            # and the active One-Hot encoded traits (which are 1.0)
            feature_impact = feature_impact[feature_impact['Input_Value'] > 0]
            
            feature_impact['Abs_Impact'] = feature_impact['Impact'].abs()
            top_factors = feature_impact.sort_values(by='Abs_Impact', ascending=False).head(5)
            
            # --- 6. DISPLAY RESULTS ---           
            # --- 7. DISPLAY RESULTS ---
            st.markdown("### 📊 Prediction Results")
            
            col_res1, col_res2 = st.columns([1, 1])
            
            with col_res1:
                if risk_score > 60:
                    st.error(f"🚨 **HIGH RISK**: **{risk_score}%** probability of Early Attrition (< 12 Months).")
                    st.warning("**Action:** Assign a floor mentor. Verify boarding/transport.")
                elif risk_score > 35:
                    st.warning(f"⚠️ **MEDIUM RISK**: **{risk_score}%** probability of Early Attrition (< 12 Months).")
                    st.info("**Action:** Standard onboarding. Schedule 30-day check-in.")
                else:
                    st.success(f"✅ **LOW RISK**: **{risk_score}%** probability of Early Attrition (< 12 Months).")
                    st.info("**Action:** Highly stable match. Proceed with standard integration.")
                    
            with col_res2:
                st.markdown("**Explainable AI: Why did the model give this score?**")
                
                fig, ax = plt.subplots(figsize=(5, 3))
                colors = ['#ff9999' if val > 0 else '#99ff99' for val in top_factors['Impact']]
                
                ax.barh(top_factors['Feature'], top_factors['Impact'], color=colors)
                ax.set_xlabel("Impact on Risk Score")
                ax.set_title("Top Driving Factors", fontsize=10)
                ax.invert_yaxis() 
                
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                
                st.pyplot(fig)