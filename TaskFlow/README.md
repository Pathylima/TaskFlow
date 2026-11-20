# TaskFlow — Sistema de gerenciamento de tarefas

## 1. Descrição
O TaskFlow é um sistema web acadêmico de gerenciamento de tarefas, desenvolvido para a empresa fictícia TechFlow Solutions, que presta serviços a uma startup de logística. A aplicação permite cadastrar, consultar, editar, excluir e acompanhar tarefas por status e prioridade.

## 2. Objetivo e escopo inicial
O objetivo é demonstrar como práticas de Engenharia de Software e métodos ágeis podem apoiar a organização de atividades, a priorização de demandas e o acompanhamento do trabalho. O escopo inicial contempla cadastro de tarefas com título, descrição e prioridade; listagem; alteração de status; edição e exclusão.

## 3. Metodologia
Será utilizado Kanban para visualizar o fluxo de trabalho no GitHub Projects, com as colunas **To Do**, **In Progress** e **Done**. As tarefas serão divididas em cartões e movidas conforme o progresso. O repositório usará commits semânticos, testes automatizados e integração contínua.

## 4. Tecnologias
- Python 3.12
- Flask para aplicação web
- HTML e CSS para interface
- JSON para persistência local simples
- Pytest para testes automatizados
- GitHub Actions para integração contínua

## 5. Como executar localmente
É necessário ter Python 3.10 ou superior instalado.

1. Clone o repositório e abra a pasta no terminal.
2. Crie um ambiente virtual (recomendado): `python -m venv .venv`.
3. Ative-o no Windows CMD: `.venv\\Scripts\\activate.bat`; no PowerShell: `.venv\\Scripts\\Activate.ps1`; no Linux/macOS: `source .venv/bin/activate`.
4. Instale as dependências: `python -m pip install -r requirements.txt`.
5. Inicie a aplicação: `python src/app.py`.
6. Abra no navegador o endereço `http://127.0.0.1:5000`.

As tarefas são guardadas em `instance/tasks.json`, criado automaticamente na primeira gravação. Esse arquivo não é enviado ao Git por estar no `.gitignore`.

## 6. Testes automatizados
Execute `python -m pytest -v` na raiz do projeto. Os testes verificam o carregamento da página, criação e persistência, validação do título e da prioridade, edição, alteração de status, exclusão e filtro por prioridade. O workflow em `.github/workflows/tests.yml` instala as dependências e executa os testes a cada `push` e `pull_request`.

> O status de aprovação dos testes deve ser confirmado pela execução local ou pela aba **Actions** do GitHub; não declare o workflow como aprovado antes de ver a execução concluída.

## 7. Mudança de escopo simulada
**Escopo inicial:** cadastrar, listar, editar, excluir e atualizar o status das tarefas.

**Mudança adicionada:** filtro de tarefas por prioridade e status. A mudança foi proposta para ajudar a equipe de logística a localizar tarefas críticas com mais rapidez, sem alterar o fluxo principal do sistema. Ela deve ser registrada como novo cartão no Kanban e em um commit específico após a implementação.

## 8. Organização dos diretórios
```text
TaskFlow/
├── .github/workflows/tests.yml
├── docs/
│   ├── diagrama_casos_de_uso.mmd
│   └── diagrama_classes.mmd
├── src/app.py
├── templates/index.html
├── tests/test_app.py
├── .gitignore
├── README.md
└── requirements.txt
```

## 9. Gestão de tarefas no Kanban
Crie um GitHub Project vinculado ao repositório com as colunas `To Do`, `In Progress` e `Done`. Sugestão de cartões iniciais: (1) definir escopo; (2) criar estrutura de pastas; (3) implementar persistência JSON; (4) criar rota de cadastro; (5) montar interface; (6) implementar alteração de status; (7) implementar edição; (8) implementar exclusão; (9) escrever testes; (10) configurar GitHub Actions; (11) criar diagramas UML; (12) adicionar filtros de status/prioridade; (13) documentar mudança de escopo; (14) preparar demonstração e vídeo.

## 10. Histórico de commits sugerido
Crie commits reais, pequenos e com mensagens correspondentes às alterações que você de fato realizar. Sugestões:
- `docs: adiciona descrição inicial do projeto`
- `chore: cria estrutura de diretórios`
- `feat: implementa cadastro e listagem de tarefas`
- `feat: adiciona alteração de status`
- `feat: permite editar tarefas`
- `feat: permite excluir tarefas`
- `test: adiciona testes das rotas principais`
- `ci: configura execução de testes no GitHub Actions`
- `docs: adiciona diagramas UML`
- `feat: adiciona filtros por status e prioridade`

Não crie commits apenas para atingir a quantidade mínima: cada commit deve representar uma mudança real.

## 11. Limitações conhecidas
Este é um protótipo acadêmico, com armazenamento em arquivo JSON e sem autenticação ou banco de dados multiusuário. Não deve ser usado para dados reais ou sensíveis. O projeto pode ser ampliado em versões futuras.
