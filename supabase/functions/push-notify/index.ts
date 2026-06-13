// Edge Function: push-notify
// Verifica reinforcement_queue e envia push para cada usuário
// com itens cuja due_date <= now() e resolved_at IS NULL.
// Deve ser chamada via Supabase Cron (diariamente às 08:00 BRT = 11:00 UTC).

import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

// ── Helpers base64url ─────────────────────────────────────
function b64urlDecode(s: string): Uint8Array {
  const pad = '='.repeat((4 - (s.length % 4)) % 4)
  return Uint8Array.from(atob(s.replace(/-/g, '+').replace(/_/g, '/') + pad), (c) => c.charCodeAt(0))
}
function b64urlEncode(buf: ArrayBuffer): string {
  return btoa(String.fromCharCode(...new Uint8Array(buf)))
    .replace(/\+/g, '-').replace(/\//g, '_').replace(/=/g, '')
}

// ── VAPID JWT ─────────────────────────────────────────────
async function makeVapidJwt(
  audience: string,
  subject: string,
  publicKeyB64: string,
  privateKeyB64: string
): Promise<string> {
  const header = b64urlEncode(new TextEncoder().encode(JSON.stringify({ alg: 'ES256', typ: 'JWT' })))
  const now = Math.floor(Date.now() / 1000)
  const payload = b64urlEncode(new TextEncoder().encode(JSON.stringify({ aud: audience, exp: now + 43200, sub: subject })))
  const sigInput = `${header}.${payload}`

  // Importa chave privada raw (32 bytes P-256)
  const privRaw = b64urlDecode(privateKeyB64)
  // Constrói PKCS8 wrapper para P-256
  const pkcs8 = new Uint8Array([
    0x30, 0x41, 0x02, 0x01, 0x00, 0x30, 0x13, 0x06, 0x07, 0x2a, 0x86, 0x48,
    0xce, 0x3d, 0x02, 0x01, 0x06, 0x08, 0x2a, 0x86, 0x48, 0xce, 0x3d, 0x03,
    0x01, 0x07, 0x04, 0x27, 0x30, 0x25, 0x02, 0x01, 0x01, 0x04, 0x20,
    ...privRaw,
  ])

  const cryptoKey = await crypto.subtle.importKey('pkcs8', pkcs8, { name: 'ECDSA', namedCurve: 'P-256' }, false, ['sign'])
  const sigBytes = await crypto.subtle.sign({ name: 'ECDSA', hash: 'SHA-256' }, cryptoKey, new TextEncoder().encode(sigInput))

  // IEEE P1363 → DER (Supabase Deno já retorna P1363 de 64 bytes)
  return `${sigInput}.${b64urlEncode(sigBytes)}`
}

// ── Envio de push (sem payload — SW usa texto padrão) ────
// Para customizar o texto, o SW checa o Supabase ao receber o evento.
async function sendPush(endpoint: string, jwt: string, vapidPublicKey: string): Promise<number> {
  const res = await fetch(endpoint, {
    method: 'POST',
    headers: {
      Authorization: `vapid t=${jwt},k=${vapidPublicKey}`,
      TTL: '86400',
      Urgency: 'normal',
    },
  })
  return res.status
}

// ── Handler principal ─────────────────────────────────────
serve(async (req) => {
  // Autorização: Supabase Cron injeta x-supabase-cron; chamadas manuais usam Bearer secret
  const isCron = req.headers.get('x-supabase-cron') === '1'
  const isManual = req.headers.get('Authorization') === `Bearer ${Deno.env.get('CRON_SECRET') ?? ''}`
  if (!isCron && !isManual) {
    return new Response('Unauthorized', { status: 401 })
  }

  const VAPID_PUBLIC = Deno.env.get('VAPID_PUBLIC_KEY')!
  const VAPID_PRIVATE = Deno.env.get('VAPID_PRIVATE_KEY')!
  const VAPID_SUBJECT = Deno.env.get('VAPID_SUBJECT')!

  // Usa service role para leitura irrestrita
  const supa = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
  )

  // 1. Usuários com reforços vencidos
  const { data: dueItems, error: qErr } = await supa
    .from('reinforcement_queue')
    .select('user_id')
    .lte('due_date', new Date().toISOString())
    .is('resolved_at', null)

  if (qErr) return new Response(JSON.stringify({ error: qErr.message }), { status: 500 })
  if (!dueItems || dueItems.length === 0) {
    return new Response(JSON.stringify({ sent: 0, message: 'Nenhum reforço pendente' }), {
      headers: { 'Content-Type': 'application/json' },
    })
  }

  // Conta por usuário
  const countByUser: Record<string, number> = {}
  for (const row of dueItems) {
    countByUser[row.user_id] = (countByUser[row.user_id] ?? 0) + 1
  }
  const userIds = Object.keys(countByUser)

  // 2. Subscriptions desses usuários
  const { data: subs, error: sErr } = await supa
    .from('push_subscriptions')
    .select('user_id, endpoint, p256dh, auth')
    .in('user_id', userIds)

  if (sErr) return new Response(JSON.stringify({ error: sErr.message }), { status: 500 })
  if (!subs || subs.length === 0) {
    return new Response(JSON.stringify({ sent: 0, message: 'Nenhuma subscription ativa' }), {
      headers: { 'Content-Type': 'application/json' },
    })
  }

  // 3. Envia push para cada subscription
  let sent = 0, failed = 0
  for (const sub of subs) {
    try {
      const origin = new URL(sub.endpoint)
      const audience = `${origin.protocol}//${origin.host}`
      const jwt = await makeVapidJwt(audience, VAPID_SUBJECT, VAPID_PUBLIC, VAPID_PRIVATE)
      const status = await sendPush(sub.endpoint, jwt, VAPID_PUBLIC)

      if (status === 201 || status === 200 || status === 202) {
        sent++
      } else if (status === 410 || status === 404) {
        // Subscription expirada — remove da tabela
        await supa.from('push_subscriptions').delete().eq('endpoint', sub.endpoint)
        failed++
      } else {
        failed++
      }
    } catch (e) {
      console.error('Push error:', e)
      failed++
    }
  }

  return new Response(JSON.stringify({ sent, failed, usersTargeted: userIds.length }), {
    headers: { 'Content-Type': 'application/json' },
  })
})
