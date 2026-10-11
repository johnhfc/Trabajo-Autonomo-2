import random
import tkinter as tk
import ttkbootstrap as ttk

# ---------------------------------------------------------------
# 1. CONSTANTES
# ---------------------------------------------------------------
CELDA = 25                    # tamaño de cada casilla en píxeles
COLUMNAS = 24
FILAS = 18
ANCHO = COLUMNAS * CELDA      # 600 px
ALTO = FILAS * CELDA          # 450 px

# Milisegundos entre movimientos (menos = más rápido)
RETRASOS = {"facil": 150, "normal": 110, "dificil": 80}
RETRASO_MINIMO = 50
ARCHIVO_RECORD = "mejor_puntaje.txt"


# Colores del tablero y de la serpiente
COLOR_CASILLA_1 = "#a2d149"
COLOR_CASILLA_2 = "#aad751"
COLOR_CABEZA = "#1e3fbf"
COLOR_CUERPO_INICIO = "#4d79f6"
COLOR_CUERPO_FIN = "#86b6ff"
COLOR_MANZANA = "#e7471d"
COLOR_MANZANA_BORDE = "#a82a0c"
COLOR_ORO = "#ffd700"
COLOR_ORO_BORDE = "#b8860b"

# Direcciones: (cambio en columna, cambio en fila)
DIRECCIONES = {
    "up": (0, -1), "w": (0, -1),
    "down": (0, 1), "s": (0, 1),
    "left": (-1, 0), "a": (-1, 0),
    "right": (1, 0), "d": (1, 0),
}

# ---------------------------------------------------------------
# 2. VARIABLES DEL JUEGO
# ---------------------------------------------------------------
estado = "menu"          # "menu", "jugando", "pausa" o "game_over"
serpiente = []           # lista de casillas (columna, fila); la cabeza es la primera
direccion = (0, 0)       # hacia dónde se quiere ir ((0, 0) = todavía quieta)
dir_movida = (1, 0)      # última dirección en la que realmente se movió
comida = (0, 0)
comida_dorada = False
puntaje = 0
mejor_puntaje = 0
nuevo_record = False
retraso = RETRASOS["normal"]
tarea = None             # identificador del "after" que repite el juego


# ---------------------------------------------------------------
# 3. RÉCORD EN ARCHIVO
# ---------------------------------------------------------------
def cargar_mejor():
    """Lee el mejor puntaje del archivo (0 si todavía no existe)."""
    try:
        with open(ARCHIVO_RECORD, "r") as archivo:
            return int(archivo.read())
    except (FileNotFoundError, ValueError):
        return 0


def guardar_mejor():
    """Guarda el mejor puntaje en el archivo."""
    try:
        with open(ARCHIVO_RECORD, "w") as archivo:
            archivo.write(str(mejor_puntaje))
    except OSError:
        pass


mejor_puntaje = cargar_mejor()


# ---------------------------------------------------------------
# 4. FUNCIONES DE DIBUJO (sirven para cualquier canvas)
# ---------------------------------------------------------------
def mezclar(color1, color2, t):
    """Devuelve un color intermedio entre color1 y color2 (t va de 0 a 1)."""
    r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
    r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    return f"#{r:02x}{g:02x}{b:02x}"


def rect_redondeado(canvas, x1, y1, x2, y2, radio, **opciones):
    """Dibuja un rectángulo con esquinas redondeadas."""
    puntos = [x1 + radio, y1, x1 + radio, y1, x2 - radio, y1, x2 - radio, y1,
              x2, y1, x2, y1 + radio, x2, y1 + radio, x2, y2 - radio,
              x2, y2 - radio, x2, y2, x2 - radio, y2, x2 - radio, y2,
              x1 + radio, y2, x1 + radio, y2, x1, y2, x1, y2 - radio,
              x1, y2 - radio, x1, y1 + radio, x1, y1 + radio, x1, y1]
    return canvas.create_polygon(puntos, smooth=True, **opciones)


def celda(columna, fila):
    """Devuelve las esquinas en píxeles de una casilla."""
    x1 = columna * CELDA
    y1 = fila * CELDA
    return x1, y1, x1 + CELDA, y1 + CELDA


def dibujar_tablero(canvas, columnas, filas):
    """Dibuja el fondo de cuadrícula con dos tonos de verde."""
    for columna in range(columnas):
        for fila in range(filas):
            if (columna + fila) % 2 == 0:
                color = COLOR_CASILLA_1
            else:
                color = COLOR_CASILLA_2
            x1, y1, x2, y2 = celda(columna, fila)
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")


