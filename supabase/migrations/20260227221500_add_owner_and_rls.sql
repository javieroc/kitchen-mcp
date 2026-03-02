ALTER TABLE "public"."ingredients"
ADD COLUMN IF NOT EXISTS "owner_id" uuid REFERENCES auth.users(id) ON DELETE CASCADE;

ALTER TABLE "public"."recipes"
ADD COLUMN IF NOT EXISTS "owner_id" uuid REFERENCES auth.users(id) ON DELETE CASCADE;

ALTER TABLE "public"."recipe_ingredients"
ADD COLUMN IF NOT EXISTS "owner_id" uuid REFERENCES auth.users(id) ON DELETE CASCADE;

CREATE INDEX IF NOT EXISTS ingredients_owner_id_idx ON "public"."ingredients" ("owner_id");
CREATE INDEX IF NOT EXISTS recipes_owner_id_idx ON "public"."recipes" ("owner_id");
CREATE INDEX IF NOT EXISTS recipe_ingredients_owner_id_idx ON "public"."recipe_ingredients" ("owner_id");

ALTER TABLE "public"."ingredients" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "public"."recipes" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "public"."recipe_ingredients" ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS ingredients_select_own ON "public"."ingredients";
DROP POLICY IF EXISTS ingredients_insert_own ON "public"."ingredients";
DROP POLICY IF EXISTS ingredients_update_own ON "public"."ingredients";
DROP POLICY IF EXISTS ingredients_delete_own ON "public"."ingredients";

CREATE POLICY ingredients_select_own ON "public"."ingredients"
FOR SELECT TO authenticated
USING ("owner_id" = auth.uid());

CREATE POLICY ingredients_insert_own ON "public"."ingredients"
FOR INSERT TO authenticated
WITH CHECK ("owner_id" = auth.uid());

CREATE POLICY ingredients_update_own ON "public"."ingredients"
FOR UPDATE TO authenticated
USING ("owner_id" = auth.uid())
WITH CHECK ("owner_id" = auth.uid());

CREATE POLICY ingredients_delete_own ON "public"."ingredients"
FOR DELETE TO authenticated
USING ("owner_id" = auth.uid());

DROP POLICY IF EXISTS recipes_select_own ON "public"."recipes";
DROP POLICY IF EXISTS recipes_insert_own ON "public"."recipes";
DROP POLICY IF EXISTS recipes_update_own ON "public"."recipes";
DROP POLICY IF EXISTS recipes_delete_own ON "public"."recipes";

CREATE POLICY recipes_select_own ON "public"."recipes"
FOR SELECT TO authenticated
USING ("owner_id" = auth.uid());

CREATE POLICY recipes_insert_own ON "public"."recipes"
FOR INSERT TO authenticated
WITH CHECK ("owner_id" = auth.uid());

CREATE POLICY recipes_update_own ON "public"."recipes"
FOR UPDATE TO authenticated
USING ("owner_id" = auth.uid())
WITH CHECK ("owner_id" = auth.uid());

CREATE POLICY recipes_delete_own ON "public"."recipes"
FOR DELETE TO authenticated
USING ("owner_id" = auth.uid());

DROP POLICY IF EXISTS recipe_ingredients_select_own ON "public"."recipe_ingredients";
DROP POLICY IF EXISTS recipe_ingredients_insert_own ON "public"."recipe_ingredients";
DROP POLICY IF EXISTS recipe_ingredients_update_own ON "public"."recipe_ingredients";
DROP POLICY IF EXISTS recipe_ingredients_delete_own ON "public"."recipe_ingredients";

CREATE POLICY recipe_ingredients_select_own ON "public"."recipe_ingredients"
FOR SELECT TO authenticated
USING ("owner_id" = auth.uid());

CREATE POLICY recipe_ingredients_insert_own ON "public"."recipe_ingredients"
FOR INSERT TO authenticated
WITH CHECK ("owner_id" = auth.uid());

CREATE POLICY recipe_ingredients_update_own ON "public"."recipe_ingredients"
FOR UPDATE TO authenticated
USING ("owner_id" = auth.uid())
WITH CHECK ("owner_id" = auth.uid());

CREATE POLICY recipe_ingredients_delete_own ON "public"."recipe_ingredients"
FOR DELETE TO authenticated
USING ("owner_id" = auth.uid());
