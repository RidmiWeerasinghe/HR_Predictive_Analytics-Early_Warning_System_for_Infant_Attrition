# Chapter 03 – Methodology

## 3.1 Introduction
The Cross-Industry Standard Process for Data Mining (CRISP-DM) framework structures this project. This analytical standard enables the systematic development of the predictive system. It breaks the project into distinct, iterative phases ranging from business understanding to deployment. Following CRISP-DM ensures the mathematical model perfectly aligns with actual HR operational requirements. 

## 3.2 Planning

### 3.2.1 Identifying Business Values
The "Predictive HR Analytics System" transitions HR departments from a reactionary protocol to a proactive retention stance. Losing skilled workers represents a major financial risk to garment factories. The system delivers specific value through:
* **Reduction in Operational Costs:** Replacing an operator incurs recruitment and training expenses. Identifying high-risk employees early saves significant capital.
* **Keeping Production on Track:** Unexpected departures create severe bottlenecks. Early warning indicators allow managers to plan workforce adjustments immediately.
* **Data-Driven Smart Decisions:** HR stops relying on intuition. The system targets retention spending toward employees mathematically proven to leave.
* **Boosting Employee Morale:** Analyzing commute logistics rather than guessing cultivates a healthier workplace culture.

### 3.2.2 Feasibility Analysis
The project underwent strict evaluation across five parameters to ensure practicality and legal soundness.

#### 3.2.2.1 Technical Feasibility
The project utilizes an industry-standard technology stack. Building a web application instead of a standalone desktop program solves factory deployment issues. HR departments operate mixed hardware. Installing heavy desktop software causes administrative issues. Web applications bypass these restrictions. Staff can access the Streamlit dashboard securely through any browser. Python acts as the core processing engine. It integrates natively with powerful open-source libraries like Pandas and Scikit-learn. The predictive engine runs efficiently on standard office workstations.

#### 3.2.2.2 Financial Feasibility
The technology stack is entirely open-source. Python, Streamlit, Scikit-learn, and MySQL Community Edition do not require licensing fees. Deploying the system costs nothing in software overhead. Retaining just three skilled operators covers the entire development time investment.

#### 3.2.2.3 Operational Feasibility
The system augments existing HR routines. It does not replace human judgment. The final dashboard features a highly intuitive interface. Users can assess single employees or run massive bulk batches seamlessly.

#### 3.2.2.4 Legal Feasibility
Data privacy forms the core of the project logic. The system processes nearly 5,000 historical records. The data engineering team extracted only demographic and role-based data to ensure legal compliance. The system strictly excludes sensitive attributes like religion or exact residential addresses. This exclusion prevents discriminatory bias in the predictive outputs.

#### 3.2.2.5 Schedule Feasibility
The work structure divides into overlapping modular phases. This includes literature review, data preprocessing, model training, and dashboard development. This separation prevents blocking bottlenecks during the software testing phase.

### 3.2.3 Work Plan
The project work breakdown structure was segmented into five concurrent stages:
* **Research and Requirements:** Executing the literature review, establishing the constraints of utilizing strictly demographic data due to organizational privacy limitations, and explicitly defining the target variable ("Infant Attrition").
* **Data Preparation:** Ingesting approximately 5,000 records of categorical HR data. Operations included cleaning inconsistencies, imputing missing values, standardizing date strings, and natively resolving class imbalance by dropping right-censored data (active employees with less than one year of tenure) to specifically isolate the Infant Attrition cohort.
* **Building the Model:** Developing the prediction logic utilizing tree-based algorithms (Random Forest/Gradient Boosting). The models were cross-validated and hyperparameter-tuned specifically to maximize 'Recall' (Sensitivity) rather than generic 'Accuracy'.
* **Creating the Product:** Translating local Python development environments into a productionized Streamlit web application, securing it via a MySQL user authentication system, and establishing interactive executive reporting dashboards.
* **Testing and Finishing:** Executing unit tests on preprocessing scripts, integration testing the bulk file uploader to the model pipeline, and performing user acceptance testing on the final dashboard framework.

## 3.3 Analysis and Requirement Gathering

