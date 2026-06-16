from flask import Flask, render_template, request, session, redirect,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime,UTC

app = Flask(__name__)
app.secret_key = "pankaj_portfolio_secret_2026"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///portfolio.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(100), unique=True, nullable=False)

    password = db.Column(db.String(200), nullable=False)

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

        return "User Registered Successfully 🎉"

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


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
