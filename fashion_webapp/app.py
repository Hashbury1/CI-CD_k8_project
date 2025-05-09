from flask import Flask, render_template, request, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy  # If using SQLAlchemy for database
# from flask_migrate import Migrate      # For database migrations

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Important for security

# Database Configuration (if using SQLAlchemy)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# Sample Blog Post Data (replace with database interaction later)
posts = [
    {
        'id': 1,
        'title': 'The Rise of Sustainable Fashion',
        'slug': 'sustainable-fashion',
        'content': 'Explore the growing movement towards eco-conscious clothing...',
        'image': 'static/img/sustainable.jpg',
        'category': 'Trends',
        'tags': ['sustainable', 'eco-friendly', 'fashion'],
        'date': '2025-05-09'
    },
    {
        'id': 2,
        'title': 'Styling a Classic Trench Coat',
        'slug': 'trench-coat-styling',
        'content': 'Versatile ways to wear a timeless trench coat...',
        'image': 'static/img/trench.jpg',
        'category': 'Style Tips',
        'tags': ['classic', 'outerwear', 'styling'],
        'date': '2025-05-08'
    },
    # Add more posts here
]

categories = ['Trends', 'Style Tips', 'Designer Spotlights']
tags = ['sustainable', 'eco-friendly', 'fashion', 'classic', 'outerwear', 'styling']

# Routes
@app.route('/')
def index():
    return render_template('index.html', posts=posts)

@app.route('/post/<slug>')
def post(slug):
    post = next((p for p in posts if p['slug'] == slug), None)
    if post:
        return render_template('post.html', post=post)
    return render_template('404.html'), 404

@app.route('/category/<name>')
def category(name):
    category_posts = [p for p in posts if p['category'] == name]
    return render_template('category.html', category=name, posts=category_posts)

@app.route('/tag/<name>')
def tag(name):
    tag_posts = [p for p in posts if name in p['tags']]
    return render_template('tag.html', tag=name, posts=tag_posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# Basic Admin Routes (Needs more robust implementation)
@app.route('/admin')
def admin_dashboard():
    return render_template('admin/dashboard.html')

@app.route('/admin/new_post', methods=['GET', 'POST'])
def admin_new_post():
    if request.method == 'POST':
        title = request.form['title']
        slug = title.lower().replace(' ', '-')
        content = request.form['content']
        # ... (handle image upload, saving to database, etc.)
        print(f"New post created: {title}")
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/new_post.html')

# Error Handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)