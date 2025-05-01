# Generador de Números Aleatorios - TP2

Este proyecto es una aplicación de escritorio desarrollada en Python que permite generar números aleatorios siguiendo distribuciones Uniforme, Exponencial o Normal. La aplicación visualiza la serie generada, muestra un histograma de frecuencias y presenta una tabla de frecuencias detallada. Utiliza un archivo `.env` para configuración inicial opcional.

## Características

*   Generación de números aleatorios para distribuciones:
    *   Uniforme (con parámetros `a` y `b`)
    *   Exponencial (con parámetro `lambda`)
    *   Normal (con parámetros `media` y `desviación estándar`, usando el método Box-Muller)
*   Interfaz gráfica de usuario (GUI) creada con `customtkinter`.
*   Visualización de la serie de números generados.
*   Generación y visualización de un histograma de frecuencias con número de intervalos configurable.
*   Cálculo y visualización de una tabla de frecuencias detallada (límites, marca de clase, frecuencias absoluta y relativa).
*   Visualización de estadísticas básicas (media, mediana, desviación estándar, mínimo, máximo) junto al histograma.
*   Configuración de valores por defecto mediante un archivo `.env`.

## Prerrequisitos

Antes de comenzar, asegúrate de tener instalado lo siguiente:

1.  **Python:** Se recomienda Python 3.7 o superior. Puedes descargarlo desde [python.org](https://www.python.org/downloads/).
2.  **pip:** El instalador de paquetes de Python. Usualmente viene incluido con las instalaciones de Python 3.4+. Puedes verificar si lo tienes ejecutando `pip --version` en tu terminal.
3.  **(Opcional - Linux):** En algunos sistemas Linux, `tkinter` (requerido por `customtkinter`) podría necesitar ser instalado por separado. Por ejemplo, en sistemas basados en Debian/Ubuntu:
    ```bash
    sudo apt-get update
    sudo apt-get install python3-tk
    ```

## Estructura del Proyecto

El proyecto consta de los siguientes archivos principales:

*   `interfaz.py`: Contiene el código de la interfaz gráfica de usuario y la lógica principal de la aplicación. Este es el archivo que se debe ejecutar.
*   `utils.py`: Contiene las funciones auxiliares para generar los números aleatorios base (uniformes 0-1) y transformarlos a las distribuciones deseadas (Uniforme, Exponencial, Normal).
*   `.env`: (Opcional, **crear manualmente**) Archivo para definir valores por defecto personalizados para la interfaz.
*   `.env.example`: Archivo de ejemplo que muestra las variables configurables en `.env`.
*   `README.md`: Este archivo de instrucciones.

## Pasos para la Ejecución

Sigue estos pasos para configurar y ejecutar el proyecto:

1.  **Obtener los Archivos del Proyecto:**
    Asegúrate de tener los archivos `interfaz.py`, `utils.py` y `.env.example` en el mismo directorio en tu computadora.
    *   **Importante:** Si `interfaz.py` contiene `from TP2.utils import ...`, necesitas ajustar la importación a `from utils import ...` ya que ambos archivos están ahora en el mismo directorio.

2.  **Abrir una Terminal o Símbolo del Sistema:**
    Navega hasta el directorio donde guardaste los archivos del proyecto. Puedes usar el comando `cd`:
    ```bash
    cd ruta/a/tu/directorio/del/proyecto
    ```
    (Reemplaza `ruta/a/tu/directorio/del/proyecto` con la ruta real).

3.  **Crear un Entorno Virtual (Recomendado):**
    Es una buena práctica aislar las dependencias del proyecto. Crea un entorno virtual (llamémoslo `venv`):
    ```bash
    python -m venv venv
    ```
    *Nota: En algunos sistemas podría ser `python3` en lugar de `python`.*

4.  **Activar el Entorno Virtual:**
    Antes de instalar paquetes o ejecutar la aplicación, debes activar el entorno:
    *   **En Windows (cmd.exe):**
        ```bash
        venv\Scripts\activate
        ```
    *   **En Windows (PowerShell):**
        ```bash
        .\venv\Scripts\Activate.ps1
        ```
        *(Si encuentras un error de ejecución de scripts, puede que necesites cambiar la política de ejecución con `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` y luego intentar activar de nuevo).*
    *   **En macOS / Linux (bash/zsh):**
        ```bash
        source venv/bin/activate
        ```
    Una vez activado, deberías ver `(venv)` al principio de la línea de comandos de tu terminal. **Todos los comandos siguientes (`pip install`, `python`) deben ejecutarse con el entorno activado.**

5.  **Instalar las Dependencias:**
    Con el entorno virtual activado, instala las bibliotecas necesarias desde `pip`:
    ```bash
    pip install customtkinter matplotlib pandas numpy
    ```
    *Nota: `tkinter` generalmente viene con Python, pero si encuentras errores relacionados con él, consulta la sección de Prerrequisitos.*

6.  **Configurar `.env` (Opcional):**
    Si deseas cambiar los valores iniciales por defecto de la aplicación (distribución, tamaño de muestra, parámetros, etc.):
    *   Copia el archivo `.env.example` a un nuevo archivo llamado `.env` en el mismo directorio.
    *   Abre `.env` con un editor de texto.
    *   Descomenta (quita el `#` del inicio) y modifica los valores de las variables que quieras cambiar.
    *   Guarda el archivo `.env`. La aplicación leerá estos valores al iniciarse. Si una variable no está en `.env` o está comentada, se usará el valor por defecto codificado en `interfaz.py`.

7.  **Ejecutar la Aplicación:**
    Asegúrate de que tu entorno virtual (`venv`) sigue activado. Luego, inicia la aplicación:
    ```bash
    python interfaz.py
    ```

8.  **Usar la Aplicación:**
    *   Se abrirá la ventana "TP2 - Generador de Números Aleatorios" con los valores por defecto (ya sea los del código o los de tu archivo `.env`).
    *   Selecciona la **distribución**, **tamaño de muestra**, **parámetros** y **número de intervalos**.
    *   Haz clic en "**Generar Muestra**".
    *   Explora los resultados en las pestañas.

9.  **Desactivar el Entorno Virtual (Cuando termines):**
    Cuando hayas terminado de usar la aplicación en esa sesión de terminal, puedes desactivar el entorno virtual:
    ```bash
    deactivate
    ```
    El prefijo `(venv)` desaparecerá de tu línea de comandos.

¡Listo! Con estos pasos, puedes ejecutar el proyecto de forma aislada usando un entorno virtual.