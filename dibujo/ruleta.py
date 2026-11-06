import tkinter as tk
import random
import numpy as np  # ¡Esta línea faltaba!


class Ruleta:
    def __init__(self, root):
        self.root = root
        self.root.title("Ruleta de Apuestas")
        self.saldo = 1000
        self.colores_ruleta = {
            0: 'green',
            1: 'red', 3: 'red', 5: 'red', 7: 'red', 9: 'red', 12: 'red',
            14: 'red', 16: 'red', 18: 'red', 19: 'red', 21: 'red', 23: 'red',
            25: 'red', 27: 'red', 30: 'red', 32: 'red', 34: 'red', 36: 'red',
            2: 'black', 4: 'black', 6: 'black', 8: 'black', 10: 'black',
            11: 'black', 13: 'black', 15: 'black', 17: 'black', 20: 'black',
            22: 'black', 24: 'black', 26: 'black', 28: 'black', 29: 'black',
            31: 'black', 33: 'black', 35: 'black'
        }

        self.crear_interfaz()

    def crear_interfaz(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        self.label_saldo = tk.Label(
            self.root, text=f"Saldo: ${self.saldo}", font=('Arial', 14))
        self.label_saldo.pack()

        self.boton_rojo = tk.Button(self.root, text="Apuesta Rojo ($100)",
                                    command=lambda: self.apostar('red'), bg='red', fg='white')
        self.boton_rojo.pack(pady=10)

        self.boton_negro = tk.Button(self.root, text="Apuesta Negro ($100)",
                                     command=lambda: self.apostar('black'), bg='black', fg='white')
        self.boton_negro.pack(pady=10)

        self.boton_girar = tk.Button(
            self.root, text="Girar Ruleta", command=self.girar_ruleta, bg='darkgreen', fg='white')
        self.boton_girar.pack(pady=20)

        self.label_resultado = tk.Label(self.root, text="", font=('Arial', 16))
        self.label_resultado.pack()

        self.canvas = tk.Canvas(self.root, width=300, height=300, bg='white')
        self.canvas.pack()
        self.dibujar_ruleta()

    def dibujar_ruleta(self):
        self.canvas.delete("all")
        for i in range(37):
            angulo = 360/37 * i
            color = self.colores_ruleta.get(i, 'green')
            self.canvas.create_arc(
                50, 50, 250, 250, start=angulo, extent=360/37, fill=color)
            self.canvas.create_text(150 + 100 * np.cos(np.radians(angulo + 360/74)),
                                    150 + 100 *
                                    np.sin(np.radians(angulo + 360/74)),
                                    text=str(i), fill='white' if color == 'black' else 'black')

    def apostar(self, color):
        if self.saldo >= 100:
            self.saldo -= 100
            self.label_saldo.config(text=f"Saldo: ${self.saldo}")
            self.apuesta_actual = color
            self.label_resultado.config(
                text=f"Apuesta a {color.upper()} confirmada")
        else:
            self.label_resultado.config(text="Saldo insuficiente")

    def girar_ruleta(self):
        if hasattr(self, 'apuesta_actual'):
            numero = random.randint(0, 36)
            color = self.colores_ruleta[numero]
            self.label_resultado.config(
                text=f"Resultado: {numero} - {color.upper()}")

            if color == self.apuesta_actual:
                self.saldo += 200
                self.label_saldo.config(text=f"Saldo: ${self.saldo}")
                self.label_resultado.config(
                    text=f"Ganaste! +$100 (Total: {numero} - {color.upper()})")

            self.dibujar_ruleta()
            self.canvas.create_oval(120, 120, 180, 180, fill='gold')
            self.canvas.create_text(
                150, 150, text=str(numero), font=('Arial', 16))
        else:
            self.label_resultado.config(text="Haz una apuesta primero")


if __name__ == "__main__":
    root = tk.Tk()
    juego = Ruleta(root)
    root.mainloop()
