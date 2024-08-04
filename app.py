import streamlit as st
import sqlite3
import pandas as pd

# Set page configuration to wide mode
st.set_page_config(layout="wide")

def fetch_data(query, db_file='neet_candidates.db'):
    with sqlite3.connect(db_file) as conn:
        df = pd.read_sql_query(query, conn)
    return df

def main():
    st.title("Neet UG-2024 AP Results")
    
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
            html, body, [class*="css"] {
                font-family: 'Inter', sans-serif;
            }
            .author-section {
                display: flex;
                align-items: center;
            }
            .author-icon {
                width: 50px;
                height: 50px;
                border-radius: 50%;
                margin-right: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="author-section">
            <div>
                <strong>Data Sorted By :</strong> MedicalHunt
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        Dr. YSR UNIVERSITY OF HEALTH SCIENCES: AP: VIJAYAWADA -08
        NEET UG Rank wise list of candidates of the State of Andhra Pradesh who appeared for NEET UG-2024 conducted by NTA, New Delhi (As per the data received from DGHS, Government of India, New Delhi)
        Cut off Marks for Eligibility to apply for admission into UG Medical/Dental courses-2024-25
    """)

    # Create columns
    col1, col2 = st.columns(2)

    with col1:
        score = st.number_input("Enter Score", min_value=0, step=1)
        gender = st.selectbox("Select Gender", ["None", "Male", "Female"])
        category = st.selectbox("Select Category", [
            "None", "UR/EWS", "OBC-(NCL) As Per Central List", "SC", "ST", 
            "UR / EWS & PwBD", "OBC & PwBD", "SC & PwBD", "ST & PwBD"
        ])
        neet_roll_no = st.text_input("Neet Roll Number (Eg String : 1203040193)")

    query = "SELECT * FROM neet_candidates WHERE 1=1"
    if score:
        query += f" AND score = {score}"
    if gender != "None":
        query += f" AND gender = '{gender}'"
    if category != "None":
        query += f" AND category = '{category}'"
    if neet_roll_no:
        query += f" AND neet_roll_no = '{neet_roll_no}'"

    df = fetch_data(query)
    
    # Drop the candidate_name column
    if 'candidate_name' in df.columns:
        df = df.drop(columns=['candidate_name'])
    
    # Adjust the index to start from 1
    df.index = df.index + 1
    
    with col2:
        st.write(df)

if __name__ == "__main__":
    main()
