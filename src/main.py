import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


current_dir = os.path.dirname(__file__)


csv_path = os.path.join(current_dir, 'data', 'Matches.csv')

print(f"Leyendo archivo desde: {csv_path}")


df = pd.read_csv(csv_path)

print(df.head())

df = df.iloc[:,:-16]

df = df.drop(columns=["MatchTime", "AwayElo","HomeElo","Form3Home","Form5Home","Form3Away","Form5Away"])

df.info()

grandes_ligas = ["SP1","F1", "E0","I1","D1","N1","P1"]

df_grandes_ligas = df[df["Division"].isin(grandes_ligas)]


df_resto_ligas = df[~df["Division"].isin(grandes_ligas)]

def lista_porcentaje_HAD(ligas):
    resultados = ligas["FTResult"].value_counts()
    porcentaje_liga =[]
    for i in resultados:
        porcentaje_liga.append(round(i/ligas["FTResult"].count(),3))
    return pd.Series(porcentaje_liga)

porcentaje_total_HAD = lista_porcentaje_HAD(df)

porcentaje_grandes_ligas_HAD = lista_porcentaje_HAD(df_grandes_ligas)

porcentaje_resto_ligas_HAD = lista_porcentaje_HAD(df_resto_ligas)

df_HAD = pd.concat([porcentaje_grandes_ligas_HAD,porcentaje_resto_ligas_HAD,porcentaje_total_HAD],axis=1)

df_HAD = df_HAD.rename(columns={0: "Media grandes ligas", 1: "Media resto ligas", 2: "Media total"})
df_HAD.index= ["Victoria Local","Empate","Victoria Visitante"]

categorias = ["Victoria Local","Empate","Victoria Visitante"]
grandes_ligas = porcentaje_grandes_ligas_HAD
resto_ligas = porcentaje_resto_ligas_HAD
total = porcentaje_total_HAD


fig, axes = plt.subplots(1, 3, figsize=(15, 5))


axes[0].pie(grandes_ligas, labels=categorias, autopct='%1.2f%%', startangle=90)
axes[0].set_title('Grandes Ligas')


axes[1].pie(resto_ligas, labels=categorias, autopct='%1.2f%%', startangle=90)
axes[1].set_title('Resto Ligas')


axes[2].pie(total, labels=categorias, autopct='%1.2f%%', startangle=90)
axes[2].set_title('Total')


plt.tight_layout()

img_dir = os.path.join(os.path.dirname(__file__), 'img')
os.makedirs(img_dir, exist_ok=True)

base_filename = "grafico_had"
counter = 1
output_path = os.path.join(img_dir, f"{base_filename}.png")

while os.path.exists(output_path):
    output_path = os.path.join(img_dir, f"{base_filename}_{counter}.png")
    counter += 1

plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f" Gráfico guardado en: {output_path}")

#Hipotesis 2

lista_amarilla_partido = df["AwayYellow"].dropna()

lista_amarilla_partido = df["HomeYellow"].dropna()

mascara_partidos_amarilla_gl = (df_grandes_ligas["HomeYellow"]>0)| (df_grandes_ligas["AwayYellow"]>0)

df_amarilla_partido_gl = df_grandes_ligas[mascara_partidos_amarilla_gl]

mascara_local_mas_amarillas_gl = df_amarilla_partido_gl["HomeYellow"] > df_amarilla_partido_gl["AwayYellow"]

resultados_amarilla_local_gl = df_amarilla_partido_gl[mascara_local_mas_amarillas_gl].value_counts(df_amarilla_partido_gl["FTResult"])

mascara_visitante_mas_amarillas_gl = df_amarilla_partido_gl["HomeYellow"] < df_amarilla_partido_gl["AwayYellow"]

resultados_amarilla_visitante_gl = df_amarilla_partido_gl[mascara_visitante_mas_amarillas_gl].value_counts(df_amarilla_partido_gl["FTResult"])

mascara_igual_amarillas_gl = df_amarilla_partido_gl["HomeYellow"] == df_amarilla_partido_gl["AwayYellow"]

resultados_amarilla_igual_gl = df_amarilla_partido_gl[mascara_igual_amarillas_gl].value_counts(df_amarilla_partido_gl["FTResult"])

df_amarillas_final_gl = pd.DataFrame([resultados_amarilla_local_gl,resultados_amarilla_visitante_gl,resultados_amarilla_igual_gl])

