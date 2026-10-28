from fastapi import FastAPI

app = FastAPI(
    title="Justice Notes API",
    description="An API for tracking moral dilemmas and votes.",
    version='0.1.0'
)

@app.get("/")
async def root():
    return {"message": "Justice Notes API is running"}

@app.get("/health")    
async def health_check():
    return {"status": "OK"}