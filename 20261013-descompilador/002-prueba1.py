from Bio import SeqIO
import re

class DNAStaticAnalyzer:
    def __init__(self, fasta_filepath):
        self.fasta_filepath = fasta_filepath
        
    def scan_genome(self):
        print(f"Cargando y escaneando estáticamente: {self.fasta_filepath}...\n")
        
        # Leemos el primer registro del archivo FASTA
        record = next(SeqIO.parse(self.fasta_filepath, "fasta"))
        seq = str(record.seq).upper()
        total_length = len(seq)
        
        print(f"=== INFORMACIÓN GENERAL ===")
        print(f"ID del Cromosoma/Scaffold: {record.id}")
        print(f"Tamaño total del 'bytecode': {total_length:,} pares de bases\n")
        
        # -------------------------------------------------------------
        # 1. BÚSQUEDA DE PROMOTORES (Patrones reguladores como Caja TATA)
        # -------------------------------------------------------------
        # Expresión regular para buscar variantes de la caja TATA (TATAAA, TATATA, etc.)
        tata_pattern = re.compile(r'TAT[AT]AA[AT]')
        promoters = [m.start() for m in tata_pattern.finditer(seq)]
        
        print(f"=== 1. ZONAS REGULADORAS (PROMOTORES DETECTADOS) ===")
        print(f"Total de cajas TATA encontradas: {len(promoters)}")
        for p in promoters[:5]:  # Mostramos los primeros 5 como ejemplo
            print(f" -> Posible promotor ubicado en la posición absoluta: {p:,}")
        print("-" * 50)

        # -------------------------------------------------------------
        # 2. BÚSQUEDA DE GENES CODIFICANTES (ORFs) Y EXONES/INTRONES
        # -------------------------------------------------------------
        # Buscamos secuencias que empiecen por ATG y terminen en un codón de stop (TAA, TAG, TGA)
        # Nota: Limitamos el tamaño mínimo para filtrar falsos positivos aleatorios.
        orf_pattern = re.compile(r'ATG(?:[ATGC]{3})+?(?:TAA|TAG|TGA)')
        
        print(f"\n=== 2. GENES CODIFICANTES Y SPLICING (EXÓN/INTRÓN) ===")
        genes_found = 0
        
        for match in orf_pattern.finditer(seq):
            start, end = match.span()
            gene_length = end - start
            
            # Filtramos para analizar genes simulados de un tamaño biológicamente viable (> 300 nucleótidos)
            if gene_length > 300 and genes_found < 3: 
                genes_found += 1
                print(f"\n[GEN CANDIDATO #{genes_found}]")
                print(f"  * Rango total en el ADN: {start:,} - {end:,} (Longitud: {gene_length} bp)")
                
                # Extraemos la secuencia interna del gen para analizar su interior
                gene_sequence = seq[start:end]
                
                # HEURÍSTICA DE SPLICING: 
                # Los intrones en eucariotas casi siempre empiezan con las letras 'GT' y terminan con 'AG' (sitios donor/acceptor)
                intron_pattern = re.compile(r'GT[ATGC]{10,200}AG')
                introns = list(intron_pattern.finditer(gene_sequence))
                
                if introns:
                    print(f"  * Estructura interna (Descompilada por heurística de Splicing):")
                    last_pos = 0
                    for i, intr in enumerate(introns):
                        intr_start, intr_end = intr.span()
                        
                        # Si hay espacio antes del intrón, es un Exón
                        if intr_start > last_pos:
                            print(f"    - [EXÓN {i+1}] (código activo): relativas {last_pos} - {intr_start}")
                            
                        print(f"    - [INTRÓN {i+1}] (eliminado en pre-mRNA, inicia con GT y termina con AG): relativas {intr_start} - {intr_end}")
                        last_pos = intr_end
                        
                    # Exón final
                    if last_pos < len(gene_sequence):
                        print(f"    - [EXÓN FINAL] (código activo): relativas {last_pos} - {len(gene_sequence)}")
                else:
                    print(f"  * Estructura: Gen continuo sin intrones detectados (posible exón único).")

        print("-" * 50)
        print(f"\n=== 3. PARTES NO CODIFICANTES (ADN INTERGÉNICO / BASURA) ===")
        print(f"Todo el espacio restante en el genoma que no forma parte de los ORFs detectados ")
        print(f"ni de los promotores opera como regiones espaciadoras, intrones masivos o secuencias reguladoras no mapeadas.")

if __name__ == "__main__":
    # Sustituye por el nombre exacto de tu archivo FASTA
    archivo_fasta = "NC 064231.1 Spodoptera frugiperda.fasta"
    
    try:
        analyzer = DNAStaticAnalyzer(archivo_fasta)
        analyzer.scan_genome()
    except FileNotFoundError:
        print(f"No se encontró el archivo '{archivo_fasta}'. Revisa la ruta.")
