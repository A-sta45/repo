import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import ttk
import math


class Estado:
    def __init__(self, canvas, nombre, x, y, radio=30):
        self.canvas = canvas
        self.nombre = nombre
        self.x = x
        self.y = y
        self.radio = radio
        self.es_inicial = False
        self.es_final = False
        self.arrastrando = False

        self.circulo = canvas.create_oval(
            x - radio, y - radio, x + radio, y + radio, fill='#fff', outline='#333', width=2)
        self.texto = canvas.create_text(
            x, y, text=nombre, font=("Segoe UI", 12, "bold"), fill="#000")

        self.vincular_eventos()

    def vincular_eventos(self):
        for elemento in [self.circulo, self.texto]:
            self.canvas.tag_bind(
                elemento, '<ButtonPress-1>', self.al_presionar)
            self.canvas.tag_bind(elemento, '<B1-Motion>', self.al_arrastrar)
            self.canvas.tag_bind(elemento, '<ButtonRelease-1>', self.al_soltar)

    def al_presionar(self, evento):
        self.arrastrando = True
        self.dx = self.x - evento.x
        self.dy = self.y - evento.y

    def al_arrastrar(self, evento):
        if self.arrastrando:
            self.x = evento.x + self.dx
            self.y = evento.y + self.dy
            self.canvas.coords(self.circulo, self.x - self.radio, self.y - self.radio,
                               self.x + self.radio, self.y + self.radio)
            self.canvas.coords(self.texto, self.x, self.y)
            self.canvas.event_generate("<Motion>")

    def al_soltar(self, evento):
        self.arrastrando = False


class Transicion:
    def __init__(self, canvas, origen, destino, simbolo):
        self.canvas = canvas
        self.origen = origen
        self.destino = destino
        self.simbolo = simbolo
        self.linea = None
        self.etiqueta = None
        self.dibujar()

    def dibujar(self):
        if self.linea:
            self.canvas.delete(self.linea)
            self.canvas.delete(self.etiqueta)

        dx = self.destino.x - self.origen.x
        dy = self.destino.y - self.origen.y
        distancia = math.hypot(dx, dy) or 0.01
        offset_x = dx / distancia * self.origen.radio
        offset_y = dy / distancia * self.origen.radio

        x_ini = self.origen.x + offset_x
        y_ini = self.origen.y + offset_y
        x_fin = self.destino.x - offset_x
        y_fin = self.destino.y - offset_y

        x_ctrl = (x_ini + x_fin) / 2 - dy * 0.3
        y_ctrl = (y_ini + y_fin) / 2 + dx * 0.3

        self.linea = self.canvas.create_line(
            x_ini, y_ini, x_ctrl, y_ctrl, x_fin, y_fin, smooth=True, arrow=tk.LAST, width=2)
        self.etiqueta = self.canvas.create_text(
            x_ctrl, y_ctrl, text=self.simbolo, font=('Segoe UI', 11, 'bold'), fill="#000")


