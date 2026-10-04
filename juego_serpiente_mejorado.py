# =====================================================
# Juego de la Serpiente (Snake)
# Hecho en Python con tkinter y ttkbootstrap
# Instalar la librería una sola vez:  pip install ttkbootstrap
# =====================================================

import random
import tkinter as tk
import ttkbootstrap as ttk

# ---------- Constantes (valores que no cambian) ----------
TAMANO = 20                  # tamaño de cada casilla en píxeles
COLUMNAS = 30                # casillas a lo ancho
FILAS = 20                   # casillas a lo alto
ANCHO = COLUMNAS * TAMANO    # ancho del tablero: 600 px
ALTO = FILAS * TAMANO        # alto del tablero: 400 px

# ---------- Variables del juego (cambian mientras se juega) ----------
serpiente = []               # lista de casillas [columna, fila]; la primera es la cabeza
direccion = "Right"          # dirección en la que se movió por última vez
proxima = "Right"            # dirección que pidió el jugador con el teclado
comida = [0, 0]              # casilla donde está la comida
puntaje = 0
mejor_puntaje = 0
velocidad = 120              # milisegundos entre cada movimiento (menos = más rápido)
jugando = False              # True mientras dura la partida
tarea = None                 # guarda la tarea programada con after()


# ---------- Funciones ----------
def dibujar_tablero():
    """Dibuja el fondo con casillas de dos tonos de verde."""
    for columna in range(COLUMNAS):
        for fila in range(FILAS):
            if (columna + fila) % 2 == 0:
                color = "#a2d149"
            else:
                color = "#aad751"
            x = columna * TAMANO
            y = fila * TAMANO
            lienzo.create_rectangle(x, y, x + TAMANO, y + TAMANO, fill=color, outline="")


def dibujar():
    """Borra y vuelve a dibujar la comida y la serpiente."""
    lienzo.delete("juego")

    # Comida (círculo rojo)
    x = comida[0] * TAMANO
    y = comida[1] * TAMANO
    lienzo.create_oval(x + 2, y + 2, x + TAMANO - 2, y + TAMANO - 2,
                       fill="#e7471d", outline="", tags="juego")

    # Serpiente: la cabeza de azul oscuro y el cuerpo de azul claro
    for parte in serpiente:
        x = parte[0] * TAMANO
        y = parte[1] * TAMANO
        if parte == serpiente[0]:
            color = "#1e3fbf"
        else:
            color = "#4d79f6"
        lienzo.create_rectangle(x + 1, y + 1, x + TAMANO - 1, y + TAMANO - 1,
                                fill=color, outline="", tags="juego")


def nueva_comida():
    """Coloca la comida en una casilla al azar que no esté ocupada por la serpiente."""
    global comida
    while True:
        columna = random.randint(0, COLUMNAS - 1)
        fila = random.randint(0, FILAS - 1)
        comida = [columna, fila]
        if comida not in serpiente:
            break


def detener():
    """Cancela el movimiento automático de la serpiente."""
    global tarea
    if tarea is not None:
        ventana.after_cancel(tarea)
        tarea = None


def iniciar():
    """Prepara una partida nueva y la arranca."""
    global serpiente, direccion, proxima, puntaje, velocidad, jugando, tarea
    detener()
    serpiente = [[10, 10], [9, 10], [8, 10]]    # empieza con 3 partes
    direccion = "Right"
    proxima = "Right"
    puntaje = 0
    velocidad = 120
    jugando = True
    nueva_comida()
    etiqueta_puntaje.config(text="Puntaje: 0")
    etiqueta_mejor.config(text="Mejor: " + str(mejor_puntaje))
    marco_menu.pack_forget()
    marco_juego.pack()
    dibujar()
    tarea = ventana.after(velocidad, ciclo)


def mover():
    """Mueve la serpiente una casilla y revisa los choques y la comida."""
    global direccion, puntaje, mejor_puntaje, velocidad
    direccion = proxima                 # se usa la dirección pedida con el teclado

    # Se calcula la casilla a la que va la cabeza
    columna = serpiente[0][0]
    fila = serpiente[0][1]
    if direccion == "Up":
        fila = fila - 1
    elif direccion == "Down":
        fila = fila + 1
    elif direccion == "Left":
        columna = columna - 1
    elif direccion == "Right":
        columna = columna + 1
    nueva = [columna, fila]

    # Choque con los bordes del tablero
    if columna < 0 or columna >= COLUMNAS or fila < 0 or fila >= FILAS:
        terminar()
        return

    # Choque con el propio cuerpo
    if nueva in serpiente:
        terminar()
        return

    serpiente.insert(0, nueva)          # la cabeza avanza a la nueva casilla
    if nueva == comida:
        # Comió: sube el puntaje, va más rápido y aparece nueva comida
        puntaje = puntaje + 10
        if puntaje > mejor_puntaje:
            mejor_puntaje = puntaje
        if velocidad > 60:
            velocidad = velocidad - 3
        etiqueta_puntaje.config(text="Puntaje: " + str(puntaje))
        etiqueta_mejor.config(text="Mejor: " + str(mejor_puntaje))
        nueva_comida()
    else:
        serpiente.pop()                 # no comió: se quita la cola para no crecer


