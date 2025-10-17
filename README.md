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


1. IOAgent → ParserAgent: parse_expression("2 + 3 * 4")
2. ParserAgent → MulAgent: perform_operation(3, 4)
3. MulAgent → ParserAgent: operation_result(12)
4. ParserAgent → SumAgent: perform_operation(2, 12)
5. SumAgent → ParserAgent: operation_result(14)
6. ParserAgent → IOAgent: final_result(14)
Manejo de Precedencia
Potencia (^): Precedencia más alta

Multiplicación/División (*, /): Precedencia media

Suma/Resta (+, -): Precedencia más baja

Resultados Obtenidos
Procesamiento correcto de expresiones básicas y complejas (con paréntesis).

Soporta números enteros y decimales.

Maneja división por cero devolviendo inf.

Comunicación visible en la interfaz para depuración y aprendizaje.

## PUNTO 3

# Calculadora Científica Kotlin - Paradigma de Objetos (POO)

Una implementación completa de una calculadora científica utilizando **Programación Orientada a Objetos** en **Kotlin**. Este proyecto demuestra los principios fundamentales de POO: **encapsulamiento**, **herencia**, **polimorfismo** y **abstracción**.

---

##  Características Principales

###  **Operaciones Básicas**
- Suma, resta, multiplicación, división
- Sobrecarga de operadores para `Int` y `Double`
- Manejo robusto de división por cero

###  **Funciones Científicas**
- **Trigonometría**: sin, cos, tan, asin, acos, atan
- **Potencias y Raíces**: potencia, raíz cuadrada, raíz cúbica, raíz n-ésima
- **Logaritmos**: log₁₀, ln, log en base arbitraria
- **Exponencial**: e^x, factorial, valor absoluto

###  **Funciones de Memoria**
- **MS**: Guardar en memoria
- **MR**: Recuperar de memoria  
- **M+**: Sumar a memoria
- **M-**: Restar de memoria
- **MC**: Limpiar memoria

###  **Evaluación de Expresiones**
- Parser completo para expresiones matemáticas complejas
- Soporte para paréntesis y precedencia de operadores
- Ejemplos: `2 + 3 * sin(45) - log(100)`, `(sqrt(16) + 2)^2 / 4`

###  **Configuración Avanzada**
- Modo de ángulos: radianes o grados
- Precisión configurable de resultados
- Historial de operaciones con timestamps

---

##  Diseño de la Solución

<img width="4631" height="3543" alt="uml_calculadora_cientifica" src="https://github.com/user-attachments/assets/d0bb174a-0933-4d8b-af8e-4b4fd1a1abcd" />


### **Arquitectura UML**

#### **Clase Base: `Calculadora`**
```kotlin
open class Calculadora {
    private var memoria: Double = 0.0
    private val historial: MutableList<String> = mutableListOf()
    
    // Polimorfismo - Sobrecarga de métodos
    open fun sumar(a: Int, b: Int): Int
    open fun sumar(a: Double, b: Double): Double
    // ... otras operaciones básicas
}
```

#### **Clase Derivada: `CalculadoraCientifica`**
```kotlin
class CalculadoraCientifica : Calculadora() {
    private var esRadianes: Boolean = true
    
    // Herencia - Extensión de funcionalidades
    fun seno(angulo: Double): Double
    fun logaritmoBase10(valor: Double): Double
    fun evaluarExpresion(expresion: String): Double
    // ... funciones científicas avanzadas
}
```

---

##  Instalación y Uso

### **Requisitos**
- **Kotlin** 1.9.10+
- **JVM** 17+
- **Gradle** 7.0+ (opcional)

### **Ejecutar la Aplicación**

#### **Opción 1: Compilación directa**
```bash
kotlinc CalculadoraCientifica.kt -include-runtime -d calculadora.jar
java -jar calculadora.jar
```

#### **Opción 2: Con Gradle**
```bash
gradle run
```

### **Interfaz de Consola**
```
╔════════════════════════════════════════╗
║     CALCULADORA CIENTÍFICA KOTLIN      ║
║        Programación Orientada a        ║
║             Objetos (POO)              ║
╚════════════════════════════════════════╝

 Calculadora> 2 + 3 * sin(45) - log(100)
 Resultado: 3.121

 Calculadora> ayuda
```

---

##  Capturas de Pantalla

<img width="4770" height="3543" alt="capturas_calculadora_kotlin" src="https://github.com/user-attachments/assets/5ad89613-1cfc-4829-af15-da1a516f8224" />


### **Ejemplos de Uso**

