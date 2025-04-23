from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from pycomm3 import LogixDriver
import os

router = APIRouter()

PLC_IP = os.getenv("PLC_IP", "192.168.1.10")  # Default IP; override in .env

class WriteTag(BaseModel):
    tag: str
    value: str

@router.get("/tags")
def read_tags(tags: list[str] = Query(...)):
    try:
        with LogixDriver(PLC_IP) as plc:
            result = plc.read(*tags)
            return {tag: r.value for tag, r in zip(tags, result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/write")
def write_tag(data: WriteTag):
    try:
        with LogixDriver(PLC_IP) as plc:
            result = plc.write((data.tag, data.value))
            return {"success": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))