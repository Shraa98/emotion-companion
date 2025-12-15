"""
Interactive breathing exercise component with animated visualization.
"""

import streamlit as st
import time

def render_breathing_exercise():
    """Render an interactive breathing exercise with visual guide."""
    
    # Center the entire breathing interface
    b_s1, b_center, b_s2 = st.columns([1, 2, 1])
    
    with b_center:
        st.markdown(f"""
            <div style="text-align: center; margin-bottom: 2rem;">
                <h3 style="color: white; font-family: 'Outfit', sans-serif; margin-bottom: 0.5rem;">
                    🌬️ Guided Breathing Exercise
                </h3>
                <p style="color: rgba(255, 255, 255, 0.8); margin-bottom: 1.5rem;">
                    Follow the breathing pattern below. This exercise calms your nervous system.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Exercise Selection
        technique = st.selectbox(
            "Select Breathing Pattern",
            ["Box Breathing (4-4-4-4)", "4-7-8 Relaxing Breath", "Deep Calm (5-5)"],
            label_visibility="collapsed"
        )
        
        # Start Button
        if not st.session_state.get("breathing_active", False): # Check session state for active breathing
            if st.button("☀️ Start Breathing Exercise", use_container_width=True, type="primary"):
                st.session_state.breathing_active = True
                st.rerun()
    
    # Instructions based on technique
    if technique == "Box Breathing (4-4-4-4)":
        instructions = [
            ("Breathe IN", 4, "#4facfe"),
            ("Hold", 4, "#667eea"),
            ("Breathe OUT", 4, "#f093fb"),
            ("Hold", 4, "#764ba2")
        ]
    elif technique == "4-7-8 Relaxing Breath": # Updated technique name
        instructions = [
            ("Breathe IN", 4, "#4facfe"),
            ("Hold", 7, "#667eea"),
            ("Breathe OUT", 8, "#f093fb")
        ]
    else:  # Calm Breathing
        instructions = [
            ("Breathe IN", 4, "#4facfe"),
            ("Breathe OUT", 6, "#f093fb")
        ]
    
    # Breathing animation
    if st.session_state.get("breathing_active", False):
        placeholder = st.empty()
        
        for cycle in range(3):  # 3 cycles
            for instruction, duration, color in instructions:
                # Display instruction
                placeholder.markdown(f"""
                    <div style="text-align: center; padding: 3rem 2rem;">
                        <div style="
                            width: 200px;
                            height: 200px;
                            margin: 0 auto 2rem auto;
                            border-radius: 50%;
                            background: {color};
                            box-shadow: 0 0 40px {color}80;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            animation: breathe {duration}s ease-in-out;
                        ">
                            <span style="color: white; font-size: 2rem; font-weight: 700;">
                                {duration}
                            </span>
                        </div>
                        <h2 style="color: white; font-family: 'Outfit', sans-serif; margin-bottom: 0.5rem;">
                            {instruction}
                        </h2>
                        <p style="color: rgba(255, 255, 255, 0.7);">
                            Cycle {cycle + 1} of 3
                        </p>
                    </div>
                    
                    <style>
                    @keyframes breathe {{
                        0%, 100% {{ transform: scale(1); }}
                        50% {{ transform: scale(1.3); }}
                    }}
                    </style>
                """, unsafe_allow_html=True)
                
                time.sleep(duration)
        
        # Completion message
        placeholder.markdown("""
            <div class="glass-card" style="text-align: center; padding: 3rem 2rem;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">✨</div>
                <h2 style="color: white; font-family: 'Outfit', sans-serif; margin-bottom: 1rem;">
                    Well Done!
                </h2>
                <p style="color: rgba(255, 255, 255, 0.8); font-size: 1.1rem;">
                    You completed 3 breathing cycles. How do you feel?
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.session_state.breathing_active = False
    
    # Benefits
    # Benefits (Centered & Square-ish)
    st.markdown("""
        <div style="display: flex; justify-content: center; margin-top: 1.5rem;">
            <div class="glass-card" style="max-width: 500px; width: 100%; text-align: left; padding: 2rem;">
                <h4 style="color: white; font-family: 'Outfit', sans-serif; margin-bottom: 1rem; text-align: center;">
                    💡 Benefits of Breathing Exercises
                </h4>
                <ul style="color: rgba(255, 255, 255, 0.8); line-height: 1.8;">
                    <li>Reduces anxiety and stress immediately</li>
                    <li>Lowers heart rate and blood pressure</li>
                    <li>Improves focus and mental clarity</li>
                    <li>Activates the parasympathetic nervous system (rest & digest)</li>
                </ul>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_quick_grounding():
    """Render the 5-4-3-2-1 grounding exercise."""
    
    # Center content
    spacer1, col_centered, spacer2 = st.columns([1, 2, 1])
    
    with col_centered:
        # Header Card with reduced bottom margin to connect with expanders
        st.markdown("""
            <div class="glass-card" style="margin-bottom: 0.5rem; border-bottom-left-radius: 5px; border-bottom-right-radius: 5px;">
                <h3 style="color: white; font-family: 'Outfit', sans-serif; margin-bottom: 0.5rem;">
                    🎯 5-4-3-2-1 Grounding Exercise
                </h3>
                <p style="color: rgba(255, 255, 255, 0.8); margin-bottom: 0;">
                    This exercise brings you back to the present moment. Take your time with each step.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Interactive checklist
        steps = [
            ("👁️ 5 things you can SEE", "Look around and name 5 things you can see right now"),
            ("✋ 4 things you can TOUCH", "Notice 4 things you can physically feel"),
            ("👂 3 things you can HEAR", "Listen carefully and identify 3 sounds"),
            ("👃 2 things you can SMELL", "Notice 2 scents around you"),
            ("👅 1 thing you can TASTE", "Focus on one taste in your mouth")
        ]
        
        for i, (title, description) in enumerate(steps, 1):
            with st.expander(title, expanded=(i == 1)):
                st.markdown(f"""
                    <div style="margin-bottom: 0.5rem; color: rgba(255, 255, 255, 0.9);">
                        {description}
                    </div>
                """, unsafe_allow_html=True)
                
                st.text_area(
                    "Write them here (optional):",
                    key=f"grounding_step_{i}",
                    height=68,
                    label_visibility="collapsed",
                    placeholder="Write what you notice here..."
                )

        st.markdown("""
            <div class="glass-card" style="margin-top: 1rem; padding: 1rem; text-align: center;">
                <p style="color: rgba(255, 255, 255, 0.9); font-size: 1rem; margin: 0;">
                    ✨ You're now more present and grounded
                </p>
            </div>
        """, unsafe_allow_html=True)
