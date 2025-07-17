import streamlit as st
import altair as alt
import pandas as pd
import pickle
from PIL import Image
import base64

# Set eco-friendly color palette
ECO_COLORS = {
    "primary": "#2E8B57",  # Sea Green
    "secondary": "#3CB371",  # Medium Sea Green
    "background": "#F5F5F5",
    "text": "#333333",
    "accent": "#8FBC8F"  # Dark Sea Green
}

# Custom CSS for eco-friendly styling
# Custom CSS for eco-friendly styling
def set_eco_style():
    st.markdown(f"""
    <style>
        .main {{
            background-color: {ECO_COLORS['background']};
            color: {ECO_COLORS['text']};
        }}
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {{
            background-color: white;
            color: {ECO_COLORS['text']};
            border: 1px solid {ECO_COLORS['secondary']};
        }}
        .stButton>button {{
            background-color: {ECO_COLORS['primary']};
            color: white;
            border: none;
            border-radius: 4px;
            padding: 0.5rem 1rem;
        }}
        .stButton>button:hover {{
            background-color: {ECO_COLORS['secondary']};
            color: white;
        }}
        .css-1aumxhk {{
            background-color: {ECO_COLORS['background']};
            color: {ECO_COLORS['text']};
        }}
        .sidebar .sidebar-content {{
            background-color: {ECO_COLORS['background']};
            color: {ECO_COLORS['text']};
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: {ECO_COLORS['primary']};
        }}
        .leafy-header {{
            color: {ECO_COLORS['primary']};
            font-weight: bold;
            display: flex;
            align-items: center;
        }}
        .leafy-header img {{
            margin-right: 10px;
        }}
        .eco-card {{
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid {ECO_COLORS['primary']};
            color: {ECO_COLORS['text']};
        }}
        .eco-metric {{
            font-size: 24px;
            color: {ECO_COLORS['primary']};
            font-weight: bold;
        }}
    </style>
    """, unsafe_allow_html=True)


# Load vectorizers and models with error handling
@st.cache_resource
def load_models():
    models = {}
    vectorizers = {}
    
    try:
        # Load vectorizers
        vectorizer_files = {
            "toxic": "toxic_vect.pkl",
            "severe_toxic": "severe_toxic_vect.pkl",
            "obscene": "obscene_vect.pkl",
            "insult": "insult_vect.pkl",
            "threat": "threat_vect.pkl",
            "identity_hate": "identity_hate_vect.pkl"
        }
        
        for name, file in vectorizer_files.items():
            with open(file, "rb") as f:
                vectorizers[name] = pickle.load(f)
        
        # Load models
        model_files = {
            "toxic": "toxic_model.pkl",
            "severe_toxic": "severe_toxic_model.pkl",
            "obscene": "obscene_model.pkl",
            "insult": "insult_model.pkl",
            "threat": "threat_model.pkl",
            "identity_hate": "identity_hate_model.pkl"
        }
        
        for name, file in model_files.items():
            with open(file, "rb") as f:
                models[name] = pickle.load(f)
                
        return models, vectorizers
        
    except FileNotFoundError as e:
        st.error(f"Model file not found: {str(e)}")
        st.stop()
    except Exception as e:
        st.error(f"Error loading models: {str(e)}")
        st.stop()

# ----------------- AUTHENTICATION ------------------
def register_user(username, password):
    if "users" not in st.session_state:
        st.session_state.users = {}
    if username in st.session_state.users:
        return False
    st.session_state.users[username] = password
    return True

def login_user(username, password):
    users = st.session_state.get("users", {})
    return username in users and users[username] == password

# ----------------- DASHBOARD ------------------
def show_dashboard():
    st.sidebar.markdown("### Intelligent Platform for Predicting and Managing Toxic Online Comments")
    st.sidebar.info(
        "Our platform leverages advanced AI algorithms to analyze and manage toxicity in online comments. "
        "Ensure a safer, more respectful digital environment by identifying and mitigating harmful interactions."
    )

    page = st.sidebar.radio("Navigation", ["Home", "Toxicity Prediction", "Upload Data"])
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.info(
        "The Intelligent Platform for Predicting and Managing Toxic Online Comments is designed to help "
        "moderators and users alike in understanding and reducing toxic behavior online. "
        "Empower your communities with insights into various levels of comment toxicity."
    )

    
    if page == "Home":
        show_home_page()
    elif page == "Toxicity Prediction":
        show_prediction_page()
    elif page == "Upload Data":
        show_upload_page()
    

def show_home_page():
    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown(f"""
        <div class="header">
            <img src="https://cdn-icons-png.flaticon.com/512/2913/2913108.png" width="40">
            <h1>Welcome to the Intelligent Platform for Predicting and Managing Toxic Online Comments</h1>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>⚡ Accurate Toxicity Detection</h3>
            <p>Analyze and predict toxicity in online comments with state-of-the-art AI algorithms, ensuring precision and speed.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Key Features</h3>
            <ul>
                <li>Real-time comment toxicity analysis</li>
                <li>Insights into multiple toxicity categories</li>
                <li>Data visualization for toxicity patterns</li>
                <li>User-friendly interface for easy navigation</li>
                <li>Customizable thresholds for toxicity levels</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🌟 Why Choose Us?</h3>
            <p>Our platform empowers moderators, businesses, and communities to maintain a positive online environment by providing:</p>
            <ul>
                <li>Comprehensive toxicity reports</li>
                <li>Actionable insights for content moderation</li>
                <li>AI-driven solutions tailored to your needs</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>💡 Did You Know?</h3>
            <p>Managing online toxicity helps foster healthier digital interactions, improving user satisfaction and engagement.</p>
        </div>
        """, unsafe_allow_html=True)


def show_prediction_page():
    st.markdown(f"""
    <div class="leafy-header">
        <img src="https://cdn-icons-png.flaticon.com/512/2491/2491905.png" width="40">
        <h1>Toxicity Analysis</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="eco-card">
        <p>Enter text below to analyze for various toxicity categories. Our models will evaluate the content 
        and provide probability scores for each toxicity type.</p>
    </div>
    """, unsafe_allow_html=True)
    
    models, vectorizers = load_models()
    
    user_input = st.text_area("Enter text to analyze:", height=150,
                            placeholder="Type or paste your text here...")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("Analyze Text", help="Click to analyze the text for toxicity"):
            if user_input:
                with st.spinner("Analyzing with eco-efficient algorithms..."):
                    data = [user_input]
                    results = {
                        "Toxic": round(models["toxic"].predict_proba(vectorizers["toxic"].transform(data))[:, 1][0], 4),
                        "Severe Toxic": round(models["severe_toxic"].predict_proba(vectorizers["severe_toxic"].transform(data))[:, 1][0], 4),
                        "Obscene": round(models["obscene"].predict_proba(vectorizers["obscene"].transform(data))[:, 1][0], 4),
                        "Insult": round(models["insult"].predict_proba(vectorizers["insult"].transform(data))[:, 1][0], 4),
                        "Threat": round(models["threat"].predict_proba(vectorizers["threat"].transform(data))[:, 1][0], 4),
                        "Identity Hate": round(models["identity_hate"].predict_proba(vectorizers["identity_hate"].transform(data))[:, 1][0], 4)
                    }
                    
                    # Display results in a clean format
                    st.markdown("### Analysis Results")
                    
                    # Create metrics in columns
                    cols = st.columns(3)
                    for i, (k, v) in enumerate(results.items()):
                        with cols[i % 3]:
                            st.metric(label=k, value=f"{v:.2%}")
                    
                    # Create visualization
                    chart_df = pd.DataFrame({
                        'Category': list(results.keys()),
                        'Probability': list(results.values())
                    })
                    
                    chart = alt.Chart(chart_df).mark_bar(color=ECO_COLORS['primary']).encode(
                        x=alt.X('Category:N', title='Toxicity Type', sort='-y'),
                        y=alt.Y('Probability:Q', title='Probability', axis=alt.Axis(format='%')),
                        tooltip=['Category', alt.Tooltip('Probability', format='.2%')]
                    ).properties(
                        height=400,
                        title='Toxicity Probability by Category'
                    )
                    
                    st.altair_chart(chart, use_container_width=True)
            else:
                st.warning("Please enter some text to analyze.")
    
    with col2:
        if st.button("Logout", key="logout_prediction"):
            st.session_state.logged_in = False
            st.session_state.page = "login"
            st.rerun()

def show_upload_page():
    st.markdown(f"""
    <div class="leafy-header">
        <img src="https://cdn-icons-png.flaticon.com/512/4301/4301699.png" width="40">
        <h1>Data Analysis</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="eco-card">
        <p>Upload a CSV file containing text data for batch analysis. Our system will process the data 
        with optimized algorithms to minimize energy consumption.</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    
    if uploaded_file is not None:
        try:
            data = pd.read_csv(uploaded_file)
            
            st.success("File uploaded successfully!")
            
            # Show basic info
            st.markdown("### Dataset Overview")
            st.write(f"Rows: {data.shape[0]}, Columns: {data.shape[1]}")
            
            # Show preview
            st.markdown("### Data Preview")
            st.dataframe(data.head())
            
            # Show statistics
            st.markdown("### Basic Statistics")
            st.write(data.describe())
            
            # Add analysis options
            st.markdown("### Analysis Options")
            if st.button("Analyze for Toxicity", key="analyze_upload"):
                st.info("Batch toxicity analysis is coming soon! Currently please use the single text analysis feature.")
            
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")



# ----------------- MAIN CONTROLLER ------------------
def main():
    # Set page config with eco-friendly theme
    st.set_page_config(
        page_title="Intelligent Platform for Predicting and Managing Toxic Online Comments",
        page_icon="🌱",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply custom styles
    set_eco_style()
    
    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "page" not in st.session_state:
        st.session_state.page = "register"
    
    # Authentication flow
    if not st.session_state.logged_in:
        if st.session_state.page == "register":
            show_registration_page()
        elif st.session_state.page == "login":
            show_login_page()
    else:
        show_dashboard()

def show_registration_page():
    st.markdown(f"""
    <div style="max-width: 500px; margin: 0 auto; padding: 20px;">
        <div class="leafy-header">
            <img src="https://cdn-icons-png.flaticon.com/512/2913/2913108.png" width="40">
            <h1>Create an Account</h1>
        </div>
        <div class="eco-card">
            <p>Join our Intelligent Platform for Predicting and Managing Toxic Online Comments  to analyze text toxicity with minimal environmental impact.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("registration_form"):
        username = st.text_input("Username", key="reg_username")
        password = st.text_input("Password", type="password", key="reg_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")
        
        submitted = st.form_submit_button("Register")
        
        if submitted:
            if not username or not password:
                st.error("Please fill in all fields")
            elif password != confirm_password:
                st.error("Passwords do not match")
            else:
                if register_user(username, password):
                    st.success("Registration successful! Please login.")
                    st.session_state.page = "login"
                    st.rerun()
                else:
                    st.error("Username already exists")
    
    st.markdown("Already have an account? [Login here](#login)", unsafe_allow_html=True)

def show_login_page():
    st.markdown(f"""
    <div style="max-width: 500px; margin: 0 auto; padding: 20px;">
        <div class="leafy-header">
            <img src="https://cdn-icons-png.flaticon.com/512/2913/2913108.png" width="40">
            <h1>Welcome Back</h1>
        </div>
        <div class="eco-card">
            <p>Login to access Intelligent Platform for Predicting and Managing Toxic Online Comments tools.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        submitted = st.form_submit_button("Login")
        
        if submitted:
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.page = "main"
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid username or password")
    
    st.markdown("Don't have an account? [Register here](#register)", unsafe_allow_html=True)

if __name__ == "__main__":
    main()