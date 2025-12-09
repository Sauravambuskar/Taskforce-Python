# TaskMaster - Daily Task Management Web App

A beautiful, modern, and feature-rich task management web application built with Flask, HTML, CSS, and JavaScript. TaskMaster helps you organize your daily tasks, track your goals, and boost your productivity with an intuitive multi-dashboard interface.

## Features

### 🎯 Core Features
- **Multi-Dashboard Interface**: Interactive dashboards for different views
- **Task Management**: Create, edit, delete, and organize tasks
- **Goal Tracking**: Set and track your long-term goals
- **Calendar View**: Visual calendar with task due dates
- **Analytics Dashboard**: Comprehensive statistics and insights
- **Category System**: Organize tasks by categories (Work, Personal, Health, Learning, Shopping)
- **Priority Levels**: Urgent, High, Medium, Low priority system
- **Progress Tracking**: Track task completion progress (0-100%)
- **Status Management**: Pending, In Progress, Completed, Cancelled

### 🎨 UI/UX Features
- **Modern Design**: Clean, professional interface with smooth animations
- **Responsive Layout**: Works perfectly on desktop, tablet, and mobile devices
- **Interactive Elements**: Hover effects, transitions, and animations
- **Color-Coded System**: Visual priority and category indicators
- **Dark/Light Theme Ready**: Easy to customize color scheme
- **Smooth Navigation**: Sidebar navigation with active state indicators

### 📊 Dashboard Features
- **Statistics Cards**: Quick overview of total, completed, pending, and in-progress tasks
- **Recent Tasks**: View your most recently created tasks
- **Upcoming Tasks**: See tasks due in the next 7 days
- **Active Goals**: Track your current goals with progress bars
- **Productivity Stats**: Weekly task creation and completion metrics

### 🔍 Advanced Features
- **Search Functionality**: Search tasks by title or description
- **Advanced Filtering**: Filter by status, priority, and category
- **Task Toggle**: Quick checkbox to mark tasks as complete
- **Progress Sliders**: Visual progress tracking with range sliders
- **Due Date Management**: Set and track task due dates
- **Overdue Indicators**: Visual alerts for overdue tasks

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd flaskk
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open your browser and navigate to: `http://localhost:5000`
   - Default login credentials:
     - Username: `admin`
     - Password: `admin123`

## Project Structure

```
flaskk/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── taskmanager.db        # SQLite database (created automatically)
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── dashboard.html    # Main dashboard
│   ├── tasks.html        # Task list page
│   ├── task_form.html    # Task create/edit form
│   ├── calendar.html     # Calendar view
│   ├── analytics.html    # Analytics dashboard
│   ├── goals.html        # Goals list page
│   ├── goal_form.html    # Goal create/edit form
│   └── login.html        # Login page
└── static/               # Static files
    ├── css/
    │   └── style.css     # Main stylesheet
    └── js/
        └── main.js       # JavaScript functionality
```

## Usage Guide

### Getting Started

1. **Login**: Use the default credentials to log in
2. **Dashboard**: View your overview and quick statistics
3. **Create Tasks**: Click "New Task" to add tasks
4. **Set Goals**: Create goals to track long-term objectives
5. **View Calendar**: Check your calendar for upcoming deadlines
6. **Analytics**: Review your productivity statistics

### Creating a Task

1. Navigate to **Tasks** → Click **New Task**
2. Fill in the task details:
   - Title (required)
   - Description (optional)
   - Priority (Low, Medium, High, Urgent)
   - Category (Work, Personal, Health, etc.)
   - Due Date (optional)
   - Progress (0-100%)
3. Click **Create Task**

### Managing Goals

1. Navigate to **Goals** → Click **New Goal**
2. Set your goal:
   - Title and description
   - Target date
   - Initial progress
3. Update progress as you work towards your goal

### Using Filters

- **Search**: Type in the search box to find tasks
- **Status Filter**: Filter by task status
- **Priority Filter**: Filter by priority level
- **Category Filter**: Filter by category

## Customization

### Adding Categories

Categories are created automatically for the default user. To add more categories, you can modify the initialization code in `app.py` or add them through the database.

### Changing Colors

Edit the CSS variables in `static/css/style.css`:
```css
:root {
    --primary-color: #6366f1;
    --secondary-color: #8b5cf6;
    /* ... more colors ... */
}
```

### Database

The application uses SQLite by default. The database file `taskmanager.db` will be created automatically on first run.

## Features Added

- ✅ Multi-dashboard interface
- ✅ Task CRUD operations
- ✅ Goal tracking system
- ✅ Calendar view with task visualization
- ✅ Analytics and statistics
- ✅ Search and filter functionality
- ✅ Progress tracking
- ✅ Priority and category system
- ✅ Responsive design
- ✅ Smooth animations and transitions
- ✅ Interactive UI elements
- ✅ Flash message notifications
- ✅ Mobile-friendly navigation

## Technologies Used

- **Backend**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript
- **Icons**: Font Awesome 6.4.0
- **Styling**: Custom CSS with CSS Variables

## Future Enhancements

Potential features you could add:
- User authentication system (multiple users)
- Task reminders and notifications
- Task templates
- Recurring tasks
- Task sharing and collaboration
- Export/import functionality
- Dark mode toggle
- Drag and drop task reordering
- Task comments and notes
- File attachments
- Time tracking
- Pomodoro timer integration

## License

This project is open source and available for personal and commercial use.

## Support

For issues or questions, please check the code comments or modify as needed for your requirements.

---

**Enjoy managing your tasks with TaskMaster! 🚀**

