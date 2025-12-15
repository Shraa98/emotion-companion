-- Create audio_entries table
-- This table stores metadata for audio journal entries and their transcriptions

CREATE TABLE IF NOT EXISTS audio_entries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Audio file information
    file_path TEXT NOT NULL,  -- Path in Supabase Storage or local storage
    file_name VARCHAR(255),
    file_size INTEGER,  -- Size in bytes
    duration FLOAT,  -- Duration in seconds
    
    -- Transcription
    transcript TEXT,
    transcription_status VARCHAR(50) DEFAULT 'pending',  -- pending, completed, failed
    
    -- Analysis results (same as journal_entries)
    mood_score INTEGER CHECK (mood_score >= 0 AND mood_score <= 10),
    sentiment FLOAT CHECK (sentiment >= -1 AND sentiment <= 1),
    sentiment_label VARCHAR(50),
    emotion VARCHAR(50),
    emotion_scores JSONB,
    themes TEXT[],
    
    -- Additional metadata
    metadata JSONB DEFAULT '{}',
    suggestions TEXT[],
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_audio_user_id ON audio_entries(user_id);
CREATE INDEX IF NOT EXISTS idx_audio_created_at ON audio_entries(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_audio_status ON audio_entries(transcription_status);

-- Add updated_at trigger
CREATE TRIGGER update_audio_entries_updated_at
    BEFORE UPDATE ON audio_entries
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
