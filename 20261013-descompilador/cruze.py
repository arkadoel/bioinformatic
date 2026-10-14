'''
Vamos a cruzar los datos de nuestros 335 candidatos heurísticos con las coordenadas oficiales del GenBank para ver cuántos han acertado de pleno cayendo dentro del rango real de un gen oficial, y cuántos se han quedado fuera.
'''


from Bio import SeqIO
from Bio.Seq import Seq
import re

def evaluar_aciertos_con_genbank(gb_filepath, fasta_filepath):
    print("=" * 70)
    print("EVALUACIÓN DE SOLAPAMIENTO: HEURÍSTICA VS GENBANK")
    print("=" * 70)
    
    # 1. Cargar la verdad oficial (GenBank)
    gb_record = next(SeqIO.parse(gb_filepath, "genbank"))
    seq = str(gb_record.seq).upper()
    
    official_genes = []
    for feature in gb_record.features:
        if feature.type == "gene":
            official_genes.append({
                "start": int(feature.location.start),
                "end": int(feature.location.end),
                "strand": feature.location.strand
            })
            
    print(f"-> Cargados {len(official_genes)} genes oficiales del GenBank.")

    # 2. Ejecutar nuestro analizador relajado sobre el FASTA
    fasta_record = next(SeqIO.parse(fasta_filepath, "fasta"))
    
    flexible_promoter_pattern = re.compile(r'TA[TA][AT]A[AT]|CAAT|GGGCGG')
    orf_pattern = re.compile(r'ATG(?:[ATGC]{3})+?(?:TAA|TAG|TGA)')
    
    validated_candidates = []
    
    # Escanear hebra directa (+)
    promoters_fwd = [m.start() for m in flexible_promoter_pattern.finditer(seq)]
    for match in orf_pattern.finditer(seq):
        start, end = match.span()
        if (end - start) > 250:
            if any((start - 300) <= p_pos < start for p_pos in promoters_fwd):
                validated_candidates.append({"start": start, "end": end, "strand": "+"})

    # Escanear hebra complementaria (-)
    rc_seq = str(Seq(seq).reverse_complement())
    promoters_rc = [m.start() for m in flexible_promoter_pattern.finditer(rc_seq)]
    for match in orf_pattern.finditer(rc_seq):
        r_start, r_end = match.span()
        if (r_end - r_start) > 250:
            if any((r_start - 300) <= p_pos < r_start for p_pos in promoters_rc):
                g_start = len(seq) - r_end
                g_end = len(seq) - r_start
                validated_candidates.append({"start": g_start, "end": g_end, "strand": "-"})

    print(f"-> Analizador heurístico detectó {len(validated_candidates)} candidatos viables.")
    print("Calculando solapamientos con la verdad oficial...\n")

    # Comprobar cuántos candidatos colisionan con algún gen oficial
    aciertos = 0
    falsos_positivos = 0

    for cand in validated_candidates:
        c_start, c_end, c_strand = cand["start"], cand["end"], cand["strand"]
        colisiona = False
        
        for og in official_genes:
            # Convertimos el entero de Biopython (1 o -1) a string ("+" o "-") para que coincidan
            og_strand_str = "+" if og["strand"] == 1 else "-"
            
            if c_strand == og_strand_str:
                # Fórmula de solapamiento de intervalos
                if max(c_start, og["start"]) <= min(c_end, og["end"]):
                    colisiona = True
                    break
                    
        if colisiona:
            aciertos += 1
        else:
            falsos_positivos += 1

    # 4. Mostrar informe final
    print("=" * 70)
    print("RESULTADOS DE LA AUDITORÍA ESTÁTICA:")
    print("=" * 70)
    print(f"  - Candidatos totales analizados: {len(validated_candidates)}")
    print(f"  - Coincidencias con genes oficiales (Aciertos): {aciertos}")
    print(f"  - Candidatos sin respaldo en GenBank (Falsos positivos/Nuevos): {falsos_positivos}")
    
    porcentaje = (aciertos / len(validated_candidates)) * 100 if len(validated_candidates) > 0 else 0
    print(f"  - Precisión de la heurística flexible: {porcentaje:.2f}%")
    print("=" * 70)

if __name__ == "__main__":
    archivo_gb = "sequence.gb"
    archivo_fasta = "NC 064231.1 Spodoptera frugiperda.fasta"
    
    try:
        evaluar_aciertos_con_genbank(archivo_gb, archivo_fasta)
    except FileNotFoundError as e:
        print(f"Error de archivo: {e}. Comprueba los nombres en la carpeta.")


'''
    Salida por pantalla:
(base)> conda activate bio_env
(bio_env) /.../20261013-descompilador pwsh> python ./cruze.py     
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
'''
