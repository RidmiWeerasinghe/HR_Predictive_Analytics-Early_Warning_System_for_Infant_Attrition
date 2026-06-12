import os

files = {
    'app/app.py': 'Main Application Router and UI Configuration',
    'app/database.py': 'MySQL Database Connection, RBAC, and Authentication Logic',
    'app/tab_single.py': 'Single Employee Risk Assessment and SHAP Explainable AI Logic',
    'app/tab_bulk.py': 'Batch CSV Upload and Strict Schema Validation Logic',
    'app/tab_dashboard.py': 'Executive Analytics Dashboard and Interactive Plotly Charts'
}

appendix_content = '# Appendix – C: Coding\n\nThis appendix contains the core source code for the Predictive HR Analytics application. The code is written in Python, utilizing Streamlit for the frontend, Scikit-Learn for machine learning inference, and MySQL for secure data persistence.\n\n'

for filepath, description in files.items():
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        appendix_content += f'### C.{list(files.keys()).index(filepath) + 1} {os.path.basename(filepath)}\n'
        appendix_content += f'**Description:** {description}\n\n'
        appendix_content += '```python\n' + code + '\n```\n\n'

md_path = '6CS007_Humanized_Report_Draft.md'
with open(md_path, 'r', encoding='utf-8') as f:
    md_text = f.read()

import re
# Use regex to replace the section starting with "# Appendix – C: Coding" up to the next "#"
new_text = re.sub(r'# Appendix – C: Coding.*?# Appendix – D:', appendix_content + '# Appendix – D:', md_text, flags=re.DOTALL)

with open(md_path, 'w', encoding='utf-8') as f:
    f.write(new_text)

print('Successfully generated and injected Appendix C.')
