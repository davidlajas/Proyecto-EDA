# Exploratory Data Analysis de Fútbol (Club Football Match Data 2000‑2025)

## Descripción
Este proyecto realiza un **análisis exploratorio de datos (EDA)** sobre partidos de fútbol de clubes entre 2000 y 2025, usando el dataset de Kaggle **[Club Football Match Data (2000‑2025)](https://www.kaggle.com/datasets/adamgbor/club-football-match-data-2000-2025/data)**.  

El objetivo es identificar patrones de rendimiento de equipos, ventaja de localía, impacto de tarjetas y expulsiones, y posibles sesgos arbitrales.

---

## Objetivos del EDA
- Analizar el desempeño de equipos locales y visitantes.  
- Evaluar la ventaja de jugar como local.  
- Explorar cómo las tarjetas amarillas y rojas afectan los resultados de los partidos.  
- Investigar posibles sesgos arbitrales hacia ciertos equipos (ej. FC Barcelona vs Real Madrid).  

---

## Hipótesis
1. **Ventaja de localía:** Se ganan más partidos como local que como visitante.  
2. **Impacto de tarjetas amarillas:** El equipo que recibe más tarjetas amarillas pierde más partidos.  
3. **Impacto de expulsiones:** El equipo que tiene más jugadores expulsados pierde el partido.  
4. **Sesgo arbitral:** El FC Barcelona recibe decisiones favorables de los árbitros más que el Real Madrid.

*Cómo probar cada hipótesis:*  
- Comparar porcentajes de victorias locales vs visitantes.  
- Analizar correlación entre tarjetas amarillas/rojas (`HomeYellowCards`, `AwayRedCards`) y resultado.  
- Revisar amonestaciones para FC Barcelona vs Real Madrid.

---

## Datos

El dataset contiene información de **38 ligas de fútbol del mundo**, desde 2000 hasta 2025, con resultados, estadísticas de partidos y cuotas de apuestas.  

### Columnas principales:

| Columna | Descripción |
|---------|-------------|
| **Date** | Fecha del partido |
| **League** | Nombre de la liga o competición |
| **HomeTeam** | Equipo local |
| **AwayTeam** | Equipo visitante |
| **FTHG** | Goles del equipo local al final del tiempo reglamentario |
| **FTAG** | Goles del equipo visitante al final del tiempo reglamentario |
| **FTR** | Resultado final: H = victoria local, D = empate, A = victoria visitante |
| **HTHG** | Goles del equipo local al medio tiempo |
| **HTAG** | Goles del equipo visitante al medio tiempo |
| **HTR** | Resultado al medio tiempo |
| **Referee** | Árbitro del partido |
| **Attendance** | Número de espectadores |
| **Odds_1, Odds_X, Odds_2** | Cuotas de apuestas: 1 = local, X = empate, 2 = visitante |
| **HomeShots, AwayShots** | Tiros realizados por local y visitante |
| **HomeCorners, AwayCorners** | Saques de esquina de local y visitante |
| **HomeYellowCards, AwayYellowCards** | Tarjetas amarillas de local y visitante |
| **HomeRedCards, AwayRedCards** | Tarjetas rojas de local y visitante |


---


## Requisitos
- Python 3.x  
- Librerías: `pandas`, `numpy`, `matplotlib`, `seaborn`  
- Jupyter Notebook para los notebooks de hipótesis (`Hipotesis1.ipynb`, etc.)

---

## Cómo ejecutar
1. Clonar el repositorio:  
git clone https://github.com/davidlajas/Proyecto-EDA.git
cd Proyecto-EDA

2. Asegúrate de que tienes instalado Python 3.x y las librerías necesarias:
pandas
matplotlib
seaborn
numpy 

3. Verifica que el dataset Matches.csv esté en la carpeta src/data/.

4. Ejecutar el script principal:

python src/main.py


Abrir y ejecutar los notebooks de hipótesis en src/Notebooks/ para análisis específicos.

# Resultados esperados / Hallazgos
(Se completan después de ejecutar main.py y los notebooks)

Distribución de goles locales vs visitantes (grafico_had.png).

Comparativa de tarjetas amarillas (grafico_amarillas.png y grafico_amarillas_comparativa.png).

Comparativa de tarjetas rojas (grafico_rojas.png y grafico_rojas_comparativa.png).

Porcentaje de victorias locales, visitantes y empates.

Impacto de tarjetas y expulsiones en los resultados.

Posible sesgo arbitral hacia FC Barcelona vs Real Madrid.




