from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import route, incident, simulate
from app.routes import test
from app.routes import qr
from app.routes import relay   # 🔥 NEW

app = FastAPI(title="PLIS Backend API")

# ✅ CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Register routers (ALL HERE)
app.include_router(route.router)
app.include_router(incident.router)
app.include_router(simulate.router)
app.include_router(test.router)
app.include_router(qr.router)
app.include_router(relay.router)   # 🔥 NEW

@app.get("/")
def home():
    return {"message": "PLIS Backend Running 🚀"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/favicon.ico")
def favicon():
    return {}