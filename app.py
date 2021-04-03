from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///question.db"
db = SQLAlchemy(app)

class question(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(40000), nullable=True)
    answer = db.Column(db.String(2000), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title} -{self.date}"

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/programming')
def programming():
    return render_template('programming.html')

@app.route('/programminglist')   
def programmingdisplay():
    ques = question(title="hello world program",description="First program",answer="print(\"Hello world\")" )
    db.session.add(ques)
    db.session.commit()
    answers = question.query.all()
    print(answers)
    return render_template('programmingdisplay.html',answers = answers)

if __name__ == '__main__':
    app.run(debug=True,port=8000)