class SimuladorAutomata:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Autómatas Finito")

        self.top_bar = tk.Frame(root, bg="#2c3e50", height=40)
        self.top_bar.pack(fill=tk.X)
        self.modo = tk.StringVar(value="AFD")

        tk.Label(self.top_bar, text="Modo:", fg="white", bg="#2c3e50",
                 font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=5)
        self.switch = ttk.Checkbutton(self.top_bar, text="AFND", variable=self.modo,
                                      onvalue="AFND", offvalue="AFD", command=self.actualizar_modo)
        self.switch.pack(side=tk.LEFT)
        self.mensaje_modo = tk.Label(self.top_bar, text="Modo AFD: solo una transición por símbolo desde un estado.",
                                     fg="lightgray", bg="#2c3e50", font=("Segoe UI", 10))
        self.mensaje_modo.pack(side=tk.LEFT, padx=20)

        self.panel = tk.Frame(root, bg="#ecf0f1")
        self.panel.pack(side=tk.LEFT, fill=tk.Y)

        self.canvas = tk.Canvas(root, bg='white', width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Motion>", self.redibujar_transiciones)
        self.canvas.bind("<Button-1>", self.crear_estado_si_corresponde)

        self.estados = []
        self.transiciones = []
        self.estado_inicial = None
        self.estado_pendiente = False
        self.alfabeto = set()

        self.btn_agregar_estado = tk.Button(self.panel, text="Agregar Estado", bg="#2980b9", fg="white",
                                            command=self.habilitar_agregar_estado)
        self.btn_agregar_estado.pack(pady=5, fill=tk.X)

        self.label_click = tk.Label(self.canvas, text="", fg="gray", bg="white",
                                    font=("Segoe UI", 10, "italic"))
        self.label_click_id = None

        self.btn_transicion = tk.Button(self.panel, text="Agregar Transición", bg="#3498db", fg="white",
                                        command=self.ventana_transicion)
        self.btn_transicion.pack(pady=5, fill=tk.X)

        self.btn_alfabeto = tk.Button(
            self.panel, text="Definir Alfabeto", bg="#8e44ad", fg="white", command=self.definir_alfabeto)
        self.btn_alfabeto.pack(pady=5, fill=tk.X)

        self.btn_simular = tk.Button(
            self.panel, text="Simular Cadena", bg="#c0392b", fg="white", command=self.simular_cadena)
        self.btn_simular.pack(pady=5, fill=tk.X)

        self.btn_inicial = tk.Button(self.panel, text="Definir Estado Inicial", bg="#27ae60", fg="white",
                                     command=self.definir_estado_inicial)
        self.btn_inicial.pack(pady=5, fill=tk.X)

        self.btn_final = tk.Button(self.panel, text="Definir Estado Final", bg="#e67e22", fg="white",
                                   command=self.definir_estado_final)
        self.btn_final.pack(pady=5, fill=tk.X)

    def actualizar_modo(self):
        modo = self.modo.get()
        if modo == "AFD":
            self.mensaje_modo.config(
                text="Modo AFD: solo una transición por símbolo desde un estado.")
        else:
            self.mensaje_modo.config(
                text="Modo AFND: se permiten múltiples transiciones por símbolo o con ε (delta).")

    def redibujar_transiciones(self, event):
        for trans in self.transiciones:
            trans.dibujar()

    def habilitar_agregar_estado(self):
        self.estado_pendiente = True
        self.mostrar_mensaje_temporal(
            "Haz clic en el canvas para agregar un estado")

    def mostrar_mensaje_temporal(self, mensaje):
        self.label_click.config(text=mensaje)
        if self.label_click_id:
            self.canvas.delete(self.label_click_id)
        self.label_click_id = self.canvas.create_window(
            400, 20, window=self.label_click)
        self.root.after(3000, lambda: self.label_click.config(text=""))

    def crear_estado_si_corresponde(self, evento):
        if self.estado_pendiente:
            nombre = simpledialog.askstring(
                "Nombre del Estado", "Ingrese el nombre del nuevo estado:")
            if nombre:
                estado = Estado(self.canvas, nombre, evento.x, evento.y)
                self.estados.append(estado)
            self.estado_pendiente = False

    def ventana_transicion(self):
        if len(self.estados) < 2:
            messagebox.showwarning(
                "Advertencia", "Debes tener al menos dos estados para crear una transición.")
            return

        simbolo = simpledialog.askstring(
            "Símbolo", "Ingrese el símbolo de transición (usa ε para delta):")
        if simbolo is None:
            return
        if simbolo == "ε":
            simbolo = "δ"

        nombre_origen = simpledialog.askstring(
            "Estado Origen", "Nombre del estado origen:")
        nombre_destino = simpledialog.askstring(
            "Estado Destino", "Nombre del estado destino:")

        origen = next(
            (e for e in self.estados if e.nombre == nombre_origen), None)
        destino = next(
            (e for e in self.estados if e.nombre == nombre_destino), None)

        if not origen or not destino:
            messagebox.showerror(
                "Error", "Estado origen o destino no encontrado.")
            return

        if self.modo.get() == "AFD":
            for t in self.transiciones:
                if t.origen == origen and t.simbolo == simbolo:
                    messagebox.showerror(
                        "Error", "En AFD no se permiten múltiples transiciones con el mismo símbolo desde un estado.")
                    return

        trans = Transicion(self.canvas, origen, destino, simbolo)
        self.transiciones.append(trans)
        self.alfabeto.add(simbolo)

    def definir_alfabeto(self):
        entrada = simpledialog.askstring(
            "Alfabeto", "Ingrese los símbolos separados por coma:")
        if entrada:
            self.alfabeto = set(s.strip() for s in entrada.split(","))
            messagebox.showinfo("Alfabeto definido",
                                f"Símbolos: {', '.join(self.alfabeto)}")

    def definir_estado_inicial(self):
        nombre = simpledialog.askstring(
            "Estado Inicial", "Nombre del estado inicial:")
        for e in self.estados:
            e.es_inicial = False
        for e in self.estados:
            if e.nombre == nombre:
                e.es_inicial = True
                self.estado_inicial = e
                messagebox.showinfo(
                    "Estado Inicial", f"El estado inicial es {nombre}.")
                return
        messagebox.showerror("Error", "Estado no encontrado.")

    def definir_estado_final(self):
        nombre = simpledialog.askstring(
            "Estado Final", "Nombre del estado final:")
        for e in self.estados:
            if e.nombre == nombre:
                e.es_final = True
                messagebox.showinfo(
                    "Estado Final", f"Estado final añadido: {nombre}.")
                return
        messagebox.showerror("Error", "Estado no encontrado.")

    def simular_cadena(self):
        cadena = simpledialog.askstring(
            "Simulación", "Ingrese la cadena a evaluar:")
        if not cadena:
            return
        # Simulación simplificada:
        if not self.estado_inicial:
            messagebox.showerror(
                "Error", "No se ha definido el estado inicial.")
            return
        actual = self.estado_inicial
        for simbolo in cadena:
            transiciones = [
                t for t in self.transiciones if t.origen == actual and t.simbolo == simbolo]
            if not transiciones:
                messagebox.showinfo(
                    "Resultado", f"Cadena rechazada. No hay transición con símbolo '{simbolo}' desde {actual.nombre}.")
                return
            actual = transiciones[0].destino
        if actual.es_final:
            messagebox.showinfo("Resultado", "Cadena aceptada.")
        else:
            messagebox.showinfo(
                "Resultado", "Cadena rechazada. No se llegó a un estado final.")


if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorAutomata(root)
    root.mainloop()