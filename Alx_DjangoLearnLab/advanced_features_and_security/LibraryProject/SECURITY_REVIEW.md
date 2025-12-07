# HTTPS & Secure Headers Configuration

## Django Settings
- SECURE_SSL_REDIRECT = True
- SECURE_HSTS_SECONDS = 31536000
- SESSION_COOKIE_SECURE = True
- CSRF_COOKIE_SECURE = True
- X_FRAME_OPTIONS = 'DENY'
- SECURE_CONTENT_TYPE_NOSNIFF = True
- SECURE_BROWSER_XSS_FILTER = True

## Deployment
- SSL/TLS configured via Nginx/Apache
- Certificates issued by Let's Encrypt

## Review Summary
- All traffic is forced to HTTPS
- Cookies and headers are secured
- Browser behavior hardened against downgrade and injection attacks