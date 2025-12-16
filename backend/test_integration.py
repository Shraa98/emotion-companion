
import sys
import os
import uuid
import logging
import json
from datetime import datetime

# Add project root to path
sys.path.append(os.getcwd())

from backend.nlp import analyze_text
from backend.crud import create_journal_entry

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

USER_TEXT = """I'm struggling with difficult emotions right now and need to process them.
as a recently graduated student I'm still a fresher without job till now, so lately I'm feeling like more depressed .
at every step I'm getting failure & don't know what else i should do?
emotionally mentally feeling a lot of pressure.
sometimes I'm literally feeling like go just die."""

from backend.models import JournalEntryResponse

def test_integration():
    logger.info("🎬 Starting Integration Test")
    
    # 1. Simulate Auth / User ID
    user_id = uuid.uuid4()
    logger.info(f"👤 Test User ID: {user_id}")
    
    try:
        # 2. Run NLP Analysis
        logger.info("🧠 Running NLP Analysis...")
        analysis_result = analyze_text(USER_TEXT)
        logger.info("✅ NLP Analysis complete.")
        
        # 3. Simulate Database Save (CRUD)
        logger.info("💾 Saving to Database...")
        entry = create_journal_entry(
            user_id=user_id,
            text=USER_TEXT,
            analysis=analysis_result
        )
        
        if entry:
            logger.info(f"✅ Entry saved successfully! ID: {entry.get('id')}")
            
            # 4. Simulate FastAPI/Pydantic Validation
            logger.info("🔍 Validating against Pydantic Model...")
            # Inject analysis as app.py does
            entry["analysis"] = analysis_result
            
            try:
                model = JournalEntryResponse(**entry)
                logger.info("✅ Pydantic Validation Passed!")
                print(model.json(indent=2))
            except Exception as validation_error:
                logger.error(f"❌ Pydantic Validation Failed: {validation_error}")
                raise
                
        else:
            logger.error("❌ Failed to save entry (returned None)")
            
    except Exception as e:
        logger.error(f"💥 CRASH DETECTED: {e}")
        # import traceback
        # traceback.print_exc()

if __name__ == "__main__":
    test_integration()
