from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from datetime import datetime

class Visibility(str, Enum):
    public = "public"
    unlisted = "unlisted"

class Option(BaseModel):
    id: str | None = None
    text: str
    votes: int = 0

class PollCreate(BaseModel):
    title: str
    description: str | None = None
    visibility: Visibility = Visibility.public
    expires_at: Optional[datetime] = None
    options: List[Option]

class Poll(BaseModel):
    id: str
    title: str
    description: str | None = None
    visibility: Visibility
    expires_at: Optional[datetime] = None
    options: List[Option]