from werkzeug.utils import secure_filename
import os
from flask import Flask, render_template, request, session, redirect,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import secrets

from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
load_dotenv()

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "pankaj_portfolio_secret_2026"
)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///portfolio.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url=
    "https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile"
    }
)
ADMIN_EMAIL = "pankajraj2025434@gmail.com"

@app.after_request
def add_header(response):

    response.headers["Cache-Control"] = \
        "no-store, no-cache, must-revalidate, max-age=0"

    response.headers["Pragma"] = "no-cache"

    response.headers["Expires"] = "0"

    return response

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "pankaj_portfolio_secret_2026"
)

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

app.config["EDUCATION_FOLDER"] = os.path.join(
    app.root_path,
    "static",
    "education_files"
)

app.config["ACHIEVEMENT_FOLDER"] = os.path.join(
    app.root_path,
    "static",
    "achievements"
)

app.config["EXPERIENCE_FOLDER"] = os.path.join(
    app.root_path,
    "static",
    "experiences"
)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///portfolio.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100),unique=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(100), unique=True, nullable=False)

    password = db.Column(db.String(200), nullable=False)

    profile_photo = db.Column(db.String(300))

    is_active = db.Column(db.Boolean,default=True)
    


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

class Education(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    level = db.Column(
        db.String(50)
    )

    institute = db.Column(
        db.String(200)
    )

    board_university = db.Column(
        db.String(200)
    )

    stream_degree = db.Column(
        db.String(200)
    )

    score = db.Column(
        db.String(50)
    )

    passing_year = db.Column(
        db.String(20)
    )

    achievements = db.Column(
        db.Text
    )

    subjects = db.Column(
        db.String(300)
    )

    city = db.Column(
        db.String(100)
    )

    state = db.Column(
        db.String(100)
    )

    rank = db.Column(
        db.String(50)
    )

    certificate_file = db.Column(
        db.String(300)
    )

    marksheet_file = db.Column(
        db.String(300)
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )

class AboutMe(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    bio = db.Column(
        db.Text
    )

    career_goal = db.Column(
        db.Text
    )

    hobbies = db.Column(
        db.Text
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )

class SocialLink(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    github = db.Column(
        db.String(300)
    )

    linkedin = db.Column(
        db.String(300)
    )

    leetcode = db.Column(
        db.String(300)
    )

    codechef = db.Column(
        db.String(300)
    )

    codeforces = db.Column(
        db.String(300)
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )

class Achievement(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200)
    )

    description = db.Column(
        db.Text
    )

    achievement_file = db.Column(
        db.String(300)
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )

    

class Experience(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    company = db.Column(
        db.String(200)
    )

    role = db.Column(
        db.String(200)
    )

    duration = db.Column(
        db.String(100)
    )

    description = db.Column(
        db.Text
    )

    certificate_file = db.Column(
        db.String(300)
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )

class Feedback(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100)
    )

    email = db.Column(
        db.String(100)
    )

    message = db.Column(
        db.Text
    )

    reply = db.Column(
        db.Text
    )
    user_id = db.Column(
        db.Integer)



class FeedbackMessage(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    feedback_id = db.Column(
        db.Integer,
        db.ForeignKey("feedback.id")
    )

    sender = db.Column(
        db.String(20)
    )

    message = db.Column(
        db.Text
    )

    user_reply = db.Column(db.Text)

class Activity(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer)

    activity = db.Column(db.String(200))

@app.route("/upload_resume", methods=["POST"])
def upload_resume():

    if "user_id" not in session:
        return redirect("/login")

    file = request.files["resume"]

    if file.filename == "":
        return "Please select a resume"

    filename = f"{session['user_id']}_{secure_filename(file.filename)}"

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

            if not user.is_active:

                user.is_active = True

                db.session.commit()

            if check_password_hash(
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

    projects = Project.query.filter_by(
        user_id=session["user_id"]
    ).all()

    skills = Skill.query.filter_by(
        user_id=session["user_id"]
    ).all()

    certificates = Certificate.query.filter_by(
        user_id=session["user_id"]
    ).all()

    educations = Education.query.filter_by(
        user_id=session["user_id"]
    ).all()

    user = User.query.get(
        session["user_id"]
    )

    about = AboutMe.query.filter_by(
        user_id=session["user_id"]
    ).first()

    resume = Resume.query.filter_by(
        user_id=session["user_id"]
    ).first()

    experiences = Experience.query.filter_by(
        user_id=session["user_id"]
    ).all()

    social = SocialLink.query.filter_by(
        user_id=session["user_id"]
    ).first()

    activities = Activity.query.filter_by(
        user_id=session["user_id"]
    ).all()

    completion = 0

    if user.profile_photo:
        completion += 10

    if about:
        completion += 15

    if skills:
        completion += 15

    if educations:
        completion += 15

    if resume:
        completion += 15

    if certificates:
        completion += 10

    if experiences:
        completion += 10

    if social:
        completion += 10

    from datetime import datetime

    hour = datetime.now().hour

    if hour < 12:
        greeting = "Good Morning"
    elif hour < 17:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    return render_template(
        "dashboard.html",
        username=session["user_name"],
        projects=projects,
        skills=skills,
        certificates=certificates,
        educations=educations,
        about=about,
        social=social,
        experiences=experiences,
        user=user,
        resume=resume,
        completion=completion,
        activities=activities,
        greeting=greeting
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

        activity = Activity(

            user_id=session["user_id"],

        activity="Added a new project"

)

        db.session.add(activity)

        db.session.commit()

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
            username=email.split("@")[0],
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
            Project.user_id == session["user_id"],
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

@app.route("/messages")
def messages():

    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])

    if user.email != ADMIN_EMAIL:
        return "Access Denied ❌"

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

    if project.user_id != session["user_id"]:
        return "Access Denied"

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

    if project.user_id != session["user_id"]:
        return "Access Denied"

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

    projects = Project.query.filter_by(
    user_id=user.id
    ).all()

    educations = Education.query.filter_by(
    user_id=session["user_id"]
    ).all()

    about = AboutMe.query.filter_by(
    user_id=session["user_id"]
    ).first()

    social = SocialLink.query.filter_by(
    user_id=session["user_id"]
    ).first()

    achievements = Achievement.query.filter_by(
    user_id=session["user_id"]
    ).all()

    experiences = Experience.query.filter_by(
    user_id=session["user_id"]).all()

    return render_template(
        "profile.html",
        user=user,
        resume=resume,
        certificates=certificates,
        skills=skills,
        educations=educations,
        about=about,
        social=social,
        achievements=achievements,
        experiences=experiences
    )

@app.route("/upload_photo", methods=["POST"])
def upload_photo():

    if "user_id" not in session:
        return redirect("/login")

    file = request.files["photo"]

    if file.filename == "":
        return "Please select a file"

    filename = f"{session['user_id']}_{secure_filename(file.filename)}"

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

    filename = f"{session['user_id']}_{secure_filename(file.filename)}"

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

    if certificate.filename:

        filepath = os.path.join(
            app.config["CERTIFICATE_FOLDER"],
            certificate.filename
        )

        if os.path.exists(filepath):
            os.remove(filepath)

    db.session.delete(certificate)

    db.session.commit()

    return redirect("/profile")


@app.route("/delete_photo")
def delete_photo():

    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])

    if user.profile_photo:

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            user.profile_photo
        )

        if os.path.exists(filepath):
            os.remove(filepath)

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

        filepath = os.path.join(
            app.config["RESUME_FOLDER"],
            resume.filename
        )

        if os.path.exists(filepath):
            os.remove(filepath)

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
@app.route("/add_education", methods=["POST"])
def add_education():

    if "user_id" not in session:
        return redirect("/login")

    certificate = request.files["certificate"]
    marksheet = request.files["marksheet"]

    certificate_name = ""
    marksheet_name = ""

    os.makedirs(
        app.config["EDUCATION_FOLDER"],
        exist_ok=True
    )

    if certificate.filename != "":

        certificate_name = f"{session['user_id']}_{secure_filename(certificate.filename)}"

        certificate.save(
            os.path.join(
                app.config["EDUCATION_FOLDER"],
                certificate_name
            )
        )

    if marksheet.filename != "":

        marksheet_name = f"{session['user_id']}_{secure_filename(marksheet.filename)}"

        marksheet.save(
            os.path.join(
                app.config["EDUCATION_FOLDER"],
                marksheet_name
            )
        )

    education = Education(
        level=request.form["level"],
        institute=request.form["institute"],
        board_university=request.form["board_university"],
        stream_degree=request.form["stream_degree"],
        score=request.form["score"],
        passing_year=request.form["passing_year"],
        subjects=request.form["subjects"],
        city=request.form["city"],
        state=request.form["state"],
        rank=request.form["rank"],
        achievements=request.form["achievements"],
        certificate_file=certificate_name,
        marksheet_file=marksheet_name,
        user_id=session["user_id"]
    )

    db.session.add(education)
    db.session.commit()

    return redirect("/profile")

