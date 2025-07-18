import pandas as pd
import numpy as np
import random
from datetime import timedelta

# Configurações iniciais
num_linhas = 10000
data_inicio = pd.to_datetime("2020-03-22")
data_fim = pd.to_datetime("2021-12-31")

# Províncias e distritos (resumido para espaço; podes expandir conforme necessário)
provincia_distritos = {
    "Cabo Delgado": [
        "Balama", "Chiúre", "Ibo", "Macomia", "Mecúfi", "Meluco", "Mocímboa da Praia",
        "Montepuez", "Mueda", "Muidumbe", "Namuno", "Nangade", "Palma", "Pemba"
    ],
    "Gaza": [
        "Bilene", "Chibuto", "Chigubo", "Chókwè", "Guijá", "Limpopo", "Mabalane", "Manjacaze",
        "Mapai", "Massangena", "Massingir", "Xai-Xai"
    ],
    "Inhambane": [
        "Funhalouro", "Govuro", "Homoíne", "Inharrime", "Inhassoro", "Jangamo", "Massinga",
        "Morrumbene", "Panda", "Vilankulo", "Zavala", "Maxixe", "Inhambane"
    ],
    "Manica": [
        "Barue", "Chimoio", "Gondola", "Guro", "Machaze", "Macossa", "Manica", "Mossurize",
        "Sussundenga", "Tambara", "Vanduzi"
    ],
    "Maputo Província": [
        "Boane", "Magude", "Manhiça", "Marracuene", "Matola", "Moamba", "Namaacha", "Matutuíne"
    ],
    "Maputo Cidade": [
        "KaMpfumu", "Nhlamankulu", "KaMaxaquene", "KaMavota", "KaMubukwana", "KaTembe", "KaNyaka (Ilha de Inhaca)"
    ],
    "Nampula": [
        "Angoche", "Eráti", "Ilha de Moçambique", "Lalaua", "Malema", "Meconta", "Mecubúri",
        "Memba", "Mogincual", "Mogovolas", "Moma", "Monapo", "Mossuril", "Muecate",
        "Murrupula", "Nacala", "Nacarôa", "Nampula", "Ribáuè"
    ],
    "Niassa": [
        "Cuamba", "Lago", "Lichinga", "Majune", "Mandimba", "Marrupa", "Maúa", "Mavago",
        "Mecanhelas", "Mecula", "Metarica", "Muembe", "N'gauma", "Sanga"
    ],
    "Sofala": [
        "Beira", "Buzi", "Caia", "Chemba", "Chibabava", "Dondo", "Gorongosa", "Machanga",
        "Marínguè", "Marromeu", "Muanza", "Nhamatanda"
    ],
    "Tete": [
        "Angónia", "Cahora-Bassa", "Changara", "Chifunde", "Chiuta", "Dôa", "Macanga",
        "Magoe", "Marara", "Moatize", "Mutarara", "Tete", "Tsangano", "Zumbo"
    ],
    "Zambézia": [
        "Alto Molócuè", "Chinde", "Gilé", "Gurué", "Ile", "Inhassunge", "Luabo", "Lugela",
        "Maganja da Costa", "Milange", "Mocuba", "Mopeia", "Morrumbala", "Quelimane"
    ]
}

provincia_pesos = {prov: 5 for prov in provincia_distritos}
provincia_pesos["Maputo Cidade"] = 10
provincia_pesos["Maputo Província"] = 8

meses_com_peso = {"2020-07": 12, "2021-01": 10, "2021-06": 14, "2021-07": 14}

# Geração de datas com peso nos surtos reais
def gerar_datas_pico(n):
    datas = pd.date_range(start=data_inicio, end=data_fim).to_list()
    pesos = [meses_com_peso.get(d.strftime("%Y-%m"), 1) for d in datas]
    return random.choices(datas, weights=pesos, k=n)

datas_diagnostico = gerar_datas_pico(num_linhas)

generos = ["Masculino", "Feminino"]
fumador_status = ["Sim"] * 7 + ["Não"] * 3
comorbidades = ["Nenhuma", "Hipertensão", "Diabetes", "Asma", "HIV", "Tuberculose", "Obesidade"]

# Função principal para gerar os dados
def gerar_dado(i):
    provincia = random.choices(list(provincia_distritos), weights=provincia_pesos.values())[0]
    distrito = random.choice(provincia_distritos[provincia])
    idade = random.randint(10, 90)
    genero = random.choice(generos)
    fumador = random.choice(fumador_status)
    comorbidade = random.choice(comorbidades)

    if idade > 60:
        gravidade = random.choices(["Moderado", "Grave", "Crítico"], weights=[2, 4, 3])[0]
    elif fumador == "Sim":
        gravidade = random.choices(["Leve", "Moderado", "Grave"], weights=[2, 3, 4])[0]
    else:
        gravidade = random.choices(["Leve", "Moderado", "Grave"], weights=[5, 3, 2])[0]

    internado = "Sim" if gravidade in ["Grave", "Crítico"] else random.choice(["Sim", "Não"])
    local_recup = "Hospital" if internado == "Sim" else "Casa"

    if idade > 65 and gravidade in ["Grave", "Crítico"] and comorbidade != "Nenhuma":
        resultado = random.choices(["Recuperado", "Óbito"], weights=[2, 5])[0]
    else:
        resultado = random.choices(["Recuperado", "Óbito"], weights=[19, 1])[0]

    data_diag = datas_diagnostico[i]

    if resultado == "Recuperado":
        if gravidade == "Leve":
            dias = random.randint(5, 10)
        elif gravidade == "Moderado":
            dias = random.randint(10, 20)
        else:
            dias = random.randint(15, 35)

        data_recup = data_diag + timedelta(days=dias)
        return {
            "ID Caso": i + 1,
            "Data de Diagnóstico": data_diag.date(),
            "Província": provincia,
            "Distrito": distrito,
            "Idade": idade,
            "Gênero": genero,
            "Fumador": fumador,
            "Comorbidades": comorbidade,
            "Gravidade do Caso": gravidade,
            "Internado": internado,
            "Local de Recuperação": local_recup,
            "Data de Recuperação": data_recup.date(),
            "Data do Óbito": None,
            "Resultado Final": resultado
        }

    else:  # Óbito
        dias = random.randint(2, 30)
        data_obito = data_diag + timedelta(days=dias)
        return {
            "ID Caso": i + 1,
            "Data de Diagnóstico": data_diag.date(),
            "Província": provincia,
            "Distrito": distrito,
            "Idade": idade,
            "Gênero": genero,
            "Fumador": fumador,
            "Comorbidades": comorbidade,
            "Gravidade do Caso": gravidade,
            "Internado": internado,
            "Local de Recuperação": None,
            "Data de Recuperação": None,
            "Data do Óbito": data_obito.date(),
            "Resultado Final": resultado
        }

# Gerar dataset
dados = [gerar_dado(i) for i in range(num_linhas)]
df = pd.DataFrame(dados)

df.to_csv("casos_covid_dummy.csv", index=False)
print("✅ Dataset gerado com sucesso!")
