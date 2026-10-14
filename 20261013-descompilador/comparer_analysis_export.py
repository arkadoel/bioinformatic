from Bio import SeqIO
import re
import os

def compare_and_export_results(gb_filepath, fasta_filepath):
    print(f"=== INICIANDO COMPARACIÓN Y EXPORTACIÓN DE GENES ===")
    
    # 1. CREAR LA CARPETA DE EXPORTACIÓN
    export_dir = "genes_exportados"
    os.makedirs(os.path.join(export_dir, "oficiales_genbank"), exist_ok=True)
    os.makedirs(os.path.join(export_dir, "heuristicos_estaticos"), exist_ok=True)
    
    # 2. CARGAR LA VERDAD OFICIAL (GenBank)
    print(f"Leyendo anotaciones oficiales de: {gb_filepath}...")
    gb_record = next(SeqIO.parse(gb_filepath, "genbank"))
    seq = str(gb_record.seq).upper()
    
    official_genes = []
    for feature in gb_record.features:
        if feature.type == "gene":
            gene_name = feature.qualifiers.get("gene", feature.qualifiers.get("locus_tag", ["UNKNOWN"]))[0]
            start = int(feature.location.start)
            end = int(feature.location.end)
            official_genes.append({
                "name": gene_name,
                "start": start,
                "end": end,
                "sequence": seq[start:end]
            })
            
    print(f"-> Se encontraron {len(official_genes)} genes oficiales. Exportándolos...")
    
    # Exportar cada gen oficial a un archivo individual
    for i, og in enumerate(official_genes):
        filename = f"{export_dir}/oficiales_genbank/gene_{i+1}_{og['name']}.txt"
        with open(filename, "w") as f:
            f.write(f">Oficial_{og['name']} range:{og['start']}-{og['end']}\n")
            f.write(og['sequence'] + "\n")

    # 3. EJECUTAR EL ANALIZADOR ESTÁTICO (Sobre la secuencia)
    print(f"Ejecutando el analizador heurístico (*ab initio*) sobre la secuencia...")
    orf_pattern = re.compile(r'ATG(?:[ATGC]{3})+?(?:TAA|TAG|TGA)')
    heuristic_genes = []
    
    for match in orf_pattern.finditer(seq):
        start, end = match.span()
        if (end - start) > 300:  # Filtro de tamaño viable
            heuristic_genes.append({
                "start": start,
                "end": end,
                "sequence": seq[start:end]
            })
            
    print(f"-> El analizador detectó {len(heuristic_genes)} candidatos. Exportándolos...")
    
    # Exportar cada candidato heurístico a un archivo individual
    for i, hg in enumerate(heuristic_genes):
        filename = f"{export_dir}/heuristicos_estaticos/candidato_{i+1}_pos_{hg['start']}_{hg['end']}.txt"
        with open(filename, "w") as f:
            f.write(f">Candidato_Heuristico range:{hg['start']}-{hg['end']}\n")
            f.write(hg['sequence'] + "\n")

    print(f"\n¡Exportación completada con éxito!")
    print(f"Los archivos se han guardado en la carpeta './{export_dir}/' organizados en subcarpetas.")

    # 4. TABLA COMPARATIVA BÁSICA
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

if __name__ == "__main__":
    archivo_gb = "sequence.gb"
    archivo_fasta = "NC 064231.1 Spodoptera frugiperda.fasta"
    
    try:
        compare_and_export_results(archivo_gb, archivo_fasta)
    except FileNotFoundError as e:
        print(f"Error de archivo: {e}. Asegúrate de tener los archivos en la carpeta.")
