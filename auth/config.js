// Supabase Configuration
const SUPABASE_URL = 'https://medfxqvfpicunnvpktjv.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1lZGZ4cXZmcGljdW5udnBrdGp2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU3NjQ3MDYsImV4cCI6MjA4MTM0MDcwNn0.dEgtS_VfOVcKHXQN4zDWqTT9fh3VpVIr__caXOxlVGY';

// Initialize Supabase client
const supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
