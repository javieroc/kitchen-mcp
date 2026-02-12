ALTER TABLE "public"."ingredients" 
ADD COLUMN "stock_quantity" numeric(10,3) DEFAULT 0.000 NOT NULL;

COMMENT ON COLUMN "public"."ingredients"."stock_quantity" IS 'Current amount of this ingredient available in the kitchen.';
