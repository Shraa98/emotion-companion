"""
Wellness content database: Quotes, stories, book recommendations, and resources.
All content is mood-based and designed to provide comfort and support.
"""

# ============================================================================
# Motivational Quotes Database (100+ quotes)
# ============================================================================

QUOTES_BY_EMOTION = {
    "anxiety": [
        {"text": "You are braver than you believe, stronger than you seem, and smarter than you think.", "author": "A.A. Milne"},
        {"text": "Worrying does not take away tomorrow's troubles. It takes away today's peace.", "author": "Randy Armstrong"},
        {"text": "You don't have to control your thoughts. You just have to stop letting them control you.", "author": "Dan Millman"},
        {"text": "Anxiety is a thin stream of fear trickling through the mind. If encouraged, it cuts a channel into which all other thoughts are drained.", "author": "Arthur Somers Roche"},
        {"text": "Nothing diminishes anxiety faster than action.", "author": "Walter Anderson"},
        {"text": "You wouldn't worry so much about what others think of you if you realized how seldom they do.", "author": "Eleanor Roosevelt"},
        {"text": "The greatest weapon against stress is our ability to choose one thought over another.", "author": "William James"},
        {"text": "Calm mind brings inner strength and self-confidence.", "author": "Dalai Lama"},
        {"text": "You are not your anxiety. You are the sky, and anxiety is just the weather.", "author": "Unknown"},
        {"text": "Breathe. It's just a bad day, not a bad life.", "author": "Unknown"},
    ],
    "sadness": [
        {"text": "The wound is the place where the Light enters you.", "author": "Rumi"},
        {"text": "Every day may not be good, but there's something good in every day.", "author": "Alice Morse Earle"},
        {"text": "You are allowed to be both a masterpiece and a work in progress simultaneously.", "author": "Sophia Bush"},
        {"text": "The sun will rise and we will try again.", "author": "Twenty One Pilots"},
        {"text": "It's okay to not be okay, as long as you are not giving up.", "author": "Unknown"},
        {"text": "Stars can't shine without darkness.", "author": "Unknown"},
        {"text": "Your current situation is not your final destination.", "author": "Unknown"},
        {"text": "Healing doesn't mean the damage never existed. It means the damage no longer controls our lives.", "author": "Akshay Dubey"},
        {"text": "You've survived 100% of your worst days. You're doing great.", "author": "Unknown"},
        {"text": "Sometimes the bravest thing you can do is ask for help.", "author": "Unknown"},
    ],
    "anger": [
        {"text": "For every minute you remain angry, you give up sixty seconds of peace of mind.", "author": "Ralph Waldo Emerson"},
        {"text": "Holding onto anger is like drinking poison and expecting the other person to die.", "author": "Buddha"},
        {"text": "Speak when you are angry and you will make the best speech you will ever regret.", "author": "Ambrose Bierce"},
        {"text": "The best fighter is never angry.", "author": "Lao Tzu"},
        {"text": "Anger is an acid that can do more harm to the vessel in which it is stored than to anything on which it is poured.", "author": "Mark Twain"},
        {"text": "When anger rises, think of the consequences.", "author": "Confucius"},
        {"text": "You will not be punished for your anger, you will be punished by your anger.", "author": "Buddha"},
        {"text": "Anger makes you smaller, while forgiveness forces you to grow beyond what you were.", "author": "Cherie Carter-Scott"},
    ],
    "fear": [
        {"text": "Fear is only as deep as the mind allows.", "author": "Japanese Proverb"},
        {"text": "Everything you've ever wanted is on the other side of fear.", "author": "George Addair"},
        {"text": "Courage is not the absence of fear, but rather the assessment that something else is more important than fear.", "author": "Franklin D. Roosevelt"},
        {"text": "Do the thing you fear and the death of fear is certain.", "author": "Ralph Waldo Emerson"},
        {"text": "Fear is a reaction. Courage is a decision.", "author": "Winston Churchill"},
        {"text": "The cave you fear to enter holds the treasure you seek.", "author": "Joseph Campbell"},
        {"text": "Feel the fear and do it anyway.", "author": "Susan Jeffers"},
    ],
    "joy": [
        {"text": "Happiness is not by chance, but by choice.", "author": "Jim Rohn"},
        {"text": "The most wasted of days is one without laughter.", "author": "E.E. Cummings"},
        {"text": "Joy is what happens when we allow ourselves to recognize how good things really are.", "author": "Marianne Williamson"},
        {"text": "Gratitude turns what we have into enough.", "author": "Aesop"},
        {"text": "The purpose of our lives is to be happy.", "author": "Dalai Lama"},
        {"text": "Happiness is letting go of what you think your life is supposed to look like.", "author": "Unknown"},
        {"text": "Collect moments, not things.", "author": "Unknown"},
    ],
    "neutral": [
        {"text": "Be yourself; everyone else is already taken.", "author": "Oscar Wilde"},
        {"text": "The only way to do great work is to love what you do.", "author": "Steve Jobs"},
        {"text": "Life is 10% what happens to you and 90% how you react to it.", "author": "Charles R. Swindoll"},
        {"text": "The best time to plant a tree was 20 years ago. The second best time is now.", "author": "Chinese Proverb"},
        {"text": "You miss 100% of the shots you don't take.", "author": "Wayne Gretzky"},
    ]
}