@app.route("/delete_education/<int:id>")
def delete_education(id):

    if "user_id" not in session:
        return redirect("/login")

    education = Education.query.get_or_404(id)

    if education.user_id != session["user_id"]:
        return "Access Denied"

    db.session.delete(education)

    db.session.commit()

    return redirect("/profile")

@app.route("/add_about", methods=["POST"])
def add_about():

    if "user_id" not in session:
        return redirect("/login")

    old_about = AboutMe.query.filter_by(
        user_id=session["user_id"]
    ).first()

    if old_about:

        old_about.bio = request.form["bio"]
        old_about.career_goal = request.form["career_goal"]
        old_about.hobbies = request.form["hobbies"]

    else:

        new_about = AboutMe(
            bio=request.form["bio"],
            career_goal=request.form["career_goal"],
            hobbies=request.form["hobbies"],
            user_id=session["user_id"]
        )

        db.session.add(new_about)

    db.session.commit()

    return redirect("/profile")

@app.route("/add_social", methods=["POST"])
def add_social():

    if "user_id" not in session:
        return redirect("/login")

    social = SocialLink.query.filter_by(
        user_id=session["user_id"]
    ).first()

    if social:

        social.github = request.form["github"]
        social.linkedin = request.form["linkedin"]
        social.leetcode = request.form["leetcode"]
        social.codechef = request.form["codechef"]
        social.codeforces = request.form["codeforces"]

    else:

        social = SocialLink(
            github=request.form["github"],
            linkedin=request.form["linkedin"],
            leetcode=request.form["leetcode"],
            codechef=request.form["codechef"],
            codeforces=request.form["codeforces"],
            user_id=session["user_id"]
        )

        db.session.add(social)

    db.session.commit()

    return redirect("/profile")

