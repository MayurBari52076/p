# ===============================
# PRACTICAL 1: ETL PROCESS
# ===============================

# Import required libraries
import pandas as pd
import sqlite3

# -------------------------------
# STEP 1: EXTRACT DATA FROM EXCEL
# -------------------------------

# Load Excel file into pandas DataFrame
excel_data = pd.read_excel("D:/Practicals/Superstore Sales Performance Analysis.xlsx")

print("Excel Data Preview:")
print(excel_data.head())


# -------------------------------
# STEP 2: CONNECT TO DATABASE
# -------------------------------

# Create connection to SQLite database (creates file if not exists)
conn = sqlite3.connect("company.db")


# -------------------------------
# STEP 3: CREATE TABLE IN DATABASE
# -------------------------------

# Create a sample employees table
conn.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER,
    name TEXT,
    salary REAL
)
""")


# -------------------------------
# STEP 4: INSERT SAMPLE DATA
# -------------------------------

conn.execute("INSERT INTO employees VALUES (1, 'Amit', 50000)")
conn.execute("INSERT INTO employees VALUES (2, 'Neha', 60000)")

# Save changes
conn.commit()


# -------------------------------
# STEP 5: EXTRACT DATA FROM SQL
# -------------------------------

sql_data = pd.read_sql_query("SELECT * FROM employees", conn)

print("\nSQL Data Preview:")
print(sql_data.head())


# -------------------------------
# STEP 6: TRANSFORM (COMBINE DATA)
# -------------------------------

# Combine Excel + SQL data
combined_data = pd.concat([excel_data, sql_data], ignore_index=True)

# Remove duplicate rows
combined_data.drop_duplicates(inplace=True)

# Fill missing values
combined_data.fillna("N/A", inplace=True)

print("\nCombined Cleaned Data:")
print(combined_data.head())


# -------------------------------
# STEP 7: LOAD TO TARGET SYSTEM
# -------------------------------

# Save final data to Excel
combined_data.to_excel("final_output.xlsx", index=False)
print("\nData saved to final_output.xlsx")

# Save final data to database
combined_data.to_sql("final_table", conn, if_exists="replace", index=False)
print("Data saved to database table: final_table")


# Close connection
conn.close()