# ============================================================================
# Book Recommendations by Emotion
# ============================================================================

BOOK_RECOMMENDATIONS = {
    "anxiety": [
        {"title": "The Anxiety Toolkit", "author": "Alice Boyes", "type": "Self-Help", "description": "Practical strategies to overcome worry and anxiety", "summary": "This book provides clinical tools to manage anxiety in daily life. Key takeaways include: 1) Identifying your anxiety triggers, 2) Breaking the cycle of rumination, 3) Using cognitive behavioral therapy (CBT) techniques to challenge anxious thoughts, and 4) Learning to tolerate uncertainty.", "link": "https://www.amazon.com/s?k=The+Anxiety+Toolkit+Alice+Boyes"},
        {"title": "Dare: The New Way to End Anxiety", "author": "Barry McDonagh", "type": "Self-Help", "description": "A proven method to overcome panic attacks and anxiety", "summary": "The 'DARE' response stands for: Defuse (don't fight the feeling), Allow (accept the anxiety), Run Toward (tell yourself you're excited), and Engage (focus on something else). This method helps disarm the brain's alarm system.", "link": "https://www.amazon.com/s?k=Dare+The+New+Way+to+End+Anxiety"},
        {"title": "The Worry Trick", "author": "David Carbonell", "type": "Self-Help", "description": "How your brain tricks you into expecting the worst", "summary": "Explains how the more you try to stop worrying, the more you worry. Suggests 'worry appointments' (scheduling time to worry) and distinguishing between productive worry (solving problems) and unproductive worry (what-ifs).", "link": "https://www.amazon.com/s?k=The+Worry+Trick+David+Carbonell"},
        {"title": "The Midnight Library", "author": "Matt Haig", "type": "Fiction", "description": "A beautiful story about life choices and possibilities", "summary": "A novel about a woman who finds a library between life and death where each book represents a different life she could have lived. It explores regrets, the meaning of happiness, and the realization that the 'perfect' life doesn't exist.", "link": "https://www.amazon.com/s?k=The+Midnight+Library+Matt+Haig"},
    ],
    "sadness": [
        {"title": "The Upward Spiral", "author": "Alex Korb", "type": "Self-Help", "description": "Using neuroscience to reverse the course of depression", "summary": "Explains the neuroscience of depression and offers small, practical steps to create an 'upward spiral'. Tips include: getting sunlight, exercising, practicing gratitude, and making decisions to reduce anxiety.", "link": "https://www.amazon.com/s?k=The+Upward+Spiral+Alex+Korb"},
        {"title": "Lost Connections", "author": "Johann Hari", "type": "Self-Help", "description": "Uncovering the real causes of depression and solutions", "summary": "Argues that depression is often caused by disconnection from meaningful work, other people, nature, and status. Suggests reconnecting with community and finding purpose as a path to healing.", "link": "https://www.amazon.com/s?k=Lost+Connections+Johann+Hari"},
        {"title": "The Gifts of Imperfection", "author": "Brené Brown", "type": "Self-Help", "description": "Let go of who you think you're supposed to be", "summary": "Encourages embracing vulnerability and imperfection. Key concepts include 'wholehearted living', cultivating self-compassion, and letting go of the need for approval and perfectionism.", "link": "https://www.amazon.com/s?k=The+Gifts+of+Imperfection+Brene+Brown"},
        {"title": "The Alchemist", "author": "Paulo Coelho", "type": "Fiction", "description": "An inspiring tale about following your dreams", "summary": "A fable about a shepherd boy who travels to Egypt to find a treasure. The core message is to listen to your heart, recognize omens, and follow your 'Personal Legend' (your life's purpose).", "link": "https://www.amazon.com/s?k=The+Alchemist+Paulo+Coelho"},
    ],
    "anger": [
        {"title": "The Cow in the Parking Lot", "author": "Leonard Scheff", "type": "Self-Help", "description": "A Zen approach to overcoming anger", "summary": "Uses the metaphor of a cow taking your parking spot: you wouldn't be angry at a cow, so why be angry at a person? Teaches how to detach from anger and respond with patience.", "link": "https://www.amazon.com/s?k=The+Cow+in+the+Parking+Lot"},
        {"title": "Anger: Wisdom for Cooling the Flames", "author": "Thich Nhat Hanh", "type": "Self-Help", "description": "Buddhist wisdom on transforming anger", "summary": "Teaches mindfulness techniques to cool the flames of anger. Suggests treating anger like a crying baby that needs care and attention, rather than suppression or explosion.", "link": "https://www.amazon.com/s?k=Anger+Wisdom+for+Cooling+the+Flames"},
        {"title": "The Dance of Anger", "author": "Harriet Lerner", "type": "Self-Help", "description": "A woman's guide to changing patterns of intimate relationships", "summary": "Focuses on how anger can be a signal that something is wrong in a relationship. Encourages using anger as a tool for change by communicating clearly and setting boundaries without being aggressive.", "link": "https://www.amazon.com/s?k=The+Dance+of+Anger+Harriet+Lerner"},
    ],
    "fear": [
        {"title": "Feel the Fear and Do It Anyway", "author": "Susan Jeffers", "type": "Self-Help", "description": "Dynamic techniques for turning fear into power", "summary": "Argues that fear is a natural part of growth. The only way to get rid of the fear of doing something is to go out and do it. Encourages moving from a place of pain (helplessness) to power (choice).", "link": "https://www.amazon.com/s?k=Feel+the+Fear+and+Do+It+Anyway"},
        {"title": "The Courage to Be Disliked", "author": "Ichiro Kishimi", "type": "Self-Help", "description": "How to free yourself and change your life", "summary": "Based on Adlerian psychology, this dialogue explores how our past doesn't determine our future. It argues that happiness comes from the courage to be disliked by others and living true to oneself.", "link": "https://www.amazon.com/s?k=The+Courage+to+Be+Disliked"},
        {"title": "Daring Greatly", "author": "Brené Brown", "type": "Self-Help", "description": "How the courage to be vulnerable transforms the way we live", "summary": "Explores how vulnerability is not weakness but our greatest measure of courage. Discusses how shame holds us back and how embracing vulnerability leads to creativity, connection, and joy.", "link": "https://www.amazon.com/s?k=Daring+Greatly+Brene+Brown"},
    ],
    "general": [
        {"title": "Atomic Habits", "author": "James Clear", "type": "Self-Help", "description": "Tiny changes, remarkable results", "summary": "Focuses on how small, consistent habits lead to massive results over time. Introduces the '4 Laws of Behavior Change': Make it Obvious, Make it Attractive, Make it Easy, and Make it Satisfying.", "link": "https://www.amazon.com/s?k=Atomic+Habits+James+Clear"},
        {"title": "The Happiness Project", "author": "Gretchen Rubin", "type": "Self-Help", "description": "One woman's year-long quest for happiness", "summary": "The author spends a year test-driving wisdom about happiness. Key takeaways: 'act the way you want to feel', 'do good to feel good', and the importance of relationships and energy.", "link": "https://www.amazon.com/s?k=The+Happiness+Project+Gretchen+Rubin"},
        {"title": "Man's Search for Meaning", "author": "Viktor Frankl", "type": "Philosophy", "description": "Finding purpose in life's challenges", "summary": "Written by a Holocaust survivor, this book argues that we cannot avoid suffering but we can choose how to cope with it and find meaning in it. 'He who has a why to live can bear almost any how.'", "link": "https://www.amazon.com/s?k=Mans+Search+for+Meaning+Viktor+Frankl"},
        {"title": "The Power of Now", "author": "Eckhart Tolle", "type": "Spirituality", "description": "A guide to spiritual enlightenment", "summary": "Emphasizes the importance of living in the present moment. Argues that most human pain is caused by identifying with the mind (past regrets or future worries) rather than the 'Now'.", "link": "https://www.amazon.com/s?k=The+Power+of+Now+Eckhart+Tolle"},
    ]
}

