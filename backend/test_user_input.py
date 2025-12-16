
import sys
import os
import json
import logging

# Add project root to path
sys.path.append(os.getcwd())

from backend.nlp import analyze_text

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

USER_TEXT = """I'm struggling with difficult emotions right now and need to process them.
as a recently graduated student I'm still a fresher without job till now, so lately I'm feeling like more depressed .
at every step I'm getting failure & don't know what else i should do?
emotionally mentally feeling a lot of pressure.
sometimes I'm literally feeling like go just die."""

def test_nlp_crash():
    logger.info("Testing NLP with user input...")
    try:
        result = analyze_text(USER_TEXT)
        logger.info("✅ Analysis Successful!")
        print(json.dumps(result, indent=2))
    except Exception as e:
        logger.error(f"❌ NLP Crashed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_nlp_crash()
