from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import route, incident, simulate
from app.routes import test
from app.routes import qr
from app.routes import relay

app = FastAPI(title="PLIS Backend API")

# ✅ FIXED CORS (IMPORTANT CHANGE)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://sarvasvachaubey.github.io"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Register routers (NO CHANGE)
app.include_router(route.router)
app.include_router(incident.router)
app.include_router(simulate.router)
app.include_router(test.router)
app.include_router(qr.router)
app.include_router(relay.router)

@app.get("/")
def home():
    return {"message": "PLIS Backend Running 🚀"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/favicon.ico")
def favicon():
    return {}