# ============================================================================
# Inspirational Short Stories
# ============================================================================

INSPIRATIONAL_STORIES = {
    "anxiety": {
        "title": "The Starfish Story",
        "content": """A young girl was walking along a beach where thousands of starfish had been washed ashore. 
        
She began picking them up one by one and throwing them back into the ocean. An old man approached her and said, "Why are you doing this? There are thousands of starfish. You can't possibly make a difference."

The girl picked up another starfish, threw it into the ocean, and replied, "I made a difference to that one."

**Lesson**: You don't have to solve everything at once. Every small action matters. Focus on what you can control right now."""
    },
    "sadness": {
        "title": "The Cracked Pot",
        "content": """A water bearer had two large pots. One was perfect, the other had a crack. Every day, the perfect pot delivered a full portion of water, while the cracked pot arrived only half full.

For two years this went on. The cracked pot was ashamed of its imperfection. One day it spoke to the water bearer: "I am ashamed of myself, and I want to apologize to you."

"Why?" asked the bearer. "What are you ashamed of?"

"I have been able to deliver only half my load because this crack in my side causes water to leak out all the way back."

The bearer smiled. "Did you notice that there were flowers only on your side of the path, but not on the other pot's side? That's because I have always known about your flaw, and I took advantage of it. I planted flower seeds on your side of the path, and every day while we walk back, you've watered them."

**Lesson**: Our flaws and imperfections can create beauty. What you see as weakness might be your greatest strength."""
    },
    "anger": {
        "title": "The Two Wolves",
        "content": """An old Cherokee told his grandson about a battle that goes on inside people.

"My son, the battle is between two wolves inside us all. One is Evil - it is anger, envy, jealousy, sorrow, regret, greed, arrogance, self-pity, guilt, resentment, inferiority, lies, false pride, superiority, and ego.

The other is Good - it is joy, peace, love, hope, serenity, humility, kindness, benevolence, empathy, generosity, truth, compassion, and faith."

The grandson thought about it for a minute and then asked his grandfather, "Which wolf wins?"

The old Cherokee simply replied, "The one you feed."

**Lesson**: You have the power to choose which emotions to nurture. Feed peace, not anger."""
    }
}

