from werkzeug.utils import secure_filename
import os
from flask import Flask, render_template, request, session, redirect,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime,UTC


app = Flask(__name__)
app.secret_key = "pankaj_portfolio_secret_2026"

app.config["UPLOAD_FOLDER"] = os.path.join(
    app.root_path,
    "static",
    "profile_photos"
)

app.config["RESUME_FOLDER"] = os.path.join(
    app.root_path,
    "static",
    "user_resumes"
)

app.config["CERTIFICATE_FOLDER"] = os.path.join(
    app.root_path,
    "static",
    "certificates"
)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///portfolio.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(100), unique=True, nullable=False)

    password = db.Column(db.String(200), nullable=False)

    profile_photo = db.Column(db.String(300))


class Project(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    technology = db.Column(db.String(200))

    description = db.Column(db.Text)

    github_link = db.Column(db.String(500))

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )


class ContactMessage(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(100),
        nullable=False
    )

    message = db.Column(
        db.Text,
        nullable=False
    )

class Resume(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    filename = db.Column(
        db.String(300)
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )

class Certificate(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200)
    )

    filename = db.Column(
        db.String(300)
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )

class Skill(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100)
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )

@app.route("/upload_resume", methods=["POST"])
def upload_resume():

    if "user_id" not in session:
        return redirect("/login")

    file = request.files["resume"]

    if file.filename == "":
        return "Please select a resume"

    filename = secure_filename(
        file.filename
    )

    os.makedirs(
        app.config["RESUME_FOLDER"],
        exist_ok=True
    )

    file.save(
        os.path.join(
            app.config["RESUME_FOLDER"],
            filename
        )
    )

    old_resume = Resume.query.filter_by(
        user_id=session["user_id"]
    ).first()

    if old_resume:

        old_resume.filename = filename

    else:

        new_resume = Resume(
            filename=filename,
            user_id=session["user_id"]
        )

        db.session.add(new_resume)

    db.session.commit()

    return redirect("/profile")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        

        user = User.query.filter_by(email=email).first()

        

        if user:
            if user and check_password_hash(
            user.password,
            password
        ):
                session["user_id"] = user.id
                session["user_name"] = user.name

                return redirect("/dashboard")

        return "Invalid Email or Password 😕"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        username=session["user_name"]
    )

@app.route("/add_project", methods=["GET", "POST"])
def add_project():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        title = request.form["title"]
        technology = request.form["technology"]
        description = request.form["description"]
        github_link = request.form["github_link"]

        project = Project(
            title=title,
            technology=technology,
            description=description,
            github_link=github_link,
            user_id=session["user_id"]
        )

        db.session.add(project)
        db.session.commit()

        return render_template(
    "success.html",
    message="Project Saved Successfully 🎉",
    redirect_url="/projects"
)

    return render_template("add_project.html")


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]

        password = generate_password_hash(
            request.form["password"]
        )

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:
            return "Email already registered 🙌"

        new_user = User(
            name=name,
            email=email,
            password=password
        )

        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.id
        session["user_name"] = new_user.name

        return redirect("/dashboard")

    return render_template("register.html")

@app.route("/projects")
def projects():

    if "user_id" not in session:
        return redirect("/login")

    search = request.args.get("search")

    if search:

        all_projects = Project.query.filter(
            Project.title.contains(search)
        ).all()

    else:

        all_projects = Project.query.filter_by(
            user_id=session["user_id"]
        ).all()

    return render_template(
        "projects.html",
        projects=all_projects
    )

@app.route("/resume")
def resume():

    return send_from_directory(
        "static/resume",
        "DSA_CompleteNotes.pdf",
        as_attachment=True
    )

@app.route("/messages")
def messages():

    if "user_id" not in session:
        return redirect("/login")

    all_messages = ContactMessage.query.all()

    return render_template(
        "messages.html",
        messages=all_messages
    )

@app.route("/edit_project/<int:id>", methods=["GET", "POST"])
def edit_project(id):

    if "user_id" not in session:
        return redirect("/login")

    project = Project.query.get_or_404(id)

    if request.method == "POST":

        project.title = request.form["title"]
        project.technology = request.form["technology"]
        project.description = request.form["description"]
        project.github_link = request.form["github_link"]

        db.session.commit()

        return redirect("/projects")

    return render_template(
        "edit_project.html",
        project=project
    )

