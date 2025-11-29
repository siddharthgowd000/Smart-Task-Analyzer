# 🎯 Smart Task Analyzer

A web application that helps you prioritize and organize your tasks intelligently. Whether you're juggling multiple projects or just trying to figure out what to tackle next, this tool analyzes your tasks and suggests the best order to work on them based on different strategies.

## What Does This Do?

Imagine you have a bunch of tasks - some are urgent, some are important, some take a long time, and some depend on others. This application takes all that information and gives you a smart, prioritized list so you know exactly what to work on next.

**Key Features:**

- 📝 Add tasks manually or import them in bulk using JSON
- 🎯 Choose from 4 different prioritization strategies
- 📊 Get detailed scores and explanations for each task
- 🎨 Visual priority indicators (High/Medium/Low)
- 🔗 Handle task dependencies automatically

## 🏗️ How It Works

This is a **full-stack web application** built with:

- **Frontend**: Plain HTML, CSS, and JavaScript (no frameworks needed!)
- **Backend**: Django REST API (Python web framework)
- **Database**: SQLite (comes built-in, no setup needed)

The frontend is a simple, clean interface where you input your tasks. When you click "Analyze Tasks", it sends your tasks to the backend server, which uses a smart scoring algorithm to prioritize them based on:

- Due dates (urgent tasks get higher priority)
- Importance level (1-10 scale)
- Estimated effort (quick wins are prioritized in some strategies)
- Dependencies (tasks that other tasks depend on get boosted)

## Getting Started

### Prerequisites

Before you start, make sure you have:

- **Python 3.8 or higher** installed on your computer
  - Check by running: `python --version` or `python3 --version`
- A web browser (Chrome, Firefox, Edge, etc.)

### Step-by-Step Setup

#### 1. Navigate to the Project Folder

Open your terminal (Command Prompt on Windows, Terminal on Mac/Linux) and go to the project directory:

```bash
cd (your folder name)
```

_Note: If you're on a different computer, adjust the path to wherever you saved this project._

#### 2. Create a Virtual Environment (Recommended)

A virtual environment keeps your project's dependencies separate from other Python projects. It's like having a separate toolbox for this project.

**On Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**On Mac/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

You'll know it worked when you see `(venv)` at the start of your terminal prompt.

_Note: If you already have a `venv` folder, you can skip creating it and just activate it._

#### 3. Install Dependencies

This project uses Django, a Python web framework. Install it with:

```bash
pip install -r requirements.txt
```

This reads the `requirements.txt` file and installs Django (version 4.2) and all its dependencies.

#### 4. Set Up the Database

Django needs to create its database tables. Run:

```bash
python manage.py migrate
```

This creates a SQLite database file (`db.sqlite3`) in your project folder. Don't worry - it's just a file, and you don't need to configure anything!

#### 5. Start the Backend Server

Now let's start the Django server:

```bash
python manage.py runserver
```

You should see something like:

```
Starting development server at http://127.0.0.1:8000/
```

**Keep this terminal window open!** The server needs to keep running. You can minimize it, but don't close it.

#### 6. Open the Frontend

Now open the `frontend/index.html` file in your web browser. You can do this by:

- Double-clicking the file in your file explorer, OR
- Right-clicking the file and selecting "Open with" → your browser, OR
- Dragging the file into your browser window

The application should now be running! You'll see a form on the left to add tasks and a results area on the right.

## 📖 How to Use

### Adding Tasks Manually

1. Fill in the form on the left side:

   - **Title**: What needs to be done (required)
   - **Due date**: When it's due (optional, but helps with prioritization)
   - **Estimated hours**: How long you think it will take
   - **Importance**: Rate from 1-10 (10 = most important)
   - **Dependencies**: If this task depends on other tasks, enter their IDs separated by commas (e.g., "1,2,3")

2. Click **"Add Task"** to add it to your list

3. Repeat for all your tasks

### Loading Tasks from JSON

If you have many tasks, you can paste them all at once as JSON:

```json
[
  {
    "title": "Fix login bug",
    "due_date": "2025-11-30",
    "estimated_hours": 3,
    "importance": 8,
    "dependencies": []
  },
  {
    "title": "Write documentation",
    "due_date": "2025-12-05",
    "estimated_hours": 5,
    "importance": 6,
    "dependencies": [1]
  }
]
```

1. Paste your JSON into the "Bulk JSON input" textarea
2. Click **"Load JSON"**
3. Your tasks will appear in the results area

### Analyzing Tasks

Once you have tasks added:

1. Select a **sorting strategy** from the dropdown:

   - **Smart Balance**: Considers all factors equally (default)
   - **Fastest Wins**: Prioritizes quick tasks you can finish fast
   - **High Impact**: Focuses on the most important tasks
   - **Deadline Driven**: Puts urgent tasks with due dates first

2. Click **"Analyze Tasks"**

3. The results will show your tasks sorted by priority, with:
   - A **score** (higher = more urgent)
   - A **priority level** (High/Medium/Low)
   - An **explanation** of why it got that score

Tasks are color-coded:

- 🔴 **Red border**: High priority
- 🟠 **Orange border**: Medium priority
- 🟢 **Green border**: Low priority


## 🛠️ Project Structure

```
Task Analyzer/
├── backend/              # Django project settings
│   ├── settings.py       # Configuration
│   └── urls.py           # Main URL routing
├── tasks/                # Main Django app
│   ├── models.py         # Task data model
│   ├── views.py          # API endpoints
│   ├── scoring.py        # Prioritization logic
│   └── urls.py           # App URL routing
├── frontend/             # Frontend files
│   ├── index.html        # Main page
│   ├── styles.css        # Styling
│   └── script.js         # Frontend logic
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
└── db.sqlite3            # Database (created after migration)
```


## 🙏 Acknowledgments

Built with:

- [Django](https://www.djangoproject.com/) - The web framework for perfectionists with deadlines
- Plain JavaScript - No frameworks, just vanilla JS for simplicity
- Modern CSS - Clean, responsive design

---

**Happy task managing!**