# ============================================================================
# Guided Activities
# ============================================================================

GUIDED_ACTIVITIES = {
    "grounding_5_4_3_2_1": {
        "name": "5-4-3-2-1 Grounding Exercise",
        "duration": "3-5 minutes",
        "steps": [
            "**5 things you can SEE**: Look around and name 5 things you can see right now",
            "**4 things you can TOUCH**: Notice 4 things you can physically feel (your feet on the floor, your back against the chair, etc.)",
            "**3 things you can HEAR**: Listen carefully and identify 3 sounds",
            "**2 things you can SMELL**: Notice 2 scents (or think of 2 favorite smells)",
            "**1 thing you can TASTE**: Focus on one taste in your mouth, or think of your favorite flavor"
        ],
        "benefit": "Brings you back to the present moment and reduces anxiety"
    },
    "box_breathing": {
        "name": "Box Breathing (4-4-4-4)",
        "duration": "2-5 minutes",
        "steps": [
            "**Breathe IN** through your nose for 4 counts",
            "**HOLD** your breath for 4 counts",
            "**Breathe OUT** through your mouth for 4 counts",
            "**HOLD** empty for 4 counts",
            "**Repeat** 4-5 times or until you feel calmer"
        ],
        "benefit": "Calms the nervous system and reduces stress"
    },
    "progressive_relaxation": {
        "name": "Progressive Muscle Relaxation",
        "duration": "10-15 minutes",
        "steps": [
            "Find a comfortable position, sitting or lying down",
            "**Feet**: Curl your toes tightly for 5 seconds, then release",
            "**Legs**: Tense your leg muscles for 5 seconds, then release",
            "**Stomach**: Tighten your abdominal muscles, then release",
            "**Hands**: Make fists for 5 seconds, then release",
            "**Arms**: Tense your arm muscles, then release",
            "**Shoulders**: Raise shoulders to ears, hold, then drop",
            "**Face**: Scrunch your face tight, then relax",
            "**Whole body**: Notice the difference between tension and relaxation"
        ],
        "benefit": "Releases physical tension and promotes deep relaxation"
    }
}

