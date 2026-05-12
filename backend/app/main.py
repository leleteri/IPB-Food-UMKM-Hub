import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .auth import routers as auth
from .order import routers as order

app = FastAPI()

origins = ["http:localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(order.router)


@app.get("/")
async def root():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