### 3.3.1 Analysis
Evaluating the existing manual retention system identified strict software functionality requirements. 
* **Functional capabilities:** The system must securely authenticate users. It must handle raw CSV bulk uploads seamlessly. It must compute individual numerical turnover risk scores for every parsed employee.
* **Non-Functional capabilities:** The system must visualize these results on an intuitive dashboard. It must provide predictions in real-time (under 10 seconds per bulk batch) to prevent workflow stagnation.

### 3.3.2 Requirement Gathering
Two primary methods established the precise architectural requirements:
* **Direct Data Analysis:** The system processed an anonymized HR dataset from Hela Apparel Holdings (Kalagedihena branch). This set contained nearly 5,000 active and resigned records. Structural integrity checks verified columns like 'Service Years' and 'Transport Mode'.
* **Literature Review:** Academic research confirmed that ensemble decision trees provide maximum accuracy for structured tabular data. This cemented the choice to avoid complex, unexplainable neural networks.

## 3.4 Designing

### 3.4.1 Physical Design
Data Flow Diagrams (DFDs) modeled the logical movement of data through the system.

#### 3.4.1.1 DFD Level 0 (Context Diagram)
The highest-level conceptual interaction maps the primary actor (HR Manager) interacting with the system boundaries. The actor inputs the "Employee Dataset". The system outputs the computed "Risk Report".

#### 3.4.1.2 DFD Level 1
This layer breaks down the main processes sequentially. The pipeline executes Data Input, Data Validation, Machine Learning Inference, MySQL Database Logging, and Prediction Output.

#### 3.4.1.3 Use Case & Activity Diagrams
Use Case diagrams map the interactions between the HR user and primary functionalities. Activity diagrams outline the sequential flow taken when processing single entries versus bulk uploads.

### 3.4.2 Architecture Design
A robust three-tier separation of concerns dictates the digital architecture. This improves long-term maintainability.
* **Presentation Layer:** Receives raw HR data via file uploads. A validation module confirms schema adherence before pushing data downstream.
* **Processing Layer (ML Engine):** The locally loaded `scikit-learn` algorithms scale numerical data and encode categorical strings. The Random Forest generates risk probabilities.
* **Output Layer (Data Visualization):** Streamlit caching converts result sets into dynamic, interactive data frames and topology charts.

### 3.4.3 Interface Design
The user interface avoids command-line interactions entirely. It features a sleek, responsive design ensuring cross-platform usability. 
* **Sidebar Navigation:** The left-hand pane serves as a persistent control hub. It securely displays user credentials and manages seamless module transitions.
* **Executive Dashboard View:** Large KPI metric cards display urgent statistics. Interactive bar charts offer granular departmental breakdowns.
* **Single Employee Assessment View:** HR personnel manually input specific demographic factors into a digital form. The system returns a percentage-based Risk Probability score instantly.
* **Bulk Batch Upload View:** This interface accepts raw CSV spreadsheets for high-volume monthly loads. It processes hundreds of records simultaneously and outputs an interactive data table.

## 3.5 Implementation
Visual Studio Code served as the primary IDE. The implementation relied strictly on open-source Python libraries.
* **Data Handling:** `pandas` and `numpy` managed dataframe manipulations and feature engineering. The system calculated true 'Age at Hiring' natively to prevent survival bias.
* **Machine Learning:** `scikit-learn` executed standard scaling, dummy variable encoding, and predictive classifier training.
* **User Interface & Database:** The `streamlit` framework generated the live web application. The `mysql.connector` established persistent connections to a local database. It managed authentication hashes and batch tracking metrics.
* **Version Control:** Git managed iterative feature enhancements securely.

## 3.6 Machine Learning Theoretical Architecture & Model Selection

### 3.6.1 The Mathematical Basis of Random Forest
The Random Forest Classifier powers this artifact. This ensemble method orchestrates hundreds of individual Decision Trees simultaneously. Individual decision trees operate by splitting the dataset into smaller subsets geographically. The algorithm calculates the Gini Impurity at each potential node to find the optimal splitting point. The algorithm seeks to maximize Information Gain. 