# ============================================================================
# Crisis Resources
# ============================================================================

CRISIS_RESOURCES = {
    "helplines": [
        {"name": "National Suicide Prevention Lifeline (US)", "number": "988", "available": "24/7"},
        {"name": "Crisis Text Line (US)", "number": "Text HOME to 741741", "available": "24/7"},
        {"name": "SAMHSA National Helpline", "number": "1-800-662-4357", "available": "24/7"},
    ],
    "apps": [
        {"name": "Calm", "description": "Meditation and sleep stories"},
        {"name": "Headspace", "description": "Mindfulness and meditation"},
        {"name": "Sanvello", "description": "Mood tracking and CBT tools"},
        {"name": "Wysa", "description": "AI mental health support"},
    ],
    "websites": [
        {"name": "BetterHelp", "url": "https://www.betterhelp.com", "description": "Online therapy platform"},
        {"name": "7 Cups", "url": "https://www.7cups.com", "description": "Free emotional support"},
        {"name": "MentalHealth.gov", "url": "https://www.mentalhealth.gov", "description": "Government mental health resources"},
    ]
}

# ============================================================================
# Helper Functions
# ============================================================================

def get_random_quote(emotion: str) -> dict:
    """Get a random motivational quote for the given emotion."""
    import random
    emotion_lower = emotion.lower()
    if emotion_lower not in QUOTES_BY_EMOTION:
        emotion_lower = "neutral"
    quotes = QUOTES_BY_EMOTION[emotion_lower]
    return random.choice(quotes)


def get_book_recommendations(emotion: str, limit: int = 3) -> list:
    """Get book recommendations for the given emotion."""
    emotion_lower = emotion.lower()
    if emotion_lower not in BOOK_RECOMMENDATIONS:
        emotion_lower = "general"
    books = BOOK_RECOMMENDATIONS[emotion_lower]
    return books[:limit]


def get_inspirational_story(emotion: str) -> dict:
    """Get an inspirational story for the given emotion."""
    emotion_lower = emotion.lower()
    if emotion_lower in INSPIRATIONAL_STORIES:
        return INSPIRATIONAL_STORIES[emotion_lower]
    return None


def get_guided_activity(activity_type: str = "grounding_5_4_3_2_1") -> dict:
    """Get a guided activity by type."""
    return GUIDED_ACTIVITIES.get(activity_type, GUIDED_ACTIVITIES["grounding_5_4_3_2_1"])