df_amarillas_final_gl = df_amarillas_final_gl.rename(columns={"H":"Victoria local", "D":"Empate","A" : "Victoria visitante",})

df_amarillas_final_gl.index= ["Más amarillas a local","Más amarillas a visitante", "Igual amarillas"]

df_amarillas_final_gl = df_amarillas_final_gl[["Victoria local","Empate","Victoria visitante"]]

mascara_partidos_amarilla_rl = (df_resto_ligas["HomeYellow"]>0)| (df_resto_ligas["AwayYellow"]>0)

df_amarilla_partido_rl = df_resto_ligas[mascara_partidos_amarilla_rl]

mascara_local_mas_amarillas_rl = df_amarilla_partido_rl["HomeYellow"] > df_amarilla_partido_rl["AwayYellow"]

resultados_amarilla_local_rl = df_amarilla_partido_rl[mascara_local_mas_amarillas_rl].value_counts(df_amarilla_partido_rl["FTResult"])

mascara_visitante_mas_amarillas_rl = df_amarilla_partido_rl["HomeYellow"] < df_amarilla_partido_rl["AwayYellow"]

resultados_amarilla_visitante_rl = df_amarilla_partido_rl[mascara_visitante_mas_amarillas_rl].value_counts(df_amarilla_partido_rl["FTResult"])

mascara_igual_amarillas_rl = df_amarilla_partido_rl["HomeYellow"] == df_amarilla_partido_rl["AwayYellow"]

resultados_amarilla_igual_rl = df_amarilla_partido_rl[mascara_igual_amarillas_rl].value_counts(df_amarilla_partido_rl["FTResult"])

df_amarillas_final_rl = pd.DataFrame([resultados_amarilla_local_rl,resultados_amarilla_visitante_rl,resultados_amarilla_igual_rl])

df_amarillas_final_rl = df_amarillas_final_rl.rename(columns={"H":"Victoria local","D":"Empate","A" : "Victoria visitante"})

df_amarillas_final_rl.index= ["Más amarillas a local","Más amarillas a visitante","Igual amarillas"]

df_amarillas_final_rl = df_amarillas_final_rl[["Victoria local","Empate","Victoria visitante"]]

labels_rl = df_amarillas_final_rl.columns
amarilla_local_rl = df_amarillas_final_rl.loc["Más amarillas a local"]
amarilla_visitante_rl = df_amarillas_final_rl.loc["Más amarillas a visitante"]
amarilla_igual_rl = df_amarillas_final_rl.loc["Igual amarillas"]

total_amarilla_local_rl = sum(amarilla_local_rl)
total_amarilla_visitante_rl = sum(amarilla_visitante_rl)
total_amarilla_igual_rl = sum(amarilla_igual_rl)

porcentaje_local_rl = [x / total_amarilla_local_rl * 100 for x in amarilla_local_rl]
porcentaje_visitante_rl = [x / total_amarilla_visitante_rl * 100 for x in amarilla_visitante_rl]
porcentaje_igual_rl = [x / total_amarilla_igual_rl * 100 for x in amarilla_igual_rl]

labels_gl = df_amarillas_final_gl.columns
amarilla_local_gl = df_amarillas_final_gl.loc["Más amarillas a local"]
amarilla_visitante_gl = df_amarillas_final_gl.loc["Más amarillas a visitante"]
amarilla_igual_gl = df_amarillas_final_gl.loc["Igual amarillas"]

total_amarilla_local_gl = sum(amarilla_local_gl)
total_amarilla_visitante_gl = sum(amarilla_visitante_gl)
total_amarilla_igual_gl = sum(amarilla_igual_gl)

porcentaje_local_gl = [x / total_amarilla_local_gl * 100 for x in amarilla_local_gl]
porcentaje_visitante_gl = [x / total_amarilla_visitante_gl * 100 for x in amarilla_visitante_gl]
porcentaje_igual_gl = [x / total_amarilla_igual_gl * 100 for x in amarilla_igual_gl]


fig, axes = plt.subplots(2, 3, figsize=(15, 10))


axes[0, 0].pie(porcentaje_local_rl, labels=labels_rl, autopct='%1.1f%%', startangle=90)
axes[0, 0].set_title('RL - Más amarillas a local')

