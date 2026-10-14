# Primeros pasos y pruebas

En este momento lo que pensaba era que la mejor manera de probar formatos y aprender la estructura del adn era intentar, como todo buen programador, hacer una descompilacion del codigo (adn) a otro lenguaje mas entendible por un humano.

Esta carpeta son las diferentes pruebas

- **NC 064231.1 Spodoptera frugiperda.fasta** es el primer archivo fasta sacado de NCBI, para las pruebas.
- **sequence.gb** es la version Genbank full correspondiente al fasta anterior, tambien sacada de NCBI.

## Ejemplos de como deberia de quedar el codigo descompilado

- [000-ej-codigo.py](./000-ej-codigo.py): Ejemplo de como podria ser un adn descompilado
- [002-prueba1.py](./002-prueba1.py): Primera prueba, tomando como fuente un archivo fasta

# Configuracion de entorno

```bash
#creamos el enviroment para python
conda create -n bio_env python=3.14 -y

#instalamos biopython
pip install biopython

#lo siguiente, ya podremos ejecutar poniendo
python ./<nombre del archivo>
```
## comparer_analysis.py
> Primera version de prueba
## comparer_analysis_promotor.py
> Última version del analizador, que tiene en cuenta los promotores, los dos sentidos de lectura de las hebras.
> Usamos un patrón flexible que engloba variantes de cajas ricas en AT (TATA, TATAA, TAAA, etc.)
> y motivos de iniciación alternativos comunes en eucariotas.

- [comparer_analysis_promotor.py](./comparer_analysis_promotor.py)

La salida por pantalla:
```pwsh
python ./comparer_analysis_promotor.py

======================================================================
1. INSPECCIONANDO DIRECCIONES Y PROMOTORES EN EL GENBANK
======================================================================
Total de genes oficiales analizados en GenBank:
  - Hebra positiva (+): 320 genes
  - Hebra negativa (-): 339 genes
  - Elementos reguladores/promotores explícitamente anotados: 0

======================================================================
2. ANALIZADOR HEURÍSTICO RELAJADO SOBRE EL FASTA
======================================================================
Leyendo secuencia FASTA desde: NC 064231.1 Spodoptera frugiperda.fasta...
Escaneando hebra directa (+) con patrones relajados...
Escaneando hebra complementaria (-) con patrones relajados...

======================================================================
RESUMEN DE HALLAZGOS DEL ANALIZADOR HEURÍSTICO FLEXIBLE:
======================================================================
  - Candidatos detectados en hebra directa (+): 194
  - Candidatos detectados en hebra negativa (-): 141
  - Total de candidatos viables con promotores relajados: 335
======================================================================

```

## Cruze.py

>Comparamos los datos dados por el analizador/descompilador heuristico, con los datos reales vistos por investigadores y anotados en GenBank


```pwsh
(base) pwsh> conda activate bio_env
(bio_env) pwsh> python ./cruze.py     

======================================================================
EVALUACIÓN DE SOLAPAMIENTO: HEURÍSTICA VS GENBANK
======================================================================
-> Cargados 659 genes oficiales del GenBank.
-> Analizador heurístico detectó 2516 candidatos viables.
Calculando solapamientos con la verdad oficial...

======================================================================
RESULTADOS DE LA AUDITORÍA ESTÁTICA:
======================================================================
  - Candidatos totales analizados: 2516
  - Coincidencias con genes oficiales (Aciertos): 1313
  - Candidatos sin respaldo en GenBank (Falsos positivos/Nuevos): 1203
  - Precisión de la heurística flexible: 52.19%
======================================================================
```

# Resumen de la estructura del ADN como si fuese un sistema informático

>Comentarios de la IA tras revisar la estructura de ADN

1. **El Almacenamiento (DNA): El binario estático o código fuente original**
    - Es el disco duro del sistema. Una estructura de solo lectura (excepto por mutaciones), ultra-protegida en el núcleo, que contiene todo el mapa de instrucciones globales del sistema pero que no se ejecuta directamente de forma masiva. Está escrito en un alfabeto estricto de 4 caracteres (A, C, G, T).

2. **El Nivel Intermedio (mRNA): El Bytecode o Intermediate Language (IL)**
    - Cuando la célula necesita ejecutar una rutina, no abre el binario original y lo altera; el motor de transcripción compila un fragmento del DNA y emite una copia temporal y portátil: el ARN mensajero (mRNA).

    - Este mRNA viaja fuera del núcleo (sale al "runtime" del citoplasma) y es puro bytecode listo para ser interpretado.

3. **El Motor de Ejecución (Ribosoma / Máquina Virtual): El CLR o Intérprete**
    - El ribosoma actúa exactamente como el Common Language Runtime (CLR) o una máquina virtual. Lee el bytecode del mRNA triplete a triplete (codón a codón) y va traduciendo las instrucciones de manera secuencial.

4. **La Capa de Aplicación en Memoria (Proteínas): Los objetos dinámicos y la lógica de negocio**
    - Una vez que el bytecode se interpreta, se instancia una cadena lineal de aminoácidos que inmediatamente se compila a sí misma en el espacio tridimensional (el plegamiento).

    - Las proteínas no son solo datos estáticos; son instancias vivas y activas en memoria (como objetos en ejecución). Algunas actúan como funciones puras (enzimas que procesan inputs y devuelven outputs químicos), otras como elementos estructurales del framework, y otras como componentes de UI o canales de comunicación.

**El "Garbage Collector" Biológico**
    
- Y para cerrar el círculo del paralelismo con la programación: cuando una proteína cumple su ciclo de vida, se desnaturaliza, pierde su forma y la célula la desarma (degrada) reciclando sus aminoácidos básicos para liberar memoria RAM. ¡Es un sistema con gestión automática de memoria a nivel molecular!

Mirar la biología como una arquitectura de software multicapa desmitifica por completo los libros de texto y convierte la genética en algo profundamente intuitivo para un programador.












