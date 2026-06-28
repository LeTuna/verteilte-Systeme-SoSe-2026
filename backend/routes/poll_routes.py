from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import update
from datetime import datetime
import uuid

from db import get_db, get_or_create_voter_id
from models.db_models import PollDB, OptionDB, VoteDB
from models.polls import PollCreate

router = APIRouter(prefix="/polls", tags=["Polls"])

@router.post("/")
def create_poll(poll: PollCreate, db: Session = Depends(get_db)):
    poll_id = str(uuid.uuid4())

    db_poll = PollDB(
        id=poll_id,
        title=poll.title,
        description=poll.description,
        visibility=poll.visibility,
        expires_at=poll.expires_at
    )

    db.add(db_poll)

    options_response = []

    for opt in poll.options:
        option_id = str(uuid.uuid4())

        db.add(OptionDB(
            id=option_id,
            text=opt.text,
            votes=0,
            poll_id=poll_id
        ))

        options_response.append({
            "id": option_id,
            "text": opt.text,
            "votes": 0
        })

    db.commit()

    return {
        "id": poll_id,
        "title": poll.title,
        "description": poll.description,
        "visibility": poll.visibility.value,
        "expires_at": poll.expires_at,
        "options": options_response
    }

@router.get("/")
def get_all_polls(db: Session = Depends(get_db)):
    polls = db.query(PollDB).filter(
        PollDB.visibility == "public"
    ).all()

    return [
        {
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "visibility": p.visibility
        }
        for p in polls
    ]

@router.get("/{poll_id}")
def get_poll(poll_id: str, db: Session = Depends(get_db)):
    poll = db.query(PollDB).filter(PollDB.id == poll_id).first()

    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")

    return {
        "id": poll.id,
        "title": poll.title,
        "description": poll.description,
        "visibility": poll.visibility,
        "expires_at": poll.expires_at,
        "options": [
            {
                "id": opt.id,
                "text": opt.text,
                "votes": opt.votes
            }
            for opt in poll.options
        ]
    }

@router.post("/{poll_id}/vote/{option_id}")
def vote(poll_id: str, option_id: str, response: Response, db: Session = Depends(get_db), voter_id: str = Depends(get_or_create_voter_id)):

    poll = db.query(PollDB).filter(PollDB.id == poll_id).first()

    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    
    if poll.expires_at and poll.expires_at < datetime.utcnow():
        raise HTTPException(status_code=403, detail="Poll expired")
    
    existing_vote = db.query(VoteDB).filter(
        VoteDB.poll_id == poll_id,
        VoteDB.voter_id == voter_id
    ).first()

    if existing_vote:
        raise HTTPException(status_code=403, detail="Already voted")

    result = db.execute(
        update(OptionDB)
        .where(
            OptionDB.id == option_id,
            OptionDB.poll_id == poll_id
        )
        .values(votes=OptionDB.votes + 1)
        .returning(OptionDB.votes)
    )

    row = result.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Option not found")

    db.commit()

    response.set_cookie(
        key="voter_id",
        value=voter_id,
        httponly=True,
        samesite="lax"
    )

    return {
        "message": "vote counted",
        "votes": row[0]
    }