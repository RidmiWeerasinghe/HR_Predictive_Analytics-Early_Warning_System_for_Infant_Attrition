import re

short_appendix = """# Appendix – C: Coding

This appendix contains the core, critical code snippets demonstrating the technical complexity of the Predictive HR Analytics application, specifically highlighting the Machine Learning integration, Explainable AI (SHAP), and security protocols.

### C.1 Authentication & Security (database.py)
**Description:** Demonstrates the secure password hashing and role-based access control (RBAC) verification logic.
```python
import hashlib
import mysql.connector

def hash_password(password):
    \"\"\"Securely hashes passwords using SHA-256.\"\"\"
    return hashlib.sha256(password.encode()).hexdigest()

def verify_login(username, password):
    \"\"\"Checks the database for matching username, hashed password, and active status.\"\"\"
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    hashed_input = hash_password(password)
    
    cursor.execute("SELECT id, username, role, acc_sts, password_hash FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    
    if not user:
        return {"status": "error", "message": "User not found."}
    if user['password_hash'] != hashed_input:
        return {"status": "error", "message": "Invalid password."}
    if user['acc_sts'] != 1:
        return {"status": "error", "message": "Account is inactive."}
        
    return {"status": "success", "user_data": user}
```

### C.2 Explainable AI Integration (tab_single.py)
**Description:** Demonstrates how the SHAP (SHapley Additive exPlanations) library is integrated with the Random Forest model to generate dynamic "Top Driving Factors" for individual employee predictions.
```python
import shap
import pandas as pd

# 1. Align input with training columns
input_aligned = input_encoded.reindex(columns=model_columns, fill_value=0)

# 2. Make the Prediction
probabilities = model.predict_proba(input_aligned)[0]
risk_score = round(probabilities[1] * 100, 1)

# 3. EXPLAINABLE AI (SHAP)
input_aligned = input_aligned.astype(float)
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(input_aligned, check_additivity=False)

employee_shap_values = shap_values[1][0] if isinstance(shap_values, list) else shap_values[0]

# 4. Bind impact scores to actual input values
feature_impact = pd.DataFrame({
    'Feature': input_aligned.columns,
    'Impact': employee_shap_values,
    'Input_Value': input_aligned.iloc[0].values
})

# 5. Filter for active traits and find top 5 factors
feature_impact = feature_impact[feature_impact['Input_Value'] > 0]
feature_impact['Abs_Impact'] = feature_impact['Impact'].abs()
top_factors = feature_impact.sort_values(by='Abs_Impact', ascending=False).head(5)
```

### C.3 Batch Processing & Schema Validation (tab_bulk.py)
**Description:** Demonstrates the strict schema validation protocol ensuring uploaded CSV files perfectly match the Random Forest model's required feature architecture before bulk inference is allowed.
```python
import pandas as pd
import streamlit as st

# 1. Validate strict schema adherence before inference
required_cols = ['Age_Numeric', 'Gender', 'Marial Status', 'Race', 'District', 
                 'Transport mode', 'Level', 'Team', 'Designation', 'Grade']
                 
missing_cols = [col for col in required_cols if col not in inference_data.columns]

if missing_cols:
    st.error(f"Error: Missing required feature columns: {', '.join(missing_cols)}")
    st.stop()
    
# 2. Convert & Encode the entire batch
bulk_encoded = pd.get_dummies(inference_data)

# 3. Align with training columns
bulk_aligned = bulk_encoded.reindex(columns=model_columns, fill_value=0)

# 4. Make Predictions for all rows simultaneously
bulk_probabilities = model.predict_proba(bulk_aligned)[:, 1]
risk_scores = (bulk_probabilities * 100).round(1)
```

"""

md_path = '6CS007_Humanized_Report_Draft.md'
with open(md_path, 'r', encoding='utf-8') as f:
    text = f.read()

new_text = re.sub(r'# Appendix – C: Coding.*?# Appendix – D:', short_appendix + '# Appendix – D:', text, flags=re.DOTALL)

with open(md_path, 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Trimmed Appendix C to just the critical code snippets successfully!")
