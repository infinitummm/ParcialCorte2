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

# USO

Instala Mesa versión 0.8.9:

pip install mesa==0.8.9

python perceptron_mesa.py

## PUNTO 2

Calculadora Basada en el Paradigma de Agentes (Mesa)
Este repositorio implementa una calculadora distribuida donde cada operación aritmética es gestionada por un agente autónomo. Utiliza el framework Mesa 0.8.9 para modelar agentes, mensajes y coordinación, y ofrece una interfaz gráfica en Tkinter para interactuar y visualizar la comunicación entre agentes.

Diseño de la Solución
La arquitectura se basa en agentes especializados y un sistema de mensajes asíncrono:

- IOAgent (ID 0)

   - Recibe expresiones del usuario

   - Envía la expresión al ParserAgent

   - Muestra el resultado final

- ParserAgent (ID 1)

   - Tokeniza y convierte infix a postfix

   - Coordina precedencia de operadores

   - Envía tareas a los agentes de operación

   - Ensambla resultados parciales

- OperationAgents

   - SumAgent (ID 2): Sumas

   - SubAgent (ID 3): Restas

   - MulAgent (ID 4): Multiplicaciones

   - DivAgent (ID 5): Divisiones (gestiona división por cero)

   - PowAgent (ID 6): Potenciaciones

- MessageQueue

   - Cola de mensajes con timestamps

   - Identificación de emisor y receptor

   - Tipos de mensaje: parse_expression, perform_operation, operation_result, final_result

<img width="4770" height="3543" alt="image" src="https://github.com/user-attachments/assets/5cf5e86b-2087-4380-804f-ab2240fcd226" />


Capturas de Pantalla de la Simulación

La siguiente imagen muestra la interfaz principal, la comunicación paso a paso y las estadísticas generadas durante el cálculo de expresiones:

<img width="4769" height="3543" alt="image" src="https://github.com/user-attachments/assets/d0289316-572d-494f-aa2d-204c14c2b5d3" />



Requisitos

pip install mesa==0.8.9 numpy matplotlib tk

Ejecución

Clona o descarga este repositorio.

Ejecuta la aplicación:


python CalculadoraAgentes.py

En la interfaz:

Ingresa la expresión matemática (enteros o decimales, con soporte de + - * / ** ( )).

Presiona Calcular para iniciar el proceso.

Presiona Limpiar para reiniciar la entrada y los resultados.

Arquitectura Técnica y Comunicación

Flujo de Procesamiento

IOAgent envía parse_expression al ParserAgent

ParserAgent convierte a notación postfix y envía perform_operation al agente correspondiente

OperationAgent realiza la operación y devuelve operation_result al ParserAgent

ParserAgent envía final_result al IOAgent

Ejemplo para 2 + 3 * 4:

text
1. IOAgent → ParserAgent: parse_expression("2 + 3 * 4")
2. ParserAgent → MulAgent: perform_operation(3, 4)
3. MulAgent → ParserAgent: operation_result(12)
4. ParserAgent → SumAgent: perform_operation(2, 12)
5. SumAgent → ParserAgent: operation_result(14)
6. ParserAgent → IOAgent: final_result(14)
Manejo de Precedencia
Potencia (**): Precedencia más alta

Multiplicación/División (*, /): Precedencia media

Suma/Resta (+, -): Precedencia más baja

Resultados Obtenidos
Procesamiento correcto de expresiones básicas y complejas (con paréntesis).

Soporta números enteros y decimales.

Maneja división por cero devolviendo inf.

Comunicación visible en la interfaz para depuración y aprendizaje.




