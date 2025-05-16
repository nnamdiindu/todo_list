import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, select, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from typing import List
from flask_login import UserMixin, login_user, current_user, LoginManager, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from forms import EditForm, LoginForm, RegisterForm

load_dotenv()

app = Flask(__name__)

class Base(DeclarativeBase):
    pass

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URI")
app.secret_key = os.environ.get("SECRET_KEY")
db = SQLAlchemy(model_class=Base)
db.init_app(app)
bootstrap = Bootstrap5(app)
login_manager = LoginManager(app)


class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(250), nullable=False)

    # Define the relationship: one user can have many tasks
    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="user")


class Task(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task_name: Mapped[str] = mapped_column(String(250), nullable=False)

    # Foreign key to link to the User table
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))

    # Define the relationship from the task back to the user
    user: Mapped["User"] = relationship("User", back_populates="tasks")


with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/", methods=["GET", "POST"])
def home():
    # Initialize session tasks list if it doesn't exist
    if "guest_tasks" not in session:
        session["guest_tasks"] = []

    if request.method == "POST":
        task = request.form.get("task")
        if task:
            # Update session with new task
            guest_tasks = session["guest_tasks"]
            guest_tasks.append(task)
            session["guest_tasks"] = guest_tasks

    return render_template("index.html", tasks=session["guest_tasks"], current_user=current_user)

@app.route("/dashboard")
@login_required
def dashboard():
    user_tasks = db.session.execute(select(Task).where(Task.user_id == current_user.id)).scalars().all()
    return render_template("index.html", tasks=user_tasks, current_user=current_user)

@app.route("/add-task", methods=["GET", "POST"])
@login_required
def add_task():
    if request.method == "POST":
        new_task = Task(
            task_name=request.form.get("task"),
            user_id=current_user.id
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for("dashboard"))


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = db.session.execute(select(User).where(User.email == form.email.data)).scalar_one_or_none()
        if user:
            if form.email.data == user.email:
                flash("You already signed up, login instead.")
                return redirect(url_for("login"))

        hashed_and_salted_password = generate_password_hash(
            password=form.password.data,
            method="pbkdf2:sha256",
            salt_length=8
        )
        new_user = User(
            name = form.name.data,
            email = form.email.data,
            password = hashed_and_salted_password
        )
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for("dashboard"))
    return render_template("register.html", form=form, current_user=current_user)


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.execute(select(User).where(User.email == form.email.data)).scalar_one_or_none()
        if user:
            if user.email == form.email.data:
                if check_password_hash(user.password, form.password.data):
                    login_user(user)
                    return redirect(url_for("dashboard"))
                else:
                    flash("Incorrect password, please try again.")
                    return redirect(url_for("login"))
        else:
            flash("Email doesn't exist, please sign up")
            return redirect(url_for("register"))
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/edit/<int:task_id>", methods=["POST", "GET"])
def edit(task_id):
    form= EditForm()
    selected_task = db.get_or_404(Task, task_id)
    if request.method == "POST":
        selected_task.task_name = form.name.data
        db.session.commit()
        return redirect(url_for("dashboard"))
    form.name.data = selected_task.task_name

    return render_template("edit.html", form=form, current_user=current_user)


@app.route("/delete/<int:task_id>", methods=["POST", "GET"])
def delete(task_id):
    selected_task = db.get_or_404(Task, task_id)
    db.session.delete(selected_task)
    db.session.commit()
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True)