#Joao Henrique Silva de Miranda
import pdfplumber
import pandas as pd
import zipfile
import os

# Nome do arquivo PDF do Anexo I (resultado do Teste 1)
pdf_path = "Anexo_I.pdf"
# Nome do arquivo CSV intermediário
csv_filename = "Rol_de_Procedimentos.csv"

# Lista para armazenar as linhas de todas as páginas
all_rows = []
header = None

# Abre o PDF e extrai a tabela de cada página
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        table = page.extract_table()
        if table:
            # Na primeira página, define o cabeçalho e os dados
            if header is None:
                header = table[0]
                data_rows = table[1:]
            else:
                # Se o cabeçalho for repetido em páginas subsequentes, descarta-o
                if table[0] == header:
                    data_rows = table[1:]
                else:
                    data_rows = table
            all_rows.extend(data_rows)

# Verifica se foi encontrado algum cabeçalho (ou seja, se alguma tabela foi extraída)
if header is None:
    print("Nenhuma tabela encontrada no PDF.")
    exit(1)

# Cria o DataFrame com os dados extraídos
df = pd.DataFrame(all_rows, columns=header)

# Mapeamento para substituir as abreviações pelas descrições completas
col_mapping = {
    "OD": "Procedimentos Odontológicos",       # ajuste conforme a legenda do PDF
    "AMB": "Procedimentos Ambulatoriais"         # ajuste conforme a legenda do PDF
}

# Renomeia as colunas se existirem
df.rename(columns=col_mapping, inplace=True)

# Salva os dados em formato CSV
df.to_csv(csv_filename, index=False, encoding="utf-8")
print(f"Dados salvos em {csv_filename}")

# Compacta o CSV em um arquivo ZIP com o nome solicitado
zip_filename = "Teste_Joao_Henrique_Silva_de_Miranda.zip"
with zipfile.ZipFile(zip_filename, 'w') as zipf:
    zipf.write(csv_filename)
print(f"Arquivo ZIP criado: {zip_filename}")

# (Opcional) Remove o arquivo CSV se não for necessário mantê-lo separado
os.remove(csv_filename)
