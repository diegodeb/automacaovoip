from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'STI@2024'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # True para administradores

# Criação do banco de dados e do usuário administrador padrão
with app.app_context():
    db.create_all()
    # Criando um usuário administrador padrão se ele não existir
    if not User.query.filter_by(username="admin").first():
        hashed_password = generate_password_hash("admin123", method='pbkdf2:sha256')
        admin_user = User(username="admin", password=hashed_password, is_admin=True)
        db.session.add(admin_user)
        db.session.commit()

# Rota para a página de administração de usuários
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'user' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
    
    users = User.query.all()
    
    return render_template('admin.html', users=users)

@app.route('/add_user', methods=['POST'])
def add_user():
    if 'user' in session and session.get('is_admin'):
        username = request.form['username']
        password = request.form['password']
        is_admin = 'is_admin' in request.form
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        new_user = User(username=username, password=hashed_password, is_admin=is_admin)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Novo usuário adicionado com sucesso!')
        return redirect(url_for('admin'))
    return redirect(url_for('login'))


# Rota para deletar um usuário
@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    if 'user' in session and session.get('is_admin'):
        user = User.query.get(id)
        if user:
            db.session.delete(user)
            db.session.commit()
            flash('Usuário deletado com sucesso!')
    return redirect(url_for('admin'))

# Rota para editar um usuário
@app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    if 'user' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
    
    user = User.query.get(id)
    if request.method == 'POST':
        user.username = request.form['username']
        if request.form['password']:
            user.password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        user.is_admin = 'is_admin' in request.form
        db.session.commit()
        
        flash('Informações do usuário atualizadas!')
        return redirect(url_for('admin'))
    
    return render_template('edit_user.html', user=user)


#############
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Verifica se o usuário logado é um administrador
    if 'user' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        new_user = User(username=username, password=hashed_password, is_admin=False)  # Novo usuário N1
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user'] = username
            session['is_admin'] = user.is_admin
            return redirect(url_for('index'))
        else:
            return "Login falhou. Verifique o nome de usuário e a senha."
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('is_admin', None)
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    provision_config = None
    mac = None
    username = None
    ippabx = None
    label = None
    password = None

    # Nome do arquivo de exemplo
    nome_arquivo = 'PROVISION_TEMPLATE'

    # Carregando o conteúdo do arquivo
    with open(nome_arquivo, 'r') as arquivo:
        conteudo = arquivo.read()
    provision_template = conteudo  # Carregando no contexto local

    # Listando os diretórios de provisionamento
    directories = [d for d in os.listdir('provision_files') if os.path.isdir(os.path.join('provision_files', d))]
    base_directory = os.path.abspath('provision_files')

    if request.method == 'POST':
        if 'generate_config' in request.form:
            chamado = request.form.get('chamado')
            mac = request.form.get('mac', "")
            ramal = request.form.get('ramal', "")
            ippabx = request.form.get('ippabx', "")
            label = request.form.get('label', "")
            password = request.form.get('password', "")

            # Substituindo os valores no template de provisionamento
            provision_config = (
                    provision_template
                    .replace('{{ mac }}', mac)
                    .replace('{{ ramal }}', ramal)
                    .replace('{{ ippabx }}', ippabx)
                    .replace('{{ label }}', label)
                    .replace('{{ password }}', password)
            )

            # Criando diretório de provisionamento
            if not os.path.exists(base_directory):
                os.makedirs(base_directory)

            directory = os.path.join(base_directory, mac)
            os.makedirs(directory, exist_ok=True)
            with open(os.path.join(directory, f"{mac}.conf"), "w") as f:
                f.write(provision_config)
                
        elif 'select_directory' in request.form:
            selected_directory = request.form.get('select_directory')
            if selected_directory:
                mac = selected_directory
                with open(os.path.join('provision_files', selected_directory, f"{selected_directory}.conf"), "r") as f:
                    provision_config = f.read()

    return render_template(
      'index.html',
      provision_config=provision_config,
      mac=mac,
      username=username,
      ippabx=ippabx,
      label=label,
      password=password,
      directories=directories
    )

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5600, debug=True)

