"""
Integration module for wellness features to keep the main app file clean.
"""

import streamlit as st
import importlib
import backend.wellness_content
importlib.reload(backend.wellness_content)

from backend.wellness_content import (
    get_random_quote, get_book_recommendations, 
    get_inspirational_story, CRISIS_RESOURCES
)
from components.breathing_exercise import (
    render_breathing_exercise, render_quick_grounding
)
from components.motivational_content import (
    render_quote_card, render_book_recommendations,
    render_inspirational_story, render_crisis_resources
)

def render_wellness_toolkit(analysis: dict):
    """Render the complete wellness toolkit section."""
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <div class="result-card">
            <h2 style="color: white; font-family: 'Outfit', sans-serif; margin-bottom: 0.5rem;">
                🌟 Your Wellness Toolkit
            </h2>
            <p style="color: rgba(255, 255, 255, 0.8); margin-bottom: 0;">
                Interactive tools and resources to help you feel better right now
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Get emotion for personalized content
    primary_emotion = analysis.get("emotion", {}).get("primary_emotion", "neutral")
    
    # Initialize session state for active tab if not present
    if "active_wellness_tab" not in st.session_state:
        st.session_state.active_wellness_tab = "Motivation"

    # Custom styling for the navigation buttons to look like tabs/pills
    st.markdown("""
        <style>
        /* General Button Style */
        div.stButton > button {
            width: 100%;
            border-radius: 12px;
            height: 3rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        /* Secondary Button (Inactive) - Dimmed */
        div.stButton > button [kind="secondary"] {
            border: 1px solid rgba(255,255,255,0.05) !important;
            background-color: rgba(255,255,255,0.02) !important;
            color: rgba(255, 255, 255, 0.4) !important; /* Dim text */
        }
        
        /* Secondary Hover - Slightly brighter */
        div.stButton > button:hover {
            border-color: rgba(255, 213, 0, 0.5) !important;
            color: rgba(255, 213, 0, 0.8) !important;
            background-color: rgba(255,255,255,0.05) !important;
        }

        /* Primary Button (Active) - Bright & Highlighted */
        div.stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #FFD500 0%, #FFA500 100%) !important;
            color: black !important;
            border: none !important;
            box-shadow: 0 4px 15px rgba(255, 213, 0, 0.3) !important;
            font-weight: 700 !important;
            opacity: 1 !important;
        }
        
        /* Force inactive buttons to look dim specifically targeting standard st-emotion-cache classes if needed, 
           but generally standard button selectors work best in Streamlit */
        button[kind="secondary"] {
            opacity: 0.5;
        }
        button[kind="secondary"]:hover {
            opacity: 0.8;
        }
        </style>
    """, unsafe_allow_html=True)

    # Navigation Grid (Single Row of 5)
    cols = st.columns(5)
    
    with cols[0]:
        if st.button("🌬️ Breathing", type="primary" if st.session_state.active_wellness_tab == "Breathing" else "secondary", use_container_width=True, key="btn_breathing"):
            st.session_state.active_wellness_tab = "Breathing"
    with cols[1]:
        if st.button("💭 Motivation", type="primary" if st.session_state.active_wellness_tab == "Motivation" else "secondary", use_container_width=True, key="btn_motivation"):
            st.session_state.active_wellness_tab = "Motivation"
    with cols[2]:
        if st.button("📚 Reading", type="primary" if st.session_state.active_wellness_tab == "Reading" else "secondary", use_container_width=True, key="btn_reading"):
            st.session_state.active_wellness_tab = "Reading"
    with cols[3]:
        if st.button("🎯 Activities", type="primary" if st.session_state.active_wellness_tab == "Activities" else "secondary", use_container_width=True, key="btn_activities"):
            st.session_state.active_wellness_tab = "Activities"
    with cols[4]:
        if st.button("🆘 Crisis", type="primary" if st.session_state.active_wellness_tab == "Crisis" else "secondary", use_container_width=True, key="btn_crisis"):
            st.session_state.active_wellness_tab = "Crisis"
            
    st.markdown("<hr style='margin: 1rem 0; border: 0; border-top: 1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    
    # Content Rendering based on active tab
    if st.session_state.active_wellness_tab == "Breathing":
        render_breathing_exercise()
    
    elif st.session_state.active_wellness_tab == "Motivation":
        # Persist quote in session state
        quote_key = f"quote_{primary_emotion}"
        if quote_key not in st.session_state:
            st.session_state[quote_key] = get_random_quote(primary_emotion)
            
        render_quote_card(st.session_state[quote_key], primary_emotion)
        
        story = get_inspirational_story(primary_emotion)
        if story:
            st.markdown("<br>", unsafe_allow_html=True)
            render_inspirational_story(story)
            
    elif st.session_state.active_wellness_tab == "Reading":
        books = get_book_recommendations(primary_emotion, limit=4)
        render_book_recommendations(books)
        
    elif st.session_state.active_wellness_tab == "Activities":
        render_quick_grounding()
        
        # Center the activities section
        s1, c_main, s2 = st.columns([1, 5, 1]) # 5/7 width
        
        with c_main:
            st.markdown("""
                <h3 style="color: white; font-family: 'Outfit', sans-serif; margin: 2rem 0 1rem 0; padding-left: 0.5rem; border-left: 4px solid #FFD500;">
                    🧘 More Guided Activities
                </h3>
            """, unsafe_allow_html=True)
            
            activity_col1, activity_col2 = st.columns(2)
            
            with activity_col1:
                with st.expander("📝 Gratitude Journaling"):
                    st.markdown("""
                        <p style="color: rgba(255, 255, 255, 0.9); line-height: 1.6;">
                            Write down 3 things you're grateful for today:
                        </p>
                    """, unsafe_allow_html=True)
                    g1 = st.text_area("Thing 1:", key="gratitude_1", height=60)
                    g2 = st.text_area("Thing 2:", key="gratitude_2", height=60)
                    g3 = st.text_area("Thing 3:", key="gratitude_3", height=60)
                    
                    if st.button("Save Gratitude", key="save_gratitude", use_container_width=True):
                        if g1 or g2 or g3:
                            import requests
                            from backend.config import settings
                            
                            entry_text = "🙏 Gratitude Journal:\n"
                            if g1: entry_text += f"1. {g1}\n"
                            if g2: entry_text += f"2. {g2}\n"
                            if g3: entry_text += f"3. {g3}\n"
                            
                            try:
                                # Use localhost specifically for requests
                                api_url = f"http://localhost:{settings.api_port}/api/journal/"
                                requests.post(api_url, json={
                                    "user_id": st.session_state.user_id,
                                    "text": entry_text
                                })
                                st.success("Saved to your journal!")
                            except Exception as e:
                                st.error(f"Failed to save: {e}")
                        else:
                            st.warning("Please write something first.")
            
            with activity_col2:
                with st.expander("💪 Positive Affirmations"):
                    st.markdown("""
                        <p style="color: rgba(255, 255, 255, 0.9); line-height: 1.6; margin-bottom: 1rem;">
                            Repeat these affirmations out loud:
                        </p>
                        <ul style="color: rgba(255, 255, 255, 0.85); line-height: 2;">
                            <li>I am capable and strong</li>
                            <li>I deserve peace and happiness</li>
                            <li>I am doing my best, and that's enough</li>
                            <li>This feeling is temporary</li>
                            <li>I have overcome challenges before</li>
                        </ul>
                    """, unsafe_allow_html=True)
                    
                    if st.button("Save to Journal", key="save_affirmations", use_container_width=True):
                         import requests
                         from backend.config import settings
                         try:
                            entry_text = "💪 I practiced my positive affirmations today:\n- I am capable and strong\n- I deserve peace and happiness\n- I am doing my best, and that's enough"
                            api_url = f"http://localhost:{settings.api_port}/api/journal/"
                            requests.post(api_url, json={
                                "user_id": st.session_state.user_id,
                                "text": entry_text
                            })
                            st.success("Practice logged!")
                         except:
                            st.error("Could not save.")
                        
    elif st.session_state.active_wellness_tab == "Crisis":
        render_crisis_resources()
