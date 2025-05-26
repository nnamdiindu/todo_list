# ✅ To-Do List

A simple and intuitive To-Do List application to help you manage your daily tasks efficiently.

🔗 **Live Demo:** [https://todo-list-xnc9.onrender.com](https://todo-list-xnc9.onrender.com)

---

## 📸 Screenshots

<!-- Replace with actual screenshots -->
![Home Page]![image](https://github.com/user-attachments/assets/160f22fc-6dd9-42d9-abb6-43b5f7f5028f)

---

## 🚀 Features

- 📝 **Add Tasks**: Easily add new tasks to your list.
- 🗑️ **Delete Tasks**: Remove tasks that are no longer needed.
- 🖊️ **Edit Tasks**: Modify task details as needed.
- 📱 **Responsive Design**: Accessible on both desktop and mobile devices.

---

## 🛠️ Built With

- **Python 3** / **Flask**: Backend framework.
- **Jinja2**: Templating engine.
- **SQLite**: Lightweight database for storing tasks.
- **Bootstrap 5**: Frontend framework for responsive design.
- **Render**: Deployment platform.

---

## 📦 Installation (Local Setup)

To run this project locally, follow the steps below:

```bash
# 1. Clone the repository
git clone (https://github.com/nnamdiindu/todo_list.git)
cd todo_list

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate
On Windows: venv\Scripts\activate

# 3. Install required packages
pip install -r requirements.txt

# 4. Set up environment variables
Create a .env file in the root directory and add:
SECRET_KEY and your_flask_secret_key

# 5. Initialize the database
flask db init
flask db migrate
flask db upgrade

# 6. Run the Flask development server
flask run
