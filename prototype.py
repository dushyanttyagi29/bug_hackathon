import subprocess
import re
from transformers import pipeline


error_explainer = pipeline("text2text-generation", model="google/flan-t5-base")

def compile_java(java_file_path):
    result = subprocess.run(['javac', java_file_path], capture_output=True, text=True)
    return result.stderr  

def parse_errors(compiler_output):
    
    pattern = re.compile(r"^(.*\.java):(\d+): error: (.*)$", re.MULTILINE)
    matches = pattern.findall(compiler_output)

    if not matches:
        return "✅ No compilation errors found."

    full_report = ""
    for _, line, message in matches:
        severity = classify_severity(message)
        ai_suggestion = get_ai_suggestion(message)

        full_report += f"\n🔴 Line {line}: {message.strip()}\n"
        full_report += f"Type: {severity}\n"
        full_report += f"Suggestion: {ai_suggestion.strip()}\n"
        full_report += "-" * 60 + "\n"
    return full_report

def classify_severity(message):
    major_keywords = ["cannot find symbol", "class, interface", "illegal start", "incompatible", "not a statement"]
    for keyword in major_keywords:
        if keyword in message.lower():
            return "Major"
    return "Minor"


