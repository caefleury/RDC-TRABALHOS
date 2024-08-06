# RDC-TRABALHOS

Projetos da matéria REDES DE COMPUTADORES

## Projeto 1

### Introdução

A compreensão do desenvolvimento de aplicações cliente servidor e da compreensão dos
protocolos de rede pode ser aprofundada ao “ver os protocolos em ação”, observando a
sequência de mensagens trocadas entre duas entidades de protocolo, investigando os detalhes
da operação do protocolo e fazendo com que os protocolos executem certas ações e, em seguida,
observar essas ações e suas consequências. Isso pode ser feito em cenários simulados ou em
um ambiente de rede “real”, como a Internet.

Neste projeto o objetivo é desenvolver uma aplicação na arquitetura cliente servidor e executa-
la em uma rede em diferentes cenários usando seu próprio computador e uma rede privada. Este
projeto requer a utilização de sockets, linguagens de programação e o aplicativo WIRESHARK,
assim como da definição de um ambiente simples que utilize a arquitetura cliente servidor. O
objetivo é aprofundar os conhecimentos na camada de aplicação e verificar e avaliar como os
pacotes são enviados e recebidos entre um conjunto de clientes e um servidor, enquanto é
utilizada uma aplicação de rede.

### Descrição geral do projeto

Deverá ser escolhida um tipo de aplicação para desenvolver e implementar seu próprio
protocolo. No relatório devem ser descritos tipo, formato e tamanho de mensagens, além da
sequência de transmissão ̃ ao delas para a implementação das funcionalidades requeridas. As
aplicações podem ser:

1. Streaming de vídeo
2. Chat em grupo ou
3. Utilitário desincronização de arquivos.

## Projeto de Chat em Grupo

Este projeto é uma aplicação de chat em grupo desenvolvida utilizando Flask para o backend e WebSockets para comunicação em tempo real. A interface do usuário foi construída com HTML, CSS (Bootstrap) e JavaScript (jQuery e Socket.IO).

### Estrutura do Projeto

- `app.py`: Arquivo principal que inicializa a aplicação Flask.
- `models.py`: Define os modelos de dados usando SQLAlchemy.
- `routes.py`: Define as rotas da aplicação.
- `templates/`: Diretório que contém os arquivos HTML.
- `static/`: Diretório que contém arquivos estáticos como CSS e JavaScript.

### Pré-requisitos

- Python 3.8 ou superior
- Pip (gerenciador de pacotes do Python)
- Virtualenv (opcional, mas recomendado)

### Tecnologias Utilizadas

- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-SocketIO
- HTML, CSS (Bootstrap)
- JavaScript (jQuery, Socket.IO)
