from fastapi import FastAPI, Request

from fastapi.responses import JSONResponse

from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your React app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

appointment_data = {
    1: {"appointment_id": 6789,
        "name": "Sudip Halder",
        "age": 30,
        "aadhar": "5012",
        },
    2: {"id": 2,
        "name": "Aahnik Daw",
        "age": 30,
        "aadhar": "3096",
        }}

user_data = {
    12345: {"name": "Sudip Halder",
            "age": 30,
            "aadhar": "5012",
            "appointment_id": 6789,
            }
}


@app.get("/ping")
async def root():
    data = {"message": "connected"}
    return JSONResponse(content=data)


@app.get("/api/get-qr-data/{userid}")
async def get_data(userid: int):
    data = {
        "appointment_id": user_data[userid]["appointment_id"],
        "aadhar": user_data[userid]["aadhar"]
    }
    return JSONResponse(content=data)


@app.post("/api/scan")
async def scan_qr(request: Request):
    data = await request.json()
    appointment_id = data.get("appointment_id")
    client_aadhar = data.get("aadhar")
    verified = (appointment_data[appointment_id]["aadhar"] == client_aadhar)
    if verified:
        send_data = json.dumps({
            "verified": True,
            "queue_number": 4,
        })
    else:
        send_data = json.dumps({"verified": True})
    return send_data
