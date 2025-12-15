"""
Motivational quote cards and inspirational content display.
"""

import streamlit as st
import random


def render_quote_card(quote_data: dict, emotion: str):
    """Render a beautiful quote card with emotion-based styling."""
    
    # Color scheme based on emotion
    color_schemes = {
        "anxiety": {"gradient": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)", "shadow": "rgba(79, 172, 254, 0.4)"},
        "sadness": {"gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)", "shadow": "rgba(102, 126, 234, 0.4)"},
        "anger": {"gradient": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)", "shadow": "rgba(245, 87, 108, 0.4)"},
        "fear": {"gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)", "shadow": "rgba(102, 126, 234, 0.4)"},
        "joy": {"gradient": "linear-gradient(135deg, #ffd89b 0%, #19547b 100%)", "shadow": "rgba(255, 216, 155, 0.4)"},
        "neutral": {"gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)", "shadow": "rgba(102, 126, 234, 0.4)"}
    }
    
    scheme = color_schemes.get(emotion.lower(), color_schemes["neutral"])
    
    # Center the quote card
    _, col_centered, _ = st.columns([1, 2, 1])
    with col_centered:
        st.markdown(f"""
            <div style="
                background: {scheme['gradient']};
                padding: 2.5rem 2rem;
                border-radius: 20px;
                box-shadow: 0 8px 32px {scheme['shadow']};
                margin: 1.5rem 0;
                animation: fadeInUp 0.6s ease;
            ">
                <div style="text-align: center;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">💭</div>
                    <p style="
                        color: white;
                        font-size: 1.3rem;
                        line-height: 1.6;
                        font-style: italic;
                        margin-bottom: 1.5rem;
                        font-weight: 500;
                    ">
                        "{quote_data['text']}"
                    </p>
                    <p style="
                        color: rgba(255, 255, 255, 0.9);
                        font-size: 1rem;
                        font-weight: 600;
                    ">
                        — {quote_data['author']}
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    

def render_book_recommendations(books: list):
    """Render book recommendation cards."""
    
    # Center book recommendations
    s1, c_main, s2 = st.columns([1, 6, 1]) # Slightly wider for books
    
    with c_main:
        st.markdown("""
            <div class="glass-card" style="margin-bottom: 1rem;">
                <h3 style="color: white; font-family: 'Outfit', sans-serif; margin-bottom: 0.5rem;">
                    📚 Recommended Reading
                </h3>
                <p style="color: rgba(255, 255, 255, 0.8); margin-bottom: 0;">
                    Click on a book to read the summary and key takeaways.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        for book in books:
            # Use expander as the main card interaction
            with st.expander(f"📖 {book['title']} - by {book['author']}", expanded=False):
                st.markdown(f"""<div style="padding: 0.5rem;">
    <p style="color: #FFD500; font-size: 0.9rem; margin-bottom: 0.5rem; font-weight: 600;">{book['type']}</p>
    <p style="color: rgba(255, 255, 255, 0.9); line-height: 1.6; margin-bottom: 1.5rem; font-style: italic;">"{book['description']}"</p>
    <div style="background: rgba(255, 255, 255, 0.05); border-left: 3px solid #FF6500; padding: 1rem; border-radius: 0 10px 10px 0;">
    <h5 style="color: white; margin-bottom: 0.5rem; font-family: 'Outfit', sans-serif;">📑 Summary & Key Takeaways</h5>
    <p style="color: rgba(255, 255, 255, 0.85); line-height: 1.6; font-size: 0.95rem; margin-bottom: 1rem;">{book.get('summary', 'Summary not available.')}</p>
    <div style="margin-top: 0.5rem;">
        <a href="{book.get('link', '#')}" target="_blank" rel="noopener noreferrer" style="
            display: inline-block;
            background: linear-gradient(135deg, #FF6500 0%, #FFD500 100%);
            color: #002a54;
            padding: 0.5rem 1rem;
            border-radius: 25px;
            text-decoration: none;
            font-weight: 700;
            font-size: 0.9rem;
            transition: transform 0.2s;
        ">🛒 Get this Book</a>
    </div>
    </div>
    </div>""", unsafe_allow_html=True)


def render_inspirational_story(story: dict):
    """Render an inspirational story in an expandable card."""
    
    if not story:
        return
    
    content_html = story['content'].replace('\n', '<br>')
    
    _, col_wrap, _ = st.columns([1, 3, 1])
    with col_wrap:
        with st.expander(f"✨ 📖 {story['title']} - Click to Read", expanded=False):
            st.markdown(f"""<div style="color: rgba(255, 255, 255, 0.9); line-height: 1.8; font-size: 1.05rem; padding: 1rem 0;">
    {content_html}
    </div>""", unsafe_allow_html=True)


def render_crisis_resources():
    """Render crisis resources and helplines."""
    
    # Center crisis resources
    s1, c_main, s2 = st.columns([1, 5, 1])
    
    with c_main:
        # Main header card with reduced bottom margin
        st.markdown("""
            <div class="glass-card" style="border-left: 4px solid #f5576c; margin-bottom: 1rem;">
                <h3 style="color: #f5576c; font-family: 'Outfit', sans-serif; margin-bottom: 0.5rem;">
                    🆘 Need Immediate Help?
                </h3>
                <p style="color: rgba(255, 255, 255, 0.9); margin-bottom: 0; line-height: 1.6;">
                    If you're in crisis or need someone to talk to right now, these resources are available 24/7:
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        # Helper function for consistent card styling
        def resource_card(title, items):
            items_html = "".join([f'<li style="margin-bottom: 0.5rem;">{item}</li>' for item in items])
            return f"""
                <div class="glass-card" style="height: 100%; min-height: 220px; display: flex; flex-direction: column;">
                    <h4 style="color: white; margin-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 0.5rem;">
                        {title}
                    </h4>
                    <ul style="color: rgba(255, 255, 255, 0.9); line-height: 1.6; padding-left: 1.2rem; margin: 0; flex-grow: 1;">
                        {items_html}
                    </ul>
                </div>
            """

        with col1:
            st.markdown(resource_card("📞 Crisis Helplines", [
                "<strong>988</strong> - Suicide Prevention Lifeline",
                "<strong>741741</strong> - Crisis Text Line (Text HOME)",
                "<strong>1-800-662-4357</strong> - SAMHSA Helpline"
            ]), unsafe_allow_html=True)
        
        with col2:
            st.markdown(resource_card("💻 Online Resources", [
                "BetterHelp - Online therapy",
                "7 Cups - Free emotional support",
                "MentalHealth.gov - Resources"
            ]), unsafe_allow_html=True)
