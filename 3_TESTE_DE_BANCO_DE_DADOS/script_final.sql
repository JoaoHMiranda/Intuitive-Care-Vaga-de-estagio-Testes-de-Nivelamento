-- Joao Henruque Silva de Miranda
-- 1. Dropar tabelas na ordem correta
DROP TABLE IF EXISTS demonstracoes_contabeis;
DROP TABLE IF EXISTS operadoras;

-- 2. Criar tabela de operadoras
CREATE TABLE operadoras (
    cnpj            VARCHAR(20) PRIMARY KEY,
    nome_fantasia   VARCHAR(255),
    razao_social    VARCHAR(255),
    uf              CHAR(2)
);

-- 3. Criar tabela de demonstrações contábeis
CREATE TABLE demonstracoes_contabeis (
    id              SERIAL PRIMARY KEY,
    cnpj_operadora  VARCHAR(20),
    data_referencia DATE,
    categoria       VARCHAR(255),
    despesa         NUMERIC(18,2),
    CONSTRAINT fk_operadoras FOREIGN KEY (cnpj_operadora) REFERENCES operadoras(cnpj)
);

-- 4. Importar dados das operadoras
\copy operadoras(cnpj, nome_fantasia, razao_social, uf)
FROM '/home/joaoh/programacao/teste/3_TESTE_DE_BANCO_DE_DADOS/Relatorio_cadop.csv'
WITH (FORMAT csv, HEADER true, ENCODING 'UTF8', DELIMITER ';');

-- 5. Importar dados de demonstrações contábeis (2023)
\copy demonstracoes_contabeis FROM '/home/joaoh/programacao/teste/3_TESTE_DE_BANCO_DE_DADOS/2023/1T2023.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8', DELIMITER ';');
\copy demonstracoes_contabeis FROM '/home/joaoh/programacao/teste/3_TESTE_DE_BANCO_DE_DADOS/2023/2T2023.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8', DELIMITER ';');
\copy demonstracoes_contabeis FROM '/home/joaoh/programacao/teste/3_TESTE_DE_BANCO_DE_DADOS/2023/3T2023.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8', DELIMITER ';');
\copy demonstracoes_contabeis FROM '/home/joaoh/programacao/teste/3_TESTE_DE_BANCO_DE_DADOS/2023/4T2023.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8', DELIMITER ';');

-- 5. Importar dados de demonstrações contábeis (2024)
\copy demonstracoes_contabeis FROM '/home/joaoh/programacao/teste/3_TESTE_DE_BANCO_DE_DADOS/2024/1T2024.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8', DELIMITER ';');
\copy demonstracoes_contabeis FROM '/home/joaoh/programacao/teste/3_TESTE_DE_BANCO_DE_DADOS/2024/2T2024.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8', DELIMITER ';');
\copy demonstracoes_contabeis FROM '/home/joaoh/programacao/teste/3_TESTE_DE_BANCO_DE_DADOS/2024/3T2024.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8', DELIMITER ';');
\copy demonstracoes_contabeis FROM '/home/joaoh/programacao/teste/3_TESTE_DE_BANCO_DE_DADOS/2024/4T2024.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8', DELIMITER ';');

-- 6. Consulta: Top 10 operadoras (último trimestre)
WITH max_data_cte AS (
    SELECT MAX(data_referencia) AS max_dt
    FROM demonstracoes_contabeis
)
SELECT o.nome_fantasia,
       SUM(dc.despesa) AS total_despesa
FROM demonstracoes_contabeis dc
JOIN operadoras o ON dc.cnpj_operadora = o.cnpj
JOIN max_data_cte m ON TRUE
WHERE dc.categoria ILIKE '%ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'
  AND dc.data_referencia BETWEEN (m.max_dt - INTERVAL '3 months') AND m.max_dt
GROUP BY o.nome_fantasia
ORDER BY total_despesa DESC
LIMIT 10;

-- 7. Consulta: Top 10 operadoras (último ano)
WITH max_data_cte AS (
    SELECT MAX(data_referencia) AS max_dt
    FROM demonstracoes_contabeis
)
SELECT o.nome_fantasia,
       SUM(dc.despesa) AS total_despesa
FROM demonstracoes_contabeis dc
JOIN operadoras o ON dc.cnpj_operadora = o.cnpj
JOIN max_data_cte m ON TRUE
WHERE dc.categoria ILIKE '%ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'
  AND dc.data_referencia BETWEEN (m.max_dt - INTERVAL '1 year') AND m.max_dt
GROUP BY o.nome_fantasia
ORDER BY total_despesa DESC
LIMIT 10;
