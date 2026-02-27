from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr, validator
from typing import List
from datetime import datetime

app = FastAPI(
    title="API Biblioteca Digital",
    version="1.0.0"
)