@app.route("/delete_project/<int:id>")
def delete_project(id):

    if "user_id" not in session:
        return redirect("/login")

    project = Project.query.get_or_404(id)

    if project.user_id != session["user_id"]:
        return "Access Denied"

    db.session.delete(project)
    db.session.commit()

    return redirect("/projects")

@app.route("/project/<int:id>")
def project_detail(id):

    if "user_id" not in session:
        return redirect("/login")

    project = Project.query.get_or_404(id)

    return render_template(
        "project_detail.html",
        project=project
    )

@app.route("/skills")
def skills():
    return render_template("skills.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        name = request.form["name"]

        email = request.form["email"]

        message = request.form["message"]

        new_message = ContactMessage(
            name=name,
            email=email,
            message=message
        )

        db.session.add(new_message)

        db.session.commit()

        return render_template(
            "success.html",
            message="Message Sent Successfully 🎉",
            redirect_url="/contact"
)

    return render_template("contact.html")

@app.route("/users")
def users():

    all_users = User.query.all()

    output = ""

    for user in all_users:
        output += f"{user.name} - {user.email}<br>"

    return output

@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(
        session["user_id"]
    )

    resume = Resume.query.filter_by(
        user_id=session["user_id"]
    ).first()

    certificates = Certificate.query.filter_by(
        user_id=session["user_id"]
    ).all()

    skills = Skill.query.filter_by(
    user_id=session["user_id"]).all()

    return render_template(
        "profile.html",
        user=user,
        resume=resume,
        certificates=certificates,
        skills=skills
    )

@app.route("/upload_photo", methods=["POST"])
def upload_photo():

    if "user_id" not in session:
        return redirect("/login")

    file = request.files["photo"]

    if file.filename == "":
        return "Please select a file"

    filename = secure_filename(file.filename)

    os.makedirs(
        app.config["UPLOAD_FOLDER"],
        exist_ok=True
    )

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(filepath)

    user = User.query.get(session["user_id"])

    user.profile_photo = filename

    db.session.commit()

    return redirect("/profile")

@app.route("/upload_certificate", methods=["POST"])
def upload_certificate():

    if "user_id" not in session:
        return redirect("/login")

    title = request.form["title"]

    file = request.files["certificate"]

    if file.filename == "":
        return "Please select a certificate"

    filename = secure_filename(file.filename)

    os.makedirs(
        app.config["CERTIFICATE_FOLDER"],
        exist_ok=True
    )
    file.save(
        os.path.join(
            app.config["CERTIFICATE_FOLDER"],
            filename
        )
    )
    new_certificate = Certificate(
        title=title,
        filename=filename,
        user_id=session["user_id"]
    )
    db.session.add(new_certificate)

    db.session.commit()

    return redirect("/profile")

@app.route("/delete_certificate/<int:id>")
def delete_certificate(id):

    if "user_id" not in session:
        return redirect("/login")

    certificate = Certificate.query.get_or_404(id)

    if certificate.user_id != session["user_id"]:
        return "Access Denied"

    db.session.delete(certificate)
    db.session.commit()

    return redirect("/profile")


@app.route("/delete_photo")
def delete_photo():

    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])

    user.profile_photo = None

    db.session.commit()

    return redirect("/profile")


@app.route("/delete_resume")
def delete_resume():

    if "user_id" not in session:
        return redirect("/login")

    resume = Resume.query.filter_by(
        user_id=session["user_id"]
    ).first()

    if resume:
        db.session.delete(resume)
        db.session.commit()

    return redirect("/profile")

@app.route("/add_skill", methods=["POST"])
def add_skill():

    if "user_id" not in session:
        return redirect("/login")

    skill_name = request.form["skill"]

    new_skill = Skill(
        name=skill_name,
        user_id=session["user_id"]
    )

    db.session.add(new_skill)
    db.session.commit()

    return redirect("/profile")

@app.route("/delete_skill/<int:id>")
def delete_skill(id):

    if "user_id" not in session:
        return redirect("/login")

    skill = Skill.query.get_or_404(id)

    if skill.user_id != session["user_id"]:
        return "Access Denied"

    db.session.delete(skill)

    db.session.commit()

    return redirect("/profile")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)