axes[0, 1].pie(porcentaje_igual_rl, labels=labels_rl, autopct='%1.1f%%', startangle=90)
axes[0, 1].set_title("RL - Igual amarillas")

axes[0, 2].pie(porcentaje_visitante_rl, labels=labels_rl, autopct='%1.1f%%', startangle=90)
axes[0, 2].set_title('RL - Más amarillas a visitante')


axes[1, 0].pie(porcentaje_local_gl, labels=labels_gl, autopct='%1.1f%%', startangle=90)
axes[1, 0].set_title('GL - Más amarillas a local')

axes[1, 1].pie(porcentaje_igual_gl, labels=labels_gl, autopct='%1.1f%%', startangle=90)
axes[1, 1].set_title('GL - Igual amarillas')

axes[1, 2].pie(porcentaje_visitante_gl, labels=labels_gl, autopct='%1.1f%%', startangle=90)
axes[1, 2].set_title('GL - Más amarillas a visitante')

plt.suptitle('Distribución de resultados según amarillas (RL vs GL)', fontsize=16, y=1.02)
plt.tight_layout()


img_dir = os.path.join(os.path.dirname(__file__), 'img')
os.makedirs(img_dir, exist_ok=True)


base_filename = "grafico_amarillas"
counter = 1
output_path = os.path.join(img_dir, f"{base_filename}.png")

while os.path.exists(output_path):
    output_path = os.path.join(img_dir, f"{base_filename}_{counter}.png")
    counter += 1

plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f" Gráfico guardado en: {output_path}")

#Hipotesis 3

mascara_partidos_roja_gl = (df_grandes_ligas["HomeRed"]>0)| (df_grandes_ligas["AwayRed"]>0)

df_roja_partido_gl = df_grandes_ligas[mascara_partidos_roja_gl]

mascara_local_mas_rojas_gl = df_roja_partido_gl["HomeRed"] > df_roja_partido_gl["AwayRed"]

resultados_roja_local_gl = df_roja_partido_gl[mascara_local_mas_rojas_gl].value_counts(df_roja_partido_gl["FTResult"])

mascara_visitante_mas_rojas_gl = df_roja_partido_gl["HomeRed"] < df_roja_partido_gl["AwayRed"]

resultados_roja_visitante_gl = df_roja_partido_gl[mascara_visitante_mas_rojas_gl].value_counts(df_roja_partido_gl["FTResult"])

df_rojas_final_gl = pd.DataFrame([resultados_roja_local_gl,resultados_roja_visitante_gl])

df_rojas_final_gl = df_rojas_final_gl.rename(columns={"H":"Victoria local","D":"Empate","A" : "Victoria visitante" })

df_rojas_final_gl.index= ["Más rojas a local","Más rojas a visitante"]

df_rojas_final_gl = df_rojas_final_gl[["Victoria local","Empate","Victoria visitante"]]

mascara_partidos_roja_rl = (df_resto_ligas["HomeRed"]>0)| (df_resto_ligas["AwayRed"]>0)

df_roja_partido_rl = df_resto_ligas[mascara_partidos_roja_rl]

mascara_local_mas_rojas_rl = df_roja_partido_rl["HomeRed"] > df_roja_partido_rl["AwayRed"]

resultados_roja_local_rl = df_roja_partido_rl[mascara_local_mas_rojas_rl].value_counts(df_roja_partido_rl["FTResult"])

mascara_visitante_mas_rojas_rl = df_roja_partido_rl["HomeRed"] < df_roja_partido_rl["AwayRed"]

resultados_roja_visitante_rl = df_roja_partido_rl[mascara_visitante_mas_rojas_rl].value_counts(df_roja_partido_rl["FTResult"])

df_rojas_final_rl = pd.DataFrame([resultados_roja_local_rl,resultados_roja_visitante_rl])

df_rojas_final_rl = df_rojas_final_rl.rename(columns={"H":"Victoria local","D":"Empate","A" : "Victoria visitante"})

df_rojas_final_rl.index= ["Más rojas a local","Más rojas a visitante"]

df_rojas_final_rl = df_rojas_final_rl[["Victoria local","Empate","Victoria visitante"]]

labels_rl = df_rojas_final_rl.columns
roja_local_rl = df_rojas_final_rl.loc["Más rojas a local"]
roja_visitante_rl = df_rojas_final_rl.loc["Más rojas a visitante"]

