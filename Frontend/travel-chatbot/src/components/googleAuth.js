const GOOGLE_CLIENT_ID = process.env.REACT_APP_GOOGLE_CLIENT_ID || "";

export const isGoogleEnabled = () => Boolean(GOOGLE_CLIENT_ID);

export const loadGoogleScript = (callback) => {
  if (!GOOGLE_CLIENT_ID) return;

  // Already loaded
  if (window.google?.accounts) {
    callback();
    return;
  }

  // Script tag already added but still loading — wait for it
  const existing = document.getElementById("google-gsi-script");
  if (existing) {
    existing.addEventListener("load", callback);
    return;
  }

  const script = document.createElement("script");
  script.id = "google-gsi-script";
  script.src = "https://accounts.google.com/gsi/client";
  script.async = true;
  script.defer = true;
  script.onload = callback;
  document.body.appendChild(script);
};

export const initGoogleButton = (elementId, handleCredentialResponse) => {
  if (!window.google?.accounts || !GOOGLE_CLIENT_ID) return;
  const el = document.getElementById(elementId);
  if (!el) return;

  window.google.accounts.id.initialize({
    client_id: GOOGLE_CLIENT_ID,
    callback: handleCredentialResponse,
    ux_mode: "popup",
  });
  window.google.accounts.id.renderButton(el, {
    theme: "outline",
    size: "large",
    width: 320,
  });
};
