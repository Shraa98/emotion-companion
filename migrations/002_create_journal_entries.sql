-- Create journal_entries table
-- This table stores journal text entries with emotional analysis results

CREATE TABLE IF NOT EXISTS journal_entries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    
    -- Analysis results
    mood_score INTEGER CHECK (mood_score >= 0 AND mood_score <= 10),
    sentiment FLOAT CHECK (sentiment >= -1 AND sentiment <= 1),
    sentiment_label VARCHAR(50),  -- POSITIVE, NEGATIVE, NEUTRAL
    emotion VARCHAR(50),  -- Primary detected emotion
    emotion_scores JSONB,  -- All emotion scores as JSON
    themes TEXT[],  -- Array of extracted themes/keywords
    
    -- Additional metadata
    metadata JSONB DEFAULT '{}',  -- Flexible field for additional data
    highlighted_phrases JSONB,  -- Phrases that contributed to analysis
    suggestions TEXT[],  -- Coping suggestions provided
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for common queries
CREATE INDEX IF NOT EXISTS idx_journal_user_id ON journal_entries(user_id);
CREATE INDEX IF NOT EXISTS idx_journal_created_at ON journal_entries(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_journal_emotion ON journal_entries(emotion);
CREATE INDEX IF NOT EXISTS idx_journal_mood_score ON journal_entries(mood_score);

-- Create GIN index for JSONB fields for faster queries
CREATE INDEX IF NOT EXISTS idx_journal_metadata ON journal_entries USING GIN (metadata);
CREATE INDEX IF NOT EXISTS idx_journal_emotion_scores ON journal_entries USING GIN (emotion_scores);

-- Add updated_at trigger
CREATE TRIGGER update_journal_entries_updated_at
    BEFORE UPDATE ON journal_entries
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