total_roja_local_rl = sum(roja_local_rl)
total_roja_visitante_rl = sum(roja_visitante_rl)

porcentaje_local_rl = [x / total_roja_local_rl * 100 for x in roja_local_rl]
porcentaje_visitante_rl = [x / total_roja_visitante_rl * 100 for x in roja_visitante_rl]

labels_gl = df_rojas_final_gl.columns
roja_local_gl = df_rojas_final_gl.loc["Más rojas a local"]
roja_visitante_gl = df_rojas_final_gl.loc["Más rojas a visitante"]

total_roja_local_gl = sum(roja_local_gl)
total_roja_visitante_gl = sum(roja_visitante_gl)

porcentaje_local_gl = [x / total_roja_local_gl * 100 for x in roja_local_gl]
porcentaje_visitante_gl = [x / total_roja_visitante_gl * 100 for x in roja_visitante_gl]

fig, axes = plt.subplots(2, 2, figsize=(10, 7))

axes[0, 0].pie(porcentaje_local_rl, labels=labels_rl, autopct='%1.1f%%', startangle=90)
axes[0, 0].set_title('RL - Más rojas a local')

axes[0, 1].pie(porcentaje_visitante_rl, labels=labels_rl, autopct='%1.1f%%', startangle=90)
axes[0, 1].set_title('RL - Más rojas a visitante')

axes[1, 0].pie(porcentaje_local_gl, labels=labels_gl, autopct='%1.1f%%', startangle=90)
axes[1, 0].set_title('GL - Más rojas a local')

axes[1, 1].pie(porcentaje_visitante_gl, labels=labels_gl, autopct='%1.1f%%', startangle=90)
axes[1, 1].set_title('GL - Más rojas a visitante')

plt.suptitle('Distribución de resultados según rojas (RL vs GL)', fontsize=10, y=1.02)
plt.tight_layout()


img_dir = os.path.join(os.path.dirname(__file__), 'img')
os.makedirs(img_dir, exist_ok=True)


base_filename = "grafico_rojas"
counter = 1
output_path = os.path.join(img_dir, f"{base_filename}.png")

while os.path.exists(output_path):
    output_path = os.path.join(img_dir, f"{base_filename}_{counter}.png")
    counter += 1

plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f" Gráfico guardado en: {output_path}")

#Hipotesis 4

mascara_barsa = (df["HomeTeam"] == "Barcelona") | (df["AwayTeam"] == "Barcelona")

df_barsa_amarillas = df[mascara_barsa]

df_barsa_amarillas.dropna(inplace=True)

Am_Recib_H_Bar = df_barsa_amarillas.loc[df_barsa_amarillas["HomeTeam"] == "Barcelona","HomeYellow"].sum()

Falt_H_Bar = df_barsa_amarillas.loc[df_barsa_amarillas["HomeTeam"] == "Barcelona","HomeFouls"].sum()

Falt_Ama_H_Bar = Falt_H_Bar/Am_Recib_H_Bar

Am_Rival_H_Bar = df_barsa_amarillas.loc[df_barsa_amarillas["HomeTeam"] == "Barcelona","AwayYellow"].sum()

Falt_Rival_H_Bar = df_barsa_amarillas.loc[df_barsa_amarillas["HomeTeam"] == "Barcelona","AwayFouls"].sum()

Falt_Ama_H_Riv_Bar = Falt_Rival_H_Bar/Am_Rival_H_Bar

Am_Recib_A_Bar = df_barsa_amarillas.loc[df_barsa_amarillas["AwayTeam"] == "Barcelona","AwayYellow"].sum()

Falt_A_Bar = df_barsa_amarillas.loc[df_barsa_amarillas["AwayTeam"] == "Barcelona","AwayFouls"].sum()

Falt_Ama_A_Bar = Falt_A_Bar/Am_Recib_A_Bar

Am_Rival_A_Bar = df_barsa_amarillas.loc[df_barsa_amarillas["AwayTeam"] == "Barcelona","HomeYellow"].sum()

Falt_Rival_A_Bar = df_barsa_amarillas.loc[df_barsa_amarillas["AwayTeam"] == "Barcelona","HomeFouls"].sum()

Falt_Ama_A_Riv_Bar = Falt_Rival_A_Bar/Am_Rival_A_Bar

