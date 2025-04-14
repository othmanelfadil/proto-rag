from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# table for user info
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

# table to retain chat history (should use langraph for better persistence)    
class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    question = Column(String)
    answer = Column(String)

 # record token usage by user (if relevant model is used)    
class TokenUsage(Base):
    __tablename__ = "token_usage"
    user_id = Column(Integer, ForeignKey("users.id"))
    tokens_used = Column(Integer)
                             