@app.route("/delete_about")
def delete_about():

    if "user_id" not in session:
        return redirect("/login")

    about = AboutMe.query.filter_by(
        user_id=session["user_id"]
    ).first()

    if about:

        db.session.delete(about)
        db.session.commit()

    return redirect("/profile")

@app.route("/delete_social")
def delete_social():

    if "user_id" not in session:
        return redirect("/login")

    social = SocialLink.query.filter_by(
        user_id=session["user_id"]
    ).first()

    if social:

        db.session.delete(social)
        db.session.commit()

    return redirect("/profile")

@app.route("/add_achievement", methods=["POST"])
def add_achievement():

    if "user_id" not in session:
        return redirect("/login")

    file = request.files["achievement_file"]

    filename = ""

    os.makedirs(
        app.config["ACHIEVEMENT_FOLDER"],
        exist_ok=True
    )

    if file.filename != "":

        filename = f"{session['user_id']}_{secure_filename(file.filename)}"

        file.save(
            os.path.join(
                app.config["ACHIEVEMENT_FOLDER"],
                filename
            )
        )

    achievement = Achievement(
        title=request.form["title"],
        description=request.form["description"],
        achievement_file=filename,
        user_id=session["user_id"]
    )

    db.session.add(achievement)

    db.session.commit()

    return redirect("/profile")

@app.route("/delete_achievement/<int:id>")
def delete_achievement(id):

    if "user_id" not in session:
        return redirect("/login")

    achievement = Achievement.query.get_or_404(id)

    if achievement.user_id != session["user_id"]:
        return "Access Denied"

    if achievement.achievement_file:

        filepath = os.path.join(
            app.config["ACHIEVEMENT_FOLDER"],
            achievement.achievement_file
        )

        if os.path.exists(filepath):
            os.remove(filepath)

    db.session.delete(achievement)

    db.session.commit()

    return redirect("/profile")

