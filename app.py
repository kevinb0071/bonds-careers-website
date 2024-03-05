from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime, timezone
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, EmailField, FileField

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
    items = db.relationship('Applications', backref='job_application', lazy=True)
    @property
    def prettier_salary(self):
        if len(str(self.salary)) >= 4:
            return f"${str(self.salary)[:-3]},{str(self.salary)[-3:]}"
        else:
            return f"${self.salary}"

    def __repr__(self):
        return f"{self.title}"

class Applications(db.Model):
   
    id: Mapped[int] = mapped_column(db.Integer(), primary_key=True)
    job_id: Mapped[int] = mapped_column(db.Integer(), db.ForeignKey('jobs.id'), nullable=True)
    full_name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(), nullable=False)
    linkedin: Mapped[str] = mapped_column(db.String(), nullable=True)
    education: Mapped[str] = mapped_column(db.String(2000), nullable=False)
    work_experience: Mapped[str] = mapped_column(db.String(2000), nullable=False)
    resume: Mapped[str] = mapped_column(db.String(255), nullable=True)

    def __repr__(self):
        return f"{self.full_name}"

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


class ApplicationForm(FlaskForm):
    full_name = StringField(label='Full Name:')
    email = EmailField(label='Email Address:')
    linkedin = StringField(label="Your LinkedIn URL:")
    education = TextAreaField(label='Education:')
    work_experience = TextAreaField(label='Work Experience:')
    resume = StringField(label='Your Resume URL:')
    submit = SubmitField("Apply")





@app.route("/")
@app.route("/home")
def home():
    jobs = Jobs.query.all()
    return render_template("home.html", jobs=jobs)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = JobForm()
    if form.validate_on_submit():
        job = Jobs(
            title=form.title.data,
            location=form.location.data,
            salary=form.salary.data,
            currency=form.currency.data,
            requirements=form.requirements.data,
            responsibilities=form.responsibilities.data,
        )
        db.session.add(job)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("addjob.html", form=form)

@app.route('/job/<int:id>')
def show_job(id):
    form = ApplicationForm()
    job = Jobs.query.filter_by(id=id).first()
    return render_template('job.html', job=job, form=form)

@app.route("/job/apply", methods=["GET", "POST"])
def apply_to_job():
    form = ApplicationForm()
    if request.method == 'POST':
        job_id = request.form.get("job_id")
        job_id = Jobs.query.filter_by(id=job_id).first()

        application = Applications(
            job_id = str(job_id),
            full_name = form.full_name.data,
            email = form.email.data,
            linkedin = form.linkedin.data,
            education = form.education.data,
            work_experience = form.work_experience.data,
            resume = form.resume.data
        )
        db.session.add(application)
        db.session.commit()
        return redirect(url_for('home'))
        

    
           





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
