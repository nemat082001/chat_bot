# src/jarvis_backend.py
"""
FastAPI backend server for JARVIS system
Connects React frontend with your existing Python components
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import sys
import os

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import your existing components
from integrate_jarvis_fixed import CompleteJarvisSystem
from complete_jarvis_advanced_features import JarvisFormulaCalculator

app = FastAPI(title="JARVIS API", version="1.0.0")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize your JARVIS system
jarvis_system = None

class QueryRequest(BaseModel):
    query: str
    session_id: Optional[str] = "default"
    input_data: Optional[Dict[str, Any]] = None

class CalculationRequest(BaseModel):
    formula_id: int
    inputs: Dict[str, float]

class StepRequest(BaseModel):
    step_name: str
    input_data: Dict[str, Any]
    session_id: Optional[str] = "default"

@app.on_event("startup")
async def startup_event():
    """Initialize JARVIS system on startup"""
    global jarvis_system
    print("🚀 Initializing JARVIS system...")
    jarvis_system = CompleteJarvisSystem()
    
    if jarvis_system.setup_system():
        print("✅ JARVIS system ready!")
    else:
        print("❌ Failed to initialize JARVIS system")

@app.get("/")
async def root():
    return {"message": "JARVIS API is running", "status": "ready"}

@app.get("/system-info")
async def get_system_info():
    """Get system status and information"""
    if not jarvis_system:
        raise HTTPException(status_code=500, detail="System not initialized")
    
    return jarvis_system.get_system_info()

@app.post("/query")
async def process_query(request: QueryRequest):
    """Main query endpoint - routes to appropriate handler"""
    if not jarvis_system:
        raise HTTPException(status_code=500, detail="System not initialized")
    
    try:
        result = jarvis_system.query(
            request.query, 
            session_id=request.session_id,
            input_data=request.input_data
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/calculate")
async def calculate_formula(request: CalculationRequest):
    """Direct formula calculation endpoint"""
    calculator = JarvisFormulaCalculator()
    
    try:
        result = calculator.calculate(request.formula_id, request.inputs)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/pipeline-step")
async def execute_pipeline_step(request: StepRequest):
    """Execute specific pipeline step"""
    if not jarvis_system:
        raise HTTPException(status_code=500, detail="System not initialized")
    
    try:
        result = jarvis_system.advanced_chatbot.pipeline.execute_step(
            request.step_name, 
            request.input_data
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/formulas")
async def get_available_formulas():
    """Get list of available formulas"""
    calculator = JarvisFormulaCalculator()
    return {
        "formulas": calculator.formula_names,
        "total_count": len(calculator.formula_names)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)