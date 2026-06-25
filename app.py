from werkzeug.utils import secure_filename
import os
from flask import Flask, render_template, request, session, redirect,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func
from datetime import datetime,timedelta,UTC
import os
import secrets
import random
from flask_mail import Mail, Message
from authlib.integrations.flask_client import OAuth
from flask import url_for
import requests
from flask_migrate import Migrate
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# app.secret_key = "pankaj_portfolio_secret_2026"

app.secret_key = os.getenv("SECRET_KEY")
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True

app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")

app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

mail = Mail(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///portfolio.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "pdf"
}

def allowed_file(filename):

    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )

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

    cover_photo = db.Column(db.String(200))

    is_active = db.Column(db.Boolean,default=True)
    
class Project(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    technology = db.Column(db.String(200))

    description = db.Column(db.Text)

    github_link = db.Column(db.String(500))

    featured = db.Column(db.Boolean,default=False)

    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))

    project_image = db.Column(db.String(200))

    live_demo = db.Column(db.String(500))

class ContactMessage(db.Model):

    id = db.Column(db.Integer,primary_key=True)

    name = db.Column(db.String(100),nullable=False)

    email = db.Column(db.String(100),nullable=False)

    message = db.Column(db.Text,nullable=False)

    receiver_id = db.Column(db.Integer,db.ForeignKey("user.id"))

class Resume(db.Model):

    id = db.Column(db.Integer,primary_key=True)

    filename = db.Column(db.String(300))

    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))

class Certificate(db.Model):

    id = db.Column(db.Integer,primary_key=True)

    title = db.Column(db.String(200))

    filename = db.Column(db.String(300))

    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))

class Skill(db.Model):

    id = db.Column(db.Integer,primary_key=True)

    name = db.Column(db.String(100))

    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))

class Education(db.Model):

    id = db.Column(db.Integer,primary_key=True)

    level = db.Column(db.String(50))

    institute = db.Column(db.String(200))

    board_university = db.Column(db.String(200))

    stream_degree = db.Column(db.String(200))

    score = db.Column(db.String(50))

    passing_year = db.Column(db.String(20))

    achievements = db.Column(db.Text)

    subjects = db.Column(db.String(300))

    city = db.Column(db.String(100))

    state = db.Column(db.String(100))

    rank = db.Column(db.String(50))

    certificate_file = db.Column(db.String(300))

    marksheet_file = db.Column(db.String(300))

    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))

class AboutMe(db.Model):

    id = db.Column(db.Integer,primary_key=True)

    bio = db.Column(db.Text)

    career_goal = db.Column(db.Text)

    hobbies = db.Column(db.Text)

    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))

class SocialLink(db.Model):

    id = db.Column(db.Integer,primary_key=True)

    github = db.Column(db.String(300))

    linkedin = db.Column(db.String(300))

    leetcode = db.Column(db.String(300))

    codechef = db.Column(db.String(300))

    codeforces = db.Column(db.String(300))

    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))

class Achievement(db.Model):

    id = db.Column(db.Integer,primary_key=True)

    title = db.Column(db.String(200))

    description = db.Column(db.Text)

    achievement_file = db.Column(db.String(300))

    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))

class Experience(db.Model):

    id = db.Column(db.Integer,primary_key=True)

    company = db.Column(db.String(200))

    role = db.Column(db.String(200))

    duration = db.Column(db.String(100))

    description = db.Column(db.Text)

    certificate_file = db.Column(db.String(300))

    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))

class Feedback(db.Model):

    id = db.Column(db.Integer,primary_key=True)

    name = db.Column(db.String(100))

    email = db.Column(db.String(100))

    message = db.Column(db.Text)

    reply = db.Column(db.Text)

    user_id = db.Column(db.Integer)

class FeedbackMessage(db.Model):

    id = db.Column(db.Integer,primary_key=True)

    feedback_id = db.Column(db.Integer,db.ForeignKey("feedback.id"))

    sender = db.Column(db.String(20))

    message = db.Column(db.Text)

    user_reply = db.Column(db.Text)

class Activity(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer)

    activity = db.Column(db.String(200))

class PortfolioView(db.Model):

    id = db.Column(db.Integer,primary_key=True)

    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))

    user = db.relationship("User")

    count = db.Column(db.Integer,default=0)

class PortfolioVisitor(db.Model):

    id = db.Column(db.Integer,primary_key=True)

    portfolio_owner_id = db.Column(db.Integer)

    visitor_ip = db.Column(db.String(100))

class PortfolioLike(db.Model):

    id = db.Column(db.Integer,primary_key=True)

    portfolio_owner_id = db.Column(db.Integer,db.ForeignKey("user.id"))

    visitor_ip = db.Column(db.String(100))

