import os
import subprocess
import tempfile
import shutil
from typing import List, Dict, Any


def write_files_to_dir(files: List[Dict[str, str]], base_dir: str):
    for f in files:
        path = os.path.join(base_dir, f['path'])
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(f['content'])


def run_tests_in_sandbox(language: str, files: List[Dict[str, str]], test_files: List[Dict[str, str]]):
    tmp = tempfile.mkdtemp(prefix='tcgb_')
    try:
        write_files_to_dir(files, tmp)
        write_files_to_dir(test_files, tmp)
        if language.lower() == 'python':
            cmd = ['coverage', 'run', '-m', 'pytest', '-q']
            proc = subprocess.run(cmd, cwd=tmp, capture_output=True, text=True)
            stdout = proc.stdout
            stderr = proc.stderr
            cov_cmd = ['coverage', 'json', '-o', 'coverage.json']
            subprocess.run(cov_cmd, cwd=tmp)
            cov_json = None
            cov_path = os.path.join(tmp, 'coverage.json')
            if os.path.exists(cov_path):
                with open(cov_path, 'r') as fh:
                    cov_json = fh.read()
            return {'returncode': proc.returncode, 'stdout': stdout, 'stderr': stderr, 'coverage': cov_json}
        elif language.lower() in ('javascript', 'js'):
            if not os.path.exists(os.path.join(tmp, 'package.json')):
                pj = {'name': 'autogen', 'version': '1.0.0', 'scripts': {'test': 'jest --json --outputFile=jest_output.json'}}
                with open(os.path.join(tmp, 'package.json'), 'w') as fh:
                    import json
                    fh.write(json.dumps(pj))
            subprocess.run(['npm', 'install', '--no-audit', '--no-fund'], cwd=tmp, capture_output=True, text=True)
            proc2 = subprocess.run(['npm', 'test'], cwd=tmp, capture_output=True, text=True)
            jest_out = None
            jest_path = os.path.join(tmp, 'jest_output.json')
            if os.path.exists(jest_path):
                with open(jest_path, 'r') as fh:
                    jest_out = fh.read()
            return {'returncode': proc2.returncode, 'stdout': proc2.stdout, 'stderr': proc2.stderr, 'jest': jest_out}
        elif language.lower() == 'java':
            subprocess.run(['mvn', '-v'], cwd=tmp, capture_output=True, text=True)
            run_proc = subprocess.run(['mvn', 'test'], cwd=tmp, capture_output=True, text=True)
            return {'returncode': run_proc.returncode, 'stdout': run_proc.stdout, 'stderr': run_proc.stderr}
        else:
            raise ValueError('Unsupported language')
    finally:
        shutil.rmtree(tmp)