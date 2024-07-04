# Pseudo-texto
Código (básico) para generar pseudo-texto a partir de texto ya dado y un quasi-núcleo (concepto de teoría de gráficas).

El código en Qn_basic.py, se divide en tres partes importantes y una última para vizualizar la digráfica y quasi-núcleo.

La primera parte es respecto a la generación de una digráfica a partir de un texto o textos dados.

Lo que se hace es extraer como tal las palabras y caracteres especiales que están en los textos, y se usa la librería de networkx para crear la digráfica.

Para la segunda parte, se quitan ciertos vértices de la digráfica anterior para agilizar el proceso de encontrar un quasi-núcleo de la digráfica completa.

OJO: Este proceso se puede modificar para que ciertos vértices no estén en el quasi-núcleo.

Finalmente la tercera parte importante, es la generación de pseudo textos; el algoritmo para generarlos es bastante básico, se puede mejorar.

El segundo archivo llamado Cont.py, es un chatbot que usa el metodo para generar pseudo textos del archivo Qn_basic.py; se puede modificar el código para que el quasi-núcleo se actualize (de cierta forma) con el input del usuario o dejar el quasi-núcleo fijo para una converssación.
