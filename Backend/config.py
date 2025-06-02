# app/config.py
import os
from datetime import timedelta

SECRET_KEY = os.getenv("SECRET_KEY", "replace-with-a-secure‑random‑string")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 小时有效期