def dibujar_segmento(canvas, columna, fila, color, etiqueta):
    """Dibuja una parte del cuerpo de la serpiente."""
    x1, y1, x2, y2 = celda(columna, fila)
    rect_redondeado(canvas, x1 + 2, y1 + 2, x2 - 2, y2 - 2, 8,
                    fill=color, outline="", tags=etiqueta)


def dibujar_cabeza(canvas, columna, fila, mirando, etiqueta):
    """Dibuja la cabeza con dos ojos que miran hacia donde avanza."""
    x1, y1, x2, y2 = celda(columna, fila)
    rect_redondeado(canvas, x1 + 1, y1 + 1, x2 - 1, y2 - 1, 9,
                    fill=COLOR_CABEZA, outline="", tags=etiqueta)

    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    fx, fy = mirando        # hacia adelante
    px, py = -fy, fx        # hacia el costado
    for lado in (-1, 1):
        ex = cx + fx * 5 + px * lado * 6
        ey = cy + fy * 5 + py * lado * 6
        canvas.create_oval(ex - 4, ey - 4, ex + 4, ey + 4,
                           fill="white", outline="", tags=etiqueta)
        canvas.create_oval(ex + fx * 1.5 - 2, ey + fy * 1.5 - 2,
                           ex + fx * 1.5 + 2, ey + fy * 1.5 + 2,
                           fill="#101010", outline="", tags=etiqueta)


def dibujar_serpiente(canvas, cuerpo, mirando, etiqueta):
    """Dibuja el cuerpo con degradado (de atrás hacia adelante) y la cabeza."""
    total = len(cuerpo)
    for i in range(total - 1, 0, -1):
        color = mezclar(COLOR_CUERPO_INICIO, COLOR_CUERPO_FIN, i / total)
        dibujar_segmento(canvas, cuerpo[i][0], cuerpo[i][1], color, etiqueta)
    dibujar_cabeza(canvas, cuerpo[0][0], cuerpo[0][1], mirando, etiqueta)


def dibujar_manzana(canvas, columna, fila, dorada, etiqueta):
    """Dibuja la comida: manzana roja o manzana dorada."""
    x1, y1, x2, y2 = celda(columna, fila)
    if dorada:
        relleno, borde = COLOR_ORO, COLOR_ORO_BORDE
    else:
        relleno, borde = COLOR_MANZANA, COLOR_MANZANA_BORDE
    cx = (x1 + x2) / 2
    canvas.create_oval(x1 + 3, y1 + 5, x2 - 3, y2 - 2, fill=relleno,
                       outline=borde, width=2, tags=etiqueta)
    canvas.create_oval(x1 + 7, y1 + 9, x1 + 11, y1 + 13, fill="white",
                       outline="", tags=etiqueta)                     # brillo
    canvas.create_line(cx, y1 + 6, cx + 1, y1 + 1, fill="#5d4037",
                       width=2, tags=etiqueta)                        # tallo
    canvas.create_oval(cx + 1, y1 + 1, cx + 8, y1 + 6, fill="#2e7d32",
                       outline="", tags=etiqueta)                     # hoja


# ---------------------------------------------------------------
# 5. VENTANA PRINCIPAL
# ---------------------------------------------------------------
ventana = ttk.Window(title="Snake - Juego de la Serpiente", themename="darkly",
                     size=(680, 700), resizable=(False, False))
ventana.place_window_center()

dificultad_var = tk.StringVar(value="normal")


def aplicar_estilos():
    """Letra más grande para botones (se repite al cambiar de tema)."""
    ventana.style.configure("TButton", font=("Helvetica", 12, "bold"))
    ventana.style.configure("Toolbutton", font=("Helvetica", 11, "bold"))


aplicar_estilos()

# ---------------------------------------------------------------
# 6. PANTALLA DEL MENÚ
# ---------------------------------------------------------------
marco_menu = ttk.Frame(ventana, padding=20)

ttk.Label(marco_menu, text="SNAKE", font=("Helvetica", 56, "bold"),
          bootstyle="success").pack(pady=(10, 0))
ttk.Label(marco_menu, text="El juego de la serpiente",
          font=("Helvetica", 14), bootstyle="light").pack(pady=(0, 15))

# Banner decorativo: una serpiente persiguiendo una manzana
banner = tk.Canvas(marco_menu, width=16 * CELDA, height=3 * CELDA,
                   highlightthickness=0)
