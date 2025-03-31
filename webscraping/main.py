import requests
from bs4 import BeautifulSoup
import os
import zipfile

def download_pdfs(url, download_folder):
    """Executa a raspagem e faz o dowload dos arquivos PDF."""
    response = requests.get(url)
    if response.status_code != 200:
        print("Erro ao acessar a página.")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True)
    pdf_links = [link['href'] for link in links if ('Anexo_I' in link['href'] or 'Anexo_II' in link['href']) and link['href'].endswith('.pdf')]
    
    if not pdf_links:
        print("Nenhum PDF encontrado.")
        return []
    
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    
    downloaded_files = []
    for pdf_link in pdf_links:
        pdf_url = pdf_link if pdf_link.startswith("http") else url + pdf_link
        pdf_name = os.path.join(download_folder, os.path.basename(pdf_url))
        
        pdf_response = requests.get(pdf_url, stream=True)
        if pdf_response.status_code == 200:
            with open(pdf_name, 'wb') as pdf_file:
                for chunk in pdf_response.iter_content(chunk_size=1024):
                    pdf_file.write(chunk)
            print(f"Baixado: {pdf_name}")
            downloaded_files.append(pdf_name)
        else:
            print(f"Erro ao baixar {pdf_url}")
    
    return downloaded_files

def zip_files(files, zip_name):
    """Compacta os arquivos PDF em um ZI."""
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for file in files:
            zipf.write(file, os.path.basename(file))
    print(f"Arquivos compactados em {zip_name}")
    
def main():
    """""Função principal para executar o download e compactação dos PDFs."""
    url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
    download_folder = "downloads"
    zip_name = "anexos.zip"
    
    pdf_files = download_pdfs(url, download_folder)
    
    if pdf_files:
        zip_files(pdf_files, zip_name)

if __name__ == "__main__":
    main()
