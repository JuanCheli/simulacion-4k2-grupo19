import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from utils import *
from tkinter import filedialog
import os

# Parche para atrapar el TclError en _activate_placeholder
_original_activate = ctk.CTkEntry._activate_placeholder
def _safe_activate_placeholder(self):
    try:
        _original_activate(self)
    except tk.TclError:
        pass
ctk.CTkEntry._activate_placeholder = _safe_activate_placeholder

# valor crítico χ² para α=0.05, df = 1..30 (PUEDE SER IMPORTADO COMO CONSTANTE)
CHI2_CRITICOS_005 = {
    1: 3.841, 
    2: 5.991,
    3: 7.815, 
    4: 9.488, 
    5: 11.070,
    6: 12.592, 
    7: 14.067, 
    8: 15.507, 
    9: 16.919,
    10: 18.307,
    11: 19.675,
    12: 21.026, 
    13: 22.362, 
    14: 23.685,
    15: 24.996,
    16: 26.296,
    17: 27.587, 
    18: 28.869, 
    19: 30.144,
    20: 31.410,
    21: 32.671,
    22: 33.924, 
    23: 35.172, 
    24: 36.415,
    25: 37.652,
    26: 38.885,
    27: 40.113,
    28: 41.337,
    29: 42.557
}


# Configuración inicial de CustomTkinter
ctk.set_appearance_mode("System")  # Modos: "System" (por defecto), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Temas: "blue" (por defecto), "green", "dark-blue"

class DistribucionesApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana
        self.title("TP2 - Generador de Números Aleatorios")
        self.geometry("1200x800")
        
        # Variables para almacenar la selección y los valores
        self.distribucion_var = ctk.StringVar(value="uniforme")
        self.tamano_muestra_var = ctk.StringVar(value="100")
        self.num_intervalos_var = ctk.StringVar(value="10")
        
        # Variables para cada distribución
        self.uniforme_a_var = ctk.StringVar(value="0")
        self.uniforme_b_var = ctk.StringVar(value="1")
        self.exponencial_lambda_var = ctk.StringVar(value="1")
        self.normal_media_var = ctk.StringVar(value="0")
        self.normal_desviacion_var = ctk.StringVar(value="1")
        
        # Datos generados
        self.datos_generados = None
        
        # Crear el marco principal
        self.marco_principal = ctk.CTkFrame(self)
        self.marco_principal.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Título de la aplicación
        self.titulo = ctk.CTkLabel(self.marco_principal, text="Generador de Números Aleatorios - Simulación",
                                  font=ctk.CTkFont(size=20, weight="bold"))
        self.titulo.pack(pady=10)
        
        # Marco para la selección de distribución
        self.crear_selector_distribucion()
        
        # Marco para el tamaño de muestra
        self.crear_selector_tamano_muestra()
        
        # Marco para los parámetros (cambiará según la distribución seleccionada)
        self.marco_parametros = ctk.CTkFrame(self.marco_principal)
        self.marco_parametros.pack(padx=10, pady=10, fill="x")
        
        # Crear los parámetros iniciales (uniforme por defecto)
        self.actualizar_parametros()
        
        # Marco para los intervalos del histograma
        self.crear_selector_intervalos()
        
        # Botón para generar la muestra
        self.boton_generar = ctk.CTkButton(self.marco_principal, text="Generar Muestra", 
                                         command=self.generar_muestra,
                                         font=ctk.CTkFont(size=14, weight="bold"),
                                         height=40)
        self.boton_generar.pack(pady=15)

        # Botón para exportar la muestra
        self.boton_exportar = ctk.CTkButton(self.marco_principal, text="Exportar a Excel",
                                            command=self.exportar_a_excel,
                                            font=ctk.CTkFont(size=14),
                                            height=40,
                                            fg_color="#28a745",  # Color verde para distinguirlo
                                            hover_color="#218838")
        self.boton_exportar.pack(pady=5)
        
        # Crear pestañas para mostrar diferentes vistas
        self.crear_pestanas()
        
        # Configurar el cambio de parámetros cuando cambie la distribución
        self.distribucion_var.trace_add("write", lambda *args: self.actualizar_parametros())

    def exportar_a_excel(self):
        """
        Exporta los datos generados a un archivo Excel.
        """
        if self.datos_generados is None:
            messagebox.showerror("Error", "No hay datos para exportar. Genera una muestra primero.")
            return

        # Importamos aquí para evitar problemas si no está instalado openpyxl
        try:
            from export_excel import exportar_a_excel
            exportar_a_excel(self)
        except ImportError:
            messagebox.showerror("Error",
                                 "No se pudo cargar el módulo de exportación. Asegúrate de tener instalado openpyxl:\n\npip install openpyxl")
    
    def crear_selector_distribucion(self):
        marco_distribucion = ctk.CTkFrame(self.marco_principal)
        marco_distribucion.pack(padx=10, pady=10, fill="x")
        
        # Etiqueta de selección
        etiqueta = ctk.CTkLabel(marco_distribucion, text="Selecciona la distribución:",
                             font=ctk.CTkFont(size=14))
        etiqueta.pack(side="left", padx=10)
        
        # Radio buttons para cada distribución
        opciones = ["uniforme", "exponencial", "normal"]
        for i, opcion in enumerate(opciones):
            radio = ctk.CTkRadioButton(marco_distribucion, text=opcion.capitalize(),
                                     variable=self.distribucion_var, value=opcion,
                                     font=ctk.CTkFont(size=13))
            radio.pack(side="left", padx=10)
    
    def crear_selector_tamano_muestra(self):
        marco_tamano = ctk.CTkFrame(self.marco_principal)
        marco_tamano.pack(padx=10, pady=10, fill="x")
        
        # Etiqueta para el tamaño de muestra
        etiqueta = ctk.CTkLabel(marco_tamano, text="Tamaño de muestra:",
                             font=ctk.CTkFont(size=14))
        etiqueta.pack(side="left", padx=10)
        
        # Entrada para el tamaño de muestra
        entrada = ctk.CTkEntry(marco_tamano, textvariable=self.tamano_muestra_var, width=120)
        entrada.pack(side="left", padx=10)
        
        # Etiqueta de información sobre el límite
        info = ctk.CTkLabel(marco_tamano, text="(máx. 1,000,000)",
                         font=ctk.CTkFont(size=12, slant="italic"))
        info.pack(side="left")
    
    def crear_selector_intervalos(self):
        marco_intervalos = ctk.CTkFrame(self.marco_principal)
        marco_intervalos.pack(padx=10, pady=10, fill="x")
        
        # Etiqueta para los intervalos
        etiqueta = ctk.CTkLabel(marco_intervalos, text="Número de intervalos para el histograma:",
                             font=ctk.CTkFont(size=14))
        etiqueta.pack(side="left", padx=10)
        
        # Combobox para seleccionar intervalos
        opciones_intervalos = ["10", "15", "20", "25"]
        combo = ctk.CTkComboBox(marco_intervalos, values=opciones_intervalos, 
                              variable=self.num_intervalos_var, width=80)
        combo.pack(side="left", padx=10)
    
    def actualizar_parametros(self):
        # Limpiar el marco de parámetros
        for widget in self.marco_parametros.winfo_children():
            widget.destroy()
        
        distribucion = self.distribucion_var.get()
        
        if distribucion == "uniforme":
            # Parámetros para distribución uniforme (a, b)
            etiqueta_a = ctk.CTkLabel(self.marco_parametros, text="Valor mínimo (a):",
                                   font=ctk.CTkFont(size=14))
            etiqueta_a.grid(row=0, column=0, padx=10, pady=5, sticky="e")
            
            entrada_a = ctk.CTkEntry(self.marco_parametros, textvariable=self.uniforme_a_var, width=100)
            entrada_a.grid(row=0, column=1, padx=10, pady=5, sticky="w")
            
            etiqueta_b = ctk.CTkLabel(self.marco_parametros, text="Valor máximo (b):",
                                   font=ctk.CTkFont(size=14))
            etiqueta_b.grid(row=0, column=2, padx=10, pady=5, sticky="e")
            
            entrada_b = ctk.CTkEntry(self.marco_parametros, textvariable=self.uniforme_b_var, width=100)
            entrada_b.grid(row=0, column=3, padx=10, pady=5, sticky="w")
            
        elif distribucion == "exponencial":
            # Parámetro para distribución exponencial (lambda)
            etiqueta_lambda = ctk.CTkLabel(self.marco_parametros, text="Lambda (λ):",
                                        font=ctk.CTkFont(size=14))
            etiqueta_lambda.grid(row=0, column=0, padx=10, pady=5, sticky="e")
            
            entrada_lambda = ctk.CTkEntry(self.marco_parametros, textvariable=self.exponencial_lambda_var, width=100)
            entrada_lambda.grid(row=0, column=1, padx=10, pady=5, sticky="w")
            
        elif distribucion == "normal":
            # Parámetros para distribución normal (media, desviación estándar)
            etiqueta_media = ctk.CTkLabel(self.marco_parametros, text="Media (μ):",
                                       font=ctk.CTkFont(size=14))
            etiqueta_media.grid(row=0, column=0, padx=10, pady=5, sticky="e")
            
            entrada_media = ctk.CTkEntry(self.marco_parametros, textvariable=self.normal_media_var, width=100)
            entrada_media.grid(row=0, column=1, padx=10, pady=5, sticky="w")
            
            etiqueta_desviacion = ctk.CTkLabel(self.marco_parametros, text="Desviación estándar (σ):",
                                            font=ctk.CTkFont(size=14))
            etiqueta_desviacion.grid(row=0, column=2, padx=10, pady=5, sticky="e")
            
            entrada_desviacion = ctk.CTkEntry(self.marco_parametros, textvariable=self.normal_desviacion_var, width=100)
            entrada_desviacion.grid(row=0, column=3, padx=10, pady=5, sticky="w")
    
    def crear_pestanas(self):
        # Marco para las pestañas
        self.marco_pestanas = ctk.CTkTabview(self.marco_principal)
        self.marco_pestanas.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Crear pestañas
        self.marco_pestanas.add("Serie Generada")
        self.marco_pestanas.add("Histograma")
        self.marco_pestanas.add("Tabla de Frecuencias")
        
        # Configurar la pestaña de serie generada
        self.marco_serie = ctk.CTkFrame(self.marco_pestanas.tab("Serie Generada"))
        self.marco_serie.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Texto y scrollbar para mostrar la serie
        self.frame_texto = ctk.CTkFrame(self.marco_serie)
        self.frame_texto.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Scrollbar y texto
        self.scrollbar_y = ctk.CTkScrollbar(self.frame_texto)
        self.scrollbar_y.pack(side="right", fill="y")
        
        self.scrollbar_x = ctk.CTkScrollbar(self.frame_texto, orientation="horizontal")
        self.scrollbar_x.pack(side="bottom", fill="x")
        
        self.texto_serie = ctk.CTkTextbox(self.frame_texto, yscrollcommand=self.scrollbar_y.set,
                                       xscrollcommand=self.scrollbar_x.set, wrap="none",
                                       font=ctk.CTkFont(family="Courier", size=11))
        self.texto_serie.pack(fill="both", expand=True)
        
        self.scrollbar_y.configure(command=self.texto_serie.yview)
        self.scrollbar_x.configure(command=self.texto_serie.xview)
        
        self.texto_serie.insert("1.0", "Genera una muestra para ver la serie de números aleatorios")
        self.texto_serie.configure(state="disabled")
        
        # Configurar la pestaña de histograma
        self.marco_histograma = ctk.CTkFrame(self.marco_pestanas.tab("Histograma"))
        self.marco_histograma.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Configurar la pestaña de tabla de frecuencias
        self.marco_tabla = ctk.CTkFrame(self.marco_pestanas.tab("Tabla de Frecuencias"))
        self.marco_tabla.pack(fill="both", expand=True, padx=5, pady=5)
    
    def generar_muestra(self):
        try:
            # Validar tamaño de muestra
            tamano = int(self.tamano_muestra_var.get())
            if tamano <= 0:
                messagebox.showerror("Error", "El tamaño de la muestra debe ser positivo")
                return
            if tamano > 1000000:
                messagebox.showerror("Error", "El tamaño máximo permitido es 1,000,000")
                return
            
            distribucion = self.distribucion_var.get()
            num_intervalos = int(self.num_intervalos_var.get())
            
            parametros = {}
            if distribucion == "uniforme":
                a = float(self.uniforme_a_var.get())
                b = float(self.uniforme_b_var.get())
                if a >= b:
                    messagebox.showerror("Error", "El valor mínimo debe ser menor que el valor máximo")
                    return
                parametros = {"a": a, "b": b}
                titulo = f"Distribución Uniforme [a={a}, b={b}]"
            
            elif distribucion == "exponencial":
                lambda_val = float(self.exponencial_lambda_var.get())
                if lambda_val <= 0:
                    messagebox.showerror("Error", "Lambda debe ser positivo")
                    return
                parametros = {"lambda": lambda_val}
                titulo = f"Distribución Exponencial [λ={lambda_val}]"
            
            elif distribucion == "normal":
                media = float(self.normal_media_var.get())
                desviacion = float(self.normal_desviacion_var.get())
                if desviacion <= 0:
                    messagebox.showerror("Error", "La desviación estándar debe ser positiva")
                    return
                parametros = {"media": media, "desviacion": desviacion}
                titulo = f"Distribución Normal [μ={media}, σ={desviacion}]"
            
            # Generar números aleatorios uniformes entre 0 y 1 con función personalizada
            aleatorios_unif_0_1 = generar_nros_aleatorios(tamano)

            # Transformar a la distribución seleccionada usando tus funciones
            if distribucion == "uniforme":
                self.datos_generados = transformar_uniforme(aleatorios_unif_0_1, parametros["a"], parametros["b"])
            elif distribucion == "exponencial":
                self.datos_generados = transformar_exponencial(aleatorios_unif_0_1, parametros["lambda"])
            elif distribucion == "normal":
                self.datos_generados = transformar_normal(aleatorios_unif_0_1, parametros["media"], parametros["desviacion"])

            # Redondear a 4 decimales
            self.datos_generados = [round(x, 4) for x in self.datos_generados]
            
            # Mostrar resultados
            self.mostrar_serie(self.datos_generados)
            self.mostrar_histograma(self.datos_generados, titulo, num_intervalos)
            self.mostrar_tabla_frecuencias(self.datos_generados, num_intervalos)
            self.marco_pestanas.set("Serie Generada")

            print(f"Parámetros para generación externa: {distribucion}, tamaño={tamano}, parámetros={parametros}")
            return {
                "distribucion": distribucion,
                "tamano": tamano,
                "parametros": parametros,
                "num_intervalos": num_intervalos
            }

        except ValueError as e:
            messagebox.showerror("Error", f"Error en los valores ingresados: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")
    
    def mostrar_serie(self, datos):
        # Habilitar el texto para edición
        self.texto_serie.configure(state="normal")
        
        # Limpiar el texto
        self.texto_serie.delete("1.0", "end")
        
        # Formato de la serie
        filas_por_linea = 10
        texto = ""
        
        for i, valor in enumerate(datos):
            if i > 0 and i % filas_por_linea == 0:
                texto += "\n"
            texto += f"{valor:.4f}\t"
        
        # Insertar el texto
        self.texto_serie.insert("1.0", texto)
        
        # Deshabilitar el texto para evitar edición
        self.texto_serie.configure(state="disabled")
    
    def mostrar_histograma(self, datos, titulo, num_intervalos):
        # Limpiar el marco de histograma
        for widget in self.marco_histograma.winfo_children():
            widget.destroy()
        
        # Crear una figura para el histograma
        fig = Figure(figsize=(8, 5), dpi=100)
        ax = fig.add_subplot(111)
        
        # Crear histograma con número específico de intervalos
        n, bins, patches = ax.hist(datos, bins=num_intervalos, alpha=0.7, color='skyblue', edgecolor='black')
        
        # Añadir etiquetas a las barras (frecuencias)
        for i in range(len(n)):
            if n[i] > 0:  # Solo mostrar etiquetas en barras con frecuencia > 0
                ax.text(bins[i] + (bins[i+1] - bins[i])/2, n[i] + max(n)*0.02, 
                        f"{int(n[i])}", ha='center', va='bottom', fontsize=8)
        
        # Configurar los ejes y títulos
        ax.set_title(titulo)
        ax.set_xlabel("Valor")
        ax.set_ylabel("Frecuencia")
        
        # Ajustar el diseño
        fig.tight_layout()
        
        # Añadir la figura al marco
        canvas = FigureCanvasTkAgg(fig, master=self.marco_histograma)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
        
        # Añadir estadísticas básicas
        marco_stats = ctk.CTkFrame(self.marco_histograma)
        marco_stats.pack(fill="x", padx=5, pady=5)
        
        # Calcular estadísticas
        media = np.mean(datos)
        mediana = np.median(datos)
        desv_est = np.std(datos)
        min_valor = np.min(datos)
        max_valor = np.max(datos)
        
        # Formato de estadísticas
        estadisticas = [
            f"Media: {media:.4f}", 
            f"Mediana: {mediana:.4f}", 
            f"Desv. Estándar: {desv_est:.4f}",
            f"Mín: {min_valor:.4f}", 
            f"Máx: {max_valor:.4f}"
        ]
        
        # Mostrar estadísticas en una fila
        for i, stat in enumerate(estadisticas):
            etiqueta = ctk.CTkLabel(marco_stats, text=stat)
            etiqueta.grid(row=0, column=i, padx=10, pady=5)
    
    def mostrar_tabla_frecuencias(self, datos, num_intervalos):
        # — Limpieza y setup —
        for w in self.marco_tabla.winfo_children():
            w.destroy()
        # Histograma y listas mutables
        frecuencias, bordes = np.histogram(datos, bins=num_intervalos)
        frecuencias = frecuencias.tolist()
        bordes      = bordes.tolist()

        n    = len(datos)
        dist = self.distribucion_var.get()

        # — 1) Frecuencias esperadas iniciales —
        f_esperadas = []
        for i in range(len(frecuencias)):
            a, b = bordes[i], bordes[i+1]
            if dist == "uniforme":
                a0, b0 = float(self.uniforme_a_var.get()), float(self.uniforme_b_var.get())
                p = (b - a) / (b0 - a0)
            elif dist == "exponencial":
                lam = float(self.exponencial_lambda_var.get())
                p = cdf_exponencial(b, lam) - cdf_exponencial(a, lam)
            else:  # normal
                mu, sigma = float(self.normal_media_var.get()), float(self.normal_desviacion_var.get())
                p = cdf_normal(b, mu, sigma) - cdf_normal(a, mu, sigma)
            f_esperadas.append(p * n)

        # — 2) Función auxiliar de agrupamiento —
        def agrupar(i, j):
            i0, j0 = sorted((i, j))
            bordes[i0+1]       = bordes[j0+1]
            frecuencias[i0]   += frecuencias[j0]
            f_esperadas[i0]   += f_esperadas[j0]
            del bordes[j0+1], frecuencias[j0], f_esperadas[j0]

        # — 3) Agrupar intervalos con fe < 5 —
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
                        vecino = idx+1 if f_esperadas[idx+1] < f_esperadas[idx-1] else idx-1
                    agrupar(idx, vecino)
                    changed = True
                    break

        # — 4) Construcción de la tabla —
        k = len(frecuencias)
        titulo = ctk.CTkLabel(self.marco_tabla,
            text=f"Tabla de Frecuencias ({k} intervalos tras agrupamiento)",
            font=ctk.CTkFont(size=16, weight="bold"))
        titulo.pack(pady=10)

        frame = ctk.CTkFrame(self.marco_tabla)
        frame.pack(fill="both", expand=True, padx=5, pady=5)
        scrollbar = ctk.CTkScrollbar(frame); scrollbar.pack(side="right", fill="y")
        lienzo = tk.Canvas(frame, yscrollcommand=scrollbar.set,
                        background="#2b2b2b", highlightthickness=0)
        lienzo.pack(side="left", fill="both", expand=True)
        scrollbar.configure(command=lienzo.yview)
        tabla = ctk.CTkFrame(lienzo); lienzo.create_window((0,0), window=tabla, anchor="nw")

        # Encabezados
        cols = ["#","Limite inferior","Limite superior","Marca de clase","Frecuencia observada","Frecuencia esperada"]
        for c, h in enumerate(cols):
            lbl = ctk.CTkLabel(tabla, text=h, font=ctk.CTkFont(weight="bold"))
            lbl.grid(row=0, column=c, padx=8, pady=4, sticky="nsew")
        ttk.Separator(tabla, orient="horizontal")\
            .grid(row=1, column=0, columnspan=len(cols), sticky="ew", pady=4)

        total = sum(frecuencias)
        for i in range(k):
            # número de intervalo
            ctk.CTkLabel(tabla, text=str(i+1)).grid(row=i+2, column=0)
            # límites
            ctk.CTkLabel(tabla, text=f"{bordes[i]:.4f}").grid(row=i+2, column=1)
            ctk.CTkLabel(tabla, text=f"{bordes[i+1]:.4f}").grid(row=i+2, column=2)
            # marca de clase
            marca = (bordes[i] + bordes[i+1]) / 2
            ctk.CTkLabel(tabla, text=f"{marca:.4f}").grid(row=i+2, column=3)
            # observada y esperada
            ctk.CTkLabel(tabla, text=str(frecuencias[i])).grid(row=i+2, column=4)
            ctk.CTkLabel(tabla, text=f"{f_esperadas[i]:.2f}").grid(row=i+2, column=5)

        # — 5) Cálculo final de χ² y decisión —
        chi2 = sum((o - e)**2/e for o,e in zip(frecuencias, f_esperadas))
        if dist == "uniforme":
            df = k - 1
        elif dist == "exponencial":
            df = k - 2
        else:
            df = k - 3
        crit = CHI2_CRITICOS_005.get(df, float('nan'))
        decision = "Rechazar H₀" if chi2 > crit else "No rechazar H₀"
        texto = f"χ²={chi2:.3f}  df={df}  χ²₀.₀₅={crit:.3f} → {decision}"
        lbl_res = ctk.CTkLabel(tabla, text=texto, font=ctk.CTkFont(size=12, weight="bold"))
        lbl_res.grid(row=k+3, column=0, columnspan=len(cols), pady=10)

        tabla.update_idletasks()
        lienzo.config(scrollregion=lienzo.bbox("all"))

        
# Función para iniciar la aplicación
def iniciar_app():
    app = DistribucionesApp()
    app.mainloop()
    
if __name__ == "__main__":
    iniciar_app()
