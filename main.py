from datetime import datetime
from enum import Enum
from typing import List, Optional

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Initialize FastAPI app
app = FastAPI(title="Trading App")

# ---------------------- EXCEPTION HANDLERS ----------------------


@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException):
    """Handle validation exceptions and return a custom JSON response."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


# ---------------------- MOCK DATA ----------------------

fake_users = [
    {
        "id": 1,
        "role": "admin",
        "name": "Bob",
        "degree": [
            {"id": 1, "created_at": "2023-06-01T00:30:00", "type_degree": "newbie"}
        ],
    },
    {
        "id": 2,
        "role": "investor",
        "name": "Rob",
        "degree": [
            {"id": 2, "created_at": "2018-03-01T00:00:00", "type_degree": "expert"}
        ],
    },
    {
        "id": 3,
        "role": "investor",
        "name": "Ivan",
        "degree": [
            {"id": 3, "created_at": "2023-04-01T00:00:00", "type_degree": "newbie"}
        ],
    },
    {
        "id": 4,
        "role": "trader",
        "name": "Fred",
        "degree": [
            {"id": 4, "created_at": "2019-01-01T00:00:00", "type_degree": "expert"}
        ],
    },
    {
        "id": 5,
        "role": "trader",
        "name": "John",
        "degree": [
            {"id": 5, "created_at": "2023-01-01T00:00:00", "type_degree": "expert"}
        ],
    },
    {"id": 6, "role": "trader", "name": "Rich"},
    {
        "id": 7,
        "role": "trader",
        "name": "Nick",
        "degree": [
            {"id": 7, "created_at": "2020-01-01T00:00:00", "type_degree": "newbie"}
        ],
    },
]
fake_users2 = [
    {"id": 1, "role": "admin", "name": "Bob"},
    {"id": 2, "role": "investor", "name": "Rob"},
    {"id": 3, "role": "investor", "name": "Ivan"},
    {"id": 4, "role": "trader", "name": "Fred"},
    {"id": 5, "role": "trader", "name": "John"},
    {"id": 6, "role": "trader", "name": "Rich"},
    {"id": 7, "role": "trader", "name": "Nick"},
]
fake_trades = [
    {
        "id": 1,
        "user_id": 1,
        "currency": "BTC",
        "side": "buy",
        "price": 123.0,
        "amount": 2.12,
    },
    {
        "id": 3,
        "user_id": 3,
        "currency": "BTC",
        "side": "sell",
        "price": 144.4,
        "amount": 2.12,
    },
    {
        "id": 2,
        "user_id": 2,
        "currency": "BTC",
        "side": "buy",
        "price": 123.0,
        "amount": 2.34,
    },
    {
        "id": 1,
        "user_id": 1,
        "currency": "BTC",
        "side": "buy",
        "price": 123.0,
        "amount": 2.54,
    },
]


# ---------------------- MODELS ----------------------


class DegreeType(Enum):
    newbie = "newbie"
    expert = "expert"


class Degree(BaseModel):
    """Model for user's degree."""

    id: int
    created_at: datetime
    type_degree: DegreeType


class User(BaseModel):
    """Model for user."""

    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] = None


class Trade(BaseModel):
    """Model for trade."""

    id: int
    user_id: int
    currency: str
    side: str
    price: float = Field(ge=0)
    amount: float


# ---------------------- ROUTES ----------------------


@app.get("/users/{user_id}", response_model=List[User])
def get_user(user_id: int):
    """Retrieve a user by their ID."""
    return [user for user in fake_users if user.get("id") == user_id]


@app.get("/trades")
def get_trades(limit: int = 3, offset: int = 0):
    """Retrieve trades with optional limit and offset."""
    return fake_trades[offset:][:limit]


@app.post("/user/{user_id}")
def change_user_name(user_id: int, new_name: str):
    """Change the name of a user by their ID."""
    current_user = list(filter(lambda user: user.get("id") == user_id, fake_users2))[0]
    current_user["name"] = new_name
    return {"status": 200, "data": current_user}


@app.post("/trades")
def add_trades(trades: List[Trade]):
    """Add new trades."""
    fake_trades.extend(trades)
    return {"status": 200, "data": fake_trades}


# ---------------------- MAIN ENTRY ----------------------

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
