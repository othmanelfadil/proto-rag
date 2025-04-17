from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .models import User, TokenUsage, Conversation
from .database import get_db, init_db
from .auth import hash_password, verify_password, create_access_token, get_current_user
from .rag import ingest_document, answer_question, generate_exam
from pydantic import BaseModel
import os 

app = FastAPI()

class UserCreate(BaseModel):
    username: str
    password: str
    
class QuestionRequest(BaseModel):
    question: str
    
class ExamRequest(BaseModel):
    num_questions: int
    
init_db()

@app.post("/register")
def register
  
