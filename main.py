from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="Justice Notes API",
    description="An API for tracking moral dilemmas and votes.",
    version="0.1.0"
)

# ==========================================
# 1. PYDANTIC MODELS (Data Schemas)
# ==========================================

class DilemmaCreate(BaseModel):
    title: str
    description: str

class DilemmaResponse(DilemmaCreate):
    id: int

# ==========================================
# 2. IN-MEMORY DATABASE (Temporary)
# ==========================================
# We use a dictionary to store dilemmas. 
# Key = id, Value = the dilemma object
fake_db = {}
current_id = 1

# ==========================================
# 3. ENDPOINTS
# ==========================================

@app.get("/")
async def root():
    return {"message": "Justice Notes API is running"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/dilemmas", response_model=DilemmaResponse, status_code=status.HTTP_201_CREATED)
async def create_dilemma(dilemma: DilemmaCreate):
    global current_id
    
    # Create the new dilemma object with an ID
    new_dilemma = DilemmaResponse(
        id=current_id,
        title=dilemma.title,
        description=dilemma.description
    )
    
    # Save to our fake database
    fake_db[current_id] = new_dilemma
    current_id += 1
    
    return new_dilemma

@app.get("/dilemmas", response_model=List[DilemmaResponse])
async def get_all_dilemmas():
    return list(fake_db.values())

@app.get("/dilemmas/{dilemma_id}", response_model=DilemmaResponse)
async def get_dilemma(dilemma_id: int):
    if dilemma_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Dilemma not found"
        )
    return fake_db[dilemma_id]