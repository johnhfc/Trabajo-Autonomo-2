

import turtle
import random
import time

# ---------------------------------------------------------------
# 1. Variables iniciales
# ---------------------------------------------------------------
RETRASO = 0.1      # segundos entre cada movimiento (menor = más rápido)
puntaje = 0        # puntos de la partida actual
mejor_puntaje = 0  # mejor puntaje mientras el programa esté abierto

# ---------------------------------------------------------------
# 2. Configuración de la ventana
# ---------------------------------------------------------------
pantalla = turtle.Screen()
pantalla.title("Juego de la Serpiente")
pantalla.bgcolor("black")
pantalla.setup(width=600, height=600)
pantalla.tracer(0)  # apaga la animación automática; actualizamos a mano

# ---------------------------------------------------------------
# 3. Objetos del juego
# ---------------------------------------------------------------
# Cabeza de la serpiente
cabeza = turtle.Turtle()
cabeza.speed(0)
cabeza.shape("square")
cabeza.color("green")
cabeza.penup()
cabeza.goto(0, 0)
cabeza.direction = "stop"  # al inicio no se mueve

# Comida
comida = turtle.Turtle()
comida.speed(0)
comida.shape("circle")
comida.color("red")
comida.penup()
comida.goto(0, 100)

# Lista que guarda los segmentos del cuerpo
segmentos = []

# Marcador de puntos
marcador = turtle.Turtle()
marcador.speed(0)
marcador.color("white")
marcador.penup()
marcador.hideturtle()
marcador.goto(0, 260)


# ---------------------------------------------------------------
# 4. Funciones
# ---------------------------------------------------------------
def actualizar_marcador():
    """Borra y vuelve a escribir el puntaje en pantalla."""
    marcador.clear()
    marcador.write(f"Puntaje: {puntaje}   Mejor: {mejor_puntaje}",
                   align="center", font=("Courier", 18, "normal"))


# Funciones de dirección: la serpiente no puede girar 180 grados
def ir_arriba():
    if cabeza.direction != "down":
        cabeza.direction = "up"


def ir_abajo():
    if cabeza.direction != "up":
        cabeza.direction = "down"


def ir_izquierda():
    if cabeza.direction != "right":
        cabeza.direction = "left"


def ir_derecha():
    if cabeza.direction != "left":
        cabeza.direction = "right"


def mover():
    """Mueve la cabeza 20 píxeles según su dirección."""
    if cabeza.direction == "up":
        cabeza.sety(cabeza.ycor() + 20)
    if cabeza.direction == "down":
        cabeza.sety(cabeza.ycor() - 20)
    if cabeza.direction == "left":
        cabeza.setx(cabeza.xcor() - 20)
    if cabeza.direction == "right":
        cabeza.setx(cabeza.xcor() + 20)


def reiniciar():
    """Se llama cuando el jugador pierde: reinicia la partida."""
    global puntaje
    time.sleep(1)
    cabeza.goto(0, 0)
    cabeza.direction = "stop"
    for segmento in segmentos:
        segmento.goto(1000, 1000)  # los saca de la pantalla
    segmentos.clear()
    puntaje = 0
    actualizar_marcador()


# ---------------------------------------------------------------
# 5. Teclado
# ---------------------------------------------------------------
pantalla.listen()
pantalla.onkeypress(ir_arriba, "Up")
pantalla.onkeypress(ir_abajo, "Down")
pantalla.onkeypress(ir_izquierda, "Left")
pantalla.onkeypress(ir_derecha, "Right")
pantalla.onkeypress(ir_arriba, "w")
pantalla.onkeypress(ir_abajo, "s")
pantalla.onkeypress(ir_izquierda, "a")
pantalla.onkeypress(ir_derecha, "d")

actualizar_marcador()

# ---------------------------------------------------------------
# 6. Bucle principal del juego
# ---------------------------------------------------------------
try:
    while True:
        pantalla.update()

        # a) Choque con los bordes de la ventana
        if (cabeza.xcor() > 280 or cabeza.xcor() < -280 or
                cabeza.ycor() > 280 or cabeza.ycor() < -280):
            reiniciar()

        # b) La cabeza toca la comida
        if cabeza.distance(comida) < 20:
            # La comida aparece en un lugar aleatorio de la cuadrícula
            comida.goto(random.randint(-13, 13) * 20,
                        random.randint(-13, 13) * 20)

            # Se agrega un nuevo segmento al cuerpo
            nuevo_segmento = turtle.Turtle()
            nuevo_segmento.speed(0)
            nuevo_segmento.shape("square")
            nuevo_segmento.color("lightgreen")
            nuevo_segmento.penup()
            nuevo_segmento.goto(1000, 1000)
            segmentos.append(nuevo_segmento)

            # Se suman puntos y se actualiza el mejor puntaje
            puntaje += 10
            if puntaje > mejor_puntaje:
                mejor_puntaje = puntaje
            actualizar_marcador()

        # c) Cada segmento sigue al que tiene delante (de atrás hacia adelante)
        for i in range(len(segmentos) - 1, 0, -1):
            segmentos[i].goto(segmentos[i - 1].xcor(),
                              segmentos[i - 1].ycor())

        # d) El primer segmento va a donde estaba la cabeza
        if len(segmentos) > 0:
            segmentos[0].goto(cabeza.xcor(), cabeza.ycor())

        # e) Se mueve la cabeza
        mover()

        # f) Choque de la cabeza con su propio cuerpo
        for segmento in segmentos:
            if segmento.distance(cabeza) < 20:
                reiniciar()

        time.sleep(RETRASO)

except turtle.Terminator:
    # Ocurre cuando el jugador cierra la ventana, salimos sin error.
    pass
