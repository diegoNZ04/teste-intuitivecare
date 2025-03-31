import pdfplumber
import pandas as pd
import zipfile
import os

pdf_path = 'transformacao-dados/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf'
csv_filename = 'Rol_de_Procedimentos.csv'
zip_filename = f'Teste_Diego.zip'
descricao_od = {"S": "SIM", "N": "NÃO"}
descricao_amb = {"S": "SIM", "N": "NÃO"}
data = []

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                data.append(row)
                           
df = pd.DataFrame(data)

df.columns = ["Procedimento", "OD", "AMB"] + list(df.columns[3:])


df["OD"] = df["OD"].map(descricao_od).fillna(df["OD"])
df["AMB"] = df["AMB"].map(descricao_amb).fillna(df["AMB"])

df.to_csv(csv_filename, index=False, encoding="utf-8-sig")

with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(csv_filename)
    
print(f"Arquivo ZIP gerado: {zip_filename}")



    
    