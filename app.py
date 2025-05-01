from flask import Flask , render_template ,request,redirect,get_flashed_messages,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///todo.db"
app.secret_key = "Faltu_Todo"
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column (db.Integer , primary_key = True , nullable = False)
    title = db.Column (db.String(200) ,nullable = False)
    description = db.Column (db.Text , nullable = False)
    created_at = db.Column(db.DateTime , default = datetime.utcnow)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 

with app.app_context():
    db.create_all()


    
@app.route('/' , methods = [ 'GET' ,'POST'])
def home ():
    if request.method == 'POST': 
        title = request.form.get('title').strip()
        description = request.form.get('description').strip()
        if title and description :
            new_todo = Todo(title=title ,description=description)
            db.session.add(new_todo)
            db.session.commit()
            flash("Todo added successfully", "success")
            return redirect ('/')

        else:
            flash("Title and Description cannot be empty","danger")

    alltodo = Todo.query.all()
    return render_template('index.html', alltodo=alltodo)


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first_or_404()
    db.session.delete(todo)
    db.session.commit()
    flash("Todo deleted successfully", "success")
    return redirect ('/')

@app.route('/update/<int:sno>',methods = [ 'GET' ,'POST'])
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first_or_404()   

    if request.method == 'POST':
         title = request.form.get('title').strip()
         description = request.form.get('description').strip()
         todo.title = title
         todo.description = description
         db.session.commit()
         flash("Todo updated successfully", "success")
         return redirect('/')
    return render_template('update.html', todo=todo)
         
@app.route('/about')
def about():
    return render_template('about.html')

   

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
