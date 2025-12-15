"""
Emotion Companion - Premium UI with Glassmorphism Design
A beautiful, production-ready emotional wellness companion.
"""

import streamlit as st
import requests
import json
from uuid import uuid4
import plotly.graph_objects as go
from pathlib import Path
import sys
import os

# Add project root to path to allow imports from backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import wellness integration (sibling import)
from wellness_integration import render_wellness_toolkit

# ============================================================================
# Configuration
# ============================================================================

API_BASE_URL = "http://localhost:8000/api"

st.set_page_config(
    page_title="Emotion Companion",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load custom CSS directly to avoid caching issues
st.markdown("""
    <style>
    /* Emotion Companion - Balanced Premium Design */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap');

    :root {
        /* Palette */
        --color-bg: #151520; /* Deep Charcoal/Slate - No more Blue */
        --color-card-bg: rgba(255, 255, 255, 0.05); /* White Glass */
        --color-accent-orange: #FF6500;
        --color-accent-yellow: #FFD500;
        --color-text-main: #ffffff;
        --color-text-muted: #E0E0E0; /* Neutral Light Grey */
        
        /* Gradients */
        --header-gradient: linear-gradient(135deg, #FF6500 0%, #FFD500 100%); /* Orange to Yellow */
        --card-border: rgba(255, 255, 255, 0.1);
    }

    * { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background: var(--color-bg);
        background-image: 
            radial-gradient(circle at 10% 20%, rgba(255, 101, 0, 0.1) 0%, transparent 40%),
            radial-gradient(circle at 90% 80%, rgba(140, 50, 255, 0.1) 0%, transparent 40%); /* Subtle Purple Glow */
    }

    #MainMenu, footer, header { visibility: hidden; }

    /* Header with Warm Gradient */
    .custom-header {
        background: rgba(255, 255, 255, 0.05);
        border-left: 8px solid var(--color-accent-orange);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
    }
    .custom-header h1 { 
        font-family: 'Outfit', sans-serif; 
        font-weight: 800; 
        font-size: 3.5rem; 
        background: var(--header-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0; 
        text-shadow: none;
    }
    .custom-header p { color: var(--color-text-muted); font-size: 1.2rem; margin-top: 0.5rem; }

    /* Glass Cards - Neutral to break up blue */
    .glass-card {
        background: var(--color-card-bg);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid var(--card-border);
        padding: 2rem;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    .glass-card:hover { 
        transform: translateY(-5px); 
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3); 
        border-color: var(--color-accent-yellow); 
    }

    /* Input Areas */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid transparent !important;
        border-radius: 15px !important;
        color: #002a54 !important;
        font-size: 1.05rem !important;
        padding: 1.5rem !important;
        font-weight: 500 !important;
    }
    .stTextArea textarea:focus { 
        border-color: var(--color-accent-orange) !important; 
        box-shadow: 0 0 20px rgba(255, 101, 0, 0.2) !important; 
        background: white !important; 
    }

    /* Buttons - Pop with Orange */
    .stButton>button {
        background: var(--header-gradient) !important;
        color: #002a54 !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 1rem 3rem !important;
        font-size: 1.1rem !important;
        font-weight: 800 !important;
        box-shadow: 0 8px 20px rgba(255, 101, 0, 0.3) !important;
        font-family: 'Outfit', sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton>button:hover { 
        transform: translateY(-3px); 
        box-shadow: 0 12px 30px rgba(255, 213, 0, 0.5) !important; 
        color: #000 !important;
    }

    /* Result Cards */
    .result-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        border: 1px solid var(--card-border);
        padding: 1.5rem;
        margin: 1rem 0;
    }

    /* Emotion Badge */
    .emotion-badge {
        display: inline-flex; align-items: center; gap: 0.5rem;
        background: linear-gradient(135deg, #FF6500 0%, #FF4500 100%); 
        padding: 0.75rem 1.5rem;
        border-radius: 50px; font-weight: 700; font-size: 1.2rem;
        box-shadow: 0 4px 16px rgba(255, 69, 0, 0.4); color: white;
    }

    /* Suggestion Cards */
    .suggestion-card {
        background: rgba(255, 255, 255, 0.05);
        border-left: 5px solid var(--color-accent-yellow); 
        padding: 1rem 1.5rem; margin: 0.75rem 0;
        border-radius: 10px; color: white; line-height: 1.6;
    }
    .suggestion-card:hover { 
        background: rgba(255, 255, 255, 0.1); 
        border-left-color: var(--color-accent-orange); 
    }
    .suggestion-card strong { color: var(--color-accent-yellow); font-weight: 700; }

    /* Metrics */
    .stMetric { 
        background: rgba(255, 255, 255, 0.05); 
        border-radius: 15px; 
        border: 1px solid var(--card-border); 
        padding: 1.5rem !important; 
    }
    .stMetric label { color: var(--color-text-muted) !important; }
    .stMetric [data-testid="stMetricValue"] { color: var(--color-accent-yellow) !important; font-family: 'Outfit', sans-serif !important; }

    /* Tabs - High Visibility */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: transparent; }
    .stTabs [data-baseweb="tab"] {
        height: 50px; white-space: pre-wrap; background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px 10px 0 0; gap: 1px; padding: 10px;
        color: var(--color-text-muted); border: 1px solid transparent; transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab"]:hover { background-color: rgba(255, 255, 255, 0.1); color: white; }
    .stTabs [aria-selected="true"] { 
        background-color: var(--color-accent-orange) !important; 
        color: white !important; 
        font-weight: bold; 
        box-shadow: 0 -4px 10px rgba(255, 101, 0, 0.2);
    }

    /* Expanders - Distinct & Visible */
    [data-testid="stExpander"] { background-color: transparent !important; border: none !important; margin-bottom: 1rem !important; }
    [data-testid="stExpander"] details { 
        background-color: rgba(255, 255, 255, 0.03) !important; 
        border-radius: 10px !important; 
        border: 1px solid var(--card-border) !important; 
    }
    [data-testid="stExpander"] summary {
        color: white !important; font-family: 'Outfit', sans-serif !important; font-size: 1.1rem !important;
        background-color: rgba(255, 255, 255, 0.08) !important; 
        border-radius: 10px !important; padding: 1rem !important;
        border: 1px solid transparent;
    }
    [data-testid="stExpander"] summary:hover { 
        color: var(--color-accent-yellow) !important; 
        background-color: rgba(255, 255, 255, 0.12) !important; 
        border-color: var(--color-accent-yellow);
    }
    [data-testid="stExpander"] summary svg { fill: white !important; }
    [data-testid="stExpander"] [data-testid="stMarkdownContainer"] p { color: rgba(255, 255, 255, 0.9) !important; }
    
    /* Theme Tags - Pills */
    .theme-tag {
        display: inline-block;
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 50px;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        color: white;
        font-size: 0.95rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .theme-tag:hover {
        background: rgba(255, 255, 255, 0.2);
        border-color: var(--color-accent-yellow);
        color: var(--color-accent-yellow);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }

    /* Plotly Fix */
    .js-plotly-plot .plotly .main-svg { background: transparent !important; }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# Session State
# ============================================================================

# Import Auth
from backend.supabase_client import get_supabase

# Initialize Auth Client
# We use the existing supabase client which already has auth configured
supabase = get_supabase()

# ============================================================================
# Session State
# ============================================================================

if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid4())
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "auth_token" not in st.session_state:
    st.session_state.auth_token = None
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "show_results" not in st.session_state:
    st.session_state.show_results = False

# ============================================================================
# Authentication Gate (Main Page) - Figma Template Design
# ============================================================================

# If user is not authenticated, show login/signup page
if not st.session_state.auth_token:
    # Hide Streamlit default elements for auth page
    st.markdown("""
        <style>
        /* Hide Streamlit branding and padding for auth page */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }
        
        /* Full-screen split layout */
        .auth-wrapper {
            display: flex;
            min-height: 100vh;
            width: 100%;
        }
        
        /* Left Panel - Branding */
        .auth-left {
            flex: 1;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 3rem;
            position: relative;
            overflow: hidden;
        }
        
        .auth-left::before {
            content: '';
            position: absolute;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
            background-size: 50px 50px;
            animation: drift 20s linear infinite;
        }
        
        @keyframes drift {
            from { transform: translate(0, 0); }
            to { transform: translate(50px, 50px); }
        }
        
        .brand-content {
            position: relative;
            z-index: 1;
            text-align: center;
            color: white;
        }
        
        .brand-logo {
            font-size: 5rem;
            margin-bottom: 1.5rem;
            animation: float 3s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
        }
        
        .brand-title {
            font-family: 'Outfit', sans-serif;
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 1rem;
            text-shadow: 0 4px 20px rgba(0,0,0,0.2);
        }
        
        .brand-tagline {
            font-size: 1.3rem;
            font-weight: 300;
            opacity: 0.95;
        }
        
        /* Right Panel - Auth Form */
        .auth-right {
            flex: 1;
            background: #f8f9fa;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 3rem;
        }
        
        /* Auth Card */
        .auth-card {
            background: white;
            border-radius: 20px;
            padding: 3rem 2.5rem;
            box-shadow: 0 10px 40px rgba(0,0,0,0.08);
            max-width: 420px;
            width: 100%;
        }
        
        .auth-card-title {
            font-family: 'Outfit', sans-serif;
            font-size: 1.8rem;
            font-weight: 700;
            color: #1a1a2e;
            margin-bottom: 0.5rem;
            text-align: center;
        }
        
        .auth-card-subtitle {
            font-size: 0.95rem;
            color: #6c757d;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        /* Input Styling */
        .stTextInput > div > div > input {
            background: #f8f9fa !important;
            border: 2px solid #e9ecef !important;
            border-radius: 10px !important;
            padding: 0.9rem 1rem !important;
            font-size: 0.95rem !important;
            color: #1a1a2e !important;
            transition: all 0.3s ease !important;
        }
        
        .stTextInput > div > div > input:focus {
            background: white !important;
            border-color: #667eea !important;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        }
        
        .stTextInput > label {
            color: #1a1a2e !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        /* Radio Buttons */
        .stRadio > div {
            justify-content: center;
            gap: 0.5rem;
            margin-bottom: 2rem;
        }
        
        .stRadio > div > label {
            background: #f8f9fa;
            padding: 0.6rem 1.8rem;
            border-radius: 10px;
            color: #6c757d;
            border: 2px solid #e9ecef;
            transition: all 0.3s ease;
            font-weight: 600;
            cursor: pointer;
        }
        
        .stRadio > div > label:has(input:checked) {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-color: #667eea;
        }
        
        .stRadio > div > label > div:first-child {
            display: none;
        }
        
        /* Button Styling */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.9rem 2rem !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
        }
        
        /* Helper Text */
        .helper-text {
            text-align: center;
            margin-top: 1.5rem;
            color: #6c757d;
            font-size: 0.9rem;
        }
        
        .helper-text a {
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Create two-column layout
    left_col, right_col = st.columns([1, 1], gap="small")
    
    with left_col:
        st.markdown("""
            <div class="auth-left">
                <div class="brand-content">
                    <div class="brand-logo">🌟</div>
                    <h1 class="brand-title">Emotion<br/>Companion</h1>
                    <p class="brand-tagline">Start your journey to<br/>emotional wellness</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with right_col:
        st.markdown('<div class="auth-right">', unsafe_allow_html=True)
        
        # Auth mode selector
        auth_mode = st.radio(
            "mode",
            ["Login", "Sign Up"],
            horizontal=True,
            label_visibility="collapsed",
            key="auth_mode_select"
        )
        
        # Card title based on mode
        if auth_mode == "Login":
            st.markdown("""
                <div class="auth-card-title">Welcome Back!</div>
                <div class="auth-card-subtitle">Login to your account</div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="auth-card-title">Create Account</div>
                <div class="auth-card-subtitle">Start your wellness journey</div>
            """, unsafe_allow_html=True)
        
        # Form fields
        email = st.text_input(
            "Email",
            placeholder="your@email.com",
            key="email_input"
        )
        
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="password_input"
        )
        
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        
        # Submit button
        if auth_mode == "Login":
            if st.button("🚀 Log In", type="primary", use_container_width=True, key="login_submit"):
                if not email or not password:
                    st.error("⚠️ Please enter both email and password")
                else:
                    try:
                        with st.spinner("Authenticating..."):
                            response = supabase.auth.sign_in_with_password({"email": email, "password": password})
                            if response and response.user:
                                st.session_state.auth_token = response.session.access_token
                                st.session_state.user_email = response.user.email
                                st.session_state.user_id = response.user.id
                                st.success("✅ Welcome back!")
                                st.rerun()
                    except Exception as e:
                        st.error(f"❌ Login failed: {str(e)}")
            
            st.markdown('<div class="helper-text">Don\'t have an account? <a href="#" onclick="return false;">Sign Up</a></div>', unsafe_allow_html=True)
        
        else:  # Sign Up
            if st.button("✨ Create Account", type="primary", use_container_width=True, key="signup_submit"):
                if not email or not password:
                    st.error("⚠️ Please enter both email and password")
                elif len(password) < 6:
                    st.error("⚠️ Password must be at least 6 characters")
                else:
                    try:
                        with st.spinner("Creating your account..."):
                            response = supabase.auth.sign_up({"email": email, "password": password})
                            if response and response.user:
                                st.success("✅ Account created! Please log in.")
                                st.balloons()
                    except Exception as e:
                        st.error(f"❌ Signup failed: {str(e)}")
            
            st.markdown('<div class="helper-text">Already have an account? <a href="#" onclick="return false;">Log In</a></div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Stop execution - don't show main app
    st.stop()

# ============================================================================
# Authenticated User - Show Logout in Sidebar
# ============================================================================

with st.sidebar:
    st.markdown("### 👤 Account")
    st.success(f"Logged in as:\n{st.session_state.user_email}")
    if st.button("🚪 Log Out", use_container_width=True):
        st.session_state.user_id = str(uuid4())
        st.session_state.user_email = None
        st.session_state.auth_token = None
        st.session_state.analysis_result = None
        st.session_state.show_results = False
        try:
            supabase.auth.sign_out()
        except:
            pass
        st.rerun()
    st.markdown("---")

# ============================================================================
# Helper Functions
# ============================================================================

def call_api(endpoint: str, method: str = "GET", data: dict = None):
    """Make API request to backend."""
    url = f"{API_BASE_URL}/{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=30)
        
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot connect to backend API. Make sure it's running on port 8000.")
        return None
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out. The analysis is taking longer than expected.")
        return None
    except Exception as e:
        st.error(f"❌ Error: {e}")
        return None


def create_mood_gauge(mood_score: int):
    """Create an animated mood gauge visualization."""
    # Calculate percentage
    percentage = (mood_score / 10) * 100
    
    # Determine color based on mood
    if mood_score <= 3:
        color = "#f5576c"
    elif mood_score <= 5:
        color = "#f093fb"
    elif mood_score <= 7:
        color = "#4facfe"
    else:
        color = "#00f2fe"
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = mood_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Mood Score", 'font': {'size': 24, 'color': 'white', 'family': "Outfit"}},
        number = {'font': {'size': 60, 'color': 'white', 'family': "Outfit"}},
        gauge = {
            'axis': {'range': [None, 10], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': color},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "rgba(255, 255, 255, 0.3)",
            'steps': [
                {'range': [0, 3], 'color': 'rgba(245, 87, 108, 0.3)'},
                {'range': [3, 5], 'color': 'rgba(240, 147, 251, 0.3)'},
                {'range': [5, 7], 'color': 'rgba(79, 172, 254, 0.3)'},
                {'range': [7, 10], 'color': 'rgba(0, 242, 254, 0.3)'}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': mood_score
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "white", 'family': "Inter"},
        height=250,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig


def create_emotion_radar(emotion_scores: dict):
    """Create a radar chart for emotion scores."""
    emotions = list(emotion_scores.keys())
    scores = list(emotion_scores.values())
    
    fig = go.Figure(data=go.Scatterpolar(
        r=scores,
        theta=emotions,
        fill='toself',
        fillcolor='rgba(102, 126, 234, 0.3)',
        line=dict(color='#667eea', width=2)
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                gridcolor='rgba(255, 255, 255, 0.2)',
                tickfont=dict(color='white')
            ),
            angularaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.2)',
                tickfont=dict(color='white', size=12)
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "white", 'family': "Inter"},
        height=350,
        margin=dict(l=80, r=80, t=40, b=40)
    )
    
    return fig


def display_results(result: dict):
    """Display analysis results with beautiful UI."""
    if not result or "analysis" not in result:
        return
    
    analysis = result["analysis"]
    
    # Main Grid Layout (2 Columns)
    c1, c2 = st.columns([1, 1], gap="medium")
    
    with c1:
        # --- LEFT COLUMN: Analysis & Breakdown ---
        
        # 1. Emotional Analysis Header & Metrics Card
        st.markdown("""
            <div class="glass-card" style="margin-bottom: 1rem; text-align: center; padding: 1rem;">
                <h3 style="color: white; font-family: 'Outfit', sans-serif; margin: 0; font-size: 1.3rem;">
                    ✨ Your Emotional Analysis
                </h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Metrics Card (Emoji + Gauge)
        m_col1, m_col2 = st.columns([1, 1.2]) 
        with m_col1:
             emotion = analysis.get("emotion", {})
             emoji = emotion.get("emoji", "😐")
             primary_emotion = emotion.get("primary_emotion", "neutral").title()
             sentiment = analysis.get("sentiment", {}).get("label", "NEUTRAL")
             sent_conf = analysis.get("sentiment", {}).get("score", 0)
             
             if sentiment == "POSITIVE": s_color = "#00f2fe"
             elif sentiment == "NEGATIVE": s_color = "#f5576c"
             else: s_color = "#f093fb"

             st.markdown(f"""
                <div class="glass-card" style="text-align: center; padding: 1.5rem; height: 100%; display: flex; flex-direction: column; justify-content: center;">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">{emoji}</div>
                    <div class="emotion-badge" style="margin-bottom: 0.5rem;">{primary_emotion}</div>
                    <small style="color:{s_color}; font-weight:bold;">{sentiment}</small>
                </div>
             """, unsafe_allow_html=True)
        
        with m_col2:
             mood_score = analysis.get("mood_score", 5)
             # Custom HTML Title for Gauge
             st.markdown("""
                <div style="text-align: center; margin-bottom: -10px;">
                    <h4 style="color: white; font-family: 'Outfit', sans-serif; margin: 0;">Mood Score</h4>
                </div>
             """, unsafe_allow_html=True)
             fig_gauge = create_mood_gauge(mood_score)
             # Remove title from chart, maximize size
             fig_gauge.update_layout(title=None, margin=dict(l=20, r=20, t=20, b=20), height=180)
             st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})

        # 2. Emotion Breakdown Header & Chart
        st.markdown("""
            <div class="glass-card" style="margin-top: 1.5rem; margin-bottom: 1rem; text-align: center; padding: 1rem;">
                <h3 style="color: white; font-family: 'Outfit', sans-serif; margin: 0; font-size: 1.3rem;">
                    🎭 Emotion Breakdown
                </h3>
            </div>
        """, unsafe_allow_html=True)
        
        emotion_scores = emotion.get("emotion_scores", {})
        if emotion_scores:
            fig_radar = create_emotion_radar(emotion_scores)
            fig_radar.update_layout(height=280, margin=dict(l=40, r=40, t=10, b=20))
            st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False})

    with c2:
        # --- RIGHT COLUMN: Themes & Suggestions ---
        
        # 3. Key Themes
        themes = analysis.get("themes", [])
        if themes:
            st.markdown("""
                <div class="glass-card" style="margin-bottom: 1rem; text-align: center; padding: 1rem;">
                    <h3 style="color: white; font-family: 'Outfit', sans-serif; margin: 0; font-size: 1.3rem;">
                        🏷️ Key Themes
                    </h3>
                </div>
            """, unsafe_allow_html=True)
            
            themes_html = " ".join([f'<span class="theme-tag" style="margin: 0.3rem; display:inline-block;">{theme}</span>' for theme in themes[:6]])
            st.markdown(f"""
                <div class="glass-card" style="padding: 1.5rem; text-align: center; min-height: 120px; display: flex; align-items: center; justify-content: center; flex-wrap: wrap;">
                    {themes_html}
                </div>
            """, unsafe_allow_html=True)

        # 4. Personalized Suggestions
        suggestions = analysis.get("suggestions", [])
        if suggestions:
            st.markdown("""
                <div class="glass-card" style="margin-top: 1.5rem; margin-bottom: 1rem; text-align: center; padding: 1rem;">
                    <h3 style="color: white; font-family: 'Outfit', sans-serif; margin: 0; font-size: 1.3rem;">
                        💡 Personalized Suggestions
                    </h3>
                </div>
            """, unsafe_allow_html=True)
            
            for i, suggestion in enumerate(suggestions, 1):
                st.markdown(f"""
                    <div class="suggestion-card" style="animation: fadeInUp {0.5 + i*0.1}s ease; padding: 1rem; margin-bottom: 0.8rem;">
                        <strong style="color: #FFD500; font-size: 1rem; margin-right: 0.5rem;">{i}.</strong> 
                        <span style="color: rgba(255, 255, 255, 0.9);">
                            {suggestion}
                        </span>
                    </div>
                """, unsafe_allow_html=True)
    
    # Wellness Toolkit Integration
    render_wellness_toolkit(analysis)
    
    # Note
    st.success("✅ Analysis complete! Entry saved to your private journal history.")


# ============================================================================
# Main UI
# ============================================================================

# Custom Header
st.markdown("""
    <div class="custom-header" style="text-align: center;">
        <h1>🌟 Emotion Companion</h1>
        <p>Your AI-powered emotional wellness companion</p>
    </div>
""", unsafe_allow_html=True)

# Main content
# User wants input to be the main focus first, taking up square center

st.markdown("""
    <div class="glass-card" style="max-width: 800px; margin: 0 auto; text-align: center;">
        <h2 style="color: white; font-family: 'Outfit', sans-serif; margin-bottom: 0.5rem;">
            📝 Write Your Journal Entry
        </h2>
        <p style="color: rgba(255, 255, 255, 0.8); margin-bottom: 0; font-size: 0.95rem; line-height: 1.5;">
            Express your thoughts and feelings freely. Our AI will help you understand your emotions better.
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

# Input container centered with restricted width
c_spacer1, c_main, c_spacer2 = st.columns([1, 2, 1])
with c_main:
    # Input Method Tabs
    tab_write, tab_voice = st.tabs(["✍️ Write Journal", "🎤 Voice Journal"])
    
    with tab_write:
        journal_text = st.text_area(
            "How are you feeling today?",
            height=300, # Increased height to make it more square
            placeholder="Write about your feelings, thoughts, or experiences...",
            label_visibility="collapsed"
        )
        
        # Button Row
        b_col1, b_col2 = st.columns([3, 1])
        with b_col1:
            analyze_button = st.button("✨ Analyze Text", use_container_width=True, type="primary")
        with b_col2:
            clear_button = st.button("🔄 Clear", use_container_width=True)
            
        if clear_button:
            st.session_state.show_results = False
            st.session_state.analysis_result = None
            st.rerun()
            
    with tab_voice:
        st.markdown("""
            <div class="glass-card" style="text-align: center; padding: 2rem;">
                <p style="color: rgba(255,255,255,0.8); margin-bottom: 1rem;">
                    Record your thoughts. We'll transcribe and analyze them for you.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        audio_value = st.audio_input("Record a voice note")
        
        if audio_value:
            st.audio(audio_value)
            process_audio = st.button("✨ Transcribe & Analyze Audio", use_container_width=True, type="primary")
            
            if process_audio:
                with st.spinner("🎧 Uploading and processing audio..."):
                    # Create form data for upload
                    files = {"file": ("voice_note.wav", audio_value, "audio/wav")}
                    data = {"user_id": st.session_state.user_id}
                    
                    # Direct request since call_api helper handles JSON, not multipart
                    try:
                        url = f"{API_BASE_URL}/audio/upload"
                        response = requests.post(url, data=data, files=files, timeout=60)
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.session_state.analysis_result = result
                            st.session_state.show_results = True
                            st.rerun()
                        else:
                            st.error(f"❌ Error: {response.text}")
                            
                    except Exception as e:
                        st.error(f"❌ Connection Error: {e}")
    # Old button code removed
    pass

# Analysis Logic
if analyze_button and journal_text:
    if len(journal_text) < 10:
        st.warning("⚠️ Please write at least 10 characters for meaningful analysis.")
    else:
        with st.spinner("🔮 Analyzing your emotions..."):
            data = {
                "user_id": st.session_state.user_id,
                "text": journal_text
            }
            result = call_api("journal/", method="POST", data=data)
            
            if result:
                st.session_state.analysis_result = result
                st.session_state.show_results = True
                st.rerun()

# Display Results Section
if st.session_state.show_results and st.session_state.analysis_result:
    display_results(st.session_state.analysis_result)
else:
    # Optional: Placeholder or just empty until analysis
    pass

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style="text-align: center; color: rgba(255, 255, 255, 0.5); padding: 2rem 0;">
        <p>Made with ❤️ for your emotional wellbeing</p>
        <p style="font-size: 0.8rem;">If you're in crisis, please contact a mental health professional or crisis helpline</p>
    </div>
""", unsafe_allow_html=True)
