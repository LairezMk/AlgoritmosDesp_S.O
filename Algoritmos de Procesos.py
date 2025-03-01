from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
import pygame
from PIL import Image

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")  # Modo oscuro para una apariencia más moderna
        ctk.set_default_color_theme("Hades.json")
        
        
        self.title("Algoritmos de Procesos")
        self.geometry("800x600")
        self.resizable(False, False)
        
        self.label = ctk.CTkLabel(self, text="Algoritmos de Procesos", font=("Arial", 24))
        self.label.pack(pady=20)
        
        self.button_iniciar = ctk.CTkButton(self, text="Iniciar", font=("Arial", 18), command=self.abrir_grafica)
        self.button_iniciar.pack(pady=20)
        
        self.button_salir = ctk.CTkButton(self, text="Salir", font=("Arial", 18), fg_color="red", hover_color="darkred", command=self.on_closing)
        self.button_salir.pack(pady=20)

        
        
        self.set_icon("Windows.jpg")
    
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
            self.iconphoto(False, ctk.CTkImage(light_image=img, size=(32, 32)))
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
        
        self.button_volver = ctk.CTkButton(self, text="Volver al inicio", font=("Arial", 15), fg_color="gray", hover_color="darkgray", command=self.volver_inicio)
        self.button_volver.pack(pady=20)
    
    def ejecutar_algoritmo(self):
        try:
            num_procesos = int(self.num_procesos.get())
            if 1 <= num_procesos <= 10:
                self.mostrar_animacion(num_procesos)
            else:
                CTkMessagebox(title="Error", message="Ingrese un número entre 1 y 10.")
        except ValueError:
            CTkMessagebox(title="Error", message="Ingrese un número válido.")
    
    def mostrar_animacion(self, num_procesos):
        plt.figure()
        plt.plot(np.random.rand(10))
        plt.title(f"Animación con {num_procesos} procesos")
        plt.show()
    
    def volver_inicio(self):
        self.destroy()
        self.root.deiconify()
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