class PasswordResetOTP(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120))
    otp = db.Column(db.String(6))

    created_at = db.Column(db.DateTime,default=datetime.utcnow)

class Badge(db.Model):

    id = db.Column(db.Integer,primary_key=True)

    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))

    badge_name = db.Column(db.String(100))

class PortfolioComment(db.Model):

    id = db.Column(db.Integer,primary_key=True)

    portfolio_owner_id = db.Column(db.Integer)

    visitor_name = db.Column(db.String(100))

    comment = db.Column(db.Text)

class RegistrationOTP(db.Model):

    id = db.Column(db.Integer,primary_key=True)

    email = db.Column(db.String(120))

    otp = db.Column(db.String(6))

class LoginHistory(db.Model):

    id = db.Column(db.Integer,primary_key=True)

    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))

    ip_address = db.Column(db.String(100))

    city = db.Column(db.String(100))

    state = db.Column(db.String(100))

    country = db.Column(db.String(100))

    login_time = db.Column(db.DateTime,default=datetime.utcnow)

@app.route("/upload_resume", methods=["POST"])
def upload_resume():

    if "user_id" not in session:
        return redirect("/login")

    file = request.files["resume"]

    if not allowed_file(file.filename):
        return "Only PDF files allowed"

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

        user = User.query.filter_by(
            email=email
        ).first()

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

                ip = request.remote_addr

                try:

                    response = requests.get(
                        f"http://ip-api.com/json/{ip}"
                    )

                    data = response.json()

                    ip = data.get("query")
                    city = data.get("city")
                    state = data.get("regionName")
                    country = data.get("country")

                    print("IP =", ip)

                    print("Status Code =", response.status_code)

                    print("Response =", response.text)

                    data = response.json()

                    city = data.get(
                        "city"
                    )

                    state = data.get(
                        "regionName"
                    )

                    country = data.get(
                        "country"
                    )

                except:

                    city = "Unknown"
                    state = "Unknown"
                    country = "Unknown"

                history = LoginHistory(

                    user_id=user.id,

                    ip_address=ip,

                    city=city,

                    state=state,

                    country=country

                )

                db.session.add(
                    history
                )

                db.session.commit()

                return redirect(
                    "/dashboard"
                )

        return "Invalid Email or Password 😕"

    return render_template(
        "login.html"
    )
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
        live_demo = request.form["live_demo"]
        image = request.files["project_image"]

        filename = None

        if image and image.filename:

            filename = secure_filename(image.filename)

            image.save(
                os.path.join(
                    "static/project_images",
                    filename
                )
            )

        featured = (
            "featured" in request.form
        )

        project = Project(
            title=title,
            technology=technology,
            description=description,
            github_link=github_link,
            featured=featured,
            user_id=session["user_id"],
            project_image=filename,
            live_demo=live_demo
        )

        activity = Activity(
            user_id=session["user_id"],
            activity="Added a new project"
        )

        db.session.add(project)
        db.session.add(activity)

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

        otp = str(
            random.randint(
                100000,
                999999
            )
        )

        session["reg_name"] = name
        session["reg_email"] = email
        session["reg_password"] = password
        session["reg_otp"] = otp

        msg = Message(
            subject="Portfolio Registration OTP",
            sender=app.config["MAIL_USERNAME"],
            recipients=[email]
        )

        msg.body = f"""
Hi, Welcome to Student Service Platform,
To Create professional Public Portfolio to showcase their skills to everyone on internet
before going to further please read Term & Condition...
Your Registration Code is: {otp}

This OTP will expire in 5 minutes.
"""

        try:

            mail.send(msg)

            return redirect(
                "/verify_registration_otp"
            )

        except Exception as e:

            return f"Email Error: {e}"

    return render_template(
        "register.html"
    )
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

    user_messages = ContactMessage.query.filter_by(
        receiver_id=session["user_id"]
    ).all()

    return render_template(
        "messages.html",
        messages=user_messages
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

@app.route("/about", methods=["GET", "POST"])
def about():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    about = AboutMe.query.filter_by(
        user_id=user_id
    ).first()

    if request.method == "POST":

        bio = request.form["bio"]
        career_goal = request.form["career_goal"]
        hobbies = request.form["hobbies"]

        if about:

            about.bio = bio
            about.career_goal = career_goal
            about.hobbies = hobbies

        else:

            about = AboutMe(
                bio=bio,
                career_goal=career_goal,
                hobbies=hobbies,
                user_id=user_id
            )

            db.session.add(about)

        db.session.commit()

        return redirect("/dashboard")

    return render_template(
        "about.html",
        about=about
    )

@app.route("/contact", methods=["GET", "POST"])
def contact():

    owner_id = request.form.get("owner_id") or request.args.get("user")

    owner = None
    social = None

    if owner_id:

        owner = User.query.get(owner_id)

        social = SocialLink.query.filter_by(
            user_id=owner_id
        ).first()

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        new_message = ContactMessage(
            name=name,
            email=email,
            message=message,
            receiver_id=owner_id
        )

        db.session.add(new_message)
        db.session.commit()

        return render_template(
            "success.html",
            message="Message Sent Successfully 🎉",
            redirect_url="/"
        )

    return render_template(
        "contact.html",
        owner=owner,
        social=social
    )

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

    if not allowed_file(file.filename):
        return "Only PNG, JPG, JPEG files allowed"

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

    old_password = request.form[
        "old_password"
    ]

    new_password = request.form[
        "new_password"
    ]

    confirm_password = request.form[
        "confirm_password"
    ]

    if not check_password_hash(
        user.password,
        old_password
    ):
        return "Current Password Incorrect"

    if new_password != confirm_password:
        return "Passwords Do Not Match"

    otp = str(
        random.randint(
            100000,
            999999
        )
    )

    session["password_change_otp"] = otp
    session["new_password"] = new_password

    msg = Message(
        subject="Password Change OTP",
        sender=app.config["MAIL_USERNAME"],
        recipients=[user.email]
    )

    msg.body = f"""
Your Password Change OTP is: {otp}

This OTP will expire in 5 minutes.
"""

    try:

        mail.send(msg)

    except Exception as e:

        return f"Email Error: {e}"

    return redirect(
        "/verify_password_change_otp"
    )

@app.route(
    "/verify_password_change_otp",
    methods=["GET", "POST"]
)
def verify_password_change_otp():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        entered_otp = request.form[
            "otp"
        ]

        if entered_otp == session.get(
            "password_change_otp"
        ):

            user = User.query.get(
                session["user_id"]
            )

            user.password = (
                generate_password_hash(
                    session["new_password"]
                )
            )

            db.session.commit()

            session.pop(
                "password_change_otp",
                None
            )

            session.pop(
                "new_password",
                None
            )

            return redirect(
                "/settings"
            )

        return "Invalid OTP"

    return render_template(
        "verify_password_change_otp.html"
    )

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

    otp = str(
        random.randint(
            100000,
            999999
        )
    )

    session["new_email"] = new_email
    session["email_change_otp"] = otp

    msg = Message(
        subject="Email Change OTP",
        sender=app.config["MAIL_USERNAME"],
        recipients=[new_email]
    )

    msg.body = f"""
Your Email Change OTP is: {otp}

This OTP will expire in 5 minutes.
"""

    mail.send(msg)

    return redirect(
        "/verify_email_change_otp"
    )
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
        username=username
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

redirect_uri = "http://127.0.0.1:5000/google_callback"
@app.route("/google_callback")
def google_callback():

    token = google.authorize_access_token()

    user_info = google.get(
    "https://openidconnect.googleapis.com/v1/userinfo"
    ).json()

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

    likes = PortfolioLike.query.filter_by(
    portfolio_owner_id=user.id
    ).count()

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

    resume = Resume.query.filter_by(
    user_id=user.id
    ).first()

    view = PortfolioView.query.filter_by(
        user_id=user.id
    ).first()

    ip = request.remote_addr

    existing_visitor = PortfolioVisitor.query.filter_by(
        portfolio_owner_id=user.id,
        visitor_ip=ip
    ).first()

    comments = PortfolioComment.query.filter_by(
        portfolio_owner_id=user.id
    ).all()

    about = AboutMe.query.filter_by(
        user_id=user.id
    ).first()

    if not existing_visitor:

        visitor = PortfolioVisitor(
            portfolio_owner_id=user.id,
            visitor_ip=ip
        )

        db.session.add(visitor)

        if not view:

            view = PortfolioView(
                user_id=user.id,
                count=0
            )

            db.session.add(view)

        view.count += 1

        db.session.commit()

    if not view:

        view = PortfolioView(
            user_id=user.id,
            count=0
        )

    update_badges(user)

    badges = Badge.query.filter_by(
        user_id=user.id
    ).all()

    return render_template(
    "public_portfolio.html",
    user=user,
    skills=skills,
    projects=projects,
    certificates=certificates,
    experiences=experiences,
    social=social,
    resume=resume,
    views=view,
    likes=likes,
    badges=badges,
    comments=comments,
    about=about
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

@app.route("/like_portfolio/<int:user_id>")
def like_portfolio(user_id):

    ip = request.remote_addr

    existing_like = PortfolioLike.query.filter_by(
        portfolio_owner_id=user_id,
        visitor_ip=ip
    ).first()

    if not existing_like:

        like = PortfolioLike(
            portfolio_owner_id=user_id,
            visitor_ip=ip
        )

        db.session.add(like)
        db.session.commit()

    total_likes = PortfolioLike.query.filter_by(
        portfolio_owner_id=user_id
    ).count()

    return {
        "likes": total_likes
    }

@app.route("/top_portfolios")
def top_portfolios():

    top_views = PortfolioView.query.order_by(
        PortfolioView.count.desc()
    ).limit(10).all()

    return render_template(
        "top_portfolios.html",
        top_views=top_views
    )

@app.route("/top_liked")
def top_liked():

    top_likes = db.session.query(
        PortfolioLike.portfolio_owner_id,
        func.count(
            PortfolioLike.id
        ).label("total_likes")
    ).group_by(
        PortfolioLike.portfolio_owner_id
    ).order_by(
        func.count(
            PortfolioLike.id
        ).desc()
    ).all()

    return render_template(
        "top_liked.html",
        top_likes=top_likes
    )

@app.route("/forgot_password", methods=["GET","POST"])
def forgot_password():

    if request.method == "POST":

        email = request.form["email"]

        print("ENTERED EMAIL =", email)

        user = User.query.filter_by(
            email=email
        ).first()

        print("USER =", user)

        if user:

            otp = str(
                random.randint(
                    100000,
                    999999
                )
            )

            print("OTP =", otp)

            reset = PasswordResetOTP(
                email=email,
                otp=otp
            )

            db.session.add(reset)
            db.session.commit()

            msg = Message(
                subject="Portfolio Password Reset OTP",
                sender=app.config["MAIL_USERNAME"],
                recipients=[email]
            )

            msg.body = f"""
Your OTP is: {otp}

This OTP will expire in 5 minutes please paste this OTP in Your OTP Section
"""

            try:

                mail.send(msg)

                print(
                    "EMAIL SENT SUCCESSFULLY"
                )

            except Exception as e:

                print(
                    "EMAIL ERROR =",
                    e
                )

            session["reset_email"] = email

            return redirect(
                "/verify_otp"
            )

        else:

            print(
                "USER NOT FOUND"
            )

            return "Email not registered"

    return render_template(
        "forgot_password.html"
    )

@app.route("/verify_otp", methods=["GET","POST"])
def verify_otp():

    if request.method == "POST":

        entered_otp = request.form["otp"]

        record = PasswordResetOTP.query.filter_by(
            email=session["reset_email"],
            otp=entered_otp
        ).first()

        if record:

            

            if datetime.now(UTC).replace(tzinfo=None) - record.created_at > timedelta(minutes=5):
                return "OTP Expired"

            db.session.delete(record)
            db.session.commit()

            return redirect("/reset_password")

        return "Invalid OTP"

    return render_template(
        "verify_otp.html"
    )
@app.route("/reset_password", methods=["GET","POST"])
def reset_password():

    if request.method == "POST":

        new_password = request.form[
            "password"
        ]

        user = User.query.filter_by(
            email=session["reset_email"]
        ).first()

        if user:

            user.password = generate_password_hash(
                new_password
            )

            db.session.commit()

            session.pop(
                "reset_email",
                None
            )

            return redirect("/login")

        db.session.commit()

        return redirect("/login")

    return render_template(
        "reset_password.html"
    )

@app.route("/upload_cover", methods=["GET", "POST"])
def upload_cover():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        file = request.files["cover"]

        if file.filename == "":
            return "Please select a file"

        if not allowed_file(file.filename):
            return "Invalid file"

        os.makedirs(
            "static/cover_photos",
            exist_ok=True
        )

        filename = secure_filename(
            file.filename
        )

        file.save(
            os.path.join(
                "static/cover_photos",
                filename
            )
        )

        user = User.query.get(
            session["user_id"]
        )

        user.cover_photo = filename

        db.session.commit()

        return redirect("/profile")

    return render_template(
        "upload_cover.html"
    )

@app.route("/google_login")
def google_login():

    redirect_uri = url_for(
        "google_callback",
        _external=True
    )

    return google.authorize_redirect(
        redirect_uri
    )


def update_badges(user):

    views = PortfolioView.query.filter_by(
        user_id=user.id
    ).first()

    likes = PortfolioLike.query.filter_by(
        portfolio_owner_id=user.id
    ).count()

    Badge.query.filter_by(
        user_id=user.id
    ).delete()

    if views and views.count >= 50:

        db.session.add(
            Badge(
                user_id=user.id,
                badge_name="🔥 Top Viewed Creator"
            )
        )

    if likes >= 10:

        db.session.add(
            Badge(
                user_id=user.id,
                badge_name="❤️ Top Liked Creator"
            )
        )

    if likes >= 5 and views and views.count >= 20:

        db.session.add(
            Badge(
                user_id=user.id,
                badge_name="🚀 Rising Developer"
            )
        )

    db.session.commit()

@app.route("/analytics")
def analytics():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    views = PortfolioView.query.filter_by(
        user_id=user_id
    ).first()

    likes = PortfolioLike.query.filter_by(
        portfolio_owner_id=user_id
    ).count()

    projects = Project.query.filter_by(
        user_id=user_id
    ).count()

    certificates = Certificate.query.filter_by(
        user_id=user_id
    ).count()

    skills = Skill.query.filter_by(
        user_id=user_id
    ).count()

    educations = Education.query.filter_by(
        user_id=user_id
    ).count()

    return render_template(
        "analytics.html",
        views=views.count if views else 0,
        likes=likes,
        projects=projects,
        certificates=certificates,
        skills=skills,
        educations=educations
    )

@app.route(
    "/add_comment/<int:user_id>",
    methods=["POST"]
)
def add_comment(user_id):

    visitor_name = request.form[
        "visitor_name"
    ]

    comment_text = request.form[
        "comment"
    ]

    comment = PortfolioComment(
        portfolio_owner_id=user_id,
        visitor_name=visitor_name,
        comment=comment_text
    )

    db.session.add(comment)
    db.session.commit()

    return redirect(request.referrer)

@app.route("/resend_otp")
def resend_otp():

    email = session.get(
        "reset_email"
    )

    if not email:

        return redirect(
            "/forgot_password"
        )

    otp = str(
        random.randint(
            100000,
            999999
        )
    )

    PasswordResetOTP.query.filter_by(
        email=email
    ).delete()

    reset = PasswordResetOTP(
        email=email,
        otp=otp
    )

    db.session.add(reset)
    db.session.commit()

    print(
        "NEW OTP =",
        otp
    )

    return redirect(
        "/verify_otp"
    )

@app.route("/check_users")
def check_users():

    users = User.query.all()

    for user in users:
        print(
            user.id,
            user.username,
            user.email
        )

    return "Check Terminal"

@app.route("/delete_cover")
def delete_cover():

    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(
        session["user_id"]
    )

    if user.cover_photo:

        path = os.path.join(
            "static/cover_photos",
            user.cover_photo
        )

        if os.path.exists(path):
            os.remove(path)

        user.cover_photo = None

        db.session.commit()

    return redirect("/profile")

@app.route(
    "/verify_registration_otp",
    methods=["GET", "POST"]
)
def verify_registration_otp():

    if request.method == "POST":

        entered_otp = request.form["otp"]

        if entered_otp == session.get(
            "reg_otp"
        ):

            new_user = User(
                username=(
                    session["reg_email"]
                    .split("@")[0]
                    + str(random.randint(1000,9999))
                ),
                name=session["reg_name"],
                email=session["reg_email"],
                password=session["reg_password"]
            )

            db.session.add(new_user)
            db.session.commit()

            session["user_id"] = new_user.id
            session["user_name"] = new_user.name

            return redirect("/dashboard")

        return "Invalid OTP"

    return render_template(
        "verify_registration_otp.html"
    )

@app.route(
    "/verify_email_change_otp",
    methods=["GET", "POST"]
)
def verify_email_change_otp():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        entered_otp = request.form["otp"]

        if entered_otp == session.get(
            "email_change_otp"
        ):
            
            user = User.query.get(
                session["user_id"]
            )

            user.email = session[
                "new_email"
            ]

            db.session.commit()

            return redirect("/settings")

        return "Invalid OTP"

    return render_template(
        "verify_email_change_otp.html"
    )

@app.route("/admin_login_history")
def admin_login_history():

    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(
    session["user_id"]
)

    if user.email != "pankajraj2025434@gmail.com":
        return "Access Denied"

    history = db.session.query(
        LoginHistory,
        User
    ).join(
        User,
        LoginHistory.user_id == User.id
    ).order_by(
        LoginHistory.login_time.desc()
    ).all()

    return render_template(
        "admin_login_history.html",
        history=history
    )

if __name__ == "__main__":

    with app.app_context():
        db.create_all()
    app.run(debug=True) 