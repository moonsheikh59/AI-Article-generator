from flask import Blueprint, render_template,request,flash,jsonify
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from .key import OPENAI_KEY
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
import os
views = Blueprint('views',__name__)


os.environ["OPENAI_API_KEY"] = OPENAI_KEY

@views.route('/',methods = ['GET','POST'])
@login_required
def home():
    if request.method == 'POST': 
        data = request.form.get('data') #Gets the note from the HTML 
        if len(data) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=data, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    print(note)
    noteId = note['noteId']
    print(noteId)
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})

@views.route('/generate', methods=['GET', 'POST'])
def generate():
  if request.method == 'POST':
    prompt = PromptTemplate.from_template("Generate a blog on title {title}?")
    llm = OpenAI(temperature=0.8)
    chain = LLMChain(llm=llm, prompt=prompt)
    prompt = request.json.get('prompt')
    output = chain.run(prompt)
    return output
