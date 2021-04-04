from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///question.db"
db = SQLAlchemy(app)

class question(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=True)
    description = db.Column(db.String(40000), nullable=True)
    answer = db.Column(db.String(2000), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title} -{self.date}"

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/programming',methods=['GET','POST'])
def programming():
    title = ""
    description = ""
    answer = ""
    if request.method=='POST':
        title = request.form['title']
        description = request.form['description']
        answer = request.form['answer']
        ques = question(title=title,description=description,answer=answer)
        db.session.add(ques)
        db.session.commit()
        return redirect('/programminglist')
    return render_template('programming.html')

@app.route('/programminglist')   
def programmingdisplay():
    answers = question.query.all()
    print(answers)
    return render_template('programmingdisplay.html',answers = answers)

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/certificates')
def certificates():
    return render_template('certificates.html')

@app.route('/delete/<int:sno>')
def delete(sno):
    delete = question.query.filter_by(sno=sno).first()
    db.session.delete(delete)
    db.session.commit()
    return redirect('/programminglist')

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        description = request.form['description']
        answer = request.form['answer']
        update = question.query.filter_by(sno=sno).first()
        update.title = title
        update.description = description
        update.answer = answer
        db.session.add(update)
        db.session.commit()
        return redirect('/programminglist')

    update = question.query.filter_by(sno=sno).first()
    return render_template('update.html', update=update)

@app.route('/view/<int:sno>' ,methods=['GET','POST'])
def view(sno):
    if request.method=='POST':
        return redirect('/programminglist')
    view = question.query.filter_by(sno=sno).first()
    return render_template('view.html', view=view)

if __name__ == '__main__':
    app.run(debug=False,port=8000)