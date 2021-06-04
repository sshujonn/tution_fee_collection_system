class EnvConst():
    PROD="production"
    DEV="development"
    ACTIVE=DEV


if EnvConst.ACTIVE == EnvConst.DEV:
    CURRENT_SITE_URL = "127.0.0.1:8000"
elif EnvConst.ACTIVE == EnvConst.PROD:
    CURRENT_SITE_URL = ""