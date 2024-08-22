import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

class UltronCarpetApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Bienvenidos a Ultron Carpet')
        self.root.geometry('500x400')  # Tamaño inicial de la ventana

        # Ruta de destino inicial (vacía)
        self.ruta_base = ''

        # Lista de frames para los campos y botones de eliminar
        self.frames_campos = []
        self.campos = []

        # Crear el canvas y la barra de desplazamiento
        self.canvas = tk.Canvas(root)
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Crear un frame dentro del canvas para contener los widgets
        self.frame_canvas = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame_canvas, anchor="nw")

        # Actualizar el tamaño del canvas cuando cambie el contenido
        self.frame_canvas.bind("<Configure>", self.on_frame_configure)

        # Crear los widgets de la interfaz
        self.crear_widgets()

    def crear_widgets(self):
        # Etiqueta de bienvenida
        ttk.Label(self.frame_canvas, text='Bienvenidos a Ultron Carpet', font=('Arial', 18)).pack(pady=10)

        # Frame principal para los campos y botones de eliminar
        self.frame_campos = tk.Frame(self.frame_canvas)
        self.frame_campos.pack(pady=10, fill='both', expand=True)

        # Agregar el primer campo
        self.agregar_campo()

        # Botón para agregar más campos
        ttk.Button(self.frame_canvas, text='Agregar Carpeta', command=self.agregar_campo).pack(pady=5)

        # Botón para seleccionar ruta
        ttk.Button(self.frame_canvas, text='Seleccionar Ruta', command=self.seleccionar_ruta).pack(pady=10)

        # Botón para crear carpetas
        ttk.Button(self.frame_canvas, text='Crear Carpetas', command=self.crear_carpetas).pack(pady=10)

    def on_frame_configure(self, event):
        # Actualizar el tamaño del canvas al cambiar el tamaño del frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def agregar_campo(self):
        # Crear un frame para el campo y el botón de eliminar
        frame_campo = tk.Frame(self.frame_campos, borderwidth=1, relief='solid')
        frame_campo.pack(pady=5, fill='x', padx=10)

        # Campo de entrada con placeholder
        campo = tk.Entry(frame_campo, width=40, font=('Arial', 12))
        campo.pack(side='left', padx=5, pady=5)
        campo.insert(0, 'Nombre de Carpeta')
        campo.bind("<FocusIn>", lambda e: self.eliminar_placeholder(campo))
        campo.bind("<FocusOut>", lambda e: self.agregar_placeholder(campo))
        campo.config(fg='gray')

        # Botón para eliminar el campo
        boton_eliminar = ttk.Button(frame_campo, text='Eliminar', command=lambda: self.eliminar_campo(frame_campo))
        boton_eliminar.pack(side='right', padx=5, pady=5)

        # Añadir a las listas
        self.frames_campos.append(frame_campo)
        self.campos.append(campo)

    def eliminar_placeholder(self, campo):
        # Eliminar el placeholder cuando se hace clic
        if campo.get() == 'Nombre de Carpeta':
            campo.delete(0, tk.END)
            campo.config(fg='black')  # Cambiar el color del texto a negro

    def agregar_placeholder(self, campo):
        # Añadir el placeholder si el campo está vacío
        if campo.get() == '':
            campo.insert(0, 'Nombre de Carpeta')
            campo.config(fg='gray')  # Cambiar el color del texto a gris

    def eliminar_campo(self, frame_campo):
        # Eliminar el frame y el campo asociado
        if frame_campo in self.frames_campos:
            self.frames_campos.remove(frame_campo)
            for campo in self.campos:
                if campo.master == frame_campo:
                    self.campos.remove(campo)
                    break
            frame_campo.destroy()

    def seleccionar_ruta(self):
        # Diálogo para seleccionar la ruta
        self.ruta_base = filedialog.askdirectory()
        if not self.ruta_base:
            messagebox.showwarning("Advertencia", "No se ha seleccionado ninguna ruta.")

    def crear_carpetas(self):
        if not self.ruta_base:
            messagebox.showwarning("Advertencia", "Primero selecciona una ruta.")
            return

        nombres_carpetas = [campo.get().strip() for campo in self.campos]
        # Eliminar nombres vacíos
        nombres_carpetas = [nombre for nombre in nombres_carpetas if nombre]

        if not nombres_carpetas:
            messagebox.showwarning("Advertencia", "Introduce al menos un nombre de carpeta.")
            return

        # Crear carpetas
        for nombre in nombres_carpetas:
            ruta_completa = os.path.join(self.ruta_base, nombre)
            try:
                os.makedirs(ruta_completa, exist_ok=True)
                print(f'Carpeta creada: {ruta_completa}')
                # Mostrar mensaje de éxito después de un pequeño retardo
                self.root.after(500, lambda: messagebox.showinfo("Éxito", "Las carpetas se han creado correctamente."))
            except Exception as e:
                messagebox.showerror("Error", f'Error al crear la carpeta {ruta_completa}: {e}')

# Configurar la ventana principal
root = tk.Tk()
app = UltronCarpetApp(root)
root.mainloop()
