import streamlit as st
import sqlite3
import pandas as pd
import firebase_admin
from firebase_admin import credentials, db
import bcrypt
import os

# Initialize Firebase Admin SDK only if it's not already initialized
if not firebase_admin._apps:
    try:
        # Load Firebase credentials
        cred = credentials.Certificate('medi-rakesh-503bc-firebase-adminsdk-pfk5i-69f267ec31.json')
        # Initialize Firebase app with credentials and database URL
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://medi-rakesh-503bc-default-rtdb.firebaseio.com/'
        })
        print("Firebase Initialized")
    except Exception as e:
        print(f"Failed to initialize Firebase: {e}")

# Set page configuration to wide mode
st.set_page_config(layout="wide")

def fetch_data(query, db_file='neet_candidates.db'):
    with sqlite3.connect(db_file) as conn:
        df = pd.read_sql_query(query, conn)
    return df

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8'), salt.decode('utf-8')

def verify_password(stored_hash, password):
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))

def authenticate_user(username, password):
    try:
        # Reference to the user in Firebase Realtime Database
        user_ref = db.reference("user_details").child(username)
        user_data = user_ref.get()

        if user_data:
            # Verify password
            stored_hash = user_data.get("hashed_password")
            if stored_hash and verify_password(stored_hash, password):
                # Check if the user is in RequestedUsers
                requested_user_ref = db.reference("requested_users").child(username)
                requested_user_data = requested_user_ref.get()

                if requested_user_data:
                    return "User not yet accepted"

                # Check if the user is in AcceptedUsers
                accepted_user_ref = db.reference("accepted_users").child(username)
                accepted_user_data = accepted_user_ref.get()

                if accepted_user_data:
                    return "Authenticated"
                else:
                    return "Invalid username or password"
            else:
                return "Invalid username or password"
        else:
            return "Invalid username or password"
    except Exception as e:
        return f"Authentication error: {str(e)}"

def main():
    st.title("Neet UG-2024 AP Results")

    # Initialize session state variables if not already present
    if "auth_status" not in st.session_state:
        st.session_state.auth_status = None
    if "username" not in st.session_state:
        st.session_state.username = None

    # Authentication section
    st.sidebar.header("Login")
    username_input = st.sidebar.text_input("Username", key="username_input")
    password_input = st.sidebar.text_input("Password", type="password", key="password_input")
    login_button = st.sidebar.button("Login")
    logout_button = st.sidebar.button("Logout")

    if logout_button:
        st.session_state.auth_status = None
        st.session_state.username = None
        st.sidebar.success("Logged out successfully")
        st.experimental_rerun()

    if login_button:
        auth_status = authenticate_user(username_input, password_input)
        if auth_status == "Authenticated":
            st.session_state.auth_status = "Authenticated"
            st.session_state.username = username_input
            st.sidebar.success("Login successful")
            st.experimental_rerun()
        else:
            st.sidebar.error(auth_status)

    if st.session_state.auth_status == "Authenticated":  # Show the main app only if the user is authenticated
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
    else:
        st.sidebar.info("Please log in to view the content.")

if __name__ == "__main__":
    main()
