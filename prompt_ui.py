import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit.components.v1 as components

# Load environment variables
load_dotenv()

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

# Page configuration
st.set_page_config(
    page_title="Research Tool",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS to hide Streamlit default elements
st.markdown("""
<style>
    .stApp > header {visibility: hidden;}
    .stApp > div > div > div > div > div > section > div {padding-top: 0rem;}
    .stSelectbox > div > div > div > div {background-color: transparent;}
    .stButton > button {display: none;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Custom UI Component
def custom_ui():
    # Read the HTML file (save the artifact content as 'custom_ui.html')
    with open('custom_ui.html', 'r') as f:
        html_content = f.read()
    
    # Modify the generateSummary function to use Streamlit
    html_content = html_content.replace(
        'onclick="generateSummary()"',
        'onclick="generateSummaryStreamlit()"'
    )
    
    # Add Streamlit-specific JavaScript
    streamlit_js = """
    <script>
        function generateSummaryStreamlit() {
            const paper = document.getElementById('paper-select').value;
            const style = document.getElementById('style-select').value;
            const length = document.getElementById('length-select').value;
            
            // Send data to Streamlit
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: {
                    paper: paper,
                    style: style,
                    length: length,
                    action: 'generate'
                }
            }, '*');
        }
    </script>
    """
    
    html_content = html_content.replace('</body>', streamlit_js + '</body>')
    
    # Display the custom component
    result = components.html(html_content, height=800, scrolling=True)
    
    return result

# Main app
def main():
    # Display custom UI
    user_input = custom_ui()
    
    # Process the input if received
    if user_input and user_input.get('action') == 'generate':
        with st.spinner("Generating summary..."):
            input_dict = {
                'paper_name': user_input['paper'],
                'style': user_input['style'],
                'length': user_input['length']
            }
            
            # Generate summary
            result = chain.invoke(input_dict)
            
            # Display result (you can modify this to send back to the custom UI)
            st.success("Summary generated!")
            st.write(result)

if __name__ == "__main__":
    main()