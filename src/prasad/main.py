from fastapi import FastAPI
from prasad.auth.routers.authentication import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from prasad.db.db import init_db, drop_user_collection

STATIC_DIR = "static"

app = FastAPI(
    title="Prasad",
    version="1.0",
    description="Prasad",
)



origins = [
    "http://localhost",
    "http://localhost:8000",
    "https://prasad.mtscorporate.com",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="src/prasad/static"), name="static")


@app.on_event("startup")
async def startup():
    await  init_db()

@app.get("/",tags=["Root"])
async def root():
    return {"message": "Hello Prasad"}

@app.delete("/drop-collection",tags=["Drop Collection"])
async def drop_collection():
    await drop_user_collection()
    return {"message": "Collection dropped successfully"}



### routers
app.include_router(auth_router,prefix="/api/v1")
