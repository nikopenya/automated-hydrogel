# **Laboratorio Automatizado de Síntesis y Caracterización de Materia Blanda**
**Una plataforma "Self-Driving Lab" guiada por datos para el descubrimiento de hidrogeles**

Este repositorio contiene el ecosistema completo de scripts de Python y protocolos de automatización desarrollados para una plataforma de descubrimiento de materiales de alto rendimiento y lazo cerrado (*closed-loop*). El flujo de trabajo integra con éxito el Diseño de Experimentos (DoE), el manejo automatizado de líquidos, la caracterización mecánica de alto rendimiento y el Aprendizaje Automático Explicable (XAI) para acelerar el diseño de hidrogeles biocompatibles y redes semi-interpenetradas.

---

### **Arquitectura del Repositorio**

El código está modularizado en cuatro fases operativas principales, guiando al usuario desde el diseño experimental teórico hasta el modelado físico predictivo:

### **Fase 1: Diseño Experimental (DoE)**
Algoritmos diseñados para mapear espacios composicionales multicomponente utilizando el **Muestreo por Hipercubo Latino (LHS)**. Estos scripts maximizan la diversidad de las formulaciones al tiempo que integran estrictos umbrales de seguridad reológica para evitar atascos de pipeteo en el robot.
* `LHSlap.py`: Genera el espacio de muestreo 2D para el sistema base de hidrogeles PEGDA/LAP.
* `LHSpva.ipynb`: Cuaderno interactivo que genera el espacio de muestreo 3D para redes semi-IPN de PVA/PEGDA/LAP reforzadas viscoelásticamente, incluyendo visualizaciones 3D con Plotly.
* `LHSriboflavin.py`: Mapea la matriz de muestreo 3D para los sistemas fotopolimerizables biocompatibles de Tipo II PEGDA/TEOA/Riboflavina.

### **Fase 2: Síntesis Robótica Automatizada**
Scripts de la **API v2.21 de Opentrons Flex** programados para comandar el robot manipulador de líquidos y realizar una dosificación, mezcla y formulación precisas en microplacas estándar SBS de 96 pocillos.
* `LAPoptimo_1.py`, `LAPoptimo_2.py`, `LAPoptimo_3.py`: Protocolos de síntesis por lotes (PEGDA/LAP) que dividen 32 formulaciones únicas (con 3 réplicas cada una) a lo largo de 3 microplacas.
* `PVAoptimo_1.py`, `PVAoptimo_2.py`, `PVAoptimo_3.py`: Protocolos de manejo de líquidos de alta viscosidad diseñados a medida y optimizados para matrices que contienen PVA.
* `RFoptimo_1.py`, `RFoptimo_2.py`, `RFoptimo_3.py`: Protocolos de formulación para el sistema PEGDA/RF/TEOA, altamente dependiente de la cinética.

### **Fase 3: Caracterización de Alto Rendimiento y Control de Hardware**
Un conjunto de scripts para gestionar el diagnóstico de hardware, el posicionamiento y la adquisición de datos para el Indentador Automatizado de Materia Blanda (ASMI).
* `button.py`: Script de utilidad y diagnóstico diseñado para verificar el protocolo de enlace (*handshake*) hardware-software antes de la ejecución. Asegura la correcta comunicación serial y el flujo de datos entre el sensor de fuerza Vernier, el entorno de control del ASMI y el ordenador anfitrión.
* `home.py`: Script de posicionamiento que retrae y devuelve de forma segura los ejes CNC a su posición de cero absoluto (*Home* de la máquina), garantizando una carga y descarga segura de las microplacas.
* `measure.py`: El script central de adquisición de datos y control. Se comunica de forma asíncrona con el sensor de fuerza Vernier Go Direct® y controla la estructura CNC Genmitsu 3018-PRO mediante GRBL (G-Code). Realiza una detección determinista de la superficie y ajusta automáticamente las curvas brutas de indentación a la **mecánica de contacto de Hertz** (rango efectivo: 0.3–0.7 mm), generando gráficos de control de calidad (QC) en tiempo real.

### **Fase 4: Análisis Exploratorio de Datos y Machine Learning**
Cuadernos de Jupyter para la curación de datos, validación metrológica y modelado predictivo utilizando ensamblados basados en árboles (Random Forest, ExtraTrees, XGBoost) y Regresión por Procesos Gaussianos (GPR).

* `Analisis*.ipynb` (`LAP`, `PVA`, `RF`): **Curación de Datos y EDA**. Aplica un estricto umbral que descarta errores relativos de ajuste ≤25 % para limpiar los datos brutos. Valida la estabilidad inter/intra-sesión del hardware y mapea el espacio composición-propiedad utilizando superficies interactivas 2D/3D de Plotly.
* `ML_LAP_code_limpio_basico.ipynb`, `ML_RF_code_limpio_basico.ipynb`, `ML_PVA_code_limpio_basico.ipynb`: **Modelos Predictivos Base**. Entrena los algoritmos utilizando variables operativas directas (concentraciones absolutas de precursores y tiempo sumergido en agua) como espacio de características principal y extrae los valores **SHAP (*SHapley Additive exPlanations*)** para traducir las predicciones del modelo en leyes físicas interpretables.
* `ML_LAP_code_limpio.ipynb`, `ML_RF_code_limpio.ipynb`, `ML_PVA_code_limpio.ipynb`: **Modelos Avanzados de XAI**. Implementa Ingeniería de Características (*Feature Engineering*, p. ej., ratios estequiométricos) y extrae los valores **SHAP** para desglosar la "caja negra" del algoritmo en principios físicos termodinámicos.

---

## **Flujo de Trabajo (Guía Rápida)**

1. **Diseñar:** Ejecuta el script `LHS*.py` correspondiente para generar un espacio de diseño químico equilibrado y sin solapamientos.
2. **Sintetizar:** Carga las coordenadas y volúmenes resultantes en los protocolos de Opentrons `*optimo*.py` para iniciar la formulación autónoma en las microplacas.
3. **Caracterizar:** Tras el curado UV, transfiere las placas a la plataforma ASMI. Ejecuta `measure.py` para iniciar la secuencia de mapeo mecánico desatendido.
4. **Modelar:** Ejecuta los cuadernos `Analisis*.ipynb` para limpiar metrológicamente los datos de Hertz brutos, seguido de los pipelines `ML*.ipynb` para entrenar las arquitecturas predictivas y extraer la importancia de las variables.

---
## **Disponibilidad de Datos**

Los conjuntos de datos experimentales completos generados, curados y analizados durante este proyecto se encuentran disponibles en abierto en este repositorio. Estos archivos contienen los parámetros de diseño de las formulaciones (p. ej., concentraciones de precursores, tiempos sumergidos en agua) junto con sus correspondientes propiedades mecánicas (módulo de Young, error de ajuste matemático de Hertz) obtenidas de forma autónoma mediante la plataforma ASMI.

* `Sistema_LAP.csv`: Conjunto de datos completo de alto rendimiento para el sistema base de hidrogeles PEGDA/LAP.
* `Sistema_PVA.csv`: Conjunto de datos para las redes de polímeros semi-interpenetradas (semi-IPN) de PVA/PEGDA/LAP.
* `Sistema_RF.csv`: Conjunto de datos para el sistema fotopolimerizable biocompatible de Tipo II PEGDA/TEOA/Riboflavina.

> **Nota:** Estos *datasets* actúan como la entrada principal para los flujos de trabajo (*pipelines*) de Machine Learning y XAI detallados en la Fase 4.

---
---

# **Automated Platform for Soft Matter Synthesis and Characterization**
**A data-driven "Self-Driving Lab" platform for hydrogel discovery**

This repository contains the complete ecosystem of Python scripts and automation protocols developed for a high-throughput, closed-loop materials discovery platform. The workflow successfully integrates Design of Experiments (DoE), automated liquid handling, high-throughput mechanical characterization, and Explainable Machine Learning (XAI) to accelerate the design of biocompatible hydrogels and semi-interpenetrating networks.

---

### **Repository Architecture**

The codebase is modularized into four main operational phases, guiding the user from theoretical experimental design to predictive physical modeling:

### **Phase 1: Experimental Design (DoE)**
Algorithms designed to map multicomponent compositional spaces using **Latin Hypercube Sampling (LHS)**. These scripts maximize formulation diversity while integrating strict rheological safety thresholds to prevent pipetting jams on the robot.
* `LHSlap.py`: Generates the 2D sampling space for the baseline PEGDA/LAP hydrogel system.
* `LHSpva.ipynb`: An interactive notebook that generates the 3D sampling space for viscoelastically reinforced PVA/PEGDA/LAP semi-IPN networks, including 3D visualizations using Plotly.
* `LHSriboflavin.py`: Maps the 3D sampling matrix for Type II biocompatible photopolymerizable PEGDA/TEOA/Riboflavin systems.

### **Phase 2: Automated Robotic Synthesis**
Scripts utilizing the **Opentrons Flex API v2.21** programmed to command the liquid handling robot to perform precise dispensing, mixing, and formulation in standard SBS 96-well microplates.
* `LAPoptimo_1.py`, `LAPoptimo_2.py`, `LAPoptimo_3.py`: Batch synthesis protocols (PEGDA/LAP) that split 32 unique formulations (with 3 replicates each) across 3 microplates.
* `PVAoptimo_1.py`, `PVAoptimo_2.py`, `PVAoptimo_3.py`: Custom-tailored high-viscosity liquid handling protocols optimized for PVA-containing matrices.
* `RFoptimo_1.py`, `RFoptimo_2.py`, `RFoptimo_3.py`: Formulation protocols for the highly kinetics-dependent PEGDA/RF/TEOA system.

### **Phase 3: High-Throughput Characterization and Hardware Control**
A suite of scripts to manage hardware diagnostics, positioning, and data acquisition for the Automated Soft Matter Indenter (ASMI).
* `button.py`: A utility and diagnostic script designed to verify the hardware-software handshake prior to execution. It ensures proper serial communication and data flow between the Vernier force sensor, the ASMI control environment, and the host computer.
* `home.py`: A positioning script that safely retracts and returns the CNC axes to their absolute zero position (Machine Home), guaranteeing safe loading and unloading of microplates.
* `measure.py`: The core data acquisition and control script. It communicates asynchronously with the Vernier Go Direct® force sensor and controls the Genmitsu 3018-PRO CNC frame via GRBL (G-Code). It performs deterministic surface detection and automatically fits raw indentation curves to **Hertzian contact mechanics** (effective range: 0.3–0.7 mm), generating real-time quality control (QC) plots.

### **Phase 4: Exploratory Data Analysis and Machine Learning**
Jupyter notebooks for data curation, metrological validation, and predictive modeling using tree-based ensembles (Random Forest, ExtraTrees, XGBoost) and Gaussian Process Regression (GPR).

* `Analisis*.ipynb` (`LAP`, `PVA`, `RF`): **Data Curation and EDA**. Applies a strict threshold discarding relative fitting errors ≤25% to clean raw data. It validates hardware inter/intra-session stability and maps the composition-property space using interactive 2D/3D Plotly surfaces.
* `ML_LAP_code_limpio_basico.ipynb`, `ML_RF_code_limpio_basico.ipynb`, `ML_PVA_code_limpio_basico.ipynb`: **Baseline Predictive Models**. Trains algorithms using direct operational variables (absolute precursor concentrations and water immersion time) as the primary feature space, and extracts **SHAP (*SHapley Additive exPlanations*)** values to translate model predictions into interpretable physical laws.
* `ML_LAP_code_limpio.ipynb`, `ML_RF_code_limpio.ipynb`, `ML_PVA_code_limpio.ipynb`: **Advanced XAI Models**. Implements Feature Engineering (e.g., stoichiometric ratios) and extracts **SHAP** values to break down the algorithm's "black box" into thermodynamic physical principles.

---

## **Workflow (Quick Start Guide)**

1. **Design:** Run the corresponding `LHS*.py` script to generate a balanced, non-overlapping chemical design space.
2. **Synthesize:** Load the resulting coordinates and volumes into the Opentrons `*optimo*.py` protocols to initiate autonomous formulation in the microplates.
3. **Characterize:** Following UV curing, transfer the plates to the ASMI platform. Run `measure.py` to start the unattended mechanical mapping sequence.
4. **Model:** Run the `Analisis*.ipynb` notebooks to metrologically clean raw Hertz data, followed by the `ML*.ipynb` pipelines to train predictive architectures and extract feature importance.

---
## **Data Availability**

The complete experimental datasets generated, curated, and analyzed during this project are openly available in this repository. These files contain the formulation design parameters (e.g., precursor concentrations, water immersion times) along with their corresponding mechanical properties (Young's modulus, Hertz mathematical fitting error) obtained autonomously via the ASMI platform.

* `Sistema_LAP.csv`: Full high-throughput dataset for the baseline PEGDA/LAP hydrogel system.
* `Sistema_PVA.csv`: Dataset for the PVA/PEGDA/LAP semi-interpenetrating polymer networks (semi-IPN).
* `Sistema_RF.csv`: Dataset for the Type II biocompatible photopolymerizable PEGDA/TEOA/Riboflavin system.

> **Note:** These datasets serve as the primary input for the Machine Learning and XAI pipelines detailed in Phase 4.

---
---

## **Requirements and Installation / Requisitos e Instalación**

To run the design, hardware control, and machine learning scripts locally, ensure you have the following scientific library suite installed:

Para ejecutar localmente los scripts de diseño, control de hardware y machine learning, asegúrate de tener instalado el siguiente conjunto de librerías científicas:

```bash
pip install numpy pandas scipy matplotlib openpyxl plotly pyserial scikit-learn xgboost shap
