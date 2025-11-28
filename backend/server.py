from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os

app = FastAPI(title="TestSmith Backend")

# Serve static frontend
app.mount("/static", StaticFiles(directory="public"), name="static")

@app.get("/")
async def root():
    return FileResponse("public/index.html")


# -------------------------
# API MODELS
# -------------------------
class CodeFile(BaseModel):
    path: str
    content: str

class AnalyzeRequest(BaseModel):
    language: str
    files: List[CodeFile]
    entrypoint: Optional[str] = None

class GenerateRequest(AnalyzeRequest):
    options: Optional[Dict[str, Any]] = {}

class RunTestsRequest(BaseModel):
    language: str
    files: Optional[List[CodeFile]] = None
    test_files: Optional[List[CodeFile]] = None


# -------------------------
# API ROUTES
# -------------------------
@app.post('/analyze')
async def analyze(req: AnalyzeRequest):
    from analyzer import analyze_code
    return analyze_code(req.language, req.files, req.entrypoint)

@app.post('/generate-tests')
async def generate_tests(req: GenerateRequest):
    from analyzer import analyze_code
    from generator import generate_tests_for_project
    analysis = analyze_code(req.language, req.files, req.entrypoint)
    tests = generate_tests_for_project(req.language, req.files, analysis, req.options)
    return {'tests': tests}

@app.post('/run-tests')
async def run_tests(req: RunTestsRequest):
    from runner import run_tests_in_sandbox
    return run_tests_in_sandbox(req.language, req.files or [], req.test_files or [])

@app.get('/suggest-ci')
async def suggest_ci():
    with open('ci_template.yml', 'r') as f:
        return {'ci': f.read()}


# -------------------------
# Run with: uvicorn server:app --reload
# -------------------------