banner.pack(pady=(0, 20))
dibujar_tablero(banner, 16, 3)
dibujar_manzana(banner, 12, 1, False, "deco")
dibujar_serpiente(banner, [(9, 1), (8, 1), (7, 1), (6, 1), (5, 1), (4, 1), (3, 1)],
                  (1, 0), "deco")

# Elegir dificultad
caja_dificultad = ttk.Labelframe(marco_menu, text=" Dificultad ", padding=12,
                                 bootstyle="success")
caja_dificultad.pack(pady=(0, 12))
for texto, valor in (("Fácil", "facil"), ("Normal", "normal"), ("Difícil", "dificil")):
    ttk.Radiobutton(caja_dificultad, text=texto, value=valor,
                    variable=dificultad_var, width=9,
                    bootstyle="success-outline-toolbutton").pack(side="left", padx=5)

# Elegir tema (colores de toda la interfaz)


# Botones principales (comando se asigna más abajo, cuando existan las funciones)
boton_jugar = ttk.Button(marco_menu, text="JUGAR", bootstyle="success", width=24)
boton_jugar.pack(pady=(5, 8), ipady=8)
boton_salir = ttk.Button(marco_menu, text="SALIR", bootstyle="danger-outline", width=24)
boton_salir.pack(ipady=4)

etq_menu_record = ttk.Label(marco_menu, text="", font=("Helvetica", 14, "bold"),
                            bootstyle="warning")
etq_menu_record.pack(pady=(18, 4))
ttk.Label(marco_menu, text="Enter: jugar   |   1, 2, 3: dificultad   |   Esc: salir",
          font=("Helvetica", 9), bootstyle="light").pack()

# ---------------------------------------------------------------
# 7. PANTALLA DEL JUEGO
# ---------------------------------------------------------------
marco_juego = ttk.Frame(ventana, padding=15)

# Barra superior con las estadísticas
barra = ttk.Frame(marco_juego)
barra.pack(fill="x", pady=(0, 8))
estilo_etiqueta = {"font": ("Helvetica", 15, "bold"), "anchor": "center", "padding": (10, 8)}
etq_puntaje = ttk.Label(barra, text="PUNTAJE  0", bootstyle="inverse-success", **estilo_etiqueta)
etq_nivel = ttk.Label(barra, text="NIVEL  1", bootstyle="inverse-info", **estilo_etiqueta)
etq_mejor = ttk.Label(barra, text="MEJOR  0", bootstyle="inverse-warning", **estilo_etiqueta)
etq_puntaje.pack(side="left", expand=True, fill="x", padx=(0, 6))
etq_nivel.pack(side="left", expand=True, fill="x", padx=6)
etq_mejor.pack(side="left", expand=True, fill="x", padx=(6, 0))

# Barra de progreso hacia el siguiente nivel
progreso = ttk.Progressbar(marco_juego, maximum=50, value=0,
                           bootstyle="success-striped")
progreso.pack(fill="x", pady=(0, 10))

# Tablero: un canvas dentro de un marco de color
marco_canvas = ttk.Frame(marco_juego, padding=4, bootstyle="success")
marco_canvas.pack()
canvas = tk.Canvas(marco_canvas, width=ANCHO, height=ALTO, highlightthickness=0)
canvas.pack()
dibujar_tablero(canvas, COLUMNAS, FILAS)

# Botones inferiores
fila_botones = ttk.Frame(marco_juego)
fila_botones.pack(pady=(12, 4))
boton_pausa = ttk.Button(fila_botones, text="Pausa (P)", bootstyle="warning-outline", width=14)
boton_pausa.pack(side="left", padx=6)
boton_menu = ttk.Button(fila_botones, text="Menú (Esc)", bootstyle="light-outline", width=14)
boton_menu.pack(side="left", padx=6)
ttk.Label(marco_juego, text="Flechas o WASD para moverte", font=("Helvetica", 9),
          bootstyle="light").pack()


# ---------------------------------------------------------------
# 8. PANELES SOBRE EL TABLERO (pausa y game over)
# ---------------------------------------------------------------
def crear_panel():
    """Crea un panel con borde de color; devuelve (panel_externo, contenido)."""
    externo = ttk.Frame(marco_juego, padding=3, bootstyle="success")
    interno = ttk.Frame(externo, padding=30)
    interno.pack()
    return externo, interno


panel_pausa, contenido_pausa = crear_panel()
ttk.Label(contenido_pausa, text="PAUSA", font=("Helvetica", 34, "bold"),
          bootstyle="warning").pack(pady=(0, 15))
