-- Tabela para armazenar subscriptions de push por usuário
-- Rodar no Supabase SQL Editor: https://supabase.com/dashboard/project/mmtrzxmitklpibfilbio/sql

CREATE TABLE IF NOT EXISTS push_subscriptions (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id         uuid REFERENCES auth.users NOT NULL,
  endpoint        text NOT NULL,
  p256dh          text NOT NULL,   -- chave pública do cliente (push encryption)
  auth            text NOT NULL,   -- segredo de autenticação do cliente
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now(),
  UNIQUE (user_id, endpoint)       -- um dispositivo não duplica subscription
);

-- Atualiza updated_at automaticamente
CREATE OR REPLACE FUNCTION update_push_subscriptions_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$;

CREATE TRIGGER push_subscriptions_updated_at
  BEFORE UPDATE ON push_subscriptions
  FOR EACH ROW EXECUTE FUNCTION update_push_subscriptions_updated_at();

-- RLS: cada usuário vê e gerencia apenas as próprias subscriptions
ALTER TABLE push_subscriptions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Usuário gerencia suas subscriptions"
  ON push_subscriptions
  FOR ALL
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- Index para busca rápida por user_id (usado pela Edge Function)
CREATE INDEX IF NOT EXISTS push_subscriptions_user_id_idx ON push_subscriptions(user_id);
