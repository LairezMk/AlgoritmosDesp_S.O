from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
from customtkinter import *
import matplotlib.pyplot as plt
import numpy as np
import pygame
from PIL import Image, ImageTk
from Procesos import Proceso
from Graficas import Mostrar_Procesos

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("light")  # Modo oscuro para una apariencia más moderna
        ctk.set_default_color_theme("Hades.json")
        self.title("Algoritmos de Procesos")
        self.geometry("600x480")
        self.resizable(False, False)

        side_img_data = Image.open("side-img.png")
        side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(600, 100))  # Ajustamos el tamaño de la imagen

        # Agregar la imagen en la parte superior
        CTkLabel(self, text="", image=side_img).pack(fill="x", side="top")

        frame = ctk.CTkFrame(self, width=600, height=380, fg_color="black")
        frame.pack_propagate(0)  # Evita que el frame se redimensione
        frame.pack(fill="both", expand=True)  

        # Título
        self.label = ctk.CTkLabel(master=frame, text="Algoritmos de Procesos", font=("Arial", 24), text_color="white")
        self.label.pack(pady=20)
        
        self.button_iniciar = ctk.CTkButton(master=frame, text="Iniciar", font=("Arial", 18), fg_color="#ca04ca", border_width=2,
                                            hover_color="#6a166a", border_color="white", command=self.abrir_grafica)
        self.button_iniciar.pack(pady=20)
        
        self.button_salir = ctk.CTkButton(master=frame, text="Salir", font=("Arial", 18), fg_color="#ca04ca", border_width=2,
                                            hover_color="#6a166a", border_color="white", command=self.on_closing)
        self.button_salir.pack(pady=20)

        icon_fifo = CTkImage(Image.open("fifo.png"), size=(50, 50))
        icon_sjf = CTkImage(Image.open("sjf.png"), size=(50, 50))
        icon_prio = CTkImage(Image.open("prioridad.png"), size=(50, 50))

        frame_icons = ctk.CTkFrame(master=frame, fg_color="gray25", corner_radius=8)
        frame_icons.pack(pady=10)

        CTkLabel(frame_icons, text=" FIFO ", image=icon_fifo).pack(side="left", padx=10)
        CTkLabel(frame_icons, text=" SJF ", image=icon_sjf).pack(side="left", padx=10)
        CTkLabel(frame_icons, text=" Prioridad ", image=icon_prio).pack(side="left", padx=10)

        frame_info = ctk.CTkFrame(master=frame, fg_color="gray25", corner_radius=8)
        frame_info.pack(side="bottom", anchor="se", padx=5, pady=5)

        label_autor = ctk.CTkLabel(frame_info, text="Desarrollado por:\nSamuel Herrera \nJonathan Gaviria", font=("Arial", 12), justify="left",
                                   text_color="white")
        label_autor.pack(padx=10, pady=5)

        switch = ctk.CTkSwitch(master=frame, text="Modo Oscuro", command=self.cambiar_modo, font=("Arial", 14), 
                               fg_color=["gray", "#6a166a"], bg_color="black", button_color="#ca04ca",corner_radius=10)
        switch.pack(pady=10)
        
        self.set_icon("Windows.jpg")

    def cambiar_modo(self):
            if ctk.get_appearance_mode() == "Dark":
                ctk.set_appearance_mode("Light")
            else:
                ctk.set_appearance_mode("Dark")
    
    def abrir_grafica(self):
        self.withdraw()  # Oculta la ventana principal
        Grafica(self)
    
    def on_closing(self):
        msg = CTkMessagebox(title="Exit?", message="Do you want to close the program?",
                        icon="question", option_1="Cancel", option_2="No", option_3="Yes")
        response = msg.get()
    
        if response=="Yes":
            pygame.mixer.init()
            pygame.mixer.music.load("mario64.mp3")
            pygame.mixer.music.play()
            self.after(1000, self.quit)  # Cierra toda la aplicación
            #app.destroy()

        else:
            print("Click 'Yes' to exit!")
            
    def set_icon(self, icon_path):
        try:
            img = Image.open(icon_path)
            img = img.resize((32, 32), Image.Resampling.LANCZOS)  # Redimensiona la imagen
            photo = ImageTk.PhotoImage(img)
            self.iconphoto(False, photo)
        except Exception as e:
            print(f"Error cargando el icono: {e}")

class Grafica(ctk.CTkToplevel):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.title("Graficar")
        self.geometry("800x600")
        self.resizable(False, False)
        
        self.label = ctk.CTkLabel(self, text="Ingrese la cantidad de procesos (máx 10)", font=("Arial", 20))
        self.label.pack(pady=20)
        
        self.num_procesos = ctk.CTkEntry(self, font=("Arial", 20))
        self.num_procesos.pack(pady=10)
        
        self.button_ejecutar = ctk.CTkButton(self, text="Ejecutar Algoritmo", font=("Arial", 15), command=self.ejecutar_algoritmo)
        self.button_ejecutar.pack(pady=20)
        
        #self.button_volver = ctk.CTkButton(self, text="Volver al inicio", font=("Arial", 15), fg_color="gray", hover_color="darkgray", command=self.volver_inicio)
        #self.button_volver.pack(pady=20)
    
    def ejecutar_algoritmo(self):
        try:
            num_procesos = int(self.num_procesos.get())
            if 1 <= num_procesos <= 10:
                self.pedir_datos(num_procesos)
                #self.mostrar_animacion(num_procesos)
            else:
                CTkMessagebox(title="Error", message="Ingrese un número entre 1 y 10.")
        except ValueError:
            CTkMessagebox(title="Error", message="Ingrese un número válido.")
    
    def mostrar_animacion(self, num_procesos):
        plt.figure()
        plt.plot(np.random.rand(10))
        plt.title(f"Animación con {num_procesos} procesos")
        plt.show()

    def pedir_datos(self, num_procesos):
        #Lista procesos
        self.withdraw()
        Procesos(self.root, num_procesos)
        

