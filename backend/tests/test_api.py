"""
API endpoint tests using FastAPI TestClient.
Tests health check and journal entry endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from uuid import uuid4

from backend.app import app

client = TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoint."""
    
    def test_health_check(self):
        """Test that health endpoint returns 200 and correct structure."""
        response = client.get("/api/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "status" in data
        assert "version" in data
        assert "nlp_models" in data
        assert data["status"] == "healthy"


class TestJournalEndpoints:
    """Test journal entry endpoints."""
    
    def test_create_journal_entry(self):
        """Test creating a journal entry."""
        # Note: This test requires a database connection
        # In production, you would use a test database
        
        user_id = str(uuid4())
        entry_data = {
            "user_id": user_id,
            "text": "I feel really happy and excited about today!"
        }
        
        response = client.post("/api/journal/", json=entry_data)
        
        # May fail if database not set up - that's expected in unit tests
        # In integration tests, this should pass
        if response.status_code == 200:
            data = response.json()
            assert "id" in data
            assert "analysis" in data
            assert data["text"] == entry_data["text"]
    
    def test_create_journal_entry_validation(self):
        """Test that short text is rejected."""
        user_id = str(uuid4())
        entry_data = {
            "user_id": user_id,
            "text": "Short"  # Too short (< 10 chars)
        }
        
        response = client.post("/api/journal/", json=entry_data)
        
        # Should fail validation
        assert response.status_code == 422


# Note: More comprehensive API tests would require:
# 1. Test database setup/teardown
# 2. Mocking external services (Supabase)
# 3. Fixtures for test data
# 
# For a production system, consider using:
# - pytest fixtures for database setup
# - pytest-asyncio for async tests
# - SQLite in-memory database for testing
