import joblib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Ensure we are in the correct directory
os.chdir(r"c:\Users\upeks\OneDrive\Documents\My stuff\Antigravity\HR_Predictive_Analytics")

# Load the trained Random Forest model and column names
try:
    model = joblib.load('models/rf_churn_model.pkl')
    columns = joblib.load('models/model_columns.pkl')

    # Extract standard feature importances from the Random Forest
    importances = model.feature_importances_
    
    # Create a DataFrame and sort by most important
    importance_df = pd.DataFrame({'Feature': columns, 'Importance': importances})
    
    # Let's group the dummy variables back together to show "District" as a whole, 
    # but for simplicity, we'll just show the top 15 individual features first
    importance_df = importance_df.sort_values(by='Importance', ascending=False).head(15)

    # Plot
    plt.figure(figsize=(12, 7))
    sns.barplot(x='Importance', y='Feature', data=importance_df, palette='magma')
    plt.title('Top 15 Strongest Predictors of Infant Attrition (Random Forest)', fontsize=16, fontweight='bold')
    plt.xlabel('Relative Impact on Turnover Risk', fontsize=12)
    plt.ylabel('Feature / Demographic', fontsize=12)
    plt.tight_layout()
    
    # Save the plot
    plt.savefig('feature_importance_proof.png', dpi=300)
    print("Successfully generated feature_importance_proof.png")

except Exception as e:
    print(f"Error generating plot: {e}")
