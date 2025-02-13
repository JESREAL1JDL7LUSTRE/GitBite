import os
import clerk_django
print(dir(clerk_django))

import site
print(site.getsitepackages())

import os
from dotenv import load_dotenv

load_dotenv()
clerk_frontend_url = os.getenv("CLERK_FRONTEND_API_URL")
if not clerk_frontend_url:
    raise ValueError("CLERK_FRONTEND_API_URL environment variable is not set.")

ALLOWED_PARTIES = [clerk_frontend_url]
print(ALLOWED_PARTIES)
