/* ===============================
   COOKIE CONSENT (MODAL BASED)
================================ */

const modalEl = document.getElementById('cookieConsentModal');
const modal = new bootstrap.Modal(modalEl);

/* ---------- Google consent ---------- */

function updateConsent(analytics, marketing) {
  if (!window.gtag) return;

  gtag('consent', 'update', {
    analytics_storage: analytics ? 'granted' : 'denied',
    ad_storage: marketing ? 'granted' : 'denied',
    functionality_storage: 'granted',
    security_storage: 'granted'
  });
}

/* ---------- Actions ---------- */

function acceptAllCookies() {
  localStorage.setItem('cookie_consent', 'accepted');
  updateConsent(true, true);
  modal.hide();
}

function rejectAllCookies() {
  localStorage.setItem('cookie_consent', 'rejected');
  updateConsent(false, false);
  modal.hide();
}

function saveCustomPreferences() {
  const analytics = document.getElementById('analyticsCookies').checked;
  const marketing = document.getElementById('marketingCookies').checked;

  localStorage.setItem(
    'cookie_consent',
    JSON.stringify({ analytics, marketing })
  );

  updateConsent(analytics, marketing);
  modal.hide();
}

/* ---------- Reset ---------- */

function resetCookieSettings() {
  localStorage.removeItem('cookie_consent');
  modal.show();
}

/* ---------- Init ---------- */

window.addEventListener('load', () => {
  const consent = localStorage.getItem('cookie_consent');

  if (!consent) {
    modal.show();
    return;
  }

  if (consent === 'accepted') {
    updateConsent(true, true);
  } else if (consent === 'rejected') {
    updateConsent(false, false);
  } else {
    try {
      const prefs = JSON.parse(consent);
      updateConsent(!!prefs.analytics, !!prefs.marketing);
    } catch {
      modal.show();
    }
  }
});