class Procesos(ctk.CTkToplevel):
    def __init__(self, root, num_procesos):
        super().__init__(root)
        self.title("Procesos")
        self.geometry("800x600")
        self.resizable(False, False)
        self.root= root

        # On closing
        self.protocol("WM_DELETE_WINDOW", self.volver_inicio)

        self.num_procesos = num_procesos
        self.proceso_actual = 0
        self.Lprocesos = []  # Lista de procesos

        # Crear la interfaz
        self.label_titulo = ctk.CTkLabel(self, text="", font=("Arial", 20))
        self.label_titulo.pack(pady=10)

        self.label_nombre = ctk.CTkLabel(self, text="Ingrese el nombre del proceso:", font=("Arial", 15))
        self.label_nombre.pack(pady=5)
        #Hacer que el nombre solo pueda ser de maximo 2 caracteres
        self.entry_nombre = ctk.CTkEntry(self, font=("Arial", 15))
        self.entry_nombre.pack(pady=5)

        self.label_llegada = ctk.CTkLabel(self, text="Ingrese el tiempo de llegada del proceso:", font=("Arial", 15))
        self.label_llegada.pack(pady=5)
        self.entry_llegada = ctk.CTkEntry(self, font=("Arial", 15))
        self.entry_llegada.pack(pady=5)

        self.label_rafaga = ctk.CTkLabel(self, text="Ingrese la ráfaga del proceso:", font=("Arial", 15))
        self.label_rafaga.pack(pady=5)
        self.entry_rafaga = ctk.CTkEntry(self, font=("Arial", 15))
        self.entry_rafaga.pack(pady=5)

        self.label_prioridad = ctk.CTkLabel(self, text="Ingrese la prioridad del proceso:", font=("Arial", 15))
        self.label_prioridad.pack(pady=5)
        self.entry_prioridad = ctk.CTkEntry(self, font=("Arial", 15))
        self.entry_prioridad.pack(pady=5)

        self.boton_guardar = ctk.CTkButton(self, text="Guardar", font=("Arial", 15), command=self.guardar_proceso)
        self.boton_guardar.pack(pady=20)

        self.actualizar_interfaz()

    def actualizar_interfaz(self):
        """Actualiza la interfaz para el proceso actual"""
        self.proceso_actual += 1
        if self.proceso_actual > self.num_procesos:
            self.mostrar_resumen()
            return

        self.label_titulo.configure(text=f"Ingresando el proceso {self.proceso_actual}/{self.num_procesos}")

        # Limpiar los campos de entrada
        self.entry_nombre.delete(0, "end")
        self.entry_llegada.delete(0, "end")
        self.entry_rafaga.delete(0, "end")
        self.entry_prioridad.delete(0, "end")

    def guardar_proceso(self):
        """Guarda el proceso actual y actualiza la interfaz para el siguiente"""
        nombre = self.entry_nombre.get().strip() #El .strip elimina los espacios en blanco
        llegada = self.entry_llegada.get().strip()
        rafaga = self.entry_rafaga.get().strip()
        prioridad = self.entry_prioridad.get().strip()

        # Validaciones básicas
        if not nombre or not llegada.isdigit() or not rafaga.isdigit() or not prioridad.isdigit():
            CTkMessagebox(title="Error", message="Por favor, ingrese valores válidos.")
            return

        self.Lprocesos.append(Proceso(nombre, int(llegada), int(rafaga), int(prioridad)))

        if self.proceso_actual < self.num_procesos:
            CTkMessagebox(title="Proceso Guardado", message=f"Proceso {self.proceso_actual} guardado con éxito.", icon="info")

        self.actualizar_interfaz()

    def mostrar_resumen(self):
        mensaje = "Procesos ingresados:\n"
        for i in range(len(self.Lprocesos)):
            proceso = self.Lprocesos[i]
            mensaje += (f"\nProceso {i}: {proceso.nombre}\n"
                        f"  - Llegada: {proceso.tiempo_llegada}\n"
                        f"  - Ráfaga: {proceso.rafaga}\n"
                        f"  - Prioridad: {proceso.prioridad}\n")

        CTkMessagebox(title="Resumen de Procesos", message=mensaje, icon="info")
        #self.destroy()  
        #self.volver_inicio()
        Mostrar_Procesos(self.Lprocesos)

    def volver_inicio(self):
        self.destroy()
        self.root.deiconify()
    
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
