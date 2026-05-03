# ==========================================
# PRACTICAL: DECISION TREE CLASSIFICATION
# ==========================================

# Import required libraries
import pandas as pd                                  # For data handling
from sklearn.model_selection import train_test_split # For splitting dataset
from sklearn.preprocessing import LabelEncoder       # For encoding categorical data
from sklearn.tree import DecisionTreeClassifier      # Decision Tree model
from sklearn.metrics import accuracy_score           # To evaluate model


# ------------------------------------------
# STEP 1: LOAD DATASET
# ------------------------------------------

# Load Excel file
data = pd.read_excel("Employee.xlsx")

# Display first 5 rows
print("Dataset Preview:")
print(data.head())


# ------------------------------------------
# STEP 2: DATA CLEANING
# ------------------------------------------

# Convert 'Annual Salary' to numeric
# Remove symbols like ₹, $, commas etc.
data['Annual Salary'] = (
    data['Annual Salary']
    .astype(str)                              # Convert to string first
    .str.replace(r'[^\d.]', '', regex=True)   # Keep only numbers and decimal
)

# Convert cleaned string to numeric
data['Annual Salary'] = pd.to_numeric(data['Annual Salary'], errors='coerce')

# Drop rows with missing values
data.dropna(inplace=True)


# ------------------------------------------
# STEP 3: CREATE TARGET VARIABLE
# ------------------------------------------

# Create new column: Salary Category (High / Low)
# If salary > 100000 → High, else Low
data['Salary Category'] = data['Annual Salary'].apply(
    lambda x: 'High' if x > 100000 else 'Low'
)


# ------------------------------------------
# STEP 4: ENCODE CATEGORICAL VARIABLES
# ------------------------------------------

# Convert categorical text data into numeric format
le = LabelEncoder()

data['Department'] = le.fit_transform(data['Department'])
data['Gender'] = le.fit_transform(data['Gender'])
data['Country'] = le.fit_transform(data['Country'])


# ------------------------------------------
# STEP 5: DEFINE FEATURES AND TARGET
# ------------------------------------------

# Independent variables (inputs)
X = data[['Age', 'Department', 'Gender', 'Country']]

# Dependent variable (output)
y = data['Salary Category']


# ------------------------------------------
# STEP 6: SPLIT DATA INTO TRAIN & TEST
# ------------------------------------------

# 80% training data, 20% testing data
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42   # Ensures same split every time
)


# ------------------------------------------
# STEP 7: TRAIN THE MODEL
# ------------------------------------------

# Create Decision Tree model
model = DecisionTreeClassifier()

# Train model using training data
model.fit(X_train, y_train)


# ------------------------------------------
# STEP 8: MAKE PREDICTIONS
# ------------------------------------------

# Predict on test data
y_pred = model.predict(X_test)


# ------------------------------------------
# STEP 9: EVALUATE MODEL
# ------------------------------------------

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", accuracy)
