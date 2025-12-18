/* ===============================
   COOKIE CONSENT – SINGLE MODAL
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

/* ---------- Helpers ---------- */

function setToggleState(analytics, marketing) {
  document.getElementById('analyticsCookies').checked = analytics;
  document.getElementById('marketingCookies').checked = marketing;
}

/* ---------- Actions ---------- */

function acceptAllCookies() {
  localStorage.setItem('cookie_consent', 'accepted');
  setToggleState(true, true);
  updateConsent(true, true);
  modal.hide();
}

function rejectAllCookies() {
  localStorage.setItem('cookie_consent', 'rejected');
  setToggleState(false, false);
  updateConsent(false, false);
  modal.hide();
}

function openCookieManager() {
  const consent = localStorage.getItem('cookie_consent');

  if (consent && consent !== 'accepted' && consent !== 'rejected') {
    try {
      const prefs = JSON.parse(consent);
      setToggleState(!!prefs.analytics, !!prefs.marketing);
    } catch {}
  }

  modal.show();
}

/* ---------- Save on toggle change ---------- */

document.getElementById('analyticsCookies').addEventListener('change', saveCustom);
document.getElementById('marketingCookies').addEventListener('change', saveCustom);

function saveCustom() {
  const analytics = document.getElementById('analyticsCookies').checked;
  const marketing = document.getElementById('marketingCookies').checked;

  localStorage.setItem(
    'cookie_consent',
    JSON.stringify({ analytics, marketing })
  );

  updateConsent(analytics, marketing);
}

/* ---------- Init ---------- */

window.addEventListener('load', () => {
  const consent = localStorage.getItem('cookie_consent');

  if (!consent) {
    modal.show();
    return;
  }

  if (consent === 'accepted') {
    setToggleState(true, true);
    updateConsent(true, true);
  } else if (consent === 'rejected') {
    setToggleState(false, false);
    updateConsent(false, false);
  } else {
    try {
      const prefs = JSON.parse(consent);
      setToggleState(!!prefs.analytics, !!prefs.marketing);
      updateConsent(!!prefs.analytics, !!prefs.marketing);
    } catch {
      modal.show();
    }
  }
});
