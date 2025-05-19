from flask import Flask, render_template, request, jsonify, redirect, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/gith'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

class Repository(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    creator_username = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False)
    __table_args__ = (db.UniqueConstraint('name', 'creator_username', name='unique_name_per_creator'),)

@app.route('/')
def index():
    if 'username' not in session:
        return redirect('/login')
    return render_template('index.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    
    if User.query.filter_by(username=username).first():
        return jsonify({'message': '用户名已存在'}), 400
        
    new_user = User(username=username)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': '注册成功'}), 201

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')
    
@app.route('/index', methods=['GET'])
def index_page():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user:
        session['username'] = user.username
        return jsonify({'success': True, 'message': '登录成功'})
    return jsonify({'success': False, 'message': '用户不存在'})

@app.route('/get_username')
def get_username():
    if 'username' in session:
        return jsonify({'username': session['username']})
    return jsonify({'username': None})

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({'message': '登出成功'})

@app.route('/create_repo')
def create_repo_page():
    if 'username' not in session:
        return redirect('/login')
    return render_template('create_repo.html')

@app.route('/create_repo', methods=['POST'])
def create_repo():
    if 'username' not in session:
        return jsonify({'message': '请先登录'}), 401
    
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    creator_username = session['username']
    
    if Repository.query.filter_by(name=name, creator_username=creator_username).first():
        return jsonify({'message': '仓库名已存在'}), 400
    
    new_repo = Repository(name=name, description=description, creator_username=creator_username)
    db.session.add(new_repo)
    db.session.commit()
    
    return jsonify({'message': '仓库创建成功'}), 201

@app.route('/view_repo')
def view_repo_page():
    if 'username' not in session:
        return redirect('/login')
    return render_template('view_repo.html')

@app.route('/get_repositories')
def get_repositories():
    repositories = Repository.query.all()
    return jsonify({
        'repositories': [
            {
                'name': repo.name,
                'description': repo.description,
                'creator_username': repo.creator_username
            } for repo in repositories
        ]
    }), 200

if __name__ == '__main__':
    app.run(port=5004)