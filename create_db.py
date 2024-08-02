import sqlite3
import pandas as pd

# Define the path to your CSV file
csv_file = 'cleaned_data7_ap_qualified_students_2024.csv'

# Load the data from the CSV file
df = pd.read_csv(csv_file)

# Rename the columns as required
df.columns = ['sl_no', 'neet_rank', 'neet_roll_no', 'candidate_name', 'gender', 'category', 'PwBD', 'score']

# Create a connection to the SQLite database
db_file = 'neet_candidates.db'
conn = sqlite3.connect(db_file)

# Create a table in the SQLite database and insert data
df.to_sql('neet_candidates', conn, if_exists='replace', index=False)

# Close the database connection
conn.close()
