import os
import random
import string
from flask import Flask, request, render_template_string, url_for

app = Flask(__name__)

TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <title>Automação VoIP</title>
  </head>
  <body>
    <nav class="navbar navbar-expand-lg navbar-light">
      <a class="navbar-brand" href="#">Config Generator</a>
      <div class="collapse navbar-collapse">
        <ul class="navbar-nav ml-auto">
          <li class="nav-item">
            <a class="nav-link" href="#">Home</a>
          </li>
        </ul>
      </div>
    </nav>
    <div class="container">
      <div class="row">
        <div class="col-md-8 offset-md-2">
          <div class="card">
            <div class="card-header">
              Generate Configs
            </div>
            <div class="card-body">
              <form method="post" id="generate_form">
                <div class="form-group">
                  <label for="chamado">Num Chamado</label>
                  <input type="text" class="form-control" id="chamado" name="chamado">
                </div>
                <div class="form-group">
                  <label for="address">Endereço</label>
                  <input type="text" class="form-control" id="address" name="address" placeholder="exemplo: teste.sti.ufrn.br">
                </div>
                <div class="form-group">
                  <label for="user">Username</label>
                  <input type="text" class="form-control" id="user" name="user">
                </div>
                {% if password %}
                  <p>User Password: {{ password }}</p>
                {% endif %}
                <button type="submit" name="generate_config" class="btn btn-primary">Generate</button>
              </form>
            </div>
          </div>

          <br>

          <div class="card">
            <div class="card-header">
              Select Config Folder
            </div>
            <div class="card-body">
              <form method="post" id="select_form">
                <div class="form-group">
                  <label for="select_directory">Escolha uma pasta:</label>
                  <select class="form-control" id="select_directory" name="select_directory" required>
                    <option value="">Selecione uma pasta</option>
                    {% for directory in directories %}
                      <option value="{{ directory }}">{{ directory }}</option>
                    {% endfor %}
                  </select>
                </div>
                <button type="submit" class="btn btn-primary">Renderizar</button>
              </form>
            </div>
          </div>

          <br>
          {% if nginx_proxy %}
            <div class="card mt-4">
              <div class="card-header">
                <h3>Passo 1</h3>
                <h4>Crie o arquivo da seguinte forma e no caminho: <br>/etc/nginx/conf.d/{{ address }}.conf</h4>
                <button onclick="copyToClipboard('nginx-proxy')" class="btn btn-secondary">Copiar {{ address }} proxy</button>
              </div>
              <div class="card-body">
                <pre id="nginx-proxy">{{ nginx_proxy }}</pre>
                <button onclick="copyToClipboard('nginx-proxy')" class="btn btn-secondary">Copiar {{ address }} proxy</button>
              </div>
            </div>
          {% endif %}
          {% if nginx_config %}
            <div class="card mt-4">
              <div class="card-header">
                <h3>Passo 2</h3>
                <h4>Crie o arquivo da seguinte forma e no caminho: <br>/data/conf/{{ address }}/{{ address }}.conf</h4>
                <button onclick="copyToClipboard('nginx-config')" class="btn btn-secondary">Copiar {{ address }} config</button>
              </div>
          {% endif %}
        </div>
      </div>
    </div>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <script>
      function copyToClipboard(elementId) {
        var copyText = document.getElementById(elementId).innerText;
        var textarea = document.createElement("textarea");
        textarea.textContent = copyText;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand("copy");
        document.body.removeChild(textarea);
        alert("Configuração copiada!");
      }
    </script>
  </body>
</html>
"""
PROVISION_TEMPLATE = """x"""

@app.route('/', methods=['GET', 'POST'])
def index():
    provision_config = None
    mac = None
    username = None
    ippabx = None
    label = None
    password = None

    # Nome dos arquivos de exemplo
    nome_arquivo = 'PROVISION_TEMPLATE'

    # Abrindo os arquivos para leitura
    with open(nome_arquivo, 'r') as arquivo:
        conteudo = arquivo.read()
    PROVISION_TEMPLATE = conteudo

    directories = [d for d in os.listdir('provision_files') if os.path.isdir(os.path.join('provision_files', d))]

    if request.method == 'POST':
        if 'provision_config' in request.form:
            chamado = request.form['chamado']
            mac = request.form['mac']
            username = request.form['username']
            ippabx = request.form['ippabx']
            label = request.form['label']
            password = request.form['password']

            provision_config = PROVISION_TEMPLATE.replace('{{ mac }}', mac).replace('{{ username }}', username).replace('{{ ippabx }}', ippabx).replace('{{ label }}', label).replace('{{ password }}', password)

            if not os.path.exists('provision_files'):
                os.makedirs('provision_files')

            directory = os.path.join('provision_files', mac)
            os.makedirs(directory, exist_ok=True)
            with open(os.path.join(directory, f"{mac}.conf"), "w") as f:
                f.write(provision_config)
       elif 'select_directory' in request.form:
            selected_directory = request.form['select_directory']
            if selected_directory:
                mac = selected_directory
                with open(os.path.join('provision_files', selected_directory, f"{selected_directory}.conf"), "r") as f:
                    provision_config = f.read()

   return render_template_string(TEMPLATE,
      address=address_name,
      nginx_config=nginx_config,
      nginx_proxy=nginx_proxy,
      compose_config=compose_config,
      password=password,
      user_config=user_config,
      user=user,
      container=container,
      address_certificado=address_certificado,
      directories=directories
    )

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
~                                                                                                       
                                 




