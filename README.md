[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/vU2X5r1n)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=21476111&assignment_repo_type=AssignmentRepo)
# Práctica de las estructuras BST y Tablas Hash (Criptoanálisis en campo)
(Usar el lenguaje de programación de su preferencia.)
## Objetivo de la Misión

Su equipo es la unidad de criptoanálisis de élite. Su misión es realizar **ingeniería inversa** para determinar la **constante ($\mathbf{A}$)** utilizada en la función *hash de multiplicación* del enemigo, reconstruir el patrón de colisiones, y revelar la orden militar. Su herramienta clave de análisis será el **Árbol Binario de Búsqueda (BST)**.

***

## 1. Contexto y Parámetros de la Misión

**La Intercepción:** El mensaje fue interceptado hoy, **viernes 31 de octubre**, y contiene instrucciones para un ataque inminente. La seguridad de nuestro bando depende de la rapidez con la que descifren este mensaje. Inteligencia logró identificar que los mensajes enemigos no contienen mayúsculas, acentos ni signos de puntuación, y se utiliza el código ASCII de cada caracter para su encriptación.

| Parámetro | Descripción | Valor / Definición |
| :--- | :--- | :--- |
| **Caracteres almacenados en las "cubetas" de la tabla hash**|Abecedario en español (sin mayúsculas, acentos ni signos de puntuación|27 letras|
| **Mensaje Interceptado (Ciphertext)** | **(/-.-4%(+28.%#+2/($(6(#(3(8%.-/2(+(/(6.(** |
| **Estructura Cifrado** | Tabla Hash con **Encadenamiento** |
| **Tamaño de la Tabla ($\mathbf{M}$)** | Cantidad de "cubetas" de la Tabla Hash. | 31 |
| **Incógnita $\mathbf{A}$ (Objetivo)** | Constante "de Dispersión" $A$. | |
| **Esquema Cifrado** | Sustitución simple, con **doble mapeo estático** ($\mathbf{C_A / C_B}$) al 50% de probabilidad. |

Pueden tomar como referencia para los códigos ASCIIs el siguiente sitio: https://elcodigoascii.com.ar/#google_vignette
***
## 2. Las Dos Funciones de Dispersión (Mapeos Estáticos)

El enemigo utiliza un sistema de **doble *hashing***. Cada carácter ($k$, valor ASCII) es procesado por dos funciones completamente separadas, y la sustitución final se elige arbitrariamente entre los dos resultados:

### A. Función de Multiplicación (Mapeo de Dispersión)

Esta función utiliza la constante $\mathbf{A}$ para dispersar las llaves.

$$\text{índice}_{\mathbf{A}} = \lfloor M \cdot ((k \cdot A) \pmod 1) \rfloor + 32$$

* **Incógnita $\mathbf{A}$ (Objetivo):** Constante de Dispersión $A$ (la Proporción Áurea). $A = \phi \approx \mathbf{0.61803...}$

### B. Función de División (Mapeo de Módulo)

Esta es la función de *hashing* más básica, utilizando la operación de **congruencia módulo $\mathbf{M}$**.

$$\text{índice}_{\mathbf{M}} = (k \pmod M) + 32$$

* **Constante Conocida:** $M = \mathbf{31}$.

**NOTA CRÍTICA:** Para un caracter específico, se utiliza en el mismo mensaje la misma función Hash, es decir, en el mensaje encriptado cada letra se relaciona exactamente con un solo caracter "nuevo".
***

***

## 3. Fases del Criptoanálisis

### Fase 1: Análisis de Frecuencia con BST

1.  **Implementación del BST:** Construya un **Árbol Binario de Búsqueda**. Cada nodo almacena: **Clave** = Carácter Cifrado; **Valor** = Frecuencia de aparición.
2.  **Análisis Crítico:** Implemente la función `analizar_frecuencia` que utilice la **inserción y búsqueda $O(\log N)$ del BST** para contar las frecuencias en el mensaje interceptado.
3.  **Postulación de Pares:** Extraiga del BST la lista de caracteres cifrados ordenada por frecuencia descendente. Use la estadística del español (la **'e'** y el **espacio** son las más comunes) para **postular el par clave** de sustitución más probable.

### Fase 2: Ingeniería Inversa (Descifrando la Constante $\mathbf{A}$)

**Mediante la búsqueda de la constante $A$, traten de adivinar cuál es la Tabla Hash mediante la que se codificó el mensaje.**

1.  **Búsqueda Heurística de $\mathbf{A}$:** Utilizando el par clave postulado ($k$ es el ASCII de su postulado) y la fórmula *hash* ($M=31$), implemente un algoritmo para buscar y justificar el valor de $A$ que converge en $A \approx 0.61803$.
2.  **Deducción del Patrón *Hash***: Con $A$ identificado, calcule el índice $i$ para **todos los caracteres del alfabeto** para revelar el **patrón de colisiones** exacto de la Tabla Hash enemiga.

### Fase 3: Ruptura Final del Código

1.  **Reconstrucción del Mapeo:** Combine los datos del **análisis de frecuencia (BST)** con el **patrón de colisiones deducido** para inferir el mapeo completo ($\text{carácter cifrado} \rightarrow \text{carácter original}$).
2.  **Descifrado Final:** Aplique el mapeo reconstruido al mensaje interceptado para obtener la instrucción.

***

## 4. Criterios de Éxito y Entregables

### Entregables Requeridos

1.  **Código Fuente Completo**
2.  **Tiempo de Ejecución** de la función `analizar_frecuencia` (BST).
3.  **Documentación (Justificación):**
    * Justificación formal y clara de cómo se determinó la constante $\mathbf{A \approx 0.61803}$.
    * El **mensaje descifrado final** (la orden militar).

### Criterios de Éxito de la Misión

* **Precisión:** El mensaje descifrado debe ser **idéntico** a la instrucción original.
* **Fundamento Teórico:** Demostración de la correcta implementación del BST y la justificación lógica del valor de $A$.
* **Análisis Temporal:** La medición del tiempo debe validar el rendimiento algorítmico del BST ($O(L \cdot \log N)$).