def ciclo():
    """Ciclo del juego: mover, dibujar y repetir cada 'velocidad' milisegundos."""
    global tarea
    mover()
    if jugando:
        dibujar()
        tarea = ventana.after(velocidad, ciclo)


def terminar():
    """Se llama cuando el jugador pierde: muestra GAME OVER."""
    global jugando
    jugando = False
    lienzo.create_rectangle(ANCHO // 2 - 150, ALTO // 2 - 70, ANCHO // 2 + 150, ALTO // 2 + 70,
                            fill="#14213d", outline="white", width=3, tags="juego")
    lienzo.create_text(ANCHO // 2, ALTO // 2 - 25, text="GAME OVER",
                       fill="#ff6b6b", font=("Helvetica", 30, "bold"), tags="juego")
    lienzo.create_text(ANCHO // 2, ALTO // 2 + 30, text="Puntaje: " + str(puntaje),
                       fill="white", font=("Helvetica", 18), tags="juego")


def mostrar_menu():
    """Vuelve a la pantalla del menú."""
    global jugando
    jugando = False
    detener()
    etiqueta_menu_mejor.config(text="Mejor puntaje: " + str(mejor_puntaje))
    marco_juego.pack_forget()
    marco_menu.pack(fill="both", expand=True)


def tecla(evento):
    """Lee las flechas o WASD. No permite dar la vuelta de 180 grados."""
    global proxima
    letra = evento.keysym
    if letra in ("Up", "w", "W") and direccion != "Down":
        proxima = "Up"
    if letra in ("Down", "s", "S") and direccion != "Up":
        proxima = "Down"
    if letra in ("Left", "a", "A") and direccion != "Right":
        proxima = "Left"
    if letra in ("Right", "d", "D") and direccion != "Left":
        proxima = "Right"


# ---------- Ventana principal ----------
ventana = ttk.Window(title="Snake - Juego de la Serpiente", themename="darkly")
ventana.geometry("660x600")
ventana.resizable(False, False)

# ---------- Pantalla del menú ----------
marco_menu = ttk.Frame(ventana, padding=30)

ttk.Label(marco_menu, text="SNAKE", font=("Helvetica", 56, "bold"),
          bootstyle="success").pack(pady=(40, 0))
ttk.Label(marco_menu, text="El juego de la serpiente",
          font=("Helvetica", 14)).pack(pady=(0, 40))
ttk.Button(marco_menu, text="JUGAR", bootstyle="success", width=20,
           command=iniciar).pack(pady=10, ipady=8)
ttk.Button(marco_menu, text="SALIR", bootstyle="danger-outline", width=20,
           command=ventana.destroy).pack(pady=10, ipady=4)
etiqueta_menu_mejor = ttk.Label(marco_menu, text="Mejor puntaje: 0",
                                font=("Helvetica", 14, "bold"), bootstyle="warning")
etiqueta_menu_mejor.pack(pady=30)
ttk.Label(marco_menu, text="Mueve la serpiente con las flechas o con W, A, S, D",
          font=("Helvetica", 10)).pack()

# ---------- Pantalla del juego ----------
marco_juego = ttk.Frame(ventana, padding=10)

barra = ttk.Frame(marco_juego)
barra.pack(fill="x", pady=(0, 10))
etiqueta_puntaje = ttk.Label(barra, text="Puntaje: 0", font=("Helvetica", 15, "bold"),
                             bootstyle="inverse-success", anchor="center", padding=8)
etiqueta_puntaje.pack(side="left", expand=True, fill="x", padx=(0, 5))
etiqueta_mejor = ttk.Label(barra, text="Mejor: 0", font=("Helvetica", 15, "bold"),
                           bootstyle="inverse-warning", anchor="center", padding=8)
etiqueta_mejor.pack(side="left", expand=True, fill="x", padx=(5, 0))

lienzo = tk.Canvas(marco_juego, width=ANCHO, height=ALTO, highlightthickness=0)
lienzo.pack()
dibujar_tablero()

botones = ttk.Frame(marco_juego)
botones.pack(pady=15)
ttk.Button(botones, text="Jugar de nuevo", bootstyle="success", width=16,
           command=iniciar).pack(side="left", padx=8)
ttk.Button(botones, text="Menú", bootstyle="light-outline", width=16,
           command=mostrar_menu).pack(side="left", padx=8)

# ---------- Inicio del programa ----------
ventana.bind("<Key>", tecla)    # cada tecla presionada llama a la función tecla()
mostrar_menu()
ventana.mainloop()
