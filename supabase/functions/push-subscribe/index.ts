// Edge Function: push-subscribe
// Salva ou atualiza a subscription de push de um dispositivo autenticado.
// Chamada pelo portal quando o usuário aceita notificações,
// e pelo SW no evento pushsubscriptionchange.

import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, content-type',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
}

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response(null, { headers: CORS })
  }

  const authHeader = req.headers.get('Authorization')
  if (!authHeader) {
    return new Response('Unauthorized', { status: 401, headers: CORS })
  }

  // Usa o token do usuário logado — respeita RLS
  const supa = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_ANON_KEY')!,
    { global: { headers: { Authorization: authHeader } } }
  )

  const { data: { user }, error: authErr } = await supa.auth.getUser()
  if (authErr || !user) {
    return new Response('Unauthorized', { status: 401, headers: CORS })
  }

  let body: { subscription?: { endpoint: string; keys: { p256dh: string; auth: string } } }
  try {
    body = await req.json()
  } catch {
    return new Response('Bad Request: JSON inválido', { status: 400, headers: CORS })
  }

  const sub = body?.subscription
  if (!sub?.endpoint || !sub?.keys?.p256dh || !sub?.keys?.auth) {
    return new Response('Bad Request: campos ausentes', { status: 400, headers: CORS })
  }

  const { error } = await supa.from('push_subscriptions').upsert(
    {
      user_id: user.id,
      endpoint: sub.endpoint,
      p256dh: sub.keys.p256dh,
      auth: sub.keys.auth,
    },
    { onConflict: 'user_id,endpoint' }
  )

  if (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { ...CORS, 'Content-Type': 'application/json' },
    })
  }

  return new Response(JSON.stringify({ ok: true }), {
    headers: { ...CORS, 'Content-Type': 'application/json' },
  })
})
