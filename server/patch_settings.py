from pathlib import Path
import re

settings_path = Path("djangoproj/settings.py")
settings = settings_path.read_text()

# Make the secret key configurable
settings, n = re.subn(
    r"SECRET_KEY\s*=\s*\\?\s*\n?\s*(['\"]).*?\1",
    'SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-only-change-this-key")',
    settings,
    count=1,
    flags=re.S,
)
assert n == 1, "Could not safely update SECRET_KEY"

# Make DEBUG configurable
settings = settings.replace(
    "DEBUG = True",
    'DEBUG = os.environ.get("DJANGO_DEBUG", "True").lower() == "true"',
    1,
)

# Add deployment hostnames to ALLOWED_HOSTS
settings = re.sub(
    r"ALLOWED_HOSTS\s*=\s*\[.*?\]",
    '''ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    ".theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai",
] + [
    host.strip()
    for host in os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")
    if host.strip()
]''',
    settings,
    count=1,
    flags=re.S,
)

# Add WhiteNoise middleware
if "whitenoise.middleware.WhiteNoiseMiddleware" not in settings:
    settings = settings.replace(
        "'django.middleware.security.SecurityMiddleware',",
        "'django.middleware.security.SecurityMiddleware',\n"
        "    'whitenoise.middleware.WhiteNoiseMiddleware',",
        1,
    )

# Use a separate directory for collected static files
settings = settings.replace(
    "STATIC_ROOT = os.path.join(BASE_DIR, 'static')",
    "STATIC_ROOT = BASE_DIR / 'collected_static'",
    1,
)

# Include React's generated JS and CSS files
settings = settings.replace(
    "STATICFILES_DIRS = [\n    BASE_DIR / 'frontend' / 'static',\n]",
    "STATICFILES_DIRS = [\n"
    "    BASE_DIR / 'frontend' / 'static',\n"
    "    BASE_DIR / 'frontend' / 'build' / 'static',\n"
    "]",
    1,
)

# Add deployment CSRF trusted origins
settings = re.sub(
    r"CSRF_TRUSTED_ORIGINS\s*=\s*\[\s*"
    r'"https://mohammadhuz1-8000\.theiadockernext-0-labs-prod-theiak8s-4-tor01\.proxy\.cognitiveclass\.ai",?\s*'
    r"\]",
    '''CSRF_TRUSTED_ORIGINS = [
    "https://mohammadhuz1-8000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai",
] + [
    origin.strip()
    for origin in os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]''',
    settings,
    count=1,
)

settings_path.write_text(settings)
print("Django settings updated.")
