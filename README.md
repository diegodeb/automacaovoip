# Automação VoIP

Este projeto é uma aplicação de automação para gerenciamento de configurações de VoIP, construída com **Python** e **Flask**. Ele permite criar, editar e gerenciar configurações de ramais, além de integrar com o sistema de automação VoIP.

## Funcionalidades

- Geração automática de configurações de ramais VoIP.
- Interface web para configuração e visualização dos dados.
- Armazenamento de dados persistentes com volumes Docker.
- Facilidade de implantação usando **Docker** e **Docker Compose**.

## Tecnologias

- **Flask** - Framework web para Python.
- **Flask-SQLAlchemy** - ORM para integração com bancos de dados.
- **Werkzeug** - Biblioteca para manipulação de segurança de senhas.
- **Docker** - Contêinerização para facilitar o deploy.
- **Docker Compose** - Gerenciamento de múltiplos containers e configurações de volumes.

## Como baixar e executar o projeto

### Requisitos

- Docker e Docker Compose instalados no seu sistema.
- Git instalado.

### Passos para clonar o repositório

1. Clone o repositório para o seu diretório local:

   ```bash
   git clone https://github.com/seu_usuario/automacaovoip.git
   cd automacaovoip
   ```
O projeto já contém um arquivo docker-compose.yml que facilita a construção e execução da aplicação em containers.

2. Para construir e iniciar a aplicação com Docker Compose, use os seguintes comandos:

Para construir a imagem e iniciar o container:

   ```bash
   docker-compose up --build
   ```
Isso irá construir a imagem, baixar as dependências e iniciar a aplicação.

Para iniciar o container em segundo plano (modo detached):

   ```bash
   docker-compose up -d
   ```
Para verificar os logs da aplicação em execução:
   
   ```bash
   docker-compose logs -f
   ```
Para parar e remover os containers:

   ```bash
   docker-compose down
   ```

3. Persistência de Dados
Os dados são savos no diretório /var/voip/data/provision_files

4. Contribuindo
   .Faça o fork deste repositório.
   .Crie uma branch para a sua feature (git checkout -b minha-feature).
   .Faça o commit das suas mudanças (git commit -am 'Adiciona nova feature').
   .Envie para o branch original (git push origin minha-feature).
   .Abra um pull request.


