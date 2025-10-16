# ParcialCorte2

## PUNTO 1

1. Diseño de la Solución
Se utilizó el paradigma de agentes con el framework Mesa (versión 0.8.9) para implementar un perceptrón de dos entradas y un sesgo.

DataPointAgent: Representa cada punto de datos 2D con etiquetas ±1.

PerceptronAgent: Implementa el algoritmo de aprendizaje perceptrón con regla de actualización de pesos y bias.

Scheduler: RandomActivation de Mesa para paso conjunto de agentes.

Visualización Tkinter: Interfaz con sliders para tasa de aprendizaje e iteraciones, botones Iniciar y Restablecer.

<img width="4469" height="3543" alt="Diseño de sistema" src="https://github.com/user-attachments/assets/98689bf7-7348-4f81-80e3-e30b1edf426c" />


2. Capturas de Pantalla de la Simulación
2.1 Estado Inicial y Entrenamiento
<img width="4770" height="3544" alt="SimulacionesPerceptron" src="https://github.com/user-attachments/assets/31edfc9f-a6eb-4e02-b3f6-a59048726da1" />


3. Informe Técnico
3.1 Funcionamiento del Perceptrón

El perceptrón clasifica puntos linealmente separables mediante la función de activación:

$$activation = w_1 x_1 + w_2 x_2 + bias$$

La predicción es:

$$y = \begin{cases} +1 & activation \ge 0 \\ -1 & activation < 0 \end{cases}$$

Los pesos y el bias se actualizan según:

$$w_i \leftarrow w_i + \alpha (d - y) x_i$$

$$bias \leftarrow bias + \alpha (d - y)$$

3.2 Implementación y Resultados
Se generaron 50 puntos aleatorios 2D linealmente separables.

Entrenamiento automático hasta convergencia o máximo de iteraciones.

Control dinámico de tasa de aprendizaje e iteraciones vía sliders.

Se monitorizó el error total por época, converge a 0 en ~45 épocas.

Precisión final alcanza 100% con frontera aprendida coincidiendo con la verdadera