boton_continuar = ttk.Button(contenido_pausa, text="CONTINUAR", bootstyle="success", width=20)
boton_continuar.pack(pady=4, ipady=4)
boton_pausa_menu = ttk.Button(contenido_pausa, text="MENÚ", bootstyle="light-outline", width=20)
boton_pausa_menu.pack(pady=4)

panel_fin, contenido_fin = crear_panel()
ttk.Label(contenido_fin, text="GAME OVER", font=("Helvetica", 34, "bold"),
          bootstyle="danger").pack(pady=(0, 10))
etq_fin_puntaje = ttk.Label(contenido_fin, text="", font=("Helvetica", 18, "bold"))
etq_fin_puntaje.pack()
etq_fin_record = ttk.Label(contenido_fin, text="", font=("Helvetica", 14, "bold"),
                           bootstyle="light")
etq_fin_record.pack(pady=(4, 15))
boton_reintentar = ttk.Button(contenido_fin, text="JUGAR DE NUEVO", bootstyle="success", width=20)
boton_reintentar.pack(pady=4, ipady=4)
boton_fin_menu = ttk.Button(contenido_fin, text="MENÚ", bootstyle="light-outline", width=20)
boton_fin_menu.pack(pady=4)


def mostrar_panel(panel):
    """Muestra un panel en el centro del tablero."""
    panel.place(in_=marco_canvas, relx=0.5, rely=0.5, anchor="center")
    panel.lift()


def ocultar_paneles():
    panel_pausa.place_forget()
    panel_fin.place_forget()


# ---------------------------------------------------------------
# 9. LÓGICA DEL JUEGO
# ---------------------------------------------------------------
def actualizar_estadisticas():
    """Actualiza las etiquetas de la barra superior."""
    nivel = 1 + puntaje // 50
    etq_puntaje.configure(text=f"PUNTAJE  {puntaje}")
    etq_nivel.configure(text=f"NIVEL  {nivel}")
    etq_mejor.configure(text=f"MEJOR  {max(puntaje, mejor_puntaje)}")
    progreso.configure(value=puntaje % 50)


def redibujar():
    """Borra lo que hay de la partida y lo vuelve a dibujar."""
    canvas.delete("juego")

    # Mensaje de inicio (se dibuja primero para quedar debajo de todo)
    if direccion == (0, 0) and estado == "jugando":
        rect_redondeado(canvas, ANCHO / 2 - 200, ALTO - 75, ANCHO / 2 + 200, ALTO - 25,
                        14, fill="#14213d", outline="", tags="juego")
        canvas.create_text(ANCHO / 2, ALTO - 50, text="Presiona una flecha o WASD para comenzar",
                           fill="white", font=("Helvetica", 13, "bold"), tags="juego")

    dibujar_manzana(canvas, comida[0], comida[1], comida_dorada, "juego")
    dibujar_serpiente(canvas, serpiente, dir_movida, "juego")


def colocar_comida():
    """Elige una casilla libre al azar para la comida."""
    global comida, comida_dorada
    libres = []
    for columna in range(COLUMNAS):
        for fila in range(FILAS):
            if (columna, fila) not in serpiente:
                libres.append((columna, fila))
    comida = random.choice(libres)
    comida_dorada = random.randint(1, 5) == 1   # 1 de cada 5 es dorada


def detener_ciclo():
    """Cancela el movimiento automático."""
    global tarea
    if tarea is not None:
        ventana.after_cancel(tarea)
        tarea = None


