import streamlit as st
import pandas as pd
import pickle

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Insurance Charge Predictor",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CSS STYLING (EMBEDDED) ---
# All CSS is now inside this multiline string
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
    border-radius: 5px;
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
}
"""

# --- INJECT CSS INTO THE APP ---
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


# ===================================
# --- HOME PAGE ---
# ===================================
if page == "Home":
    st.title("Insurance Premium Predictor")
    st.write("Enter the details below to get an estimate of your insurance premium.")

    # --- USER INPUT FORM ---
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input("Age", min_value=18, max_value=100, value=30, step=1)
            smoker_option = st.selectbox("Are you a smoker?", ("No", "Yes"))

        with col2:
            bmi = st.number_input("BMI (Body Mass Index)", min_value=15.0, max_value=55.0, value=25.0, step=0.1)

        submitted = st.form_submit_button("Predict Premium")

    # --- PREDICTION LOGIC ---
    if submitted:
        smoker_yes = 1 if smoker_option == "Yes" else 0
        input_data = pd.DataFrame({
            'age': [age],
            'bmi': [bmi],
            'smoker_yes': [smoker_yes]
        })

        try:
            prediction = model.predict(input_data)[0]
            st.markdown("### Prediction Result")
            st.markdown(
                f'''
                <div class="result-box">
                    The estimated annual insurance charge is: <strong>${prediction:,.2f}</strong>
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
    **InsurePredict** is a web application designed to demonstrate the power of machine learning in the insurance industry. By inputting key health metrics such as age, BMI, and smoking status, users can receive an instant estimate of their potential annual insurance premiums.

    ### The Model
    The prediction engine is powered by a **Linear Regression** model, a fundamental algorithm in machine learning. It was trained on a public dataset containing insurance information. The model learns the relationship between the input features and the final insurance charge.

    **Key Features Used by the Model:**
    - **Age:** The age of the individual.
    - **BMI (Body Mass Index):** A measure of body fat based on height and weight.
    - **Smoker Status:** Whether the individual is a smoker or not.

    ### Our Mission
    Our goal is to make complex data science concepts accessible and understandable. This tool serves as an educational resource to show how data can be leveraged to make predictions and provide valuable insights.

    **Please Note:** The predictions generated by this tool are for demonstration purposes only and should not be considered a formal insurance quote.
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
