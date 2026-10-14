# ¿Qué tipos de archivos de entrada se necesitan?
Para realizar esta descompresión, un archivo de secuencia por sí solo no basta. Necesitas una combinación de dos cosas (igual que un descompilador de software necesita el binario y un archivo de símbolos o metadatos):

## El archivo de secuencia (.fasta): 
Contiene el "bytecode" puro, es decir, la cadena gigantesca de letras (A, C, G, T). Por sí solo, es una tira ciega de código sin formato.

## El archivo de anotación (.gff3 o .gtf): 
Es el archivo clave. En bioinformática, los formatos GFF (General Feature Format) o GTF contienen el mapa de coordenadas. Le dicen al descompilador: "Desde la posición 1000 hasta la 1500 hay un exón, desde la 1501 hasta la 2000 hay un intrón", etc. Sin esto, el ordenador no sabe dónde empiezan o acaban las "funciones".

### Resumen

- El archivo **FASTA** es el binario compilado (puro código máquina).

- El archivo **GFF3 / GTF** es el archivo de símbolos (.pdb o la tabla de símbolos) que dice: "La función X se encuentra exactamente desde la dirección de memoria 5001 hasta la 8500".