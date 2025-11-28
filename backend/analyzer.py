import ast
from typing import List, Dict, Any

def analyze_python(files: List[Dict[str, str]], entrypoint: str = None) -> Dict[str, Any]:
    functions = []
    classes = []
    for f in files:
        try:
            tree = ast.parse(f['content'])
        except Exception as e:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                args = [a.arg for a in node.args.args]
                functions.append({'name': node.name, 'args': args, 'lineno': node.lineno, 'file': f['path']})
            if isinstance(node, ast.ClassDef):
                methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                classes.append({'name': node.name, 'methods': methods, 'file': f['path']})
    edge_hints = []
    for f in files:
        text = f['content']
        if '/' in text:
            edge_hints.append('Check division by zero where / or // is used in ' + f['path'])
        if '[' in text and ']' in text:
            edge_hints.append('Check index bounds in ' + f['path'])
        if 'open(' in text:
            edge_hints.append('File I/O may raise exceptions in ' + f['path'])
        if 'requests' in text or 'socket' in text:
            edge_hints.append('Network dependency detected in ' + f['path'])
    return {'language': 'python', 'functions': functions, 'classes': classes, 'edges': list(set(edge_hints))}

def analyze_javascript(files: List[Dict[str, str]], entrypoint: str = None) -> Dict[str, Any]:
    import re
    funcs = []
    edges = []
    for f in files:
        text = f['content']
        for m in re.finditer(r'function\s+(\w+)', text):
            funcs.append({'name': m.group(1), 'file': f['path']})
        if 'fetch(' in text or 'axios' in text:
            edges.append('Network calls in ' + f['path'])
        if '[' in text and ']' in text:
            edges.append('Array indexing in ' + f['path'])
    return {'language': 'javascript', 'functions': funcs, 'edges': list(set(edges))}

def analyze_java(files: List[Dict[str, str]], entrypoint: str = None) -> Dict[str, Any]:
    funcs = []
    edges = []
    for f in files:
        text = f['content']
        lines = text.splitlines()
        for i, l in enumerate(lines):
            lstr = l.strip()
            if lstr.startswith('public') and '(' in lstr and ')' in lstr and '{' in lstr:
                parts = lstr.split()
                if len(parts) >= 3:
                    name = parts[2].split('(')[0]
                    funcs.append({'name': name, 'file': f['path'], 'lineno': i + 1})
        if 'new File' in text or 'FileInputStream' in text:
            edges.append('File IO in ' + f['path'])
    return {'language': 'java', 'functions': funcs, 'edges': edges}

def analyze_code(language: str, files, entrypoint=None):
    files_formatted = [{'path': f.path, 'content': f.content} for f in files]
    if language.lower() == 'python':
        return analyze_python(files_formatted, entrypoint)
    if language.lower() == 'javascript' or language.lower() == 'js':
        return analyze_javascript(files_formatted, entrypoint)
    if language.lower() == 'java':
        return analyze_java(files_formatted, entrypoint)
    raise ValueError('Unsupported language')
