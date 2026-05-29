-- ============================================================================
-- Supabase Migration: Food Tracker Bot v2
-- Run this in your Supabase SQL Editor
-- ============================================================================

-- 1. Add new columns to food_users (for onboarding + TDEE)
ALTER TABLE food_users
ADD COLUMN IF NOT EXISTS weight_kg FLOAT,
ADD COLUMN IF NOT EXISTS height_cm FLOAT,
ADD COLUMN IF NOT EXISTS age INT,
ADD COLUMN IF NOT EXISTS gender TEXT,
ADD COLUMN IF NOT EXISTS onboarding_complete BOOLEAN DEFAULT FALSE;

-- 2. Create weight_log table (for weight tracking history)
CREATE TABLE IF NOT EXISTS weight_log (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    telegram_id BIGINT NOT NULL REFERENCES food_users(telegram_id),
    weight_kg FLOAT NOT NULL,
    logged_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Enable RLS on weight_log (same pattern as other tables)
ALTER TABLE weight_log ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can read own weight" ON weight_log
    FOR SELECT USING (telegram_id = (auth.jwt() ->> 'telegram_id')::bigint);

CREATE POLICY "Users can insert own weight" ON weight_log
    FOR INSERT WITH CHECK (telegram_id = (auth.jwt() ->> 'telegram_id')::bigint);
