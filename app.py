import streamlit as st
import pandas as pd
import pickle
import requests

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Insurance Charge Predictor",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CSS STYLING (EMBEDDED) ---
CSS_CODE = """
/* General Body Styles */
body {
    background-color: #f0f2f6;
    color: #333;
}

/* Main content area */
.main .block-container {
    padding-top: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* Hide Streamlit's default header and footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Styling for input widgets */
div[data-testid="stNumberInput"] input,
div[data-testid="stSelectbox"] div[data-baseweb="select"] {
    background-color: #ffffff;
    color: #333333;
    border-radius: 5px;
}

/* Make sure the text inside the number input is also dark */
div[data-testid="stNumberInput"] input {
    color: #333333;
}

/* Styling for the prediction button */
div[data-testid="stButton"] > button {
    border: 2px solid #007BFF;
    background-color: #007BFF;
    color: white;
    padding: 10px 24px;
    border-radius: 8px;
    font-weight: bold;
    width: 100%;
}

div[data-testid="stButton"] > button:hover {
    background-color: #0056b3;
    color: white;
    border-color: #0056b3;
}

/* Result display style */
.result-box {
    background-color: #e6f7ff;
    border-left: 5px solid #007BFF;
    padding: 20px;
    border-radius: 8px;
    margin-top: 20px;
    font-size: 1.2rem;
    color: #333;
}
"""

st.markdown(f'<style>{CSS_CODE}</style>', unsafe_allow_html=True)

# --- LOAD THE MODEL ---
try:
    with open('insurance.pkl', 'rb') as file:
        model = pickle.load(file)
except FileNotFoundError:
    st.error("Model file not found. Please ensure 'insurance.pkl' is in the root directory.")
    st.stop()
except Exception as e:
    st.error(f"An error occurred while loading the model: {e}")
    st.stop()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "About", "Contact"])

# --- Helper function to fetch exchange rate ---
def get_usd_to_inr_rate():
    try:
        response = requests.get("https://api.exchangerate.host/latest?base=USD&symbols=INR")
        data = response.json()
        return data["rates"]["INR"]
    except Exception as e:
        st.warning(f"Could not fetch live exchange rate: {e}")
        return None

# ===================================
# --- HOME PAGE ---
# ===================================
if page == "Home":
    st.title("Insurance Premium Predictor")
    st.write("Enter the details below to get an estimate of your insurance premium (converted to INR).")

    with st.form("prediction_form"):
        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input("Age", min_value=18, max_value=100, value=30, step=1)
            smoker_option = st.selectbox("Are you a smoker?", ("No", "Yes"))

        with col2:
            bmi = st.number_input("BMI (Body Mass Index)", min_value=15.0, max_value=55.0, value=25.0, step=0.1)

        submitted = st.form_submit_button("Predict Premium")

    if submitted:
        smoker_yes = 1 if smoker_option == "Yes" else 0
        input_data = pd.DataFrame({
            'age': [age],
            'bmi': [bmi],
            'smoker_yes': [smoker_yes]
        })

        try:
            prediction_usd = model.predict(input_data)[0]
            usd_to_inr = get_usd_to_inr_rate()

            if usd_to_inr is not None:
                prediction_inr = prediction_usd * usd_to_inr
                st.markdown("### Prediction Result")
                st.markdown(
                    f'''
                    <div class="result-box">
                        Estimated annual insurance charge: <strong>₹{prediction_inr:,.2f}</strong><br>
                        (approx based on USD value of ${prediction_usd:,.2f} and exchange rate ₹{usd_to_inr:.2f}/USD)
                    </div>
                    ''',
                    unsafe_allow_html=True
                )
            else:
                st.markdown("### Prediction Result")
                st.markdown(
                    f'''
                    <div class="result-box">
                        Estimated annual insurance charge (USD): <strong>${prediction_usd:,.2f}</strong><br>
                        <em>Could not convert to INR (exchange rate unavailable)</em>
                    </div>
                    ''',
                    unsafe_allow_html=True
                )

        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")

    st.markdown("---")
    st.info("💡 **Disclaimer:** This is a prediction based on a machine learning model and should be used for informational purposes only.")

# ===================================
# --- ABOUT PAGE ---
# ===================================
elif page == "About":
    st.title("About InsurePredict")
    st.image("https://images.unsplash.com/photo-1579621970795-87f54d5921ba?w=500", caption="Data-driven decisions in healthcare.")
    st.markdown("""
    ### The Project
    **InsurePredict** is a web application designed to demonstrate machine learning in the insurance domain. By inputting health features such as age, BMI, and smoking status, users get an instant estimate of their potential annual insurance premium in Indian Rupees.

    ### The Model & Conversion
    - The model is trained (or expects) values in USD.
    - The app fetches the live USD → INR exchange rate from **exchangerate.host** and converts the prediction.
    - If exchange rate fetch fails, the app falls back to showing the USD prediction.

    **Note:** Predictions are for demonstration; not a formal quote.
    """)

# ===================================
# --- CONTACT PAGE ---
# ===================================
elif page == "Contact":
    st.title("Get In Touch 📧")
    st.write("We'd love to hear from you! Please fill out the form below.")
    with st.form("contact_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area("Your Message", height=150)
        submitted = st.form_submit_button("Send Message")
        if submitted:
            if name and email and message:
                st.success("Thank you for your message! We will get back to you shortly.")
            else:
                st.error("Please fill out all the fields before sending.")
