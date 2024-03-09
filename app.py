from flask import Flask, render_template, request
import PyPDF2
import spacy

# Load Marathi language model (assuming spaCy v3 or newer)
nlp = spacy.load("en_core_web_sm")# Load English model (replace with desired language)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/submit_pdf', methods=['POST'])
def submit_pdf():
    if request.method == 'POST':
        file = request.files['pdf_file']
        if file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ''
            for page_num in range(pdf_reader.numPages):
                # Consider using pdf_reader.pages[page_num].extract_text() for clarity (PyPDF2 v2+)
                text += pdf_reader.getPage(page_num).extractText()

            doc = nlp.make_doc(text)  # Assuming spaCy v3 or newer
            summary = summarize_text(doc)
            keywords = extract_keywords(doc)
            return render_template('result.html', summary=summary, keywords=keywords)

# Define summarization and keyword extraction functions
def summarize_text(doc):
    """
    Summarizes the given document text.

    Args:
        doc (spacy.Doc): The spaCy document containing the text.

    Returns:
        str: The summarized text.
    """
    # Tokenize the document into sentences
    sentences = [sent.text for sent in doc.sents]

    # Calculate the length of the summary (for demonstration, let's take the first 3 sentences)
    summary_length = min(3, len(sentences))

    # Extract the first 'summary_length' sentences as summary
    summary = ' '.join(sentences[:summary_length])

    return summary

def extract_keywords(doc):
    """
    Extracts keywords from the given document.

    Args:
        doc (spacy.Doc): The spaCy document containing the text.

    Returns:
        list: A list of extracted keywords.
    """
    # Extract entities, nouns, and phrases as keywords
    entities = [ent.text for ent in doc.ents]
    nouns = [token.text for token in doc if token.pos_ == 'NOUN']
    phrases = [chunk.text for chunk in doc.noun_chunks]  # Assuming spaCy v3 or newer

    # Combine all extracted keywords into a single list
    keywords = entities + nouns + phrases

    # Remove duplicates
    keywords = list(set(keywords))

    return keywords

if __name__ == '__main__':
    app.run(debug=True)  # Remove for production
