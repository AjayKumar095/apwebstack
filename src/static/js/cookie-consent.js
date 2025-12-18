/* ===============================
   COOKIE CONSENT – SWITCH BASED
================================ */

const modalEl = document.getElementById('cookieConsentModal');
const modal = new bootstrap.Modal(modalEl);

/* ---------- Google Consent ---------- */

function updateConsent(analytics, marketing) {
  if (!window.gtag) return;

  gtag('consent', 'update', {
    analytics_storage: analytics ? 'granted' : 'denied',
    ad_storage: marketing ? 'granted' : 'denied',
    functionality_storage: 'granted',
    security_storage: 'granted'
  });
}

/* ---------- Helpers ---------- */

function getSwitchState() {
  return {
    analytics: document.getElementById('analyticsCookies').checked,
    marketing: document.getElementById('marketingCookies').checked
  };
}

function setSwitchState(analytics, marketing) {
  document.getElementById('analyticsCookies').checked = analytics;
  document.getElementById('marketingCookies').checked = marketing;
}

/* ---------- Actions ---------- */

// ACCEPT → use switch state
function acceptCookies() {
  const { analytics, marketing } = getSwitchState();

  localStorage.setItem(
    'cookie_consent',
    JSON.stringify({ analytics, marketing })
  );

  updateConsent(analytics, marketing);
  modal.hide();
}

// REJECT → force optional cookies OFF
function rejectCookies() {
  setSwitchState(false, false);

  localStorage.setItem(
    'cookie_consent',
    JSON.stringify({ analytics: false, marketing: false })
  );

  updateConsent(false, false);
  modal.hide();
}

// Open from footer / header
function openCookieManager() {
  const consent = localStorage.getItem('cookie_consent');

  if (consent) {
    try {
      const prefs = JSON.parse(consent);
      setSwitchState(!!prefs.analytics, !!prefs.marketing);
    } catch {}
  }

  modal.show();
}

/* ---------- Init ---------- */

window.addEventListener('load', () => {
  const consent = localStorage.getItem('cookie_consent');

  if (!consent) {
    modal.show();
    return;
  }

  try {
    const prefs = JSON.parse(consent);
    setSwitchState(!!prefs.analytics, !!prefs.marketing);
    updateConsent(!!prefs.analytics, !!prefs.marketing);
  } catch {
    modal.show();
  }
});
