/* ===============================
   SIMPLE COOKIE CONSENT
================================ */

const modalEl = document.getElementById('cookieConsentModal');
const modal = new bootstrap.Modal(modalEl);

/* Google Consent Mode */
function updateConsent(analytics, marketing) {
  if (!window.gtag) return;

  gtag('consent', 'update', {
    analytics_storage: analytics ? 'granted' : 'denied',
    ad_storage: marketing ? 'granted' : 'denied',
    functionality_storage: 'granted',
    security_storage: 'granted'
  });
}

/* Actions */
function acceptCookies() {
  localStorage.setItem(
    'cookie_consent',
    JSON.stringify({ analytics: true, marketing: true })
  );

  updateConsent(true, true);
  modal.hide();
}

function rejectCookies() {
  localStorage.setItem(
    'cookie_consent',
    JSON.stringify({ analytics: false, marketing: false })
  );

  updateConsent(false, false);
  modal.hide();
}

/* Open manually */
function openCookieManager() {
  modal.show();
}

/* Init */
window.addEventListener('load', () => {
  const consent = localStorage.getItem('cookie_consent');

  if (!consent) {
    modal.show();
    return;
  }

  try {
    const prefs = JSON.parse(consent);
    updateConsent(!!prefs.analytics, !!prefs.marketing);
  } catch {
    modal.show();
  }
});
