"""
AI Commerce Agent - Main FastAPI Application
Unified agent handling conversation, text-based recommendations, and image-based search
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import base64
import json
import os

from agent import CommerceAgent
from database import init_database, get_all_products

app = FastAPI(
    title="AI Commerce Agent API",
    description="Unified agent for commerce website with conversation, text-based recommendations, and image-based search",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_database()
    print("Database initialized")

# Request/Response models
class MessageRequest(BaseModel):
    message: str
    conversation_history: Optional[List[dict]] = []

class ImageSearchRequest(BaseModel):
    conversation_history: Optional[List[dict]] = []

class AgentResponse(BaseModel):
    response: str
    products: Optional[List[dict]] = None
    response_type: str  # 'conversation', 'text_recommendation', 'image_search'

# Initialize agent
agent = CommerceAgent()

@app.get("/")
async def root():
    return {
        "message": "AI Commerce Agent API",
        "version": "1.0.0",
        "endpoints": {
            "/chat": "POST - Handle conversation and text-based product recommendations",
            "/image-search": "POST - Handle image-based product search",
            "/products": "GET - Get all available products",
            "/health": "GET - Health check"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/products")
async def get_products():
    """Get all products in the catalog"""
    try:
        products = get_all_products()
        return {"products": products, "count": len(products)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=AgentResponse)
async def chat_with_agent(request: MessageRequest):
    """
    Unified chat endpoint for conversation and text-based product recommendations
    """
    try:
        # Check if message contains image or if it's a general query
        message_lower = request.message.lower()
        
        # Route to appropriate agent function
        result = agent.handle_message(
            message=request.message,
            history=request.conversation_history
        )
        
        return AgentResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/image-search")
async def image_search(image: UploadFile = File(...)):
    """
    Handle image-based product search
    """
    try:
        # Read image file
        image_data = await image.read()
        
        # Convert to base64 for processing
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        # Process image with agent
        result = agent.handle_image_search(
            image_data=image_base64,
            image_format=image.content_type,
            history=[]
        )
        
        return AgentResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

