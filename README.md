## Prática em Banco de Dados Relacional | Consultas SQL & Organização de Tabelas

<div align="center">

  <img src="https://github.com/Zerogallo/Banco-de-Dados-Relacional-Consultas-SQL-Organiza-o-de-Tabelas/blob/main/Captura%20de%20tela%202026-04-09%20081026.png" style="width: 600px; height: 300px;"/>
  
</div>


## 💻 README.md - Projeto de Prática com SQL (PostgreSQL)

📌 Descrição do Projeto

Este repositório documenta minha prática com bancos de dados relacionais utilizando PostgreSQL. O foco foi a criação, consulta e organização de uma tabela de produtos, aplicando comandos SQL essenciais para manipulação e ordenação de dados.

🧠 O que foi feito / Aprendizado

· Criação e estruturação da tabela produtos com colunas: codigo, nome e preco.
· Inserção de registros variados (ex: "authority" com preço 934.74, "milk" com 3.00).
· Consulta completa com SELECT * FROM public.produtos.
· Ordenação dos resultados por código usando ORDER BY codigo ASC.
· Exploração de tipos de dados como character varying(255) para strings.
· Organização e limpeza dos dados para facilitar a leitura e futuras análises.

## 🛠️ Tecnologias utilizadas

· PostgreSQL 18
· SQL (DQL - SELECT, ORDER BY)


✅ Exemplo de consulta

```sql
SELECT * 
FROM public.produtos
ORDER BY codigo ASC;
```

## 🎯 Resultado do aprendizado

Com essa prática, desenvolvi habilidade para:

· Escrever consultas SQL claras e eficientes.
· Ordenar e filtrar dados de forma lógica.
· Compreender a importância da estrutura de um banco de dados relacional para aplicações reais.