@app.route("/add_experience", methods=["POST"])
def add_experience():

    if "user_id" not in session:
        return redirect("/login")

    file = request.files["certificate"]

    filename = ""

    os.makedirs(
        app.config["EXPERIENCE_FOLDER"],
        exist_ok=True
    )

    if file.filename != "":

        filename = f"{session['user_id']}_{secure_filename(file.filename)}"

        file.save(
            os.path.join(
                app.config["EXPERIENCE_FOLDER"],
                filename
            )
        )

    experience = Experience(
        company=request.form["company"],
        role=request.form["role"],
        duration=request.form["duration"],
        description=request.form["description"],
        certificate_file=filename,
        user_id=session["user_id"]
    )

    db.session.add(experience)

    db.session.commit()

    return redirect("/profile")

@app.route("/delete_experience/<int:id>")
def delete_experience(id):

    if "user_id" not in session:
        return redirect("/login")

    experience = Experience.query.get_or_404(id)

    if experience.user_id != session["user_id"]:
        return "Access Denied"

    if experience.certificate_file:

        filepath = os.path.join(
            app.config["EXPERIENCE_FOLDER"],
            experience.certificate_file
        )

        if os.path.exists(filepath):
            os.remove(filepath)

    db.session.delete(experience)

    db.session.commit()

    #return redirect("/profile")
    return redirect("/profile#experience")

@app.route("/settings")
def settings():

    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "settings.html"
    )

@app.route("/change_password", methods=["POST"])
def change_password():

    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(
        session["user_id"]
    )

    old_password = request.form["old_password"]
    new_password = request.form["new_password"]
    confirm_password = request.form["confirm_password"]

    if not check_password_hash(
        user.password,
        old_password
    ):
        return "Current Password Incorrect"

    if new_password != confirm_password:
        return "Passwords Do Not Match"

    user.password = generate_password_hash(
        new_password
    )

    db.session.commit()

    return redirect("/settings")

@app.route("/change_email", methods=["POST"])
def change_email():

    if "user_id" not in session:
        return redirect("/login")

    new_email = request.form["new_email"]

    existing_user = User.query.filter_by(
        email=new_email
    ).first()

    if existing_user:
        return "Email already exists"

    user = User.query.get(
        session["user_id"]
    )

    user.email = new_email

    db.session.commit()
    return redirect("/settings")

@app.route("/deactivate_account")
def deactivate_account():

    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(
        session["user_id"]
    )

    user.is_active = False

    db.session.commit()

    session.clear()

    return redirect("/login")

@app.route("/confirm_delete_account")
def confirm_delete_account():

    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "confirm_delete.html"
    )

@app.route("/delete_account", methods=["POST"])
def delete_account():

    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])

    password = request.form["password"]

    if not check_password_hash(
        user.password,
        password
    ):
        return "Wrong Password"

    Project.query.filter_by(
        user_id=user.id
    ).delete()

    Skill.query.filter_by(
        user_id=user.id
    ).delete()

    Education.query.filter_by(
        user_id=user.id
    ).delete()

    Achievement.query.filter_by(
        user_id=user.id
    ).delete()

    Experience.query.filter_by(
        user_id=user.id
    ).delete()

    Resume.query.filter_by(
        user_id=user.id
    ).delete()

    Certificate.query.filter_by(
        user_id=user.id
    ).delete()

    AboutMe.query.filter_by(
        user_id=user.id
    ).delete()

    SocialLink.query.filter_by(
        user_id=user.id
    ).delete()

    Feedback.query.filter_by(
    email=user.email
    ).delete()

    db.session.delete(user)

    db.session.commit()

    session.clear()

    return render_template(
    "success.html",
    message="Account Deleted Successfully",
    redirect_url="/register"
)

@app.route("/user/<username>")
def public_profile(username):

    user = User.query.filter_by(
        name=username
    ).first()

    if not user:
        return "User Not Found"

    return render_template(
        "public_profile.html",
        user=user
    )

@app.route("/terms")
def terms():

    return render_template(
        "terms.html"
    )

@app.route("/feedback", methods=["GET", "POST"])
def feedback():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        user = User.query.get(session["user_id"])

        new_feedback = Feedback(
    name=user.name,
    email=user.email,
    message=request.form["message"],
    user_id=user.id
    )

        db.session.add(new_feedback)

        db.session.commit()

        return "Feedback Submitted Successfully ✅"

    return render_template(
        "feedback.html"
    )

@app.route("/all_feedback")
def all_feedback():

    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])

    if user.email != ADMIN_EMAIL:
        return "Access Denied ❌"

    feedbacks = Feedback.query.all()

    return render_template(
        "all_feedback.html",
        feedbacks=feedbacks
    )

