from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import tempfile
import shutil
import json
import subprocess
from typing import Tuple

app = FastAPI(title="TestCaseGenBot Backend")

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

@app.post('/analyze')
async def analyze(req: AnalyzeRequest):
    from analyzer import analyze_code
    result = analyze_code(req.language, req.files, req.entrypoint)
    return result

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
    result = run_tests_in_sandbox(req.language, req.files or [], req.test_files or [])
    return result

@app.get('/suggest-ci')
async def suggest_ci():
    with open('ci_template.yml', 'r') as f:
        return {'ci': f.read()}