import logging
from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timedelta
import jwt
import traceback
import csv
import io
from fastapi.responses import JSONResponse

# JWT Configuration
SECRET_KEY = "hello123"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Static admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"  

# Database setup
DATABASE_URL = "sqlite:///./feedback.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# OAuth2 Password Bearer Token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Models
class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    review_text = Column(String)
    sentiment = Column(String)
    confidence_score = Column(Float)

Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create JWT Token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Authenticate Admin
def authenticate_admin(username: str, password: str):
    return username == ADMIN_USERNAME and password == ADMIN_PASSWORD

# Get Current Admin from Token
def get_current_admin(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username != ADMIN_USERNAME:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# Admin Login
@app.post("/login/")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not authenticate_admin(form_data.username, form_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin credentials")
    
    access_token = create_access_token(data={"sub": form_data.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

# CSV Upload & Processing (Sentiment Analysis)
@app.post("/upload_csv/")
async def upload_csv(file: UploadFile = File(...), current_admin: str = Depends(get_current_admin)):
    """
    Upload CSV with 'id' and 'review_text' fields, process sentiment, and store results in 'export.csv'.
    """
    try:
        # Read the CSV file
        contents = await file.read()
        decoded = io.StringIO(contents.decode("utf-8"))
        csv_reader = csv.DictReader(decoded)

        # Prepare a list to hold processed rows
        processed_rows = []

        # Process each row in the CSV
        for row in csv_reader:
            review_text = row.get("review_text", "").strip()

            # Simple Sentiment Analysis (Replace with real model)
            sentiment = "positive" if "good" in review_text.lower() else "negative"
            confidence_score = 0.9 if sentiment == "positive" else 0.7  

            # Prepare the row with sentiment and confidence score
            processed_row = {
                "id": row.get("id", ""),
                "review_text": review_text,
                "sentiment": sentiment,
                "confidence_score": confidence_score
            }
            processed_rows.append(processed_row)

        # Save the results to export.csv
        with open("export.csv", "w", newline="", encoding="utf-8") as output_file:
            csv_writer = csv.DictWriter(output_file, fieldnames=["id", "review_text", "sentiment", "confidence_score"])
            csv_writer.writeheader()
            csv_writer.writerows(processed_rows)

        return JSONResponse(content={"message": "CSV processed and saved as 'export.csv'"}, status_code=200)

    except Exception as e:
        logging.error(f"Error occurred during CSV upload: {e}")
        logging.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error")