@app.route("/admin")
def admin():

    if "user_id" not in session:
        return redirect("/login")
    
    user = User.query.get(session["user_id"])

    if user.email != ADMIN_EMAIL:
        return "Access Denied ❌"
    
    users = User.query.all()

    projects = Project.query.all()

    feedbacks = Feedback.query.all()

    return render_template(
        "admin.html",
        users=users,
        projects=projects,
        feedbacks=feedbacks
    )

@app.route("/reply_feedback/<int:id>", methods=["POST"])
def reply_feedback(id):

    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])

    if user.email != ADMIN_EMAIL:
        return "Access Denied ❌"

    feedback = Feedback.query.get_or_404(id)

    feedback.reply = request.form["reply"]

    db.session.commit()

    return redirect("/all_feedback")

@app.route("/feedback_chat/<int:id>")
def feedback_chat(id):

    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])

    if user.email != ADMIN_EMAIL:
        return "Access Denied ❌"
    
    feedback = Feedback.query.get_or_404(id)

    messages = FeedbackMessage.query.filter_by(
        feedback_id=id
    ).all()

    return render_template(
        "feedback_chat.html",
        feedback=feedback,
        messages=messages
    )
@app.route("/user_reply/<int:id>", methods=["POST"])
def user_reply(id):

    if "user_id" not in session:
        return redirect("/login")

    feedback = Feedback.query.get_or_404(id)

    user = User.query.get(session["user_id"])

    if feedback.email != user.email:
        return "Access Denied ❌"

    msg = FeedbackMessage(

        feedback_id=id,

        sender="User",

        message=request.form["message"]

    )

    db.session.add(msg)

    db.session.commit()

    return redirect(
        f"/feedback_chat/{id}"
    )

@app.route("/admin_reply/<int:id>", methods=["POST"])
def admin_reply(id):

    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])

    feedback = Feedback.query.get_or_404(id)

    if feedback.email != user.email and user.email != ADMIN_EMAIL:
        return "Access Denied ❌"

    msg = FeedbackMessage(
        feedback_id=id,
        sender="Admin",
        message=request.form["message"]
    )

    db.session.add(msg)
    db.session.commit()

    return redirect(f"/feedback_chat/{id}")

@app.route("/my_feedback")
def my_feedback():

    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])

    feedbacks = Feedback.query.filter_by(
        email=user.email
    ).all()

    return render_template(
        "my_feedback.html",
        feedbacks=feedbacks
    )

@app.route("/google_login")
def google_login():

    redirect_uri = "http://127.0.0.1:5000/google_callback"

    return google.authorize_redirect(
        redirect_uri
    )

@app.route("/google_callback")
def google_callback():

    token = google.authorize_access_token()

    user_info = token["userinfo"]

    email = user_info["email"]
    name = user_info["name"]

    user = User.query.filter_by(
        email=email
    ).first()

    if not user:

        random_password = generate_password_hash(
            secrets.token_hex(16)
        )

        user = User(
            username=email.split("@")[0],
            name=name,
            email=email,
            password=random_password
        )

        db.session.add(user)
        db.session.commit()

    session["user_id"] = user.id
    session["user_name"] = user.name

    return redirect("/dashboard")

@app.route("/portfolio/<username>")
def public_portfolio(username):

    user = User.query.filter_by(
        username=username
    ).first_or_404()

    skills = Skill.query.filter_by(
        user_id=user.id
    ).all()

    projects = Project.query.filter_by(
    user_id=user.id
    ).all()

    certificates = Certificate.query.filter_by(
    user_id=user.id
    ).all()

    experiences = Experience.query.filter_by(
    user_id=user.id
    ).all()

    social = SocialLink.query.filter_by(
    user_id=user.id
    ).first()

    return render_template(
        "public_portfolio.html",
        user=user,
        skills=skills,
        projects=projects,
        certificates=certificates,
        experiences=experiences,
        social=social
    )

@app.route("/my_username")
def my_username():

    if "user_id" not in session:
        return "Login First"

    user = User.query.get(session["user_id"])

    return f"""
    Name: {user.name}<br>
    Email: {user.email}<br>
    Username: {user.username}
    """

@app.route("/share_profile")
def share_profile():

    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])

    return redirect(f"/portfolio/{user.username}")

if __name__ == "__main__":
    app.run(debug=True)