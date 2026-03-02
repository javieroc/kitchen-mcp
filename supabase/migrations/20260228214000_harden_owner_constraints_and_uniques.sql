-- 2) Enforce non-null ownership
-- Backfill legacy rows by assigning ownership to the oldest existing auth user.
DO $$
DECLARE
  legacy_owner_id uuid;
BEGIN
  SELECT id INTO legacy_owner_id
  FROM auth.users
  ORDER BY created_at ASC
  LIMIT 1;

  IF legacy_owner_id IS NULL THEN
    RAISE EXCEPTION
      'No users exist in auth.users. Create at least one user, then re-run migration %.',
      '20260228214000_harden_owner_constraints_and_uniques.sql';
  END IF;

  UPDATE "public"."ingredients"
  SET "owner_id" = legacy_owner_id
  WHERE "owner_id" IS NULL;

  UPDATE "public"."recipes"
  SET "owner_id" = legacy_owner_id
  WHERE "owner_id" IS NULL;

  -- Prefer recipe owner for links, then fallback to ingredient owner, then fallback to legacy owner.
  UPDATE "public"."recipe_ingredients" ri
  SET "owner_id" = r."owner_id"
  FROM "public"."recipes" r
  WHERE ri."recipe_id" = r."id"
    AND ri."owner_id" IS NULL
    AND r."owner_id" IS NOT NULL;

  UPDATE "public"."recipe_ingredients" ri
  SET "owner_id" = i."owner_id"
  FROM "public"."ingredients" i
  WHERE ri."ingredient_id" = i."id"
    AND ri."owner_id" IS NULL
    AND i."owner_id" IS NOT NULL;

  UPDATE "public"."recipe_ingredients"
  SET "owner_id" = legacy_owner_id
  WHERE "owner_id" IS NULL;
END $$;

ALTER TABLE "public"."ingredients"
ALTER COLUMN "owner_id" SET NOT NULL;

ALTER TABLE "public"."recipes"
ALTER COLUMN "owner_id" SET NOT NULL;

ALTER TABLE "public"."recipe_ingredients"
ALTER COLUMN "owner_id" SET NOT NULL;

-- 3) Replace global unique names with per-owner unique names
ALTER TABLE "public"."ingredients"
DROP CONSTRAINT IF EXISTS "ingredients_name_key";

ALTER TABLE "public"."recipes"
DROP CONSTRAINT IF EXISTS "recipes_name_key";

CREATE UNIQUE INDEX IF NOT EXISTS "ingredients_owner_id_name_key"
ON "public"."ingredients" ("owner_id", "name");

CREATE UNIQUE INDEX IF NOT EXISTS "recipes_owner_id_name_key"
ON "public"."recipes" ("owner_id", "name");

-- 4) Prevent duplicate links in relation table per owner/recipe/ingredient
DELETE FROM "public"."recipe_ingredients" ri
USING (
  SELECT id
  FROM (
    SELECT
      id,
      ROW_NUMBER() OVER (
        PARTITION BY owner_id, recipe_id, ingredient_id
        ORDER BY created_at, id
      ) AS rn
    FROM "public"."recipe_ingredients"
  ) ranked
  WHERE rn > 1
) dupes
WHERE ri.id = dupes.id;

CREATE UNIQUE INDEX IF NOT EXISTS "recipe_ingredients_owner_recipe_ingredient_key"
ON "public"."recipe_ingredients" ("owner_id", "recipe_id", "ingredient_id");
