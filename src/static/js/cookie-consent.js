/* ===============================
   COOKIE CONSENT SCRIPT
================================ */

const banner = document.getElementById('cookieBanner');
const settingsModalEl = document.getElementById('cookieSettingsModal');

/* ---------- Banner helpers ---------- */

function showBanner() {
  banner.classList.remove('d-none');
}

function hideBanner() {
  banner.classList.add('d-none');
}

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

/* ---------- User actions ---------- */

function acceptCookies() {
  localStorage.setItem('cookie_consent', 'accepted');
  updateConsent(true, true);
  hideBanner();
}

function rejectCookies() {
  localStorage.setItem('cookie_consent', 'rejected');
  updateConsent(false, false);
  hideBanner();
}

function savePreferences() {
  const analytics = document.getElementById('analyticsCookies').checked;
  const marketing = document.getElementById('marketingCookies').checked;

  localStorage.setItem(
    'cookie_consent',
    JSON.stringify({ analytics, marketing })
  );

  updateConsent(analytics, marketing);

  const modal = bootstrap.Modal.getInstance(settingsModalEl);

  settingsModalEl.addEventListener(
    'hidden.bs.modal',
    () => hideBanner(),
    { once: true }
  );

  modal.hide();
}

/* ---------- Init ---------- */

window.addEventListener('load', () => {
  const consent = localStorage.getItem('cookie_consent');

  if (!consent) {
    showBanner();
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
      showBanner();
    }
  }
});

/* ---------- Open from footer ---------- */

function openCookieSettings() {
  new bootstrap.Modal(settingsModalEl).show();
}
