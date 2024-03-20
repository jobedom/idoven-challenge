import logging

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.main import router as api_router
from app.lib.password import get_hashed_password

# Hack for an issue with how passlib attempts to read a
# version from bcrypt (for logging only) and fails because
# it's loading modules that no longer exist in bcrypt 4.1.x.
# https://github.com/pyca/bcrypt/issues/684
logging.getLogger("passlib").setLevel(logging.ERROR)

app = FastAPI(title="idoven-challenge")

app.include_router(api_router, prefix="/api")

print(get_hashed_password("admin1234"))


@app.get("/", include_in_schema=False)
async def health() -> JSONResponse:
    return JSONResponse({"message": "Alive!"})