However, individual trees easily overfit the data. They memorize the exact training structure. This creates high variance when introduced to unseen employee data. The Random Forest solves this Bias-Variance tradeoff via Bootstrap Aggregating (Bagging). The algorithm builds hundreds of shallow trees. It trains each tree on a random bootstrapped subset of the employee records. During deployment, a new employee file passes through all 500 trees. Each tree casts a vote on whether the employee will resign. The majority consensus dictates the final classification. This ensemble approach dramatically stabilizes variance.

### 3.6.2 Data Engineering Resolution for Class Imbalance
A critical theoretical challenge in HR Analytics is the natural occurrence of class imbalance (the 'Accuracy Paradox'). In a standard manufacturing environment, the majority of employees remain active, while a minority resign. If a machine learning algorithm is exposed to this raw distribution, the underlying loss-function mathematically biases toward the majority class, achieving artificially high accuracy simply by predicting that every employee will stay. 

To combat this, rather than generating unverified synthetic data (e.g., SMOTE) or relying solely on algorithmic class weighting, this project resolved the imbalance natively through rigorous data engineering. The scope was explicitly restricted to predicting 'Infant Attrition'. During preprocessing, right-censored records—active employees who had not yet reached the 12-month tenure threshold—were systematically removed from the training set. This isolation of the infant attrition cohort resulted in a naturally balanced dataset (50.02% vs 49.97%), fundamentally eliminating the accuracy paradox before model training commenced. This structural alignment ensured the predictive engine remained highly sensitive to the behavioral footprints of actual resignations.

### 3.6.3 Model Comparison and Selection Justification
A rigorous comparative analysis tested four classification algorithms: Logistic Regression, standard Decision Trees, Random Forest, and Gradient Boosting.

The initial baseline evaluation produced specific Recall (Sensitivity) scores for correctly identifying at-risk leavers. Gradient Boosting initially achieved the highest baseline recall. However, Gradient Boosting builds trees sequentially. Each tree attempts to correct the residual errors of the previous one. In highly noisy, categorical tabular datasets, sequential error-correction makes Gradient Boosting unstable. It becomes prone to extreme overfitting. Random Forest acts in parallel. It handles noise far more effectively. It also runs lighter computationally inside an offline Streamlit container.

The engineering team subjected the Random Forest model to an aggressive `RandomizedSearchCV` hyperparameter tuning protocol. The protocol utilized 5-Fold Stratified Cross-Validation. The grid search minimized pure Accuracy. It strictly optimized the `Recall` scoring metric. The best parameters extracted were `n_estimators=500` and `max_depth=10`.

The mathematically tuned Random Forest processed the unseen testing data. It achieved a phenomenal 96.15% Recall Rate. This performance increase decisively justified selecting Random Forest. The algorithm catches 96% of impending resignations using an interpretable, parallel-processing architecture.

## 3.7 Testing Strategy
A comprehensive test plan guaranteed correct integration between the machine learning model and the web dashboard.

### 3.7.1 Test Environment & Tools
Testing utilized an Intel Core i5 environment with 8GB RAM. This handled large Pandas dataframes seamlessly. Manual UI testing verified button flows. Validation testing utilized Scikit-Learn's `train_test_split` logic. Boundary Value Analysis tested all input forms.

### 3.7.2 Unit Testing
Unit testing verified individual analytical functions prior to UI connection.
* **Data Cleaning Tests:** The system filled missing values properly without crashing. Numerical conversions parsed text strings flawlessly.
* **Encoding Tests:** The system converted demographic text data into binary arrays perfectly matching the saved model schema.

### 3.7.3 Integration Testing
Integration testing ensured reliable communication across architectural boundaries.
* **File Upload Testing:** Streamlit loaded uploaded files safely into Pandas dataframes without memory corruption.
* **Results Display Testing:** Boolean classification arrays accurately triggered specific dynamic charts on the dashboard.

### 3.7.4 System Testing
System testing validated the end-to-end user journey in a production simulation.
* **End-to-End Workflow:** The pipeline successfully ingested a raw file, processed it globally, logged it via MySQL, and charted it seamlessly.
* **Error Handling:** The system generated specific UI error alerts when handling incorrect user inputs, effectively preventing hard crashes.
