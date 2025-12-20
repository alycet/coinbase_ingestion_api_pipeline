from fastapi import FastAPI, Request, Depends
import requests
import asyncio
from streamer import stream_and_post
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine
from typing import Annotated
from load import load_to_bigquery

class Coinbase(SQLModel, table = True):
    type: str
    sequence: int
    product_id: str
    price: float
    open_24h: Optional[str]
    volume_24h: Optional[str]
    low_24h: Optional[str]
    high_24h: Optional[str]
    volume_30d: Optional[str]
    best_bid: Optional[str]
    best_bid_size: Optional[str]
    best_ask: Optional[str]
    best_ask_size: Optional[str]
    side: Optional[str]
    time: str
    trade_id: int | None = Field(default=None, primary_key = True)
    last_size: Optional[str]



sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread" : False}
engine = create_engine(sqlite_url, echo = True, connect_args = connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    create_db_and_tables()
    task = asyncio.create_task(stream_and_post())
    yield
    # Shutdown logic (optional)
    task.cancel()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/ingest")
async def ingest_data(coinbase: Coinbase, session: SessionDep):
    try:
        print("Request received")
        session.add(coinbase)
        session.commit()
        session.refresh(coinbase)
        return {"status": "stored", "data": coinbase}
    except Exception as e:
        print("Error in /ingest:", e)
        return {"status": "error", "message": str(e)}
    
@app.post("/load-to-bigquery")
async def load_to_bq():
    try:
        rows = load_to_bigquery()
        return {"status": "success", "rows_uploaded": rows}
    except Exception as e:
        return {"status": "error", "message": str(e)}


