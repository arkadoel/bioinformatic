from Bio import SeqIO
from Bio.Seq import Seq
import re

def analizar_genbank_y_fasta(gb_filepath, fasta_filepath):
    print("=" * 70)
    print("1. INSPECCIONANDO DIRECCIONES Y PROMOTORES EN EL GENBANK")
    print("=" * 70)
    
    gb_record = next(SeqIO.parse(gb_filepath, "genbank"))
    
    gb_strands = {"+": 0, "-": 0}
    promoter_keywords = 0
    
    for feature in gb_record.features:
        if feature.type == "gene":
            strand = feature.location.strand
            if strand == 1:
                gb_strands["+"] += 1
            elif strand == -1:
                gb_strands["-"] += 1
                
        # Buscar menciones explícitas de promotores en las notas del GenBank si las hubiera
        if feature.type in ["promoter", "TATA_signal", "-10_signal", "-35_signal"]:
            promoter_keywords += 1

    print(f"Total de genes oficiales analizados en GenBank:")
    print(f"  - Hebra positiva (+): {gb_strands['+']} genes")
    print(f"  - Hebra negativa (-): {gb_strands['-']} genes")
    print(f"  - Elementos reguladores/promotores explícitamente anotados: {promoter_keywords}\n")

    print("=" * 70)
    print("2. ANALIZADOR HEURÍSTICO RELAJADO SOBRE EL FASTA")
    print("=" * 70)
    print(f"Leyendo secuencia FASTA desde: {fasta_filepath}...")
    
    fasta_record = next(SeqIO.parse(fasta_filepath, "fasta"))
    seq = str(fasta_record.seq).upper()
    
    # RELAJAMOS LA TATA: Usamos un patrón flexible que engloba variantes de cajas ricas en AT (TATA, TATAA, TAAA, etc.)
    # y motivos de iniciación alternativos comunes en eucariotas.
    flexible_promoter_pattern = re.compile(r'TA[TA][AT]A[AT]|CAAT|GGGCGG')
    orf_pattern = re.compile(r'ATG(?:[ATGC]{3})+?(?:TAA|TAG|TGA)')
    
    candidates_fwd = 0
    candidates_rev = 0
    
    # Escanear hebra directa (+)
    print("Escaneando hebra directa (+) con patrones relajados...")
    promoters_fwd = [m.start() for m in flexible_promoter_pattern.finditer(seq)]
    for match in orf_pattern.finditer(seq):
        start, end = match.span()
        if (end - start) > 250: # Umbral de tamaño flexible
            # Comprobar si hay algún motivo promotor flexible aguas arriba (hasta 300 nucleótidos antes)
            if any((start - 300) <= p_pos < start for p_pos in promoters_fwd):
                candidates_fwd += 1

    # Escanear hebra complementaria (-)
    print("Escaneando hebra complementaria (-) con patrones relajados...")
    rc_seq = str(Seq(seq).reverse_complement())
    promoters_rc = [m.start() for m in flexible_promoter_pattern.finditer(rc_seq)]
    for match in orf_pattern.finditer(rc_seq):
        start, end = match.span()
        if (end - start) > 250:
            if any((start - 300) <= p_pos < start for p_pos in promoters_rc):
                candidates_rev += 1

    print("\n" + "=" * 70)
    print("RESUMEN DE HALLAZGOS DEL ANALIZADOR HEURÍSTICO FLEXIBLE:")
    print("=" * 70)
    print(f"  - Candidatos detectados en hebra directa (+): {candidates_fwd}")
    print(f"  - Candidatos detectados en hebra negativa (-): {candidates_rev}")
    print(f"  - Total de candidatos viables con promotores relajados: {candidates_fwd + candidates_rev}")
    print("=" * 70)

if __name__ == "__main__":
    archivo_gb = "sequence.gb"
    archivo_fasta = "NC 064231.1 Spodoptera frugiperda.fasta"
    
    try:
        analizar_genbank_y_fasta(archivo_gb, archivo_fasta)
    except FileNotFoundError as e:
        print(f"Error de archivo: {e}. Comprueba que los nombres de los archivos coinciden en la carpeta.")
