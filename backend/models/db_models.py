from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db import Base

class PollDB(Base):
    __tablename__ = "polls"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    visibility = Column(String, nullable=False)

    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    options = relationship("OptionDB", back_populates="poll", cascade="all, delete-orphan")


class OptionDB(Base):
    __tablename__ = "options"

    id = Column(String, primary_key=True, index=True)
    text = Column(String, nullable=False)
    votes = Column(Integer, default=0)

    poll_id = Column(String, ForeignKey("polls.id"))
    poll = relationship("PollDB", back_populates="options")

class VoteDB(Base):
    __tablename__ = "votes"

    id = Column(String, primary_key=True, index=True)

    poll_id = Column(String, ForeignKey("polls.id"), nullable=False)
    option_id = Column(String, ForeignKey("options.id"), nullable=False)

    voter_id = Column(String, index=True, nullable=False)