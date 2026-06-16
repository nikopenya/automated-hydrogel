# Laboratorio Automatizado de Síntesis y Caracterización de Materia Blanda
**Una plataforma "Self-Driving Lab" guiada por datos para el descubrimiento de hidrogeles**

Este repositorio contiene el ecosistema completo de scripts de Python y protocolos de automatización desarrollados para una plataforma de descubrimiento de materiales de alto rendimiento y lazo cerrado (*closed-loop*). El flujo de trabajo integra con éxito el Diseño de Experimentos (DoE), el manejo automatizado de líquidos, la caracterización mecánica de alto rendimiento y el Aprendizaje Automático Explicable (XAI) para acelerar el diseño de hidrogeles biocompatibles y redes semi-interpenetradas.

---

### Arquitectura del Repositorio

El código está modularizado en cuatro fases operativas principales, guiando al usuario desde el diseño experimental teórico hasta el modelado físico predictivo:

### Fase 1: Diseño Experimental (DoE)
Algoritmos diseñados para mapear espacios composicionales multicomponente utilizando el **Muestreo por Hipercubo Latino (LHS)**. Estos scripts maximizan la diversidad de las formulaciones al tiempo que integran estrictos umbrales de seguridad reológica para evitar atascos de pipeteo en el robot.
* `LHSlap.py`: Genera el espacio de muestreo 2D para el sistema base de hidrogeles PEGDA/LAP.
* `LHSpva.ipynb`: Cuaderno interactivo que genera el espacio de muestreo 3D para redes semi-IPN de PVA/PEGDA/LAP reforzadas viscoelásticamente, incluyendo visualizaciones 3D con Plotly.
* `LHSriboflavin.py`: Mapea la matriz de muestreo 3D para los sistemas fotopolimerizables biocompatibles de Tipo II PEGDA/TEOA/Riboflavina.

### Fase 2: Síntesis Robótica Automatizada
Scripts de la **API v2.21 de Opentrons Flex** programados para comandar el robot manipulador de líquidos y realizar una dosificación, mezcla y formulación precisas en microplacas estándar SBS de 96 pocillos.
* `LAPoptimo_1.py`, `LAPoptimo_2.py`, `LAPoptimo_3.py`: Protocolos de síntesis por lotes (PEGDA/LAP) que dividen 32 formulaciones únicas (con 3 réplicas cada una) a lo largo de 3 microplacas.
* `PVAoptimo_1.py`, `PVAoptimo_2.py`: Protocolos de manejo de líquidos de alta viscosidad diseñados a medida y optimizados para matrices que contienen PVA.
* `RFoptimo_1.py`, `RFoptimo_2.py`, `RFoptimo_3.py`: Protocolos de formulación para el sistema PEGDA/RF/TEOA, altamente dependiente de la cinética.

### Fase 3: Caracterización de Alto Rendimiento y Control de Hardware
Un conjunto de scripts para gestionar el diagnóstico de hardware, el posicionamiento y la adquisición de datos para el Indentador Automatizado de Materia Blanda (ASMI).
* `button.py`: Script de utilidad y diagnóstico diseñado para verificar el protocolo de enlace (*handshake*) hardware-software antes de la ejecución. Asegura la correcta comunicación serial y el flujo de datos entre el sensor de fuerza Vernier, el entorno de control del ASMI y el ordenador anfitrión.
* `home.py`: Script de posicionamiento que retrae y devuelve de forma segura los ejes CNC a su posición de cero absoluto (*Home* de la máquina), garantizando una carga y descarga segura de las microplacas.
* `measure.py`: El script central de adquisición de datos y control. Se comunica de forma asíncrona con el sensor de fuerza Vernier Go Direct® y controla la estructura CNC Genmitsu 3018-PRO mediante GRBL (G-Code). Realiza una detección determinista de la superficie y ajusta automáticamente las curvas brutas de indentación a la **mecánica de contacto de Hertz** (rango efectivo: 0.3–0.7 mm), generando gráficos de control de calidad (QC) en tiempo real.

### Fase 4: Análisis Exploratorio de Datos y Machine Learning
Cuadernos de Jupyter para la curación de datos, validación metrológica y modelado predictivo utilizando ensamblados basados en árboles (Random Forest, ExtraTrees, XGBoost) y Regresión por Procesos Gaussianos (GPR).

* `Analisis*.ipynb` (`LAP`, `PVA`, `RF`): **Curación de Datos y EDA**. Aplica un estricto umbral que descarta errores relativos de ajuste ≤25 % para limpiar los datos brutos. Valida la estabilidad inter/intra-sesión del hardware y mapea el espacio composición-propiedad utilizando superficies interactivas 2D/3D de Plotly.
* `ML_LAP_code_limpio_basico.ipynb`, `ML_RF_code_limpio_basico.ipynb`, `ML_PVA_code_limpio_basico.ipynb`: **Modelos Predictivos Base**. Entrena los algoritmos utilizando variables operativas directas (concentraciones absolutas de precursores y tiempo sumergido en agua) como espacio de características principal y extrae los valores **SHAP (*SHapley Additive exPlanations*)** para traducir las predicciones del modelo en leyes físicas interpretables.
* `ML_LAP_code_limpio.ipynb`, `ML_RF_code_limpio.ipynb`, `ML_PVA_code_limpio.ipynb`: **Modelos Avanzados de XAI**. Implementa Ingeniería de Características (*Feature Engineering*, p. ej., ratios estequiométricos) y extrae los valores **SHAP** para desglosar la "caja negra" del algoritmo en principios físicos termodinámicos.

---

## Flujo de Trabajo (Guía Rápida)

1. **Diseñar:** Ejecuta el script `LHS*.py` correspondiente para generar un espacio de diseño químico equilibrado y sin solapamientos.
2. **Sintetizar:** Carga las coordenadas y volúmenes resultantes en los protocolos de Opentrons `*optimo*.py` para iniciar la formulación autónoma en las microplacas.
3. **Caracterizar:** Tras el curado UV, transfiere las placas a la plataforma ASMI. Ejecuta `measure.py` para iniciar la secuencia de mapeo mecánico desatendido.
4. **Modelar:** Ejecuta los cuadernos `Analisis*.ipynb` para limpiar metrológicamente los datos de Hertz brutos, seguido de los pipelines `ML*.ipynb` para entrenar las arquitecturas predictivas y extraer la importancia de las variables.

---

## Requisitos e Instalación

Para ejecutar localmente los scripts de diseño, control de hardware y machine learning, asegúrate de tener instalado el siguiente conjunto de librerías científicas:

```bash
pip install numpy pandas scipy matplotlib openpyxl plotly pyserial scikit-learn xgboost shap
