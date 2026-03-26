CREATE TABLE IF NOT EXISTS "public"."chat_threads" (
    "id" uuid DEFAULT gen_random_uuid() NOT NULL,
    "owner_id" uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    "title" text,
    "created_at" timestamp with time zone NOT NULL DEFAULT now(),
    "updated_at" timestamp with time zone NOT NULL DEFAULT now(),
    "last_message_at" timestamp with time zone NOT NULL DEFAULT now(),
    "archived_at" timestamp with time zone,
    CONSTRAINT "chat_threads_pkey" PRIMARY KEY ("id"),
    CONSTRAINT "chat_threads_id_owner_unique" UNIQUE ("id", "owner_id")
);

CREATE TABLE IF NOT EXISTS "public"."chat_messages" (
    "id" uuid DEFAULT gen_random_uuid() NOT NULL,
    "thread_id" uuid NOT NULL,
    "owner_id" uuid NOT NULL,
    "role" text NOT NULL CHECK ("role" IN ('user', 'assistant', 'system', 'tool')),
    "content" text NOT NULL,
    "sequence_no" bigint NOT NULL,
    "tools_used" text[] NOT NULL DEFAULT '{}'::text[],
    "created_at" timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT "chat_messages_pkey" PRIMARY KEY ("id"),
    CONSTRAINT "chat_messages_thread_owner_fkey"
        FOREIGN KEY ("thread_id", "owner_id")
        REFERENCES "public"."chat_threads"("id", "owner_id")
        ON DELETE CASCADE,
    CONSTRAINT "chat_messages_thread_sequence_unique" UNIQUE ("thread_id", "sequence_no")
);

CREATE INDEX IF NOT EXISTS "chat_threads_owner_id_last_message_at_idx"
ON "public"."chat_threads" ("owner_id", "last_message_at" DESC);

CREATE INDEX IF NOT EXISTS "chat_messages_owner_id_idx"
ON "public"."chat_messages" ("owner_id");

CREATE INDEX IF NOT EXISTS "chat_messages_thread_id_sequence_no_idx"
ON "public"."chat_messages" ("thread_id", "sequence_no");

CREATE OR REPLACE FUNCTION "public"."set_chat_threads_updated_at"()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS "chat_threads_set_updated_at" ON "public"."chat_threads";
CREATE TRIGGER "chat_threads_set_updated_at"
BEFORE UPDATE ON "public"."chat_threads"
FOR EACH ROW EXECUTE FUNCTION "public"."set_chat_threads_updated_at"();

CREATE OR REPLACE FUNCTION "public"."assign_chat_message_sequence_no"()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
  next_no bigint;
BEGIN
  PERFORM pg_advisory_xact_lock(hashtextextended(NEW.thread_id::text, 0));

  SELECT COALESCE(MAX(sequence_no), 0) + 1
  INTO next_no
  FROM "public"."chat_messages"
  WHERE "thread_id" = NEW.thread_id;

  NEW.sequence_no = next_no;
  RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS "chat_messages_assign_sequence_no" ON "public"."chat_messages";
CREATE TRIGGER "chat_messages_assign_sequence_no"
BEFORE INSERT ON "public"."chat_messages"
FOR EACH ROW EXECUTE FUNCTION "public"."assign_chat_message_sequence_no"();

CREATE OR REPLACE FUNCTION "public"."touch_chat_thread_on_message_insert"()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  UPDATE "public"."chat_threads"
  SET "last_message_at" = NEW.created_at,
      "updated_at" = now()
  WHERE "id" = NEW.thread_id
    AND "owner_id" = NEW.owner_id;
  RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS "chat_messages_touch_thread" ON "public"."chat_messages";
CREATE TRIGGER "chat_messages_touch_thread"
AFTER INSERT ON "public"."chat_messages"
FOR EACH ROW EXECUTE FUNCTION "public"."touch_chat_thread_on_message_insert"();

ALTER TABLE "public"."chat_threads" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "public"."chat_messages" ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "chat_threads_select_own" ON "public"."chat_threads";
DROP POLICY IF EXISTS "chat_threads_insert_own" ON "public"."chat_threads";
DROP POLICY IF EXISTS "chat_threads_update_own" ON "public"."chat_threads";
DROP POLICY IF EXISTS "chat_threads_delete_own" ON "public"."chat_threads";

CREATE POLICY "chat_threads_select_own" ON "public"."chat_threads"
FOR SELECT TO authenticated
USING ("owner_id" = auth.uid());

CREATE POLICY "chat_threads_insert_own" ON "public"."chat_threads"
FOR INSERT TO authenticated
WITH CHECK ("owner_id" = auth.uid());

CREATE POLICY "chat_threads_update_own" ON "public"."chat_threads"
FOR UPDATE TO authenticated
USING ("owner_id" = auth.uid())
WITH CHECK ("owner_id" = auth.uid());

CREATE POLICY "chat_threads_delete_own" ON "public"."chat_threads"
FOR DELETE TO authenticated
USING ("owner_id" = auth.uid());

DROP POLICY IF EXISTS "chat_messages_select_own" ON "public"."chat_messages";
DROP POLICY IF EXISTS "chat_messages_insert_own" ON "public"."chat_messages";
DROP POLICY IF EXISTS "chat_messages_update_own" ON "public"."chat_messages";
DROP POLICY IF EXISTS "chat_messages_delete_own" ON "public"."chat_messages";

CREATE POLICY "chat_messages_select_own" ON "public"."chat_messages"
FOR SELECT TO authenticated
USING ("owner_id" = auth.uid());

CREATE POLICY "chat_messages_insert_own" ON "public"."chat_messages"
FOR INSERT TO authenticated
WITH CHECK ("owner_id" = auth.uid());

CREATE POLICY "chat_messages_update_own" ON "public"."chat_messages"
FOR UPDATE TO authenticated
USING ("owner_id" = auth.uid())
WITH CHECK ("owner_id" = auth.uid());

CREATE POLICY "chat_messages_delete_own" ON "public"."chat_messages"
FOR DELETE TO authenticated
USING ("owner_id" = auth.uid());