#### **Operaciones Básicas**
```
Calculadora> 2 + 3 * 4
 Resultado: 14

 Calculadora> sqrt(16) + log(100)  
 Resultado: 6
```

#### **Funciones Científicas**
```
 Calculadora> sin(30) + cos(60)
 Resultado: 1.0

 Calculadora> exp(1) + ln(2.718)
 Resultado: 3.718
```

#### **Memoria**
```
 Calculadora> ms 42.5
 Valor 42.5 guardado en memoria

 Calculadora> m+ 7.5
 Memoria + 7.5 = 50.0
```

---

##  Principios POO Aplicados

### ** ENCAPSULAMIENTO**
- **Atributos privados**: `memoria`, `historial`, `esRadianes`  
- **Métodos públicos**: Interfaz limpia y controlada
- **Validación interna**: Protección contra valores inválidos

```kotlin
class CalculadoraCientifica : Calculadora() {
    private var esRadianes: Boolean = true  //  Encapsulado
    
    var modoAngulos: String                 //  Propiedad pública
        get() = if (esRadianes) "Radianes" else "Grados"
        set(value) { /* validación */ }
}
```

### ** HERENCIA**
- **Clase base**: `Calculadora` con operaciones fundamentales
- **Clase derivada**: `CalculadoraCientifica` extiende funcionalidades
- **Reutilización**: Código base compartido y especializado

```kotlin
//  Herencia + Override
override fun formatearResultado(resultado: Double): String {
    return when {
        abs(resultado) >= 1e6 -> "%.${precision}e".format(resultado)
        else -> super.formatearResultado(resultado)  // Llamada al padre
    }
}
```

### ** POLIMORFISMO**
- **Sobrecarga de métodos**: Misma operación, diferentes tipos
- **Override**: Comportamiento especializado en clases derivadas  
- **Operadores**: Extensiones Kotlin elegantes

```kotlin
//  Polimorfismo - Sobrecarga
open fun sumar(a: Int, b: Int): Int = a + b
open fun sumar(a: Double, b: Double): Double = a + b

//  Polimorfismo - Override
override fun dividir(a: Double, b: Double): Double {
    if (abs(b) < 1e-10) throw DivisionPorCeroException()
    return super.dividir(a, b)
}
```

### ** ABSTRACCIÓN**
- **Interfaces simples**: Operaciones complejas ocultas
- **Manejo de errores**: Excepciones específicas y descriptivas
- **Parser interno**: Evaluación de expresiones transparente

---

##  Manejo de Excepciones

### **Excepciones Personalizadas**
```kotlin
class CalculadoraException(message: String) : Exception(message)
class DivisionPorCeroException : CalculadoraException("División por cero no permitida")  
class ValorInvalidoException(mensaje: String) : CalculadoraException("Valor inválido: $mensaje")
class ExpresionInvalidaException(mensaje: String) : CalculadoraException("Expresión inválida: $mensaje")
```

### **Casos Controlados**
-  División por cero
-  Logaritmos de números negativos
-  Raíces pares de números negativos  
-  Expresiones malformadas
-  Argumentos fuera de rango

---

##  Funcionalidades Avanzadas

### ** Evaluación de Expresiones**
```kotlin
 Calculadora> 2 + 3 * sin(45) - log(10)
 Resultado: 3.121

 Calculadora> (sqrt(16) + 2)^2 / (3 + 1)  
 Resultado: 9
```

### ** Sistema de Memoria**
```kotlin
 Calculadora> ms 100       // Guardar
 Calculadora> m+ 50        // Sumar a memoria  
 Calculadora> mr           // Recuperar: 150
```

### ** Configuración**
```kotlin
 Calculadora> precision 5     // 5 decimales
 Calculadora> modo grados      // Cambiar a grados
```

### ** Historial**
```kotlin
 Calculadora> historial
 HISTORIAL DE OPERACIONES:
2024-10-16T19:30: 2 + 3 * 4 = 14
2024-10-16T19:31: sqrt(16) = 4
```

---

##  Ejemplos de Código

### **Uso Básico**
```kotlin
val calc = CalculadoraCientifica()

// Operaciones básicas
val suma = calc.sumar(2.5, 3.7)
val producto = calc.multiplicar(4, 5)

// Funciones científicas  
val seno = calc.seno(Math.PI / 2)  // 1.0
val log = calc.logaritmoBase10(100) // 2.0

// Expresiones complejas
val resultado = calc.evaluarExpresion("2 + 3 * sin(45)")
```

### **Manejo de Memoria**
```kotlin
calc.memoriaGuardar(42.0)
calc.memoriaSumar(8.0)
val valor = calc.memoriaRecuperar()  // 50.0
```



