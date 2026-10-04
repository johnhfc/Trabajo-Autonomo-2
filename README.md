#  Juego de la Serpiente (Snake) en Python

 **Lógica de Programación** — Trabajo Autónomo 2 (Paso 1 y Paso 2).

| | |
|---|---|
| **Universidad** | Universidad Internacional del Ecuador (UIDE) |
| **Asignatura** | Lógica de Programación |
| **Autor** | John Henry Freire Castillo |
| **Programa seleccionado** | Juego de la serpiente |


##  Objetivo

Analizar e implementar las funcionalidades y la arquitectura del juego de la serpiente, aplicando los conocimientos adquiridos durante las semanas de clase: estructuras condicionales, estructuras repetitivas y un código organizado y comentado.

##  Funcionalidades

Las funcionalidades fueron identificadas en el Trabajo Autónomo 1:

1. El sistema inicia una nueva partida con la serpiente en una posición inicial.
2. El jugador mueve la serpiente con el teclado (flechas o WASD).
3. El sistema detecta colisiones: contra los bordes del tablero, contra el propio cuerpo y contra la comida.
4. Cuando la serpiente come, se genera una nueva comida en una posición aleatoria y la serpiente crece.
5. El sistema actualiza y muestra el puntaje en pantalla.
6. Si hay colisión con el borde o con el propio cuerpo, la partida termina y se muestra el puntaje final.

##  Etapas del desarrollo

| Etapa | Archivo | Descripción |
|---|---|---|
| **Paso 1** — Inicio del desarrollo | `juego_serpiente_beta` | Primera base del juego: Tablero con caracteres, movimiento con W, A, S, D, comida, puntaje y choques. |
| **Paso 2** — Desarrollo del programa | `juego_serpiente_mejorado` | Versión final con ventana gráfica: menú Jugar/Salir, tablero de cuadrícula, marcador de puntaje y mejor puntaje, velocidad que aumenta al comer y pantalla de Game Over. |

##  Estructura del repositorio

```
juego-serpiente/
├── README.md
├── juego_serpiente_beta
├── juego_serpiente_mejorado
└── diagramas/
    ├── casos de uso
    ├── arquitectura capas
   
```

##  Configuración del entorno

**Herramientas:** Python 3, Visual Studio Code, Git y GitHub.

1. Instalar Python 3 (marcar la opción *Add Python to PATH*).
2. Clonar el repositorio:

   ```
   git clone <URL-DEL-REPOSITORIO>
   cd juego-serpiente
   ```

##  Cómo ejecutar

### Versión 1 — Beta (Paso 1)

Solo usa la librería estándar de Python (`os`, `time`, `random` y `msvcrt`), por lo que **no requiere instalar nada**. Funciona en **Windows**.

```
python juego_serpiente_beta.py
```

### Versión final — Mejorada (Paso 2)

Usa `tkinter` (incluido con Python) y la librería `ttkbootstrap`, que se instala una sola vez:

```
python -m pip install ttkbootstrap
python juego_serpiente_ttkbootstrap.py
```

## Controles

| Acción | Teclas |
|---|---|
| Arriba | `↑` o `W` |
| Abajo | `↓` o `S` |
| Izquierda | `←` o `A` |
| Derecha | `→` o `D` |



##  Conceptos de programación aplicados

- **Estructuras condicionales (`if`, `elif`, `else`):** dirección del movimiento, choques con bordes y cuerpo, y decidir si la serpiente come o no.
- **Estructuras repetitivas (`for`, `while`):** recorrer el tablero para dibujarlo, buscar una casilla libre para la comida y repetir el ciclo del juego.
- **Funciones:** cada tarea del juego está separada en una función con un nombre descriptivo.
- **Listas:** la serpiente se guarda como una lista de casillas `[columna, fila]`.
- **Comentarios:** las partes importantes del código están explicadas.

##  Diagramas

Los diagramas se encuentran en la carpeta [`diagramas/`](diagramas/).

**Diagrama de casos de uso**

(diagramas/Diagrama de Uso.drawio.png)

**Diagrama de arquitectura en capas**

(diagramas/Diagrama de Arquitectura.drawio.png)

**Diagramas de flujo:** [`diagramas/`](diagramas/)

##  Arquitectura

| Capa | Responsabilidad |
|---|---|
| **Presentación** | Dibujar el tablero, la serpiente, la comida y el puntaje; capturar las teclas. |
| **Lógica de juego** | Ciclo principal: mover la serpiente, detectar colisiones y generar la comida. |
| **Datos** | Estado de la partida: posición de la serpiente y de la comida, puntaje actual y mejor puntaje. |

##  Videos

- Video del Paso 1 (configuración del repositorio, avance del código y relación con los diagramas): https://drive.google.com/file/d/1X2T3ZcXLGCZX-MmBZ-kh4eXSQVxspSaB/view?usp=sharing
- Video del Paso 2 (explicación del desarrollo): https://drive.google.com/file/d/1F1FMUd-DLHame4SXPgOm36ZFTH8c89OD/view?usp=sharing 
- Video demostrativo del funcionamiento: https://drive.google.com/file/d/1p0n8wucUptIeliAbO8GP5FxlCAOFAKsV/view?usp=sharing

##  Autor

**John Henry Freire Castillo** — Estudiante de Ingeniería en Ciberseguridad, Universidad Internacional del Ecuador.
