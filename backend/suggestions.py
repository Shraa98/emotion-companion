"""
Enhanced suggestions engine with context-aware, personalized coping strategies.
"""

from typing import List, Dict
import random

# Evidence-based coping strategies by emotion and context
SUGGESTIONS_DATABASE = {
    "anxiety": {
        "work": [
            "Break down your tasks into smaller, manageable steps",
            "Practice the 5-4-3-2-1 grounding technique: name 5 things you see, 4 you hear, 3 you can touch, 2 you smell, 1 you taste",
            "Take a 10-minute walk to clear your mind and reset",
            "Write down your worries and challenge them with evidence",
            "Use the Pomodoro technique: 25 minutes focused work, 5 minutes break"
        ],
        "relationships": [
            "Communicate your feelings using 'I' statements",
            "Take deep breaths before responding in difficult conversations",
            "Write down what you want to say before the conversation",
            "Remember: you can only control your own actions, not others' reactions",
            "Consider if this worry will matter in 5 years"
        ],
        "general": [
            "Practice box breathing: inhale 4 counts, hold 4, exhale 4, hold 4",
            "Progressive muscle relaxation: tense and release each muscle group",
            "Listen to calming music or nature sounds",
            "Limit caffeine and stay hydrated",
            "Journal your thoughts to externalize worries"
        ],
        "health": [
            "Focus on what you can control right now",
            "Reach out to a healthcare professional if concerns persist",
            "Practice gentle movement like stretching or yoga",
            "Avoid excessive health-related internet searches",
            "Connect with supportive friends or family"
        ]
    },
    "sadness": {
        "general": [
            "Allow yourself to feel - emotions are valid and temporary",
            "Reach out to a trusted friend or family member",
            "Engage in a small act of self-care (shower, favorite meal, cozy space)",
            "Get outside for 15 minutes - sunlight and fresh air help",
            "Write about what you're feeling without judgment"
        ],
        "relationships": [
            "Remember that healing takes time",
            "Focus on connections that bring you comfort",
            "It's okay to set boundaries while you process",
            "Consider writing a letter (you don't have to send it)",
            "Seek support from a counselor if feelings persist"
        ],
        "work": [
            "Take a mental health day if possible",
            "Talk to your supervisor about workload if overwhelmed",
            "Celebrate small wins, even tiny ones",
            "Connect with supportive colleagues",
            "Remember: your worth isn't defined by productivity"
        ]
    },
    "anger": {
        "general": [
            "Take a timeout before responding - count to 10 slowly",
            "Physical activity can help release tension (walk, exercise)",
            "Write down what's bothering you, then tear it up",
            "Practice the STOP technique: Stop, Take a breath, Observe, Proceed mindfully",
            "Ask yourself: Will this matter in a week? A month? A year?"
        ],
        "relationships": [
            "Use 'I feel' statements instead of 'You always/never'",
            "Take a break if the conversation gets too heated",
            "Focus on the specific issue, not the person",
            "Listen to understand, not just to respond",
            "Consider if there's hurt or fear underneath the anger"
        ],
        "work": [
            "Step away from the situation if possible",
            "Document facts objectively if it's a workplace issue",
            "Channel energy into problem-solving rather than blame",
            "Talk to HR or a supervisor if it's a serious concern",
            "Practice assertive (not aggressive) communication"
        ]
    },
    "joy": {
        "general": [
            "Savor this moment - take a mental snapshot",
            "Share your joy with someone you care about",
            "Write down what made you happy to revisit later",
            "Express gratitude for the good things",
            "Use this positive energy for something creative or productive"
        ]
    },
    "fear": {
        "general": [
            "Ground yourself in the present moment",
            "Ask: What's the worst that could happen? How would I handle it?",
            "Break down the fear into specific, manageable concerns",
            "Talk to someone you trust about what scares you",
            "Remember times you've overcome challenges before"
        ]
    },
    "neutral": {
        "general": [
            "Use this calm moment for reflection or planning",
            "Practice gratitude - list 3 things you're thankful for",
            "Set a small, achievable goal for today",
            "Check in with yourself: What do you need right now?",
            "Engage in a mindful activity (tea, walk, music)"
        ]
    }
}

# Intensity-based modifiers
INTENSITY_MODIFIERS = {
    "mild": {
        "prefix": "Since you're experiencing mild {emotion}, ",
        "suggestions": [
            "This is a good time for gentle self-reflection",
            "Consider journaling to explore these feelings",
            "A short walk or stretch might help"
        ]
    },
    "moderate": {
        "prefix": "You're experiencing moderate {emotion}. ",
        "suggestions": [
            "It's important to address these feelings",
            "Consider talking to someone you trust",
            "Take some time for self-care today"
        ]
    },
    "intense": {
        "prefix": "You're experiencing intense {emotion}. ",
        "suggestions": [
            "Please prioritize your wellbeing right now",
            "Consider reaching out to a mental health professional",
            "If you're in crisis, contact a crisis helpline immediately",
            "You don't have to face this alone - support is available"
        ]
    }
}

# Crisis resources
CRISIS_RESOURCES = """
If you're experiencing a mental health crisis:
• National Suicide Prevention Lifeline: 988 (US)
• Crisis Text Line: Text HOME to 741741
• International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/
"""


def get_life_domain(text: str) -> str:
    """Detect the primary life domain from text."""
    text_lower = text.lower()
    
    work_keywords = ['work', 'job', 'boss', 'colleague', 'office', 'career', 'project', 'deadline', 'meeting', 'presentation']
    relationship_keywords = ['relationship', 'partner', 'spouse', 'friend', 'family', 'love', 'breakup', 'argument', 'lonely']
    health_keywords = ['health', 'sick', 'pain', 'doctor', 'medical', 'illness', 'body', 'physical']
    
    work_count = sum(1 for kw in work_keywords if kw in text_lower)
    relationship_count = sum(1 for kw in relationship_keywords if kw in text_lower)
    health_count = sum(1 for kw in health_keywords if kw in text_lower)
    
    if work_count > relationship_count and work_count > health_count:
        return "work"
    elif relationship_count > work_count and relationship_count > health_count:
        return "relationships"
    elif health_count > 0:
        return "health"
    else:
        return "general"


def get_emotion_intensity(mood_score: int, emotion_confidence: float) -> str:
    """Determine emotion intensity level."""
    if mood_score <= 3 or mood_score >= 8:
        if emotion_confidence > 0.7:
            return "intense"
        else:
            return "moderate"
    elif mood_score <= 5 or mood_score >= 7:
        return "moderate"
    else:
        return "mild"


def generate_personalized_suggestions(
    emotion: str,
    mood_score: int,
    text: str,
    emotion_confidence: float = 0.5
) -> Dict[str, any]:
    """
    Generate context-aware, personalized coping suggestions.
    
    Args:
        emotion: Primary detected emotion
        mood_score: Mood score (0-10)
        text: Original journal text
        emotion_confidence: Confidence in emotion detection
        
    Returns:
        Dictionary with suggestions and metadata
    """
    # Normalize emotion
    emotion_lower = emotion.lower()
    if emotion_lower not in SUGGESTIONS_DATABASE:
        emotion_lower = "neutral"
    
    # Detect life domain
    domain = get_life_domain(text)
    
    # Determine intensity
    intensity = get_emotion_intensity(mood_score, emotion_confidence)
    
    # Get base suggestions
    suggestions = []
    
    # Add domain-specific suggestions
    if domain in SUGGESTIONS_DATABASE[emotion_lower]:
        domain_suggestions = SUGGESTIONS_DATABASE[emotion_lower][domain]
        suggestions.extend(random.sample(domain_suggestions, min(2, len(domain_suggestions))))
    
    # Add general suggestions
    if "general" in SUGGESTIONS_DATABASE[emotion_lower]:
        general_suggestions = SUGGESTIONS_DATABASE[emotion_lower]["general"]
        suggestions.extend(random.sample(general_suggestions, min(3, len(general_suggestions))))
    
    # Add intensity-specific suggestions
    if intensity in INTENSITY_MODIFIERS:
        suggestions.extend(INTENSITY_MODIFIERS[intensity]["suggestions"][:2])
    
    # Add crisis resources if needed
    include_crisis = False
    if intensity == "intense" and emotion_lower in ["sadness", "anxiety", "fear"]:
        include_crisis = True
    
    return {
        "suggestions": suggestions[:5],  # Limit to 5 suggestions
        "emotion": emotion,
        "domain": domain,
        "intensity": intensity,
        "crisis_resources": CRISIS_RESOURCES if include_crisis else None
    }
