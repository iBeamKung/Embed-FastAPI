from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import pytz
import sqlite3

app = FastAPI()

class DataDetail(BaseModel):
    Device: str
    Lat: float
    Lng: float
    Dust: int
    Temp: float

class RawDataDetail(BaseModel):
    Device: str
    Time: str
    Lat: float
    Lng: float
    Dust: int
    Temp: float

@app.get("/")
async def root():
    return {"message": "Hello. Welcome to Embeded Project App!"}

@app.get("/data")
async def get_data():
    conn = sqlite3.connect("embed-data.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM embed")
    rows = cur.fetchall()
    data = [dict(row) for row in rows]
    return data

@app.post("/add-data")
async def add_data(detail_input: DataDetail):
    conn = sqlite3.connect("embed-data.db")
    cursor = conn.cursor()

    query = "INSERT INTO embed (Device, Time, Lat, Lng, Dust, Temp) VALUES (?, ?, ?, ?, ?, ?)"
    cursor.execute(query, (detail_input.Device, datetime.now(pytz.timezone('Asia/Bangkok')), detail_input.Lat, detail_input.Lng, detail_input.Dust, detail_input.Temp))

    conn.commit()
    conn.close()
    return {"message": "Item added to database"}

@app.post("/add-rawdata")
async def add_rawdata(detail_input: RawDataDetail):
    conn = sqlite3.connect("embed-data.db")
    cursor = conn.cursor()

    query = "INSERT INTO embed (Device, Time, Lat, Lng, Dust, Temp) VALUES (?, ?, ?, ?, ?, ?)"
    cursor.execute(query, (detail_input.Device, detail_input.Time, detail_input.Lat, detail_input.Lng, detail_input.Dust, detail_input.Temp))

    conn.commit()
    conn.close()
    return {"message": "Item Raw added to database"}

@app.post("/view-input")
async def create_item(itema: DataDetail):
    return itema

@app.get("/delete")
async def get_data():
    conn = sqlite3.connect("embed-data.db")
    cursor = conn.cursor()

    query = "DELETE FROM embed;"
    cursor.execute(query,)

    conn.commit()
    conn.close()
    return {"message": "Delete all Item in database"}
    return data