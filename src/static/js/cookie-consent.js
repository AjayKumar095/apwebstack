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
  hideBanner();

  bootstrap.Modal.getInstance(
    document.getElementById('cookieSettingsModal')
  ).hide();
}

function updateConsent(analytics, marketing) {
  if (window.gtag) {
    gtag('consent', 'update', {
      analytics_storage: analytics ? 'granted' : 'denied',
      ad_storage: marketing ? 'granted' : 'denied',
      functionality_storage: 'granted',
      security_storage: 'granted'
    });
  }
}

function hideBanner() {
  document.getElementById('cookieBanner').style.display = 'none';
}

function showBanner() {
  document.getElementById('cookieBanner').style.display = 'block';
}

window.addEventListener('load', () => {
  const consent = localStorage.getItem('cookie_consent');

  if (!consent) {
    showBanner();
  } else if (consent === 'accepted') {
    updateConsent(true, true);
  } else if (consent === 'rejected') {
    updateConsent(false, false);
  } else {
    const prefs = JSON.parse(consent);
    updateConsent(prefs.analytics, prefs.marketing);
  }
});

/* Optional: open settings from footer */
function openCookieSettings() {
  new bootstrap.Modal(
    document.getElementById('cookieSettingsModal')
  ).show();
}
