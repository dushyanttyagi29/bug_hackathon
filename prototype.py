# import subprocess
# import re
# from transformers import pipeline


# error_explainer = pipeline("text2text-generation", model="google/flan-t5-base")

# def compile_java(java_file_path):
#     result = subprocess.run(['javac', java_file_path], capture_output=True, text=True)
#     return result.stderr  

# def parse_errors(compiler_output):
    
#     pattern = re.compile(r"^(.*\.java):(\d+): error: (.*)$", re.MULTILINE)
#     matches = pattern.findall(compiler_output)

#     if not matches:
#         return "✅ No compilation errors found."

#     full_report = ""
#     for _, line, message in matches:
#         severity = classify_severity(message)
#         ai_suggestion = get_ai_suggestion(message)

#         full_report += f"\n🔴 Line {line}: {message.strip()}\n"
#         full_report += f"Type: {severity}\n"
#         full_report += f"Suggestion: {ai_suggestion.strip()}\n"
#         full_report += "-" * 60 + "\n"
#     return full_report

# def classify_severity(message):
#     major_keywords = ["cannot find symbol", "class, interface", "illegal start", "incompatible", "not a statement"]
#     for keyword in major_keywords:
#         if keyword in message.lower():
#             return "Major"
#     return "Minor"



# def get_ai_suggestion(error_msg):
#     prompt = f"Java error: {error_msg}. these are the errors "
#     result = error_explainer(prompt, max_length=100, do_sample=False)
#     return result[0]['generated_text']

# if __name__ == "__main__":
#     java_file = "Test.java"  
#     compiler_output = compile_java(java_file)
#     report = parse_errors(compiler_output)
#     print(report)




import subprocess
import re
from transformers import pipeline

# Load AI model for error explanations
error_explainer = pipeline("text2text-generation", model="google/flan-t5-base")

def compile_java(java_file_path):
    """Compiles a Java file and returns any errors."""
    result = subprocess.run(['javac', java_file_path], capture_output=True, text=True)
    return result.stderr  

def parse_errors(compiler_output):
    """Extracts and categorizes Java compilation errors."""
    pattern = re.compile(r"^(.*\.java):(\d+): error: (.*)$", re.MULTILINE)
    matches = pattern.findall(compiler_output)

    if not matches:
        return "✅ No compilation errors found."

    full_report = ""
    for _, line, message in matches:
        severity, score = classify_severity(message)
        ai_suggestion = get_ai_suggestion(message)

        full_report += f"\n🔴 Line {line}: {message.strip()}\n"
        full_report += f"Severity: {severity} (Score: {score}/10)\n"
        full_report += f"Suggestion: {ai_suggestion.strip()}\n"
        full_report += "-" * 60 + "\n"

    return full_report

def classify_severity(message):
    """Assigns a severity level and score based on error type."""
    error_types = {
        "Syntax Error": ["';' expected", "illegal start", "not a statement"],
        "Reference Error": ["cannot find symbol", "does not exist", "variable might not have been initialized"],
        "Structural Error": ["incompatible types", "class, interface expected", "method does not override or implement"]
    }

    for category, keywords in error_types.items():
        if any(keyword in message.lower() for keyword in keywords):
            score = (list(error_types.keys()).index(category) + 1) * 3  # Assign severity score
            return category, score

    return "Unknown Error", 2  # Default low severity for unknown errors

def get_ai_suggestion(error_msg):
    """Uses AI to generate suggestions for fixing the error."""
    prompt = f"Java error: {error_msg}. Provide a detailed explanation and solution."
    result = error_explainer(prompt, max_length=100, do_sample=False)
    return result[0]['generated_text']

if __name__ == "__main__":
    java_file = "Test.java"  
    compiler_output = compile_java(java_file)
    report = parse_errors(compiler_output)
    print(report)