/* ===============================
   COOKIE CONSENT (FINAL)
================================ */

const modalEl = document.getElementById('cookieConsentModal');
const modal = new bootstrap.Modal(modalEl);

/* Update Google Consent */
function updateConsent(analytics, marketing) {
  if (!window.gtag) return;

  gtag('consent', 'update', {
    analytics_storage: analytics ? 'granted' : 'denied',
    ad_storage: marketing ? 'granted' : 'denied',
    functionality_storage: 'granted',
    security_storage: 'granted'
  });
}

/* Delete existing cookies */
function deleteCookies() {
  document.cookie.split(';').forEach(cookie => {
    const name = cookie.split('=')[0].trim();

    document.cookie =
      name + '=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/';

    document.cookie =
      name + '=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/;domain=' + location.hostname;
  });
}

/* 🔥 NEW: Force cleanup after modal closes */
function cleanupModal() {
  setTimeout(() => {
    document.body.style.removeProperty('padding-right');
    document.body.style.removeProperty('overflow');
    document.body.classList.remove('modal-open');
    
    // Remove backdrop if stuck
    const backdrop = document.querySelector('.modal-backdrop');
    if (backdrop) backdrop.remove();
    
    // Force remove any inline styles Bootstrap might have added
    document.querySelectorAll('.navbar, .fixed-top, header').forEach(el => {
      el.style.removeProperty('padding-right');
    });
  }, 100);
}

/* Accept */
function acceptCookies() {
  localStorage.setItem(
    'cookie_consent',
    JSON.stringify({ analytics: true, marketing: true })
  );

  updateConsent(true, true);
  modal.hide();
  cleanupModal(); // 🔥 Added
}

/* Reject */
function rejectCookies() {
  localStorage.setItem(
    'cookie_consent',
    JSON.stringify({ analytics: false, marketing: false })
  );

  updateConsent(false, false);
  deleteCookies();
  modal.hide();
  cleanupModal(); // 🔥 Added
}

/* Open manually */
function openCookieManager() {
  modal.show();
}

/* Init on load */
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

/* 🔥 NEW: Listen to modal close event for extra safety */
modalEl.addEventListener('hidden.bs.modal', () => {
  cleanupModal();
});