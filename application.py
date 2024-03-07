from flask import Flask,render_template ,request ,send_file 
import pymongo

app = Flask(__name__)



client =pymongo.MongoClient("mongodb+srv://prashantwadhave5:Prash2002@cluster0.wkfocs3.mongodb.net/?retryWrites=true&w=majority") # connecting string for mongodb database for the contacted data
db = client.test
db = client.PDfSummriser  
collection = db['contact_list'] 


@app.route('/')
def index():
    return render_template('index.html') # for rendering the index html file

@app.route('/submit_pdf', methods=['POST']) # function to process on the pdf
def submit_pdf():
    pass

@app.route('/submit_contact_form', methods=['POST'])
def submit_contact_form():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        print(f"Name: {name}, Email: {email}, Message: {message}")

        # Store the form data in MongoDB
        collection.insert_one({
            'name': name,
            'email': email,
            'message': message
        })

        return  render_template('formsub.html')
    else:
        return "Method Not Allowed", 405


    
if __name__ == ('__main__'):
    app.run(debug=True)