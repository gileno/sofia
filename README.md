# SOFIA

Uma simples plataforma educacional onde são desenvolvidos projetos que por sua vez são acompanhados por líderes. Inicialmente contém apenas ferramentas básicas como:

- Sistema de Usuários
- Criação/Gerenciamento de Projetos
- Sistema de Anúncios para cada projeto
- Exibição de vídeo aulas e outros materiais digitais
- Fórum Único mas organizado por projeto e aula
- Sistema de exercícios online e offline
- Wiki para os projetos
- Relatório dos dados da plataforma (acessos dos usuários aos conteúdos)

A ideia inicial é suprir as necessidades do curso: [Python para Zumbis](http://pycursos.com/python-para-zumbis/)

## Futuramente

- Análise avançada dos dados gerados pela plataforma
- Melhoria na colaboração do projeto (ideia principal, desenvolvimento do projeto/curso em conjunto)
- Exercícios mais dinâmicos: Possibilidade de inserir código Python para validar exercícios
- Análise das dificuldades de cada usuário em cada projeto
- Sistema de recompensas (badges)

## Tecnologias utilizadas

- Python 3
- Django 1.7
- E todas as bibliotecas mencionadas no requirements.txt

## Quer testar?

A plataforma ainda está em fase de desenvolvimento mas se deseja ver a cara dela, baixe o projeto instale as seguintes ferramentas:

- [python3](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/latest/)
- Postgresql (se deseja utilizar outro banco modifique o settings.py do projeto)
- [make](https://www.gnu.org/software/make/)
- [virtualenv](https://pypi.python.org/pypi/virtualenv)

Com essas ferramentas instaladas, crie um ambiente virtual usando o virtualenv e em seguida através do terminal ou prompt de comando acesse a pasta do projeto Sofia. Antes de configurar o projeto crie um banco de dados com o nome *sofia* com direito de acesso a um usuário chamado *sofia* que tenha a senha *sofia* também. Após isso poderá rodar o comando:

```
make setup
```

Quando a plataforma estiver estável irei documentar melhor a instalação em ambiente de desenvolvimento e produção.

## Quer conversar?

E-mail para contato@gilenofilho.com.br
