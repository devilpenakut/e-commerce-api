from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import shopee  # Import the test router
from app.routers import tokopedia
from app.routers import bli_bli

def get_application():
    _app = FastAPI(title="Enablr API", version="0.0.1")

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.include_router(shopee.router)  
    _app.include_router(tokopedia.router)
    _app.include_router(bli_bli.router)

    return _app

app = get_application()
