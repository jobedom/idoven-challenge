from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.main import router as api_router

app = FastAPI(title="idoven-challenge")

app.include_router(api_router, prefix="/api")


@app.get("/", include_in_schema=False)
async def health() -> JSONResponse:
    return JSONResponse({"message": "Alive!"})
