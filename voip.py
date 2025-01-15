from flask import Flask, request, render_template, redirect, url_for, session
import os

app = Flask(__name__)

app.secret_key = "Q!W@e3r4t5"

users = {"admin": "sti@2024"}  # exemplo de dados de usuário

# Definindo o template para provisionamento
PROVISION_TEMPLATE = """x"""

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and users[username] == password:
            session['user'] = username
            return redirect(url_for('index'))
        else:
            return "Login falhou. Verifique o nome de usuário e a senha."
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
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
    app.run(host="0.0.0.0", port=5500, debug=True)