Ro_Recib_H_Bar = df_barsa_amarillas.loc[df_barsa_amarillas["HomeTeam"] == "Barcelona","HomeRed"].sum()

Falt_Ro_H_Bar = Falt_H_Bar/Ro_Recib_H_Bar 

Ro_Rival_H_Bar = df_barsa_amarillas.loc[df_barsa_amarillas["HomeTeam"] == "Barcelona","AwayRed"].sum()

Falt_Ro_H_Riv_Bar = Falt_Rival_H_Bar/Ro_Rival_H_Bar 

Ro_Recib_A_Bar = df_barsa_amarillas.loc[df_barsa_amarillas["AwayTeam"] == "Barcelona","AwayRed"].sum()

Falt_Ro_A_Bar = Falt_A_Bar/Ro_Recib_A_Bar 

Ro_Rival_A_Bar = df_barsa_amarillas.loc[df_barsa_amarillas["AwayTeam"] == "Barcelona","HomeRed"].sum()

Falt_Ro_A_Riv_Bar = Falt_Rival_A_Bar/Ro_Rival_A_Bar 

mascara_RM = (df["HomeTeam"] == "Real Madrid") | (df["AwayTeam"] == "Real Madrid")

df_RM_amarillas = df[mascara_RM]

df_RM_amarillas.dropna(inplace=True)

Am_Recib_H_RM = df_RM_amarillas.loc[df_RM_amarillas["HomeTeam"] == "Real Madrid","HomeYellow"].sum()

Falt_H_RM = df_RM_amarillas.loc[df_RM_amarillas["HomeTeam"] == "Real Madrid","HomeFouls"].sum()

Falt_Ama_H_RM = Falt_H_RM/Am_Recib_H_RM

Am_Rival_H_RM = df_RM_amarillas.loc[df_RM_amarillas["HomeTeam"] == "Real Madrid","AwayYellow"].sum()

Falt_Rival_H_RM = df_RM_amarillas.loc[df_RM_amarillas["HomeTeam"] == "Real Madrid","AwayFouls"].sum()

Falt_Ama_H_Riv_RM = Falt_Rival_H_RM/Am_Rival_H_RM

Am_Recib_A_RM = df_RM_amarillas.loc[df_RM_amarillas["AwayTeam"] == "Real Madrid","AwayYellow"].sum()

Falt_A_RM = df_RM_amarillas.loc[df_RM_amarillas["AwayTeam"] == "Real Madrid","AwayFouls"].sum()

Falt_Ama_A_RM = Falt_A_RM/Am_Recib_A_RM

Am_Rival_A_RM = df_RM_amarillas.loc[df_RM_amarillas["AwayTeam"] == "Real Madrid","HomeYellow"].sum()

Falt_Rival_A_RM = df_RM_amarillas.loc[df_RM_amarillas["AwayTeam"] == "Real Madrid","HomeFouls"].sum()

Falt_Ama_A_Riv_RM = Falt_Rival_A_RM/Am_Rival_A_RM

Ro_Recib_H_RM = df_RM_amarillas.loc[df_RM_amarillas["HomeTeam"] == "Real Madrid","HomeRed"].sum()

Falt_Ro_H_RM = Falt_H_RM/Ro_Recib_H_RM 

Ro_Rival_H_RM = df_RM_amarillas.loc[df_RM_amarillas["HomeTeam"] == "Real Madrid","AwayRed"].sum()

Falt_Ro_H_Riv_RM = Falt_Rival_H_RM/Ro_Rival_H_RM 

Ro_Recib_A_RM = df_RM_amarillas.loc[df_RM_amarillas["AwayTeam"] == "Real Madrid","AwayRed"].sum()

Falt_Ro_A_RM = Falt_H_RM/Ro_Recib_A_RM 

Ro_Rival_A_RM = df_RM_amarillas.loc[df_RM_amarillas["AwayTeam"] == "Real Madrid","HomeRed"].sum()

Falt_Ro_A_Riv_RM = Falt_Rival_A_RM/Ro_Rival_A_RM 

mask_resto_liga_sanciones = (df["Division"] == "SP1") & (df["HomeTeam"] != "Real Madrid") & (df["HomeTeam"] != "Barcelona") & (df["AwayTeam"] != "Real Madrid") & (df["AwayTeam"] != "Barcelona") 

df_resto_liga = df[mask_resto_liga_sanciones]

