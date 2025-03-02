import pandas as pd
import plotly.io as pio
from PIL import Image, ImageTk
import tkinter as tk
import customtkinter as ctk 
from io import BytesIO
import plotly.figure_factory as ff
from Procesos import *

class Mostrar_Procesos(ctk.CTkToplevel):  # Clase para mostrar la ventana con gráficos
    def __init__(self, procesos):
        super().__init__()
        self.title("Graficar")
        self.geometry("800x600")
        self.resizable(False, False)
        self.procesos = procesos

        # Crear pestañas
        self.TabView = ctk.CTkTabview(self, width=750, height=550)
        self.TabView.pack(pady=20)

        self.TabView.add("FIFO")
        self.TabView.add("SJF")
        self.TabView.add("Prioridad")

        # Crear labels en las pestañas
        self.labelfifo = ctk.CTkLabel(self.TabView.tab("FIFO"), text="Cargando...")
        self.labelfifo.pack(pady=20)

        self.labelsjf = ctk.CTkLabel(self.TabView.tab("SJF"), text="SJF")
        self.labelsjf.pack(pady=20)

        self.labelprioridad = ctk.CTkLabel(self.TabView.tab("Prioridad"), text="Prioridad")
        self.labelprioridad.pack(pady=20)

        # Llamar al método para generar la gráfica
        self.generar_grafica(self.procesos, "FIFO")
        self.generar_grafica(self.procesos, "SJF")
        self.generar_grafica(self.procesos, "Prioridad")

    def generar_grafica(self, procesos, algoritmo):

        if algoritmo == "FIFO":
            # Calcular el tiempo de espera y de sistema para el algoritmo FIFO
            procesos.sort(key=lambda x: x.tiempo_llegada)
            procesos = Fifo(procesos)[0]

        elif algoritmo == "SJF":
            # Calcular el tiempo de espera y de sistema para el algoritmo SJF
            procesos = SJF(procesos)[0]

        elif algoritmo == "Prioridad":
            # Calcular el tiempo de espera y de sistema para el algoritmo de prioridad
            procesos = Prioridad(procesos)[0]

        procesos.sort(key=lambda x: x.tiempo_llegada)

        # Convertir los datos de los procesos a una lista de diccionarios
        procesos_data = [{"Task": p.nombre, "Tiempo llegada": p.tiempo_llegada, "Ráfaga": p.rafaga, "Finish": p.tiempo_final, "Start": p.tiempo_inicio} for p in procesos]

        # Datos para la gráfica de Gantt
        df = pd.DataFrame(procesos_data)

        # Crear la gráfica de Gantt
        fig = ff.create_gantt(df, index_col="Task", show_colorbar=False, group_tasks=True)
        fig.update_layout(xaxis_type='linear', autosize=True, width=700, height=300)
        fig.update_xaxes(title="Tiempo (segundos)", dtick=1)  # Especificar eje X como numérico
        fig.update_yaxes(title="Procesos")

        # Convertir la gráfica a imagen
        img_bytes = pio.to_image(fig, format="png")
        img = Image.open(BytesIO(img_bytes))

        # Convertir la imagen a un formato compatible con tkinter
        img_tk = ImageTk.PhotoImage(img)

        if algoritmo == "FIFO":
            # Actualizar el label con la imagen en la pestaña FIFO
            self.labelfifo.configure(image=img_tk, text="")
            self.labelfifo.pack(pady=20)
            #Crear un label para mostrar el tiempo de espera y de sistema
            self.label_fifo = ctk.CTkLabel(self.TabView.tab("FIFO"), text=f"Tiempo de espera: {Fifo(procesos)[1]}")
            self.label_fifo.pack(pady=20)
            self.label_fifo = ctk.CTkLabel(self.TabView.tab("FIFO"), text=f"Tiempo de sistema: {Fifo(procesos)[2]}")
            self.label_fifo.pack(pady=20)


        elif algoritmo == "SJF":
            # Actualizar el label con la imagen en la pestaña SJF
            self.labelsjf.configure(image=img_tk, text="")
            self.labelsjf.pack(pady=20)
            #Crear un label para mostrar el tiempo de espera y de sistema
            self.label_sjf = ctk.CTkLabel(self.TabView.tab("SJF"), text=f"Tiempo de espera: {SJF(procesos)[1]}")
            self.label_sjf.pack(pady=20)
            self.label_sjf = ctk.CTkLabel(self.TabView.tab("SJF"), text=f"Tiempo de sistema: {SJF(procesos)[2]}")
            self.label_sjf.pack(pady=20)

        elif algoritmo == "Prioridad":
            # Actualizar el label con la imagen en la pestaña Prioridad
            self.labelprioridad.configure(image=img_tk, text="")
            self.labelprioridad.pack(pady=20)
            #Crear un label para mostrar el tiempo de espera y de sistema
            self.label_prioridad = ctk.CTkLabel(self.TabView.tab("Prioridad"), text=f"Tiempo de espera: {Prioridad(procesos)[1]}")
            self.label_prioridad.pack(pady=20)
            self.label_prioridad = ctk.CTkLabel(self.TabView.tab("Prioridad"), text=f"Tiempo de sistema: {Prioridad(procesos)[2]}")
            self.label_prioridad.pack(pady=20)

if __name__ == "__main__":
    procesos = [Proceso("P1", 0, 6), Proceso("P2", 1, 6), Proceso("P3", 2, 3)]
    Mostrar_Procesos = Mostrar_Procesos(procesos)
    Mostrar_Procesos.mainloop()


