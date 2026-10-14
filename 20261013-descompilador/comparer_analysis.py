from Bio import SeqIO
import re

def compare_results(gb_filepath, fasta_filepath):
    print(f"=== INICIANDO COMPARACIÓN DE ANÁLISIS ===")
    
    # 1. CARGAR LA VERDAD OFICIAL (GenBank)
    print(f"Leyendo anotaciones oficiales de: {gb_filepath}...")
    gb_record = next(SeqIO.parse(gb_filepath, "genbank"))
    
    official_genes = []
    for feature in gb_record.features:
        if feature.type == "gene":
            gene_name = feature.qualifiers.get("gene", feature.qualifiers.get("locus_tag", ["UNKNOWN"]))[0]
            official_genes.append({
                "name": gene_name,
                "start": int(feature.location.start),
                "end": int(feature.location.end)
            })
    print(f"-> Se encontraron {len(official_genes)} genes en la anotación oficial del GenBank.\n")

    # 2. EJECUTAR EL ANALIZADOR ESTÁTICO (Sobre el FASTA o la secuencia del GenBank)
    print(f"Ejecutando el analizador heurístico (*ab initio*) sobre la secuencia...")
    seq = str(gb_record.seq).upper()
    
    # Buscador de ORFs heurístico (igual que en el script anterior)
    orf_pattern = re.compile(r'ATG(?:[ATGC]{3})+?(?:TAA|TAG|TGA)')
    heuristic_genes = []
    
    for match in orf_pattern.finditer(seq):
        start, end = match.span()
        if (end - start) > 300:  # Filtro de tamaño viable
            heuristic_genes.append({"start": start, "end": end})
            
    print(f"-> El analizador heurístico detectó {len(heuristic_genes)} regiones candidatas a genes.\n")

    # 3. COMPARATIVA DE RESULTADOS
    print("=" * 60)
    print(f"{'VERDAD OFICIAL (GenBank)':<30} | {'HEURÍSTICA (Analizador Estático)':<30}")
    print("=" * 60)
    
    max_rows = max(len(official_genes), len(heuristic_genes))
    for i in range(min(max_rows, 10)):  # Mostramos una muestra de los primeros 10
        off_str = f"{official_genes[i]['name']} ({official_genes[i]['start']}-{official_genes[i]['end']})" if i < len(official_genes) else "---"
        
        if i < len(heuristic_genes):
            heur_str = f"ORF candidato ({heuristic_genes[i]['start']}-{heuristic_genes[i]['end']})"
        else:
            heur_str = "---"
            
        print(f"{off_str:<30} | {heur_str:<30}")
        
    print("=" * 60)
    print("\n[CONCLUSIÓN DE LA COMPARATIVA]:")
    print("El analizador estático (heurístico) es capaz de adivinar 'dónde hay código' buscando patrones de inicio/parada,")
    print("pero carece de contexto biológico profundo. A menudo detecta marcos de lectura abiertos que el organismo real")
    print("no utiliza, o cuyas fronteras de exones/intrones precisas solo pueden validarse mediante transcripტომas (RNA-seq)")
    print("y anotación curada por expertos (como la que refleja el archivo GenBank).")

if __name__ == "__main__":
    archivo_gb = "sequence.gb"
    archivo_fasta = "NC 064231.1 Spodoptera frugiperda.fasta" # O usa la secuencia embebida en el GenBank
    
    try:
        compare_results(archivo_gb, archivo_fasta)
    except FileNotFoundError as e:
        print(f"Error de archivo: {e}. Asegúrate de tener 'sequence.gb' en la carpeta.")
