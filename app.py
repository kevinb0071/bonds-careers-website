from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime, timezone
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///careers.sqlite"
app.secret_key = b"\xa2I\x14jZ\x80\x12\xc7"


class Base(DeclarativeBase):
  pass


db = SQLAlchemy(app, model_class=Base)


class Jobs(db.Model):
  id: Mapped[int] = mapped_column(db.Integer(), primary_key=True)
  title: Mapped[str] = mapped_column(db.String(100))
  location: Mapped[str] = mapped_column(db.String(255))
  salary: Mapped[int] = mapped_column(db.Integer())
  currency: Mapped[str] = mapped_column(db.String(10))
  requirements: Mapped[str] = mapped_column(db.String(255))
  responsibilities: Mapped[str] = mapped_column(db.String(255))
  created_at: Mapped[datetime] = mapped_column(
      default=lambda: datetime.now(timezone.utc))
  updated_at: Mapped[datetime] = mapped_column(
      default=lambda: datetime.now(timezone.utc),
      onupdate=lambda: datetime.now(timezone.utc))
  @property
  def prettier_salary(self):
        if len(str(self.salary)) >= 4:
            return f'${str(self.salary)[:-3]},{str(self.salary)[-3:]}'
        else:
            return f"${self.salary}"
  def __repr__(self):
    return f"{self.title}"


with app.app_context():
  db.create_all()


class JobForm(FlaskForm):
  title = StringField(label="Title:")
  location = StringField(label="Location:")
  salary = IntegerField(label="Salary:")
  currency = StringField(label="Currency:")
  requirements = StringField(label="Requirements:")
  responsibilities = TextAreaField(label="Responsibilities:")
  submit = SubmitField("Submit")




@app.route('/')
@app.route('/home')
def home():
  jobs = Jobs.query.all()
  return render_template('home.html', jobs=jobs)

@app.route('/add', methods=['GET', 'POST'])
def add():
  form = JobForm()
  if form.validate_on_submit():
    job = Jobs(title=form.title.data, 
               location=form.location.data, 
               salary=form.salary.data, 
               currency=form.currency.data, 
               requirements=form.requirements.data, 
               responsibilities=form.responsibilities.data)
    db.session.add(job)
    db.session.commit()
    return redirect(url_for('home'))
  return render_template('addjob.html', form=form)


@app.route('/api/jobs')
def list_jobs():
  return jsonify(Jobs)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)