def iniciar_partida():
    """Prepara una partida nueva y arranca el juego."""
    global estado, serpiente, direccion, dir_movida, puntaje, nuevo_record, retraso, tarea
    detener_ciclo()
    ocultar_paneles()

    centro = (COLUMNAS // 2, FILAS // 2)
    serpiente = [centro, (centro[0] - 1, centro[1]), (centro[0] - 2, centro[1])]
    direccion = (0, 0)
    dir_movida = (1, 0)
    puntaje = 0
    nuevo_record = False
    retraso = RETRASOS[dificultad_var.get()]

    colocar_comida()
    actualizar_estadisticas()
    marco_menu.pack_forget()
    marco_juego.pack(fill="both", expand=True)
    canvas.focus_set()
    estado = "jugando"
    redibujar()
    tarea = ventana.after(retraso, ciclo)


def terminar_partida():
    """Se llama cuando el jugador pierde."""
    global estado, mejor_puntaje, nuevo_record
    detener_ciclo()
    estado = "game_over"
    nuevo_record = puntaje > mejor_puntaje
    if nuevo_record:
        mejor_puntaje = puntaje
        guardar_mejor()
    actualizar_estadisticas()
    redibujar()

    etq_fin_puntaje.configure(text=f"Puntaje: {puntaje}")
    if nuevo_record:
        etq_fin_record.configure(text="¡NUEVO RÉCORD!", bootstyle="warning")
    else:
        etq_fin_record.configure(text=f"Mejor: {mejor_puntaje}", bootstyle="light")
    mostrar_panel(panel_fin)


def avanzar():
    """Mueve la serpiente una casilla y revisa choques y comida."""
    global dir_movida, puntaje, retraso
    if direccion == (0, 0):
        return  # todavía no se ha presionado ninguna tecla

    dir_movida = direccion
    cabeza = serpiente[0]
    nueva = (cabeza[0] + direccion[0], cabeza[1] + direccion[1])
    comiendo = (nueva == comida)

    # Choque con los bordes del tablero
    if nueva[0] < 0 or nueva[0] >= COLUMNAS or nueva[1] < 0 or nueva[1] >= FILAS:
        terminar_partida()
        return

    # Choque con su propio cuerpo (la cola se mueve, así que no cuenta si no come)
    if comiendo:
        cuerpo = serpiente
    else:
        cuerpo = serpiente[:-1]
    if nueva in cuerpo:
        terminar_partida()
        return

    serpiente.insert(0, nueva)   # la cabeza avanza
    if comiendo:
        if comida_dorada:
            puntaje += 30
        else:
            puntaje += 10
        nivel = 1 + puntaje // 50
        retraso = max(RETRASO_MINIMO, RETRASOS[dificultad_var.get()] - (nivel - 1) * 8)
        actualizar_estadisticas()
        colocar_comida()
    else:
        serpiente.pop()          # si no comió, la cola desaparece


def ciclo():
    """Un paso del juego. Se vuelve a llamar a sí misma cada 'retraso' ms."""
    global tarea
    if estado != "jugando":
        return
    avanzar()
    if estado == "jugando":
        redibujar()
        tarea = ventana.after(retraso, ciclo)


def continuar():
    """Quita la pausa."""
    global estado, tarea
    if estado == "pausa":
        estado = "jugando"
        ocultar_paneles()
        canvas.focus_set()
        tarea = ventana.after(retraso, ciclo)


def alternar_pausa():
    """Pone o quita la pausa."""
    global estado
    if estado == "jugando":
        detener_ciclo()
        estado = "pausa"
        canvas.focus_set()   # evita que la barra espaciadora active un botón
        mostrar_panel(panel_pausa)
    elif estado == "pausa":
        continuar()


def ir_menu():
    """Vuelve al menú principal."""
    global estado
    detener_ciclo()
    estado = "menu"
    ocultar_paneles()
    etq_menu_record.configure(text=f"Mejor puntaje: {mejor_puntaje}")
    marco_juego.pack_forget()
    marco_menu.pack(fill="both", expand=True)


def salir():
    """Cierra el programa."""
    detener_ciclo()
    ventana.destroy()





# ---------------------------------------------------------------
# 10. CONTROLES
# ---------------------------------------------------------------
def tecla(evento):
    """Se ejecuta cada vez que el jugador presiona una tecla."""
    global direccion
    nombre = evento.keysym.lower()

    if nombre in DIRECCIONES and estado == "jugando":
        nueva = DIRECCIONES[nombre]
        # No se permite dar la vuelta de 180° sobre sí misma
        if nueva != (-dir_movida[0], -dir_movida[1]):
            direccion = nueva
    elif nombre == "p" or (nombre == "space" and estado in ("jugando", "pausa")):
        alternar_pausa()
    elif nombre == "return" and estado in ("menu", "game_over"):
        iniciar_partida()
    elif nombre == "escape":
        if estado == "menu":
            salir()
        else:
            ir_menu()
    elif nombre in ("1", "2", "3") and estado == "menu":
        dificultad_var.set({"1": "facil", "2": "normal", "3": "dificil"}[nombre])


boton_jugar.configure(command=iniciar_partida)
boton_salir.configure(command=salir)
boton_pausa.configure(command=alternar_pausa)
boton_menu.configure(command=ir_menu)
boton_continuar.configure(command=continuar)
boton_pausa_menu.configure(command=ir_menu)
boton_reintentar.configure(command=iniciar_partida)
boton_fin_menu.configure(command=ir_menu)
ventana.bind("<Key>", tecla)
ventana.protocol("WM_DELETE_WINDOW", salir)

# ---------------------------------------------------------------
# 11. INICIO
# ---------------------------------------------------------------
ir_menu()
ventana.mainloop()