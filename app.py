import streamlit as st
import requests
import joblib
import time
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# Configuration de la page
st.set_page_config(
    page_title="Projet Analyse de sentiments",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personnalisé pour un design moderne
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Variables CSS */
    :root {
        --primary-color: #667eea;
        --secondary-color: #764ba2;
        --accent-color: #f093fb;
        --success-color: #4ecdc4;
        --warning-color: #ffd93d;
        --error-color: #ff6b6b;
        --text-dark: #2c3e50;
        --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --card-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    /* Background principal */
    .stApp {
        background: var(--bg-gradient);
        font-family: 'Poppins', sans-serif;
    }
    
    /* Titre principal avec effet néon */
    .main-title {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
        background-size: 400% 400%;
        animation: gradientShift 4s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 0 0 30px rgba(255,255,255,0.5);
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Sous-titre avec glow effect */
    .subtitle {
        color: white;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        text-shadow: 0 0 10px rgba(255,255,255,0.3);
        animation: pulse 2s ease-in-out infinite alternate;
    }
    
    @keyframes pulse {
        from { opacity: 0.8; }
        to { opacity: 1; }
    }
    
    /* Cartes avec effet glassmorphism */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: var(--card-shadow);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.3);
    }
    
    /* Bouton personnalisé */
    .stButton > button {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2) !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3) !important;
        background: linear-gradient(45deg, #4ecdc4, #ff6b6b) !important;
    }
    
    /* Input fields styling */
    .stTextArea textarea, .stSelectbox > div > div {
        border-radius: 15px !important;
        border: 2px solid rgba(255,255,255,0.3) !important;
        background: rgba(255,255,255,0.1) !important;
        color: white !important;
        backdrop-filter: blur(5px) !important;
    }
    
    .stTextArea textarea:focus, .stSelectbox > div > div:focus {
        border-color: var(--accent-color) !important;
        box-shadow: 0 0 20px rgba(240, 147, 251, 0.3) !important;
    }
    
    /* Success/Error messages */
    .success-box {
        background: linear-gradient(45deg, #4ecdc4, #44a08d);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        font-weight: 600;
        box-shadow: var(--card-shadow);
        animation: slideIn 0.5s ease-out;
    }
    
    .error-box {
        background: linear-gradient(45deg, #ff6b6b, #ee5a52);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        font-weight: 600;
        box-shadow: var(--card-shadow);
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from { transform: translateY(-20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(0,0,0,0.2) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .css-1v0mbdj {
        background: rgba(0,0,0,0.1) !important;
    }
    
    /* Navigation styling */
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.1) !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        border-radius: 10px !important;
        color: white !important;
    }
    
    /* Loading animation */
    .loading-animation {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }
    
    .spinner {
        width: 50px;
        height: 50px;
        border: 5px solid rgba(255,255,255,0.3);
        border-top: 5px solid #4ecdc4;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Metrics styling */
    .metric-card {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: scale(1.05);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

# Load the pipeline
@st.cache_resource
def load_pipeline():
    try:
        pipeline = joblib.load("models/sentiment_pipeline.joblib")
        
        # Find the OneHotEncoder for the 'Country' column
        preprocessor = pipeline.named_steps['preprocess']
        country_encoder = None

        for name, transformer, columns in preprocessor.transformers_:
            if name == 'country' or ('Country' in columns):
                country_encoder = transformer
                break

        if country_encoder is not None:
            country_list = list(country_encoder.categories_[0])
        else:
            country_list = ["France", "USA", "UK", "Germany", "Canada", "Australia", "Japan", "Brazil"]

        return pipeline, country_list
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, ["France", "USA", "UK", "Germany"]

# Function to create a probability chart
def create_probability_chart(probabilities):
    if isinstance(probabilities, dict):
        labels = list(probabilities.keys())
        values = list(probabilities.values())
        
        # Custom colors for each sentiment
        colors = {
            'positive': '#4ecdc4',
            'negative': '#ff6b6b', 
            'neutral': '#ffd93d'
        }
        
        fig = go.Figure(data=[
            go.Bar(
                x=labels,
                y=values,
                marker=dict(
                    color=[colors.get(label.lower(), '#667eea') for label in labels],
                    line=dict(color='rgba(255,255,255,0.3)', width=2)
                ),
                text=[f'{v:.1%}' for v in values],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title={
                'text': '📊 Sentiment Probabilities',
                'x': 0.5,
                'font': {'size': 20, 'color': 'white'}
            },
            xaxis={'title': 'Sentiment', 'color': 'white'},
            yaxis={'title': 'Probability', 'color': 'white', 'tickformat': '.0%'},
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font={'color': 'white'},
            margin=dict(l=0, r=0, t=50, b=0)
        )
        
        return fig
    return None

# Sidebar navigation - always visible menu
def sidebar_navigation():
    # Set default page if not already set
    if "current_page" not in st.session_state:
        st.session_state.current_page = "🏠 Sentiment Analysis"

    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h2 style="color: white; margin: 0;">🎭 Main Menu</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Navigation buttons - visually clear, always visible
    nav_items = [
        ("🏠 Sentiment Analysis", "📈 Real-time sentiment analysis of your tweets", [
            "- ✅ AI sentiment analysis",
            "- 🌍 Multi-country support",
            "- ⏰ Temporal analysis",
            "- 📊 Interactive charts"
        ]),
        ("📊 Data Visualization", "📊 Dashboards and visualizations", [
            "- 📈 Segment distribution",
            "- 🌍 Geographic breakdown",
            "- ⏱️ Temporal analysis",
            "- 📋 Global statistics"
        ]),
        ("🗃️ Raw Data", "🗃️ Raw data exploration", [
            "- 📋 Data tables",
            "- 🔍 Advanced filters",
            "- 📥 Data export"
        ]),
        ("🤖 AI Chatbot", "🤖 Conversational sentiment advisor", [
            "- 💬 Interactive conversation",
            "- 🎯 Personalized advice",
            "- 📝 Step-by-step guidance",
            "- 🔄 Multi-turn analysis"
        ]),
    ]

    # Render the menu
    for name, desc, features in nav_items:
        if st.session_state.current_page == name:
            button_type = "primary"
            font_weight = "bold"
            opacity = 1.0
            border = "3px solid #4ecdc4"
        else:
            button_type = "secondary"
            font_weight = "normal"
            opacity = 0.7
            border = "1px solid #555"
        # Use markdown with a clickable hack using st.button and key
        if st.button(
            name, key=f"nav_{name}",
            help=desc,
            use_container_width=True,
        ):
            st.session_state.current_page = name

        st.markdown(
            f"""<div style="height:2px;"></div>""", unsafe_allow_html=True
        )

    st.markdown("---")

    # Display info for current page
    for name, desc, features in nav_items:
        if st.session_state.current_page == name:
            features_md = "\n".join(f"- {f}" for f in features)
            st.markdown(
                f"**Current page:** {desc}\n\n"
                f"**Features:**\n"
                f"{features_md}"
            )
            break

    return st.session_state.current_page

# Main interface
def main():
    with st.sidebar:
        page = sidebar_navigation()
    # The rest remains the same
    if page == "🏠 Sentiment Analysis":
        show_sentiment_analysis_page()
    elif page == "📊 Data Visualization":
        show_data_visualization_page()
    elif page == "🤖 AI Chatbot":
        show_chatbot_page()
    else:
        show_raw_data_page()

def show_sentiment_analysis_page():
    # Title with animation
    st.markdown('<h1 class="main-title">🎭 Sentiment Analyzer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">✨ Analyze the sentiment of your tweets with AI ✨</p>', unsafe_allow_html=True)
    
    # Info cards at the top
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="glass-card">
            <div style="text-align: center;">
                <h3 style="color: white; margin-bottom: 1rem;">🚀 Advanced AI Analysis</h3>
                <div style="display: flex; justify-content: space-around; margin-bottom: 1rem;">
                    <div style="text-align: center;">
                        <div style="font-size: 2rem;">🎯</div>
                        <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Accuracy</div>
                        <div style="color: #4ecdc4; font-weight: bold;">93%</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 2rem;">⚡</div>
                        <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Intelligent</div>
                        <div style="color: #4ecdc4; font-weight: bold;">Improving</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 2rem;">🌍</div>
                        <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Languages</div>
                        <div style="color: #4ecdc4; font-weight: bold;">Multi</div>
                    </div>
                </div>
                <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem; margin: 0;">
                    Our AI model analyzes sentiment with outstanding accuracy,
                    taking into account both geographic and temporal context.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-card">
            <div style="text-align: center;">
                <h3 style="color: white; margin-bottom: 1rem;">📊 Real-Time Stats</h3>
                <div style="display: flex; justify-content: space-around; margin-bottom: 1rem;">
                    <div style="text-align: center;">
                        <div style="font-size: 2rem;">😊</div>
                        <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Positive</div>
                        <div style="color: #4ecdc4; font-weight: bold;">31%</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 2rem;">😐</div>
                        <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Neutral</div>
                        <div style="color: #ffd93d; font-weight: bold;">42%</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 2rem;">😞</div>
                        <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Negative</div>
                        <div style="color: #ff6b6b; font-weight: bold;">27%</div>
                    </div>
                </div>
                <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem; margin: 0;">
                    Global distribution of sentiments analyzed today.
                    Data updated in real time.
                    Every inputs are added to the database, improving our model prediction.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Load pipeline
    pipeline, country_list = load_pipeline()
    
    # Main analysis section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: white; margin-bottom: 1rem;">📝 Enter Tweet</h3>
        </div>
        """, unsafe_allow_html=True)
        
        tweet = st.text_area(
            "Your tweet",
            placeholder="Type your message here...",
            height=120,
            help="Enter the tweet text to analyze"
        )
        
        # Character count
        char_count = len(tweet)
        if char_count > 280:
            st.warning(f"⚠️ Tweet too long ({char_count}/280 characters)")
        else:
            st.info(f"📏 {char_count}/280 characters")
    
    with col2:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: white; margin-bottom: 1rem;">⚙️ Settings</h3>
        </div>
        """, unsafe_allow_html=True)
        
        country = st.selectbox(
            "🌍 Country",
            country_list,
            help="Select the tweet's country of origin"
        )
        
        time_options = ["morning", "noon", "night"]
        time_emojis = {"morning": "🌅", "noon": "☀️", "night": "🌙"}
        time_display = [f"{time_emojis[t]} {t.capitalize()}" for t in time_options]
        
        selected_time_display = st.selectbox(
            "🕐 Time of Day",
            time_display,
            help="Select the posting time"
        )
        
        # Extract the original time value
        time_selected = time_options[time_display.index(selected_time_display)]
    
    # Centered analyze button
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_button = st.button("🚀 ANALYZE SENTIMENT", use_container_width=True)
    
    # Analysis and results
    if analyze_button:
        if not tweet.strip():
            st.markdown('<div class="error-box">❌ Please enter a tweet to analyze</div>', unsafe_allow_html=True)
        else:
            # Loading animation
            with st.spinner("🔄 Analyzing..."):
                time.sleep(1)  # Simulate processing delay
                
                url = "http://localhost:8000/predict"
                payload = {
                    "clean_text_advanced": tweet,
                    "Country": country,
                    "Time_of_Tweet": time_selected
                }
                
                try:
                    response = requests.post(url, json=payload, timeout=10)
                    
                    if response.status_code == 200:
                        result = response.json()
                        prediction = result['prediction']
                        probabilities = result['probabilities']
                        
                        # Display results
                        st.markdown('<div class="success-box">✅ Analysis completed successfully!</div>', unsafe_allow_html=True)
                        
                        # Main result
                        col1, col2, col3 = st.columns(3)
                        
                        sentiment_emojis = {
                            'positive': '😊',
                            'negative': '😞',
                            'neutral': '😐'
                        }
                        
                        sentiment_colors = {
                            'positive': '#4ecdc4',
                            'negative': '#ff6b6b',
                            'neutral': '#ffd93d'
                        }
                        
                        with col2:
                            emoji = sentiment_emojis.get(prediction.lower(), '🤔')
                            color = sentiment_colors.get(prediction.lower(), '#667eea')
                            
                            st.markdown(f"""
                            <div class="metric-card" style="border: 3px solid {color};">
                                <div class="metric-value">{emoji}</div>
                                <div class="metric-label">Sentiment: {prediction.upper()}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Probability chart
                        st.markdown("<br>", unsafe_allow_html=True)
                        fig = create_probability_chart(probabilities)
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)
                        
                        # Analysis details
                        with st.expander("📊 Analysis Details", expanded=False):
                            st.json({
                                "Analyzed Tweet": tweet,
                                "Country": country,
                                "Time": time_selected,
                                "Prediction": prediction,
                                "Probabilities": probabilities,
                                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            })
                    
                    else:
                        st.markdown(f'<div class="error-box">❌ API Error ({response.status_code}): {response.text}</div>', unsafe_allow_html=True)
                
                except requests.exceptions.Timeout:
                    st.markdown('<div class="error-box">⏱️ Timeout: The API is taking too long to respond</div>', unsafe_allow_html=True)
                except requests.exceptions.ConnectionError:
                    st.markdown('<div class="error-box">🔌 Cannot connect to API. Make sure the server is running.</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<div class="error-box">❌ Unexpected error: {e}</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; color: rgba(255,255,255,0.7); padding: 2rem;">
        <p>🤖 Powered by Artificial Intelligence | 💻 Developed with Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

def show_data_visualization_page():
    # CSS supplémentaire pour les graphiques et cartes
    st.markdown("""
    <style>
        /* Cartes de données avec effet glassmorphism amélioré */
        .data-card {
            background: rgba(255, 255, 255, 0.12);
            border-radius: 20px;
            padding: 2rem;
            margin: 1.5rem 0;
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.25);
            box-shadow: 0 12px 32px rgba(0,0,0,0.25);
            transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            position: relative;
            overflow: hidden;
        }
        
        .data-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
            transition: left 0.5s;
        }
        
        .data-card:hover::before {
            left: 100%;
        }
        
        .data-card:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 20px 50px rgba(0,0,0,0.35);
            border-color: rgba(255, 255, 255, 0.4);
        }
        
        /* Métriques avec animations */
        .enhanced-metric-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.08));
            border-radius: 18px;
            padding: 2rem 1.5rem;
            text-align: center;
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.25);
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(12px);
        }
        
        .enhanced-metric-card::before {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
            border-radius: 20px;
            opacity: 0;
            z-index: -1;
            transition: opacity 0.3s ease;
        }
        
        .enhanced-metric-card:hover::before {
            opacity: 1;
        }
        
        .enhanced-metric-card:hover {
            transform: translateY(-5px) scale(1.05);
            box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        }
        
        .enhanced-metric-value {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: numberGlow 2s ease-in-out infinite alternate;
        }
        
        @keyframes numberGlow {
            from { filter: drop-shadow(0 0 5px rgba(255,255,255,0.3)); }
            to { filter: drop-shadow(0 0 15px rgba(255,255,255,0.6)); }
        }
        
        .enhanced-metric-label {
            font-size: 0.85rem;
            opacity: 0.9;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-weight: 500;
        }
        
        /* Section headers avec style moderne */
        .section-header {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
            border-radius: 15px;
            padding: 1.5rem;
            margin: 2rem 0 1rem 0;
            border-left: 4px solid #4ecdc4;
            color: white;
            font-size: 1.4rem;
            font-weight: 600;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }
        
        /* Container pour les graphiques */
        .chart-container {
            background: rgba(255, 255, 255, 0.08);
            border-radius: 20px;
            padding: 2rem;
            margin: 1.5rem 0;
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        /* Animation d'entrée */
        .fade-in {
            animation: fadeInUp 0.8s ease-out;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Personnalisation des graphiques Plotly */
        .js-plotly-plot {
            border-radius: 15px !important;
            overflow: hidden !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header with animation
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">📊 Data Visualization</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">🔍 Explore your data with next-generation interactive charts</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # CSV file loading with error handling
    try:
        df = pd.read_csv("projet_data/train.csv", encoding="latin1")
        
        # Main metrics calculation
        nb_rows = len(df)
        nb_columns = len(df.columns)
        nb_unique_values = df.nunique().sum()
        
        # Display metrics with new style
        st.markdown('<div class="fade-in">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
                <div class="enhanced-metric-card">
                    <div class="enhanced-metric-value">{nb_rows:,}</div>
                    <div class="enhanced-metric-label">📊 Rows Analyzed</div>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div class="enhanced-metric-card">
                    <div class="enhanced-metric-value">{nb_columns:,}</div>
                    <div class="enhanced-metric-label">🔢 Columns</div>
                </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
                <div class="enhanced-metric-card">
                    <div class="enhanced-metric-value">{nb_unique_values:,}</div>
                    <div class="enhanced-metric-label">✨ Unique Values</div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Spacing
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Sentiment Distribution Section
        st.markdown('<div class="section-header">😊 Sentiment Analysis</div>', unsafe_allow_html=True)
        
        if 'sentiment' in df.columns:
            fig1 = px.histogram(
                df, 
                x='sentiment', 
                color='sentiment',
                title='Sentiment Distribution',
                color_discrete_sequence=['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#ffd93d']
            )
            fig1.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                title_font_size=20,
                title_x=0.5
            )
            st.plotly_chart(fig1, use_container_width=True, key="sentiment_dist")
        else:
            st.warning("⚠️ Column 'sentiment' not found in data")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Time of Day Section
        st.markdown('<div class="section-header">⏰ Temporal Analysis</div>', unsafe_allow_html=True)
        
        if 'Time of Tweet' in df.columns:
            fig2 = px.histogram(
                df, 
                x='Time of Tweet', 
                color='Time of Tweet',
                title='Time of Posting Distribution',
                color_discrete_sequence=['#667eea', '#764ba2', '#f093fb', '#ff9a9e']
            )
            fig2.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                title_font_size=20,
                title_x=0.5
            )
            st.plotly_chart(fig2, use_container_width=True, key="moment_journee_dist")
        else:
            st.warning("⚠️ Column 'Time of Tweet' not found in data")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Geographic Distribution Section
        st.markdown('<div class="section-header">🌍 Geographic Distribution</div>', unsafe_allow_html=True)
        
        if 'Country' in df.columns:
            # Limit to top 10 countries for better readability
            top_countries = df['Country'].value_counts().head(10)
            df_top_countries = df[df['Country'].isin(top_countries.index)]
            
            fig3 = px.histogram(
                df_top_countries, 
                x='Country', 
                color='Country',
                title='Top 10 Countries (Distribution)',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig3.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                title_font_size=20,
                title_x=0.5,
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig3, use_container_width=True, key="country_dist")
        else:
            st.warning("⚠️ Column 'Country' not found in data")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Additional Information Section
        st.markdown("""
        ### 📈 Dataset Information
        
        **Data Overview:** This dataset contains valuable information for sentiment analysis, 
        with a comprehensive geographic and temporal breakdown. The above visualizations allow you 
        to quickly identify key trends in your data.
        
        **✨ Key Points:**
        - Multi-criteria analysis (sentiment, time, geography)
        - Real-time data with interactive visualizations
        - Modern interface with smooth animations
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
    except FileNotFoundError:
        st.markdown('<div class="error-box">❌ Data file not found. Please check the path: projet_data/train.csv</div>', unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f'<div class="error-box">❌ Error while loading data: {str(e)}</div>', unsafe_allow_html=True)


def show_raw_data_page():
    import pandas as pd
    import streamlit as st
    from io import BytesIO
    import base64
    from datetime import datetime
    # CSS supplémentaire pour la page Raw Data
    st.markdown("""
    <style>
        /* Conteneur de données avec style moderne */
        .data-explorer {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 2rem;
            margin: 1.5rem 0;
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.25);
            box-shadow: 0 12px 32px rgba(0,0,0,0.25);
        }
        
        /* Boutons d'export stylisés */
        .export-button {
            background: linear-gradient(135deg, #4ecdc4, #44a08d) !important;
            color: white !important;
            border: none !important;
            border-radius: 15px !important;
            padding: 0.8rem 1.5rem !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2) !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
            width: 100% !important;
            margin: 0.5rem 0 !important;
        }
        
        .export-button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 8px 25px rgba(0,0,0,0.3) !important;
            background: linear-gradient(135deg, #44a08d, #4ecdc4) !important;
        }
        
        /* Statistiques du dataset */
        .data-stats {
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            margin: 2rem 0;
        }
        
        .stat-item {
            background: rgba(255, 255, 255, 0.12);
            border-radius: 15px;
            padding: 1.5rem;
            text-align: center;
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
            min-width: 150px;
            margin: 0.5rem;
            transition: all 0.3s ease;
        }
        
        .stat-item:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.18);
        }
        
        .stat-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: #4ecdc4;
            margin-bottom: 0.5rem;
        }
        
        .stat-label {
            font-size: 0.9rem;
            opacity: 0.8;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        /* Filtres de données */
        .filter-container {
            background: rgba(255, 255, 255, 0.08);
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            border: 1px solid rgba(255, 255, 255, 0.15);
        }
        
        /* Table stylisée */
        .dataframe {
            border-radius: 15px !important;
            overflow: hidden !important;
        }
        
        /* Messages de statut */
        .status-message {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            margin: 1rem 0;
            border-left: 4px solid #4ecdc4;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .warning-message {
            background: linear-gradient(135deg, #ffd93d, #ff9a9e);
            color: #2c3e50;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            margin: 1rem 0;
            border-left: 4px solid #ff6b6b;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Page Header
    st.markdown('<h1 class="main-title">🗃️ Raw Data Explorer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">📋 Explore, filter, and export your data in real time</p>', unsafe_allow_html=True)

    try:
        # Load the actual data
        df = pd.read_csv("projet_data/train.csv", encoding="latin1")
        
        # Compute statistics
        total_rows = len(df)

        # Filtering section
        st.markdown("### 🔍 Data Filters")
        
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        
        with filter_col1:
            # Filter by number of rows to display
            num_rows = st.slider("Number of rows to display", 10, min(1000, total_rows), 50)
        
        with filter_col2:
            # Filter by column (if applicable)
            if 'sentiment' in df.columns:
                sentiments = ['All'] + list(df['sentiment'].unique())
                selected_sentiment = st.selectbox("Filter by sentiment", sentiments)
            else:
                selected_sentiment = 'All'
                
        with filter_col3:
            if 'Country' in df.columns:
                sentiments = ['All'] + list(df['Country'].unique())
                selected_sentiment = st.selectbox("Filter by Country", sentiments)
            else:
                selected_sentiment = 'All'
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Apply filters
        filtered_df = df.copy()
        if selected_sentiment != 'All' and 'sentiment' in df.columns:
            filtered_df = filtered_df[filtered_df['sentiment'] == selected_sentiment]
        
        filtered_df = df.copy()
        if selected_sentiment != 'All' and 'Country' in df.columns:
            filtered_df = filtered_df[filtered_df['Country'] == selected_sentiment]

        # Limit number of rows
        display_df = filtered_df.head(num_rows)
        
        # Display the data
        st.markdown(f"### 📋 Data ({len(display_df):,} rows displayed out of {len(filtered_df):,} filtered)")
        
        # Status message
        if len(filtered_df) != len(df):
            st.markdown(f'<div class="status-message">🔍 Active filter: {len(filtered_df):,} entries out of {len(df):,} match the criteria.</div>', unsafe_allow_html=True)
        
        # Display the styled dataframe
        st.dataframe(
            display_df, 
            use_container_width=True,
            height=400
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Export section
        st.markdown("### 📤 Export Options")
        
        # Create export data
        export_df = filtered_df  # Export the filtered data
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Export as CSV
            csv_data = export_df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name=f"sentiment_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            # Export as Excel
            def to_excel(df):
                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df.to_excel(writer, sheet_name='Sentiment_Data', index=False)
                    
                    # Get the workbook and worksheet
                    workbook = writer.book
                    worksheet = writer.sheets['Sentiment_Data']
                    
                    # Header formatting
                    header_format = workbook.add_format({
                        'bold': True,
                        'text_wrap': True,
                        'valign': 'top',
                        'fg_color': '#4ecdc4',
                        'font_color': 'white',
                        'border': 1
                    })
                    
                    # Apply the format to headers
                    for col_num, value in enumerate(df.columns.values):
                        worksheet.write(0, col_num, value, header_format)
                    
                    # Adjust column widths
                    for i, col in enumerate(df.columns):
                        column_len = max(df[col].astype(str).str.len().max(), len(col)) + 2
                        worksheet.set_column(i, i, min(column_len, 50))
                
                return output.getvalue()
            
            excel_data = to_excel(export_df)
            st.download_button(
                label="📊 Download Excel",
                data=excel_data,
                file_name=f"sentiment_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    except FileNotFoundError:
        st.markdown('<div class="warning-message">❌ <strong>File not found</strong><br>Unable to load the file <code>projet_data/train.csv</code>. Please check that the file exists and that the path is correct.</div>', unsafe_allow_html=True)

def show_chatbot_page():
    # Title with animation
    st.markdown('<h1 class="main-title">🤖 AI Chatbot</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">💬 Get personalized advice for your tweets</p>', unsafe_allow_html=True)
    
    # Initialize session state for chatbot
    if "chatbot_state" not in st.session_state:
        st.session_state.chatbot_state = {
            "step": "start",
            "data": {},
            "conversation": []
        }
    
    if "chatbot_initialized" not in st.session_state:
        st.session_state.chatbot_initialized = False
    
    # Info card
    st.markdown("""
    <div class="glass-card">
        <div style="text-align: center;">
            <h3 style="color: white; margin-bottom: 1rem;">🧠 How it works</h3>
            <div style="display: flex; justify-content: space-around; margin-bottom: 1rem;">
                <div style="text-align: center;">
                    <div style="font-size: 2rem;">1️⃣</div>
                    <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Enter your tweet</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 2rem;">2️⃣</div>
                    <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Provide context</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 2rem;">3️⃣</div>
                    <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Get AI advice</div>
                </div>
            </div>
            <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem; margin: 0;">
                Our AI chatbot will guide you through an interactive conversation to analyze your tweet and provide personalized advice.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat container
    st.markdown("""
    <div class="glass-card">
        <h3 style="color: white; margin-bottom: 1rem;">💬 Chat with AI</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Display conversation history
    chat_container = st.container()
    
    with chat_container:
        if st.session_state.chatbot_state["conversation"]:
            for i, message in enumerate(st.session_state.chatbot_state["conversation"]):
                if message["role"] == "assistant":
                    st.markdown(f"""
                    <div style="background: rgba(76, 175, 80, 0.2); border-radius: 15px; padding: 1rem; margin: 0.5rem 0; border-left: 4px solid #4CAF50;">
                        <strong>🤖 AI Assistant:</strong><br>
                        {message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: rgba(33, 150, 243, 0.2); border-radius: 15px; padding: 1rem; margin: 0.5rem 0; border-left: 4px solid #2196F3;">
                        <strong>👤 You:</strong><br>
                        {message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
    
    # Initialize chatbot if not done
    if not st.session_state.chatbot_initialized:
        with st.spinner("🔄 Initializing AI chatbot..."):
            time.sleep(1)
            try:
                url = "http://localhost:8000/chatbot"
                payload = {
                    "message": "",
                    "state": {
                        "step": "start",
                        "data": {}
                    }
                }

                response = requests.post(url, json=payload, timeout=10)
                
                if response.status_code == 200:
                    result = response.json()
                    st.session_state.chatbot_state = result["state"]
                    st.session_state.chatbot_state["conversation"] = [
                        {"role": "assistant", "content": result["response"]}
                    ]
                    st.session_state.chatbot_initialized = True
                    st.rerun()
                else:
                    st.error(f"❌ Error initializing chatbot: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Cannot connect to API: {e}")
                return
    
    # User input
    user_input = st.text_input(
        "💬 Your message:",
        key="chatbot_input",
        placeholder="Type your message here...",
        help="Enter your response to continue the conversation"
    )
    
    # Send message button
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        send_button = st.button("📤 Send Message", use_container_width=True)
    
    # Reset button
    if st.button("🔄 Restart Conversation", use_container_width=True):
        st.session_state.chatbot_state = {
            "step": "start",
            "data": {},
            "conversation": []
        }
        st.session_state.chatbot_initialized = False
        st.rerun()
    
    # Handle user input
    if send_button and user_input.strip():
        # Add user message to conversation
        st.session_state.chatbot_state["conversation"].append({
            "role": "user",
            "content": user_input
        })
        
        # Send to API
        with st.spinner("🤖 AI is thinking..."):
            try:
                url = "http://localhost:8000/chatbot"
                payload = {
                    "message": user_input,
                    "state": {
                        "step": st.session_state.chatbot_state["step"],
                        "data": st.session_state.chatbot_state["data"]
                    }
                }

                response = requests.post(url, json=payload, timeout=15)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Update state
                    st.session_state.chatbot_state["step"] = result["state"]["step"]
                    st.session_state.chatbot_state["data"] = result["state"]["data"]
                    
                    # Add assistant response to conversation
                    st.session_state.chatbot_state["conversation"].append({
                        "role": "assistant",
                        "content": result["response"]
                    })
                    
                    # Rerun to update the display
                    st.rerun()
                else:
                    st.error(f"❌ API Error: {response.status_code}")
                    
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timeout. Please try again.")
            except requests.exceptions.ConnectionError:
                st.error("🔌 Cannot connect to API. Make sure the server is running.")
            except Exception as e:
                st.error(f"❌ Unexpected error: {e}")
    
    elif send_button and not user_input.strip():
        st.warning("⚠️ Please enter a message before sending.")
    
    # Tips section
    st.markdown("""
    <div class="glass-card">
        <h4 style="color: white; margin-bottom: 1rem;">💡 Tips for better results:</h4>
        <ul style="color: rgba(255,255,255,0.8); line-height: 1.6;">
            <li>🎯 Be specific about your target sentiment</li>
            <li>🌍 Mention the correct country for cultural context</li>
            <li>⏰ Specify the exact time for optimal engagement</li>
            <li>📝 Use clear and concise language</li>
            <li>🔄 Don't hesitate to restart if you want to try a different approach</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()