from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskmanager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tasks = db.relationship('Task', backref='user', lazy=True)
    goals = db.relationship('Goal', backref='user', lazy=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(7), default='#3498db')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tasks = db.relationship('Task', backref='category', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, urgent
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed, cancelled
    due_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    progress = db.Column(db.Integer, default=0)  # 0-100

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    target_date = db.Column(db.DateTime)
    progress = db.Column(db.Integer, default=0)  # 0-100
    status = db.Column(db.String(20), default='active')  # active, completed, paused
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Initialize database
with app.app_context():
    db.create_all()
    # Create default user if not exists
    if not User.query.first():
        default_user = User(
            username='admin',
            email='admin@taskmanager.com',
            password_hash=generate_password_hash('admin123')
        )
        db.session.add(default_user)
        db.session.commit()
        
        # Create default categories
        categories = [
            Category(name='Work', color='#3498db', user_id=default_user.id),
            Category(name='Personal', color='#e74c3c', user_id=default_user.id),
            Category(name='Health', color='#2ecc71', user_id=default_user.id),
            Category(name='Learning', color='#f39c12', user_id=default_user.id),
            Category(name='Shopping', color='#9b59b6', user_id=default_user.id),
        ]
        for cat in categories:
            db.session.add(cat)
        db.session.commit()

# Routes
@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    user = User.query.first()  # Simplified: using first user
    if not user:
        return redirect(url_for('login'))
    
    # Statistics
    total_tasks = Task.query.filter_by(user_id=user.id).count()
    completed_tasks = Task.query.filter_by(user_id=user.id, status='completed').count()
    pending_tasks = Task.query.filter_by(user_id=user.id, status='pending').count()
    in_progress_tasks = Task.query.filter_by(user_id=user.id, status='in_progress').count()
    
    # Recent tasks
    recent_tasks = Task.query.filter_by(user_id=user.id).order_by(Task.created_at.desc()).limit(5).all()
    
    # Upcoming tasks (next 7 days)
    upcoming_date = datetime.utcnow() + timedelta(days=7)
    upcoming_tasks = Task.query.filter(
        Task.user_id == user.id,
        Task.due_date <= upcoming_date,
        Task.status != 'completed'
    ).order_by(Task.due_date.asc()).limit(5).all()
    
    # Goals
    active_goals = Goal.query.filter_by(user_id=user.id, status='active').all()
    
    # Productivity stats (last 7 days)
    week_ago = datetime.utcnow() - timedelta(days=7)
    tasks_this_week = Task.query.filter(
        Task.user_id == user.id,
        Task.created_at >= week_ago
    ).count()
    completed_this_week = Task.query.filter(
        Task.user_id == user.id,
        Task.status == 'completed',
        Task.completed_at >= week_ago
    ).count()
    
    return render_template('dashboard.html',
                         total_tasks=total_tasks,
                         completed_tasks=completed_tasks,
                         pending_tasks=pending_tasks,
                         in_progress_tasks=in_progress_tasks,
                         recent_tasks=recent_tasks,
                         upcoming_tasks=upcoming_tasks,
                         active_goals=active_goals,
                         tasks_this_week=tasks_this_week,
                         completed_this_week=completed_this_week)

@app.route('/tasks')
def tasks():
    user = User.query.first()
    if not user:
        return redirect(url_for('login'))
    
    status_filter = request.args.get('status', 'all')
    priority_filter = request.args.get('priority', 'all')
    category_filter = request.args.get('category', 'all')
    search_query = request.args.get('search', '')
    
    query = Task.query.filter_by(user_id=user.id)
    
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    if priority_filter != 'all':
        query = query.filter_by(priority=priority_filter)
    if category_filter != 'all':
        query = query.filter_by(category_id=category_filter)
    if search_query:
        query = query.filter(Task.title.contains(search_query) | Task.description.contains(search_query))
    
    tasks = query.order_by(Task.due_date.asc(), Task.priority.desc()).all()
    categories = Category.query.filter_by(user_id=user.id).all()
    
    return render_template('tasks.html', tasks=tasks, categories=categories,
                         status_filter=status_filter, priority_filter=priority_filter,
                         category_filter=category_filter, search_query=search_query,
                         now=datetime.utcnow())

@app.route('/tasks/create', methods=['GET', 'POST'])
def create_task():
    user = User.query.first()
    if not user:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        task = Task(
            title=request.form['title'],
            description=request.form.get('description', ''),
            priority=request.form.get('priority', 'medium'),
            due_date=datetime.strptime(request.form['due_date'], '%Y-%m-%d') if request.form.get('due_date') else None,
            user_id=user.id,
            category_id=request.form.get('category_id') or None,
            progress=int(request.form.get('progress', 0))
        )
        db.session.add(task)
        db.session.commit()
        flash('Task created successfully!', 'success')
        return redirect(url_for('tasks'))
    
    categories = Category.query.filter_by(user_id=user.id).all()
    return render_template('task_form.html', task=None, categories=categories)

@app.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id):
    user = User.query.first()
    if not user:
        return redirect(url_for('login'))
    
    task = Task.query.get_or_404(task_id)
    if task.user_id != user.id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('tasks'))
    
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form.get('description', '')
        task.priority = request.form.get('priority', 'medium')
        task.due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d') if request.form.get('due_date') else None
        task.category_id = request.form.get('category_id') or None
        task.progress = int(request.form.get('progress', 0))
        task.status = request.form.get('status', 'pending')
        
        if task.status == 'completed' and not task.completed_at:
            task.completed_at = datetime.utcnow()
        elif task.status != 'completed':
            task.completed_at = None
        
        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('tasks'))
    
    categories = Category.query.filter_by(user_id=user.id).all()
    return render_template('task_form.html', task=task, categories=categories)

@app.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    user = User.query.first()
    if not user:
        return redirect(url_for('login'))
    
    task = Task.query.get_or_404(task_id)
    if task.user_id != user.id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('tasks'))
    
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('tasks'))

@app.route('/tasks/<int:task_id>/toggle', methods=['POST'])
def toggle_task(task_id):
    user = User.query.first()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
    
    task = Task.query.get_or_404(task_id)
    if task.user_id != user.id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if task.status == 'completed':
        task.status = 'pending'
        task.completed_at = None
    else:
        task.status = 'completed'
        task.completed_at = datetime.utcnow()
        task.progress = 100
    
    db.session.commit()
    return jsonify({'status': task.status, 'progress': task.progress})

@app.route('/calendar')
def calendar():
    user = User.query.first()
    if not user:
        return redirect(url_for('login'))
    
    tasks = Task.query.filter_by(user_id=user.id).all()
    return render_template('calendar.html', tasks=tasks)

@app.route('/analytics')
def analytics():
    user = User.query.first()
    if not user:
        return redirect(url_for('login'))
    
    # Task completion over time
    tasks_by_status = {
        'completed': Task.query.filter_by(user_id=user.id, status='completed').count(),
        'pending': Task.query.filter_by(user_id=user.id, status='pending').count(),
        'in_progress': Task.query.filter_by(user_id=user.id, status='in_progress').count(),
        'cancelled': Task.query.filter_by(user_id=user.id, status='cancelled').count(),
    }
    
    # Tasks by priority
    tasks_by_priority = {
        'urgent': Task.query.filter_by(user_id=user.id, priority='urgent').count(),
        'high': Task.query.filter_by(user_id=user.id, priority='high').count(),
        'medium': Task.query.filter_by(user_id=user.id, priority='medium').count(),
        'low': Task.query.filter_by(user_id=user.id, priority='low').count(),
    }
    
    # Tasks by category
    categories = Category.query.filter_by(user_id=user.id).all()
    tasks_by_category = {cat.name: Task.query.filter_by(user_id=user.id, category_id=cat.id).count() for cat in categories}
    
    # Monthly completion rate
    current_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    tasks_this_month = Task.query.filter(
        Task.user_id == user.id,
        Task.created_at >= current_month
    ).count()
    completed_this_month = Task.query.filter(
        Task.user_id == user.id,
        Task.status == 'completed',
        Task.completed_at >= current_month
    ).count()
    
    completion_rate = (completed_this_month / tasks_this_month * 100) if tasks_this_month > 0 else 0
    
    return render_template('analytics.html',
                         tasks_by_status=tasks_by_status,
                         tasks_by_priority=tasks_by_priority,
                         tasks_by_category=tasks_by_category,
                         completion_rate=completion_rate,
                         tasks_this_month=tasks_this_month,
                         completed_this_month=completed_this_month)

@app.route('/goals')
def goals():
    user = User.query.first()
    if not user:
        return redirect(url_for('login'))
    
    status_filter = request.args.get('status', 'all')
    query = Goal.query.filter_by(user_id=user.id)
    
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    goals = query.order_by(Goal.target_date.asc()).all()
    return render_template('goals.html', goals=goals, status_filter=status_filter)

@app.route('/goals/create', methods=['GET', 'POST'])
def create_goal():
    user = User.query.first()
    if not user:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        goal = Goal(
            title=request.form['title'],
            description=request.form.get('description', ''),
            target_date=datetime.strptime(request.form['target_date'], '%Y-%m-%d') if request.form.get('target_date') else None,
            progress=int(request.form.get('progress', 0)),
            user_id=user.id
        )
        db.session.add(goal)
        db.session.commit()
        flash('Goal created successfully!', 'success')
        return redirect(url_for('goals'))
    
    return render_template('goal_form.html', goal=None)

@app.route('/goals/<int:goal_id>/edit', methods=['GET', 'POST'])
def edit_goal(goal_id):
    user = User.query.first()
    if not user:
        return redirect(url_for('login'))
    
    goal = Goal.query.get_or_404(goal_id)
    if goal.user_id != user.id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('goals'))
    
    if request.method == 'POST':
        goal.title = request.form['title']
        goal.description = request.form.get('description', '')
        goal.target_date = datetime.strptime(request.form['target_date'], '%Y-%m-%d') if request.form.get('target_date') else None
        goal.progress = int(request.form.get('progress', 0))
        goal.status = request.form.get('status', 'active')
        
        if goal.progress >= 100:
            goal.status = 'completed'
        
        db.session.commit()
        flash('Goal updated successfully!', 'success')
        return redirect(url_for('goals'))
    
    return render_template('goal_form.html', goal=goal)

@app.route('/goals/<int:goal_id>/delete', methods=['POST'])
def delete_goal(goal_id):
    user = User.query.first()
    if not user:
        return redirect(url_for('login'))
    
    goal = Goal.query.get_or_404(goal_id)
    if goal.user_id != user.id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('goals'))
    
    db.session.delete(goal)
    db.session.commit()
    flash('Goal deleted successfully!', 'success')
    return redirect(url_for('goals'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

