import uvicorn
from fastapi import Depends, FastAPI
from .database import create_db_and_tables
from .routers import health, token, books, authors, me
from .dependencies.authentication import get_current_user
app = FastAPI(title="Bibliotrek API")

app.include_router(health.router, dependencies=[Depends(get_current_user)])
app.include_router(books.router, dependencies=[Depends(get_current_user)])
app.include_router(authors.router, dependencies=[Depends(get_current_user)])
app.include_router(token.router)
app.include_router(me.router, dependencies=[Depends(get_current_user)])
@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()

def run() -> None:
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    run()
