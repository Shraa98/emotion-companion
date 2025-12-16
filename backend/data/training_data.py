"""
Embedded training data for Emotion Companion AI.
Small, curated dataset for training lightweight ML models.
"""

# ============================================
# Sentiment Data (Positive vs Negative)
# ============================================
SENTIMENT_DATA = [
    # POSITIVE EXAMPLES
    ("I feel absolutely amazing today!", "POSITIVE"),
    ("This is a wonderful day.", "POSITIVE"),
    ("I am so happy and grateful.", "POSITIVE"),
    ("I love my life and my family.", "POSITIVE"),
    ("Everything is going perfectly.", "POSITIVE"),
    ("I feel great about my progress.", "POSITIVE"),
    ("I accomplished so much today.", "POSITIVE"),
    ("The weather is beautiful.", "POSITIVE"),
    ("I had a fantastic time with friends.", "POSITIVE"),
    ("I'm excited about the future.", "POSITIVE"),
    ("I feel confident and improved.", "POSITIVE"),
    ("My mood is excellent right now.", "POSITIVE"),
    ("I am proud of myself.", "POSITIVE"),
    ("I feel energetic and alive.", "POSITIVE"),
    ("Life is good.", "POSITIVE"),
    ("I am thankful for everything.", "POSITIVE"),
    ("This was the best decision ever.", "POSITIVE"),
    ("I feel peaceful and content.", "POSITIVE"),
    ("My heart is full of joy.", "POSITIVE"),
    ("I am enjoying every moment.", "POSITIVE"),
    ("I feel strong and capable.", "POSITIVE"),
    ("I love learning new things.", "POSITIVE"),
    ("This is a huge success.", "POSITIVE"),
    ("I appreciate all the help.", "POSITIVE"),
    ("I am smiling from ear to ear.", "POSITIVE"),
    
    # NEGATIVE EXAMPLES
    ("I feel terrible and sad.", "NEGATIVE"),
    ("Today was a disaster.", "NEGATIVE"),
    ("I am so stressed and anxious.", "NEGATIVE"),
    ("I hate feeling this way.", "NEGATIVE"),
    ("Everything is going wrong.", "NEGATIVE"),
    ("I feel hopeless and lost.", "NEGATIVE"),
    ("I am disappointed in myself.", "NEGATIVE"),
    ("This is the worst day ever.", "NEGATIVE"),
    ("I feel lonely and isolated.", "NEGATIVE"),
    ("I am worried about everything.", "NEGATIVE"),
    ("My heart is broken.", "NEGATIVE"),
    ("I feel tired and exhausted.", "NEGATIVE"),
    ("I am angry at the situation.", "NEGATIVE"),
    ("I feel extremely frustrated.", "NEGATIVE"),
    ("Nothing seems to work out.", "NEGATIVE"),
    ("I am afraid of failing.", "NEGATIVE"),
    ("I feel empty inside.", "NEGATIVE"),
    ("This pain is unbearable.", "NEGATIVE"),
    ("I am nervous about the result.", "NEGATIVE"),
    ("I feel weak and helpless.", "NEGATIVE"),
    ("I regret my actions.", "NEGATIVE"),
    ("I am jealous of them.", "NEGATIVE"),
    ("I feel overwhelmed by work.", "NEGATIVE"),
    ("I am bored and unmotivated.", "NEGATIVE"),
    # Job/Career Stress
    ("I lost my job correctly.", "NEGATIVE"),
    ("I am a fresher and cannot find work.", "NEGATIVE"),
    ("I feel like a failure in my career.", "NEGATIVE"),
    ("Rejected from another interview.", "NEGATIVE"),
    ("I have no money and I am worried.", "NEGATIVE"),

    # Severe Depression / Despair
    ("I feel like I want to die.", "NEGATIVE"),
    ("There is no hope left for me.", "NEGATIVE"),
    ("I am struggling with difficult emotions.", "NEGATIVE"),
    ("I feel mentally and emotionally drained.", "NEGATIVE"),
    ("I getting failure at every step.", "NEGATIVE"),
]

# ============================================
# Emotion Data (Specific Emotions)
# ============================================
EMOTION_DATA = [
    # JOY / HAPPY
    ("I am so happy!", "happy"),
    ("This is wonderful news.", "happy"),
    ("I feel great joy.", "happy"),
    ("I am delighted by the result.", "happy"),
    ("I feel ecstatic!", "happy"),
    ("Smiling all day long.", "happy"),
    ("I love this feeling.", "happy"),
    ("I am celebrating today.", "happy"),
    ("We had so much fun.", "happy"),
    ("I feel on top of the world.", "happy"),
    ("I am getting a new job!", "happy"),
    ("I graduated today!", "happy"),
    
    # SADNESS / DEPRESSION
    ("I feel extremely sad.", "sad"),
    ("My heart hurts so much.", "sad"),
    ("I want to cry.", "sad"),
    ("Everything feels gloomy.", "sad"),
    ("I lost something important.", "sad"),
    ("I feel depressed and low.", "sad"),
    ("I am grieving right now.", "sad"),
    ("Tears keep falling.", "sad"),
    ("I feel very unhappy.", "sad"),
    ("I miss them so much.", "sad"),
    ("I feel like just go die.", "sad"),
    ("I am a failure.", "sad"),
    ("I am feeling depressed.", "sad"),
    ("I have no job and feel useless.", "sad"),
    ("I am struggling with emotions.", "sad"),
    ("I feel mentally pressure.", "sad"),
    
    # ANGER
    ("I am furious right now!", "angry"),
    ("This makes me so mad.", "angry"),
    ("I hate when this happens.", "angry"),
    ("I am outraged by this.", "angry"),
    ("Stop annoying me.", "angry"),
    ("I want to scream.", "angry"),
    ("This is incredibly frustrating.", "angry"),
    ("I am losing my temper.", "angry"),
    ("Don't talk to me.", "angry"),
    ("I am resentful.", "angry"),
    ("Why does this always happen to me?", "angry"),

    # FEAR / ANXIOUS / PRESSURE
    ("I am scared of what might happen.", "fear"),
    ("I feel very anxious.", "anxious"),
    ("My heart is racing with fear.", "fear"),
    ("I am terrified.", "fear"),
    ("I feel nervous and shaky.", "anxious"),
    ("I am worried about the future.", "anxious"),
    ("I have a bad feeling.", "fear"),
    ("Panic involves me.", "anxious"),
    ("I feel unsafe.", "fear"),
    ("My anxiety is high.", "anxious"),
    ("I feel a lot of pressure mentally.", "anxious"),
    ("I don't know what to do next.", "anxious"),
    ("I am worried about my job.", "anxious"),
    ("I feel overwhelmed by everything.", "anxious"),

    # SURPRISE
    ("I was shocked by the news.", "surprise"),
    ("I can't believe it!", "surprise"),
    ("Wow, that was unexpected.", "surprise"),
    ("I am amazed.", "surprise"),
    ("This caught me off guard.", "surprise"),
    ("I didn't see that coming.", "surprise"),
    ("What a surprise!", "surprise"),
    ("I am stunned.", "surprise"),

    # NEUTRAL (Calm/Bored)
    ("I am just sitting here.", "neutral"),
    ("It was a normal day.", "neutral"),
    ("Nothing special happened.", "neutral"),
    ("I feel okay.", "neutral"),
    ("Just watching TV.", "neutral"),
    ("I am waiting for the bus.", "neutral"),
    ("I feel calm and relaxed.", "calm"),
    ("Everything is quiet.", "calm"),
    ("I am a student.", "neutral"),
    ("I graduated recently.", "neutral"),
]
