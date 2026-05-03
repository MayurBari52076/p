# ===============================
# PRACTICAL 2: ETL + VISUALIZATION
# ===============================

# Import libraries
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt


# -------------------------------
# STEP 1: LOAD EXCEL DATA
# -------------------------------

data_excel = pd.read_excel("Employee.xlsx")

print("Excel Data:")
print(data_excel.head())

# Check column names
print("\nColumns:", data_excel.columns)


# -------------------------------
# STEP 2: STORE DATA INTO SQL
# -------------------------------

conn = sqlite3.connect("employee.db")

# Save Excel data into database
data_excel.to_sql("employees", conn, if_exists="replace", index=False)


# -------------------------------
# STEP 3: READ DATA FROM SQL
# -------------------------------

data_sql = pd.read_sql_query("SELECT * FROM employees", conn)

print("\nSQL Data:")
print(data_sql.head())


# -------------------------------
# STEP 4: COMBINE DATA
# -------------------------------

# Combine Excel + SQL data
data = pd.concat([data_excel, data_sql], ignore_index=True)

# Remove duplicates
data.drop_duplicates(inplace=True)

# Fill missing values using forward fill
data.fillna(method='ffill', inplace=True)

print("\nCleaned Data:")
print(data.head())


# -------------------------------
# STEP 5: DATA CLEANING (SALARY)
# -------------------------------

# Remove currency symbols and commas
data['Annual Salary'] = data['Annual Salary'].replace('[₹$,]', '', regex=True)

# Convert salary column to numeric
data['Annual Salary'] = pd.to_numeric(data['Annual Salary'], errors='coerce')


# -------------------------------
# STEP 6: VISUALIZATION
# -------------------------------

# -------- 1. Top 10 Highest Paid Employees --------
top10 = data.sort_values(by='Annual Salary', ascending=False).head(10)

plt.figure()
plt.bar(top10['Full Name'], top10['Annual Salary'])
plt.title("Top 10 Highest Paid Employees")
plt.xlabel("Employee Name")
plt.ylabel("Annual Salary")
plt.xticks(rotation=45)
plt.show()


# -------- 2. Average Salary by Department --------
dept_salary = data.groupby('Department')['Annual Salary'].mean()

plt.figure()
plt.bar(dept_salary.index, dept_salary.values)
plt.title("Average Salary by Department")
plt.xlabel("Department")
plt.ylabel("Average Salary")
plt.xticks(rotation=45)
plt.show()


# -------- 3. Employee Distribution (Pie Chart) --------
dept_count = data['Department'].value_counts()

plt.figure()
plt.pie(dept_count.values, labels=dept_count.index, autopct='%1.1f%%')
plt.title("Employees Distribution by Department")
plt.show()


# -------- 4. Salary Trend by Age (Line Chart) --------
sorted_data = data.sort_values(by='Age')

plt.figure()
plt.plot(sorted_data['Age'], sorted_data['Annual Salary'], marker='o')
plt.title("Salary Trend by Age")
plt.xlabel("Age")
plt.ylabel("Annual Salary")
plt.show()


# -------- 5. Salary Distribution (Histogram) --------
plt.figure()
plt.hist(data['Annual Salary'], bins=10)
plt.title("Salary Distribution")
plt.xlabel("Salary")
plt.ylabel("Frequency")
plt.show()


# Close database connection
conn.close()
