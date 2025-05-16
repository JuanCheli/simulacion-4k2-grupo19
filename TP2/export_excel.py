import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter
from tkinter import filedialog, messagebox
import os
import numpy as np
from interfaz import *
from utils import *


def exportar_a_excel(app):
    """
    Exporta los datos generados a un archivo Excel.
    Incluye: datos brutos, histograma y tabla de frecuencias.
    """
    # Verificar que hay datos para exportar
    if app.datos_generados is None:
        messagebox.showerror("Error", "No hay datos para exportar. Genera una muestra primero.")
        return

    # Pedir al usuario dónde guardar el archivo
    archivo = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
        title="Guardar como Excel"
    )

    if not archivo:  # Si el usuario cancela, salir
        return

    # Crear un libro de trabajo y hojas
    wb = openpyxl.Workbook()

    # Hoja 1: Datos brutos
    ws_datos = wb.active
    ws_datos.title = "Datos Generados"

    # Hoja 2: Histograma (información)
    ws_hist = wb.create_sheet("Histograma")

    # Hoja 3: Tabla de frecuencias
    ws_freq = wb.create_sheet("Tabla de Frecuencias")

    # --- Hoja 1: Datos Generados ---
    ws_datos.cell(1, 1, "Datos Generados")
    ws_datos.cell(1, 1).font = Font(bold=True, size=14)

    # Información de la distribución
    distribucion = app.distribucion_var.get()

    ws_datos.cell(3, 1, "Distribución:")
    ws_datos.cell(3, 2, distribucion.capitalize())

    fila = 4
    if distribucion == "uniforme":
        a = float(app.uniforme_a_var.get())
        b = float(app.uniforme_b_var.get())
        ws_datos.cell(fila, 1, "Valor mínimo (a):")
        ws_datos.cell(fila, 2, a)
        fila += 1
        ws_datos.cell(fila, 1, "Valor máximo (b):")
        ws_datos.cell(fila, 2, b)
    elif distribucion == "exponencial":
        lambda_val = float(app.exponencial_lambda_var.get())
        ws_datos.cell(fila, 1, "Lambda (λ):")
        ws_datos.cell(fila, 2, lambda_val)
    elif distribucion == "normal":
        media = float(app.normal_media_var.get())
        desviacion = float(app.normal_desviacion_var.get())
        ws_datos.cell(fila, 1, "Media (μ):")
        ws_datos.cell(fila, 2, media)
        fila += 1
        ws_datos.cell(fila, 1, "Desviación estándar (σ):")
        ws_datos.cell(fila, 2, desviacion)

    fila += 2
    ws_datos.cell(fila, 1, "Tamaño de muestra:")
    ws_datos.cell(fila, 2, len(app.datos_generados))

    # Estadísticas básicas
    fila += 2
    ws_datos.cell(fila, 1, "Estadísticas Básicas")
    ws_datos.cell(fila, 1).font = Font(bold=True)
    fila += 1

    media = np.mean(app.datos_generados)
    mediana = np.median(app.datos_generados)
    desv_est = np.std(app.datos_generados)
    min_valor = np.min(app.datos_generados)
    max_valor = np.max(app.datos_generados)

    ws_datos.cell(fila, 1, "Media:")
    ws_datos.cell(fila, 2, f"{media:.4f}")
    fila += 1
    ws_datos.cell(fila, 1, "Mediana:")
    ws_datos.cell(fila, 2, f"{mediana:.4f}")
    fila += 1
    ws_datos.cell(fila, 1, "Desviación estándar:")
    ws_datos.cell(fila, 2, f"{desv_est:.4f}")
    fila += 1
    ws_datos.cell(fila, 1, "Valor mínimo:")
    ws_datos.cell(fila, 2, f"{min_valor:.4f}")
    fila += 1
    ws_datos.cell(fila, 1, "Valor máximo:")
    ws_datos.cell(fila, 2, f"{max_valor:.4f}")

    # Datos brutos
    fila += 2
    ws_datos.cell(fila, 1, "Serie de Números Generados")
    ws_datos.cell(fila, 1).font = Font(bold=True)
    fila += 1

    # Encabezados
    columnas_por_fila = 10
    for j in range(columnas_por_fila):
        ws_datos.cell(fila, j + 1, f"Valor {j + 1}")
        ws_datos.cell(fila, j + 1).font = Font(bold=True)

    # Datos
    fila += 1
    for i in range(0, len(app.datos_generados), columnas_por_fila):
        col = 1
        for j in range(columnas_por_fila):
            if i + j < len(app.datos_generados):
                ws_datos.cell(fila, col, f"{app.datos_generados[i + j]:.4f}")
            col += 1
        fila += 1

    # --- Hoja 2: Histograma (datos para reconstruir) ---
    ws_hist.cell(1, 1, "Datos del Histograma")
    ws_hist.cell(1, 1).font = Font(bold=True, size=14)

    num_intervalos = int(app.num_intervalos_var.get())

    # Crear histograma
    frecuencias, bordes = np.histogram(app.datos_generados, bins=num_intervalos)

    ws_hist.cell(3, 1, "Número de intervalos:")
    ws_hist.cell(3, 2, num_intervalos)

    # Encabezados
    fila = 5
    ws_hist.cell(fila, 1, "Intervalo")
    ws_hist.cell(fila, 2, "Límite inferior")
    ws_hist.cell(fila, 3, "Límite superior")
    ws_hist.cell(fila, 4, "Marca de clase")
    ws_hist.cell(fila, 5, "Frecuencia")
    for col in range(1, 6):
        ws_hist.cell(fila, col).font = Font(bold=True)

    # Datos del histograma
    for i in range(len(frecuencias)):
        fila += 1
        ws_hist.cell(fila, 1, i + 1)
        ws_hist.cell(fila, 2, f"{bordes[i]:.4f}")
        ws_hist.cell(fila, 3, f"{bordes[i + 1]:.4f}")
        marca = (bordes[i] + bordes[i + 1]) / 2
        ws_hist.cell(fila, 4, f"{marca:.4f}")
        ws_hist.cell(fila, 5, frecuencias[i])

    # --- Hoja 3: Tabla de Frecuencias ---
    ws_freq.cell(1, 1, "Tabla de Frecuencias")
    ws_freq.cell(1, 1).font = Font(bold=True, size=14)

    # Función para recalcular la tabla de frecuencias (similar al método mostrar_tabla_frecuencias)
    def calcular_tabla_frecuencias():
        datos = app.datos_generados
        num_intervalos = int(app.num_intervalos_var.get())
        distribucion = app.distribucion_var.get()

        # Histograma y listas mutables
        frecuencias, bordes = np.histogram(datos, bins=num_intervalos)
        frecuencias = frecuencias.tolist()
        bordes = bordes.tolist()

        n = len(datos)

        # Frecuencias esperadas iniciales
        f_esperadas = []
        for i in range(len(frecuencias)):
            a, b = bordes[i], bordes[i + 1]
            if distribucion == "uniforme":
                a0, b0 = float(app.uniforme_a_var.get()), float(app.uniforme_b_var.get())
                p = (b - a) / (b0 - a0)
            elif distribucion == "exponencial":
                lam = float(app.exponencial_lambda_var.get())
                p = cdf_exponencial(b, lam) - cdf_exponencial(a, lam)
            else:  # normal
                mu, sigma = float(app.normal_media_var.get()), float(app.normal_desviacion_var.get())
                p = cdf_normal(b, mu, sigma) - cdf_normal(a, mu, sigma)
            f_esperadas.append(p * n)

        # Función auxiliar de agrupamiento
        def agrupar(i, j):
            i0, j0 = sorted((i, j))
            bordes[i0 + 1] = bordes[j0 + 1]
            frecuencias[i0] += frecuencias[j0]
            f_esperadas[i0] += f_esperadas[j0]
            del bordes[j0 + 1], frecuencias[j0], f_esperadas[j0]

        # Agrupar intervalos con fe < 5
        changed = True
        while changed:
            changed = False
            for idx, fe in enumerate(f_esperadas):
                if fe < 5:
                    if idx == 0:
                        vecino = 1
                    elif idx == len(f_esperadas) - 1:
                        vecino = idx - 1
                    else:
                        vecino = idx + 1 if f_esperadas[idx + 1] < f_esperadas[idx - 1] else idx - 1
                    agrupar(idx, vecino)
                    changed = True
                    break

        # Calcular final de χ² y decisión
        chi2 = sum((o - e) ** 2 / e for o, e in zip(frecuencias, f_esperadas))
        if distribucion == "uniforme":
            df = len(frecuencias) - 1
        elif distribucion == "exponencial":
            df = len(frecuencias) - 2
        else:
            df = len(frecuencias) - 3
        crit = CHI2_CRITICOS_005.get(df, float('nan'))
        decision = "Rechazar H₀" if chi2 > crit else "No rechazar H₀"

        return {
            "bordes": bordes,
            "frecuencias": frecuencias,
            "f_esperadas": f_esperadas,
            "chi2": chi2,
            "df": df,
            "crit": crit,
            "decision": decision
        }

    # Obtener datos de la tabla
    tabla_datos = calcular_tabla_frecuencias()

    # Encabezados
    fila = 3
    ws_freq.cell(fila, 1, f"Tabla de Frecuencias ({len(tabla_datos['frecuencias'])} intervalos tras agrupamiento)")
    ws_freq.cell(fila, 1).font = Font(bold=True)

    fila += 2
    cols = ["#", "Limite inferior", "Limite superior", "Marca de clase",
            "Frecuencia observada", "Frecuencia esperada"]
    for c, h in enumerate(cols):
        ws_freq.cell(fila, c + 1, h)
        ws_freq.cell(fila, c + 1).font = Font(bold=True)
        ws_freq.cell(fila, c + 1).alignment = Alignment(horizontal='center')
        # Color de fondo para encabezados
        ws_freq.cell(fila, c + 1).fill = PatternFill("solid", fgColor="DDDDDD")

    # Datos de la tabla
    for i in range(len(tabla_datos['frecuencias'])):
        fila += 1
        # número de intervalo
        ws_freq.cell(fila, 1, i + 1)
        # límites
        ws_freq.cell(fila, 2, f"{tabla_datos['bordes'][i]:.4f}")
        ws_freq.cell(fila, 3, f"{tabla_datos['bordes'][i + 1]:.4f}")
        # marca de clase
        marca = (tabla_datos['bordes'][i] + tabla_datos['bordes'][i + 1]) / 2
        ws_freq.cell(fila, 4, f"{marca:.4f}")
        # observada y esperada
        ws_freq.cell(fila, 5, tabla_datos['frecuencias'][i])
        ws_freq.cell(fila, 6, f"{tabla_datos['f_esperadas'][i]:.2f}")

    # Resultado prueba Chi-cuadrado
    fila += 2
    texto = f"χ²={tabla_datos['chi2']:.3f}  df={tabla_datos['df']}  χ²₀.₀₅={tabla_datos['crit']:.3f} → {tabla_datos['decision']}"
    ws_freq.cell(fila, 1, texto)
    ws_freq.merge_cells(start_row=fila, start_column=1, end_row=fila, end_column=6)
    ws_freq.cell(fila, 1).font = Font(bold=True)
    ws_freq.cell(fila, 1).alignment = Alignment(horizontal='center')

    # Ajustar anchos de columna automáticamente en todas las hojas
    for ws in [ws_datos, ws_hist, ws_freq]:
        for column in ws.columns:
            max_length = 0
            column_letter = get_column_letter(column[0].column)
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = (max_length + 2)
            ws.column_dimensions[column_letter].width = adjusted_width

    # Guardar el archivo
    wb.save(archivo)

    messagebox.showinfo("Exportación exitosa",
                        f"Los datos han sido exportados con éxito a:\n{os.path.basename(archivo)}")