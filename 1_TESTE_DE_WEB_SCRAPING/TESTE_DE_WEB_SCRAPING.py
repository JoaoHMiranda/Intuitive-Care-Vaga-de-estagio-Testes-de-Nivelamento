#Joao Henrique Silva de Miranda
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import zipfile
import os

# URL da página com os anexos
url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

# Acessa a página
response = requests.get(url)
if response.status_code != 200:
    print("Erro ao acessar o site.")
    exit(1)

soup = BeautifulSoup(response.content, 'html.parser')
links = soup.find_all('a')

anexo_i_pdf_url = None
anexo_ii_url = None

# Procura os links utilizando regex e valida se é PDF (no caso do Anexo I)
for link in links:
    texto = link.get_text(strip=True)
    href = link.get('href', '')

    if re.search(r'anexo\s*i\b', texto, re.IGNORECASE):
        if href.lower().endswith('.pdf'):  # garante que é o PDF
            anexo_i_pdf_url = urljoin(url, href)
    elif re.search(r'anexo\s*ii\b', texto, re.IGNORECASE):
        anexo_ii_url = urljoin(url, href)

if not anexo_i_pdf_url or not anexo_ii_url:
    print("Não foi possível encontrar um ou ambos os anexos desejados (Anexo I em PDF, Anexo II).")
    exit(1)

def download_pdf(url, filename):
    print(f"Baixando {filename} de {url}")
    r = requests.get(url)
    if r.status_code != 200:
        print(f"Erro ao baixar {filename}.")
        return False
    content_type = r.headers.get('Content-Type', '')
    if 'application/pdf' not in content_type:
        print(f"Aviso: O conteúdo baixado para {filename} não parece ser um PDF (Content-Type: {content_type}).")
        return False
    with open(filename, "wb") as f:
        f.write(r.content)
    with open(filename, "rb") as f:
        if f.read(5) != b'%PDF-':
            print(f"Aviso: O arquivo {filename} não possui a assinatura de um PDF válido.")
            return False
    print(f"Arquivo salvo: {filename}")
    return True

# Baixa e valida os anexos
if not download_pdf(anexo_i_pdf_url, "Anexo_I.pdf"):
    print("Falha ao baixar ou validar o Anexo I.")
    exit(1)

if not download_pdf(anexo_ii_url, "Anexo_II.pdf"):
    print("Falha ao baixar ou validar o Anexo II.")
    exit(1)

# Compacta os dois PDFs em um arquivo ZIP
zip_filename = "Anexos.zip"
print("Compactando arquivos em ZIP...")
with zipfile.ZipFile(zip_filename, 'w') as zipf:
    zipf.write("Anexo_I.pdf")
    zipf.write("Anexo_II.pdf")
print(f"Arquivo ZIP criado: {zip_filename}")