df_resto_liga = df_resto_liga.dropna()

media_fal_am_local = df_resto_liga["HomeFouls"].mean()/df_resto_liga["HomeYellow"].mean()

media_fal_am_visit = df_resto_liga["AwayFouls"].mean()/df_resto_liga["AwayYellow"].mean()

media_fal_ro_local = df_resto_liga["HomeFouls"].mean()/df_resto_liga["HomeRed"].mean()

media_fal_ro_visit = df_resto_liga["AwayFouls"].mean()/df_resto_liga["AwayRed"].mean()

Real_Madrid_amarillas = pd.Series([Falt_Ama_H_RM,Falt_Ama_H_Riv_RM,Falt_Ama_A_Riv_RM, Falt_Ama_A_RM], name = "Real Madrid")

Barsa_amarillas = pd.Series([Falt_Ama_H_Bar,Falt_Ama_H_Riv_Bar, Falt_Ama_A_Riv_Bar,Falt_Ama_A_Bar], name = "Barsa")

Resto_liga_amarillas =pd.Series([media_fal_am_local,media_fal_am_visit, media_fal_am_local, media_fal_am_visit], name ="Media liga")

df_amarillas = pd.concat([Real_Madrid_amarillas, Barsa_amarillas, Resto_liga_amarillas],axis =1)

df_amarillas = df_amarillas.rename(index={0:"Faltas realizadas/TA(como local)",1:"Faltas recibidas/TA Riv(como Local)",2:"Faltas recibidas/TA Riv (como Visitante)",3:"Faltas realizadas/TA (como Visitante)"})

df_amarillas.transpose().round(2)

estadisticas_amarillas = df_amarillas.index.tolist()

real_madrid = Real_Madrid_amarillas
barca = Barsa_amarillas
media_liga = Resto_liga_amarillas

x = np.arange(len(estadisticas_amarillas))
ancho = 0.25

plt.figure(figsize=(10, 6))

bars_rm = plt.bar(x - ancho, real_madrid, width=ancho, label="Real Madrid", color="#800080")
bars_barca = plt.bar(x, barca, width=ancho, label="Barça", color="red")
bars_media = plt.bar(x + ancho, media_liga, width=ancho, label="Media Liga", color="#7F7F7F")


def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width()/2,
            height/2,
            f"{height:.2f}",
            ha='center', va='center', color='white', fontsize=10, fontweight='bold'
        )

add_labels(bars_rm)
add_labels(bars_barca)
add_labels(bars_media)

plt.xticks(x, estadisticas_amarillas, rotation=20, fontsize=10)
plt.ylabel("Promedio de faltas/TA", fontsize=12)
plt.title("Comparativa de Faltas y TA", fontsize=14, fontweight='bold')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()


img_dir = os.path.join(os.path.dirname(__file__), 'img')
os.makedirs(img_dir, exist_ok=True)


base_filename = "grafico_amarillas_comparativa"
counter = 1
output_path = os.path.join(img_dir, f"{base_filename}.png")

while os.path.exists(output_path):
    output_path = os.path.join(img_dir, f"{base_filename}_{counter}.png")
    counter += 1


plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f" Gráfico guardado en: {output_path}")


Real_Madrid_rojas = pd.Series ([Falt_Ro_H_RM, Falt_Ro_H_Riv_RM,  Falt_Ro_A_Riv_RM, Falt_Ro_A_RM], name = "Real Madrid")
Barsa_rojas = pd.Series ([Falt_Ro_H_Bar, Falt_Ro_H_Riv_Bar, Falt_Ro_A_Riv_Bar, Falt_Ro_A_Bar], name = "Barsa")
Resto_liga_rojas = pd.Series ([media_fal_ro_local, media_fal_ro_visit, media_fal_ro_local, media_fal_ro_visit], name = "Media liga")
df_rojas = pd.concat([Real_Madrid_rojas, Barsa_rojas, Resto_liga_rojas],axis =1)

df_rojas = df_rojas.rename(index={0:"Faltas realizadas/TR(como local)",1:"Faltas recibidas/TR Riv(como Local)",2:"Faltas recibidas/TR Riv (como Visitante)",3:"Faltas realizadas/TR (como Visitante)"}) 

df_rojas.transpose().round(2)

estadisticas_rojas = df_rojas.index.tolist()

