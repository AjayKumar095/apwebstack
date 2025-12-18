/* ===============================
   COOKIE CONSENT (BANNER VERSION)
================================ */

const banner = document.getElementById('cookieBanner');

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
    document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/';
    document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/;domain=' + location.hostname;
  });
}

/* Hide banner with animation */
function hideBanner() {
  banner.classList.remove('show');
}

/* Accept */
function acceptCookies() {
  localStorage.setItem(
    'cookie_consent',
    JSON.stringify({ analytics: true, marketing: true })
  );
  updateConsent(true, true);
  hideBanner();
}

/* Reject */
function rejectCookies() {
  localStorage.setItem(
    'cookie_consent',
    JSON.stringify({ analytics: false, marketing: false })
  );
  updateConsent(false, false);
  deleteCookies();
  hideBanner();
}

/* Open manually (if you add a "Cookie Settings" link in footer) */
function openCookieManager() {
  banner.classList.add('show');
}

/* Check consent on load */
(function() {
  const consent = localStorage.getItem('cookie_consent');
  
  if (consent) {
    try {
      const prefs = JSON.parse(consent);
      updateConsent(!!prefs.analytics, !!prefs.marketing);
    } catch {
      // Show banner if data is corrupt
      setTimeout(() => banner.classList.add('show'), 500);
    }
  } else {
    // Show banner if no consent
    setTimeout(() => banner.classList.add('show'), 500);
  }
})();