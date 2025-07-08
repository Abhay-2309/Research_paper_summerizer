from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize the model
model = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.3)

# Prompt template
template = """Please summarize the research paper titled "{paper_name}" with the following specifications:

Explanation Style: {style}
Explanation Length: {length}

Mathematical Details:
- Include relevant mathematical equations if present in the paper.
- Explain the mathematical concepts using simple, intuitive code snippets where applicable.

Analogies:
- Use relatable analogies to simplify complex ideas.

Important:
- If certain information is not available in the paper, respond with: "Insufficient information available" instead of guessing.
- Ensure the summary is clear, accurate, and aligned with the provided style and length.
"""

prompt_template = PromptTemplate(
    template=template,
    input_variables=['paper_name', 'style', 'length']
)

# Create the chain
chain = prompt_template | model | StrOutputParser()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_summary():
    try:
        data = request.json
        
        input_dict = {
            'paper_name': data['paper'],
            'style': data['style'],
            'length': data['length']
        }
        
        # Generate summary using your existing chain
        result = chain.invoke(input_dict)
        
        return jsonify({
            'success': True,
            'summary': result
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)