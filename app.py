import streamlit as st
import pandas as pd
import datetime
import time

# --- Configuration ---
# You can change the password here.
RSVP_PASSWORD = "your_secret_password"
# File to store the RSVPs
DATA_FILE = "rsvps.csv"
# Set your graduation date and time here
GRADUATION_DATE = datetime.datetime(2025, 11, 1, 14, 0, 0) # Format: YYYY, M, D, H, M, S

# --- Functions to manage data ---
def initialize_data_file():
    """Initializes the CSV file if it doesn't exist."""
    try:
        pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["timestamp", "name", "guests", "message"])
        df.to_csv(DATA_FILE, index=False)

def save_rsvp(name, guests, message):
    """Appends a new RSVP to the CSV file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_rsvp = pd.DataFrame([{
        "timestamp": timestamp,
        "name": name,
        "guests": guests,
        "message": message
    }])
    new_rsvp.to_csv(DATA_FILE, mode='a', header=False, index=False)

def get_all_rsvps():
    """Reads all RSVPs from the CSV file."""
    try:
        df = pd.read_csv(DATA_FILE)
        return df
    except FileNotFoundError:
        return pd.DataFrame()

# --- Streamlit App UI ---
st.set_page_config(page_title="Graduation RSVP", layout="centered")

# --- Custom CSS for Styling ---
# This CSS block adds an image background to the entire page
# and styles the main content container and form elements.
st.markdown(
    """
    <style>
    /* Background image for the entire app */
    .stApp {
        background-image: url("matrix-style-binary-code-digital-falling-numbers-blue-background_1017-37387.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }
    /* Style the main content container to make it a central card */
    .stApp > div:first-child > section {
        background-color: rgba(255, 255, 255, 0.9); /* Slightly transparent white for readability */
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 2rem auto;
        max-width: 600px;
    }
    /* Style the form and its elements */
    .stButton button {
        background-color: #6a0dad;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stTextInput, .stNumberInput, .stTextArea {
        border-radius: 8px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True
)

# --- Page Navigation ---
query_params = st.query_params
page = query_params.get("page", "form")

if page == "form":
    # --- RSVP Form Page ---
    st.title("You're Invited!")
    st.markdown(
        "Hi there This invitation is from Joram Kariuki. Please reach out to me via, if you have any questions or concerns about attending. I can't wait to see you!. Also if you have an old Macbook you arent using or a core i7 machine feel free togift me😂😂"
    )
    st.subheader("Please RSVP for my Graduation Ceremony & Celebration.")

    with st.form(key='rsvp_form'):
        name = st.text_input("Full Name", placeholder="e.g., Jane Doe")
        
        # Guest input is now always visible
        guests = st.number_input("Number of Guests (including yourself)", min_value=0, value=1)
        
        message = st.text_area("Message (Optional)", placeholder="Leave a congratulatory message!")
        
        submit_button = st.form_submit_button(label="Submit RSVP")

    if submit_button:
        if name:
            initialize_data_file()
            save_rsvp(name, guests, message)
            st.success("RSVP submitted successfully! Thank you!")
            #st.info("You can refresh the page to submit another RSVP.")
        else:
            st.error("Please enter your full name to RSVP.")

    st.markdown("---")
    st.markdown("Developed by The Graduate😂.")
    # Live countdown timer
    countdown_placeholder = st.empty()
    while datetime.datetime.now() < GRADUATION_DATE:
        time_left = GRADUATION_DATE - datetime.datetime.now()
        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        countdown_placeholder.markdown(f"""
        ### Time to go:
        <div style="text-align:center; font-size: 2em; font-weight: bold;">
            {days} Days {hours} Hrs {minutes} Mins {seconds} Secs
        </div>
        """, unsafe_allow_html=True)
        time.sleep(1)

    countdown_placeholder.markdown("### The graduation has begun! Congratulations!")

    #st.markdown("For private access, go to the URL: `?page=admin` and enter the password.")

elif page == "admin":
    # --- Admin Page with Password Protection ---
    st.title("Admin Dashboard")
    st.subheader("View all submitted RSVPs.")

    password = st.text_input("Enter Admin Password", type="password")

    if password == RSVP_PASSWORD:
        st.success("Access Granted!")
        df_rsvps = get_all_rsvps()

        if not df_rsvps.empty:
            st.markdown("### Guest List")
            st.write(df_rsvps)
            
            # Download button
            csv_data = df_rsvps.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Guest List as CSV",
                data=csv_data,
                file_name="graduation_rsvps.csv",
                mime="text/csv",
                key="download-button"
            )
        else:
            st.info("No RSVPs have been submitted yet.")
    elif password:
        st.error("Incorrect password. Please try again.")

else:
    st.warning("Invalid page. Please go back to the home page.")

# Make sure to run this app using: streamlit run app.py
