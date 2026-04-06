-- Add category and image_url columns to recipes (nullable for backward compatibility)

ALTER TABLE recipes
  ADD COLUMN IF NOT EXISTS category text,
  ADD COLUMN IF NOT EXISTS image_url text;
