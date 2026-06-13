// Service Worker — Portal sabendo.app (André 5º ano)
const CACHE_NAME = 'sabendo-v1';

// Arquivos essenciais para funcionar offline (shell mínima)
const SHELL_URLS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/icons/icon-192.png',
];

// ── Install: pré-cache da shell ──────────────────────────
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(SHELL_URLS))
  );
  self.skipWaiting();
});

// ── Activate: limpa caches antigos ───────────────────────
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// ── Fetch: network-first, fallback para cache ─────────────
self.addEventListener('fetch', (event) => {
  // Só intercepta GETs do mesmo origem
  if (event.request.method !== 'GET') return;
  const url = new URL(event.request.url);
  if (url.origin !== self.location.origin) return;

  event.respondWith(
    fetch(event.request)
      .then((response) => {
        // Salva no cache apenas respostas bem-sucedidas de recursos estáticos
        if (response.ok && (url.pathname.endsWith('.html') || url.pathname === '/')) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
        }
        return response;
      })
      .catch(() => caches.match(event.request))
  );
});

// ── Push: recebe notificação do servidor ──────────────────
self.addEventListener('push', (event) => {
  let data = {
    title: '⚡ Sabendo.app',
    body: 'Você tem atividades para reforçar hoje!',
    icon: '/icons/icon-192.png',
    badge: '/icons/icon-192.png',
    tag: 'reforco',
    renotify: false,
    data: { url: '/?section=reforco' },
  };

  if (event.data) {
    try {
      const parsed = event.data.json();
      data = { ...data, ...parsed };
    } catch {
      data.body = event.data.text();
    }
  }

  event.waitUntil(
    self.registration.showNotification(data.title, {
      body: data.body,
      icon: data.icon,
      badge: data.badge,
      tag: data.tag,
      renotify: data.renotify,
      data: data.data,
      vibrate: [200, 100, 200],
      actions: [
        { action: 'open', title: 'Ver reforços' },
        { action: 'dismiss', title: 'Agora não' },
      ],
    })
  );
});

// ── Notification click ────────────────────────────────────
self.addEventListener('notificationclick', (event) => {
  event.notification.close();

  if (event.action === 'dismiss') return;

  const targetUrl = (event.notification.data && event.notification.data.url)
    ? event.notification.data.url
    : '/?section=reforco';

  event.waitUntil(
    self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then((clients) => {
      // Se o portal já está aberto, foca e navega
      for (const client of clients) {
        const clientUrl = new URL(client.url);
        if (clientUrl.origin === self.location.origin) {
          client.focus();
          client.navigate(targetUrl);
          return;
        }
      }
      // Se não está aberto, abre
      return self.clients.openWindow(targetUrl);
    })
  );
});

// ── Recebe chave VAPID do cliente ─────────────────────────
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'VAPID_KEY') {
    self._vapidPublicKey = event.data.key;
  }
});

// ── Push subscription change (renovação automática) ───────
self.addEventListener('pushsubscriptionchange', (event) => {
  event.waitUntil(
    self.registration.pushManager.subscribe({
      userVisibleOnly: true,
      applicationServerKey: self._vapidPublicKey,
    }).then((subscription) => {
      // Envia a nova subscription para o Supabase via fetch
      return fetch('https://mmtrzxmitklpibfilbio.supabase.co/functions/v1/push-subscribe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ subscription }),
      });
    })
  );
});
