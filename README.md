# Objetivo
Masses manager foi um protótipo de um gerenciador de massas que comecei com o intuito de:
1. aplicar os conhecimentos de **banco de dados** que venho estudando
2. interagir com a área de **desenvolvimento de software em python** com a interessante biblioteca **Flet**
3. reforçar bons hábitos de código com a construção de uma aplicação inteligente, manutenível e escalável

No geral, os resultados foram excelentes. Consegui estruturar o banco de dados, e todo o código que o segue, de forma planejada e satisfatória, consegui manter o código organizado, escalável e manutenível mesmo diante de um crescimento inesperado na lógica de negócio e, por fim, consegui usufruir bem do que a biblioteca Flet tem a oferecer. Nem tudo foram flores, no entando. Como nunca tive contato com desenvolvimento de software e muito menos com a biblioteca Flet, foi um passo muito além da perna iniciar um projeto tão "ambicioso", o que levou a decisões complicadas mais à frente. 


<div align="center">
  <h1>Masses Manager</h1>
  <img width="191" height="179" alt="pizza png" src="https://github.com/user-attachments/assets/11745a58-8568-43cc-a4ef-1b7a6100bbb0" />
</div>

## Banco de dados
O banco de dados foi estruturado de forma inteligente em duas camadas principais:
1. `database.py`, que lida com as operações de mais baixo nível, não se importando com coisas como lógica de negócio, mas servindo apenas como uma "caixa de ferramentas" para operar o banco de dados
2. `db_manager.py`, que se utiliza do banco de dados para oferecer operações mais complexas, servindo como um "painel de controle".

<div align="center">
  
  ![data file](https://github.com/user-attachments/assets/af18e1e1-e073-4caf-b011-0215cd394c05)
</div>

O banco de dados em si é uma classe que se utiliza da biblioteca **sqlite3** e que tem 3 funções principais:
1. Criar o banco utilizando um schema interno, caso não tenha sido criado
2. Fornecer conexão ao banco de dados
3. Desempenhar as operações cruas de um banco de dados

<div align="center">

  ![MassesDatabase schema](https://github.com/user-attachments/assets/c8e953eb-696f-4273-ba7c-f69509f8f948)
</div>

Já o "administrador do banco de dados" é uma classe que recebe o "bd" e faz operações mais complexas abrindo e fechando conexões. 

## App
A camada da aplicação é a responsável por fazer a ponte entre o banco de dados e a interface do programa. É nela em que a lógica de negócio é aplicada. E ela é essencialmente isso, uma classe que recebe o "dbm", "data base manager", e é passada para as "views" na interface para fazer validações e operações no banco de dados.

## UI
A interface gráfica sofreu diversos refatoramentos por falta de experiência na área, porém a versão final ficou bem satisfatória. Nela, temos duas classes importantes:
1. `interface.py`, responsável por criar e agrupar todas as "views" em um só lugar
2. `base_view.py`, uma base genérica para todas as abas do programa, responsável por instanciar todas as "views"

Não há qualquer segredo sobre a `interface.py`, porém a `base_view.py` é bem complexa, pois abrange basicamente toda a lógica da interface gráfica do programa.

### base_view.py
Todas as views têm um mesmo padrão: todas elas tem uma **área de busca**, uma **visualização do conteúdo** e uma **área para adicionar e atualizar items**:

<div align="center">

  ![base_view cerne](https://github.com/user-attachments/assets/1d29936f-a0de-4188-bd6d-11665b376913)
</div>

#### área de busca
Na parte dos produtos e clientes, a área de busca segue a mesma lógica: buscar pelo nome. As transações, por outro lado, por serem mais complexas, buscam pelo nome do cliente e data.

<div align="center">

https://github.com/user-attachments/assets/8b43a288-4be1-4443-8fd7-1729bbbfd36d
</div>

#### Vizualização do conteúdo
A parte da vizualização segue a mesma lógica para todas as partes: vizualização interativa dos dados de cada tabela.

<div align="center">
  
https://github.com/user-attachments/assets/7d380965-2f54-45c5-adcc-b6274fd92bb7
</div>

#### Adicionar e alterar conteúdo
E, por fim, uma área para executar o "CRUD". Mesma lógica com produtos e clientes, porém bem diferente com transações.

<div align="center">
  
https://github.com/user-attachments/assets/314c372a-8f3f-4ec8-9e3d-f84cf518e443
</div>

---
# Outro
O projeto não saiu como eu imaginava, mas acredito que isso seja esperado pela falta de experiência anterior citada no começo. De qualquer forma, foi muito divertido e instrutivo passar por essa experiência. Acredito que estou mais próximo de desenvolver aplicações profissionais e esse é o objetivo. 

Sinta-se livre para contribuir com o projeto!
