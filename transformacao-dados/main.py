import pdfplumber
import pandas as pd
import zipfile
import os

def get_project_path(filename):
    """Retorna o caminho absoluto do arquivo na pasta do projeto."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, filename)


def extract_tables_from_pdf(pdf_path):
    """Extrai tabelas do PDF e retorna uma lista de dados."""
    data = []
    if not os.path.exists(pdf_path):
        print(f"Erro: Arquivo PDF não encontrado em {pdf_path}")
        return data  

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        data.append(row)
    except Exception as e:
        print(f"Erro ao processar o PDF: {e}")
    return data


def process_data(data):
    """Converte os dados extraídos para um DataFrame estruturado."""
    if not data:
        print("Aviso: Nenhuma tabela foi encontrada no PDF.")
        return pd.DataFrame()  

    df = pd.DataFrame(data)

    # Define os nomes das colunas (ajuste conforme necessário)
    df.columns = ["Procedimento", "OD", "AMB"] + list(df.columns[3:])

    # Substitui as abreviações das colunas OD e AMB pelas descrições completas
    descricao_od = {"S": "SIM", "N": "NÃO"}
    descricao_amb = {"S": "SIM", "N": "NÃO"}

    df["OD"] = df["OD"].map(descricao_od).fillna(df["OD"])
    df["AMB"] = df["AMB"].map(descricao_amb).fillna(df["AMB"])

    return df


def save_csv(df, csv_path):
    """Salva o DataFrame como um arquivo CSV."""
    try:
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        print(f"Arquivo CSV gerado: {csv_path}")
    except Exception as e:
        print(f"Erro ao salvar o CSV: {e}")


def compress_to_zip(csv_path, zip_path):
    """Compacta o arquivo CSV em um ZIP."""
    try:
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(csv_path, os.path.basename(csv_path))
        print(f"Arquivo ZIP gerado: {zip_path}")
    except Exception as e:
        print(f"Erro ao compactar o ZIP: {e}")


def main():
    """Função principal que coordena a extração, processamento e salvamento dos dados."""
    pdf_path = get_project_path("Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf")
    csv_path = get_project_path("Rol_de_Procedimentos.csv")
    zip_path = get_project_path("Teste_Diego.zip")

    # Extração e processamento dos dados
    data = extract_tables_from_pdf(pdf_path)
    df = process_data(data)

    if not df.empty:
        save_csv(df, csv_path)
        compress_to_zip(csv_path, zip_path)


if __name__ == "__main__":
    main()