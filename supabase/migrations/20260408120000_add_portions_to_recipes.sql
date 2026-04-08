-- Add yield fields to recipes so scaling calculations know the reference quantity.
-- yield_amount: the numeric quantity the base recipe produces (e.g. 500, 4, 12)
-- yield_unit:   free-text label for what that number represents (e.g. "g", "portions", "cookies", "loaf")
-- Defaults keep all existing recipes valid without manual updates.

ALTER TABLE recipes
  ADD COLUMN IF NOT EXISTS yield_amount numeric(10,3) NOT NULL DEFAULT 1 CHECK (yield_amount > 0),
  ADD COLUMN IF NOT EXISTS yield_unit   text          NOT NULL DEFAULT 'portion';