real_madrid = Real_Madrid_rojas
barca = Barsa_rojas
media_liga = Resto_liga_rojas

x = np.arange(len(estadisticas_rojas))
ancho = 0.25

plt.figure(figsize=(10, 6))

bars_rm = plt.bar(x - ancho, real_madrid, width=ancho, label="Real Madrid", color="#800080")
bars_barca = plt.bar(x, barca, width=ancho, label="Barça", color="red")
bars_media = plt.bar(x + ancho, media_liga, width=ancho, label="Media Liga", color="#7F7F7F")

# --- Función para añadir etiquetas en las barras ---
def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width()/2,
            height/2,
            f"{height:.2f}",
            ha='center', va='center', color='white', fontsize=10, fontweight='bold'
        )

add_labels(bars_rm)
add_labels(bars_barca)
add_labels(bars_media)

plt.xticks(x, estadisticas_rojas, rotation=20, fontsize=10)
plt.ylabel("Promedio de faltas/TR", fontsize=12)
plt.title("Comparativa de Faltas y TR", fontsize=14, fontweight='bold')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()


img_dir = os.path.join(os.path.dirname(__file__), 'img')
os.makedirs(img_dir, exist_ok=True)


base_filename = "grafico_rojas_comparativa"
counter = 1
output_path = os.path.join(img_dir, f"{base_filename}.png")

while os.path.exists(output_path):
    output_path = os.path.join(img_dir, f"{base_filename}_{counter}.png")
    counter += 1


plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f" Gráfico guardado en: {output_path}")


RM_diferenciaTR_medialiga = ((Real_Madrid_rojas - Resto_liga_rojas)/Resto_liga_rojas)*100

B_diferenciaTR_medialiga = ((Barsa_rojas - Resto_liga_rojas)/Resto_liga_rojas)*100

df_diferencia = pd.concat([RM_diferenciaTR_medialiga,B_diferenciaTR_medialiga], axis= 1)

df_diferencia = df_diferencia.rename(index={0:"Faltas realizadas/TR(como local)",1:"Faltas recibidas/TR Riv(como Local)",2:"Faltas recibidas/TR Riv (como Visitante)",3:"Faltas realizadas/TR (como Visitante)"}) 

df_diferencia = df_diferencia.transpose().rename(index={0:"Real Madrid",1: "Barsa"})

df_diferencia.round(2)

data_diff = {
    'Métrica': [
        'Faltas realizadas/TR (Local)',
        'Faltas recibidas/TR Riv (Local)',
        'Faltas recibidas/TR Riv (Visitante)',
        'Faltas realizadas/TR (Visitante)'
    ],
    'Real Madrid': RM_diferenciaTR_medialiga,
    'Barcelona': B_diferenciaTR_medialiga
}

df = pd.DataFrame(data_diff)

fig, ax = plt.subplots(figsize=(10, 6))
bar_width = 0.35
x = range(len(df))

bars_rm = ax.barh([i + bar_width/2 for i in x], df['Real Madrid'], bar_width, label='Real Madrid', color='#1f77b4')
bars_barsa = ax.barh([i - bar_width/2 for i in x], df['Barcelona'], bar_width, label='Barcelona', color='#d62728')

ax.axvline(0, color='black', linewidth=1)

ax.set_yticks(x)
ax.set_yticklabels(df['Métrica'])
ax.set_xlabel('Diferencia respecto a la media de la liga (%)')
ax.set_title('Diferencia de faltas respecto a la media de la liga (por tipo y equipo)')
ax.legend()
ax.invert_yaxis()

def label_inside(bars):
    for bar in bars:
        value = bar.get_width()
        ax.text(
            value / 2,
            bar.get_y() + bar.get_height() / 2,
            f'{value:.1f}%',
            ha='center', va='center', color='white', fontsize=9, fontweight='bold'
        )

label_inside(bars_rm)
label_inside(bars_barsa)

plt.tight_layout()

img_dir = os.path.join(os.path.dirname(__file__), 'img')
os.makedirs(img_dir, exist_ok=True)

base_filename = "grafico_diferencia_faltas_rojas_RM_B"
counter = 1
output_path = os.path.join(img_dir, f"{base_filename}.png")

while os.path.exists(output_path):
    output_path = os.path.join(img_dir, f"{base_filename}_{counter}.png")
    counter += 1

plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f" Gráfico guardado en: {output_path}")






























