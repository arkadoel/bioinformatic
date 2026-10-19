#!/usr/bin/env python3
"""
Simulador de Traducción de ARNm a Proteína (Disassembler genético básico).
"""

# Diccionario estándar de codones de ARN (Codón -> Aminoácido / Control)
GENETIC_CODE = {
    # Fenilalanina / Leucina
    'UUU': 'F', 'UUC': 'F', 'UUA': 'L', 'UUG': 'L',
    # Leucina / Serina
    'CUU': 'Cuc', 'CUC': 'Cuc', 'CUA': 'Cuc', 'CUG': 'Cuc', # Simplificado para el ejemplo o nombres de 3 letras
    # Usemos mejor el código de 1 letra estándar, que es el más limpio:
    'UCU': 'S', 'UCC': 'S', 'UCA': 'S', 'UCG': 'S',
    'UAU': 'Y', 'UAC': 'Y', 'UAA': 'STOP', 'UAG': 'STOP',
    'UGU': 'C', 'UGC': 'C', 'UGA': 'STOP', 'UGG': 'W',
    
    'CUU': 'L', 'CUC': 'L', 'CUA': 'L', 'CUG': 'L',
    'CCU': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
    'CAU': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
    'CGU': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
    
    'AUU': 'I', 'AUC': 'I', 'AUA': 'I', 'AUG': 'M', 'AUG (START)': 'M', # AUG es Inicio y Metionina
    'ACU': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
    'AAU': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
    'AGU': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
    
    'GUU': 'V', 'GUC': 'V', 'GUA': 'V', 'GUG': 'V',
    'GCU': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
    'GAU': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
    'GGU': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G',
}

def translate_mrna(mrna_sequence: str) -> list[str]:
    """
    Busca el codón de inicio (AUG), traduce de 3 en 3 nucleótidos 
    y se detiene al encontrar un codón de parada (STOP).
    """
    mrna_sequence = mrna_sequence.upper().replace(" ", "")
    amino_acids = []
    
    # 1. Buscar el codón de inicio (AUG)
    start_index = mrna_sequence.find("AUG")
    if start_index == -1:
        print("[!] Error: No se encontró ningún codón de inicio (AUG) en la secuencia.")
        return []
    
    print(f"[*] Codón de inicio (AUG) encontrado en la posición: {start_index}")
    
    # 2. Leer en bloques de 3 (tripletes) a partir del inicio
    i = start_index
    while i < len(mrna_sequence) - 2:
        codon = mrna_sequence[i:i+3]
        aminoacid = GENETIC_CODE.get(codon, 'X') # 'X' para desconocidos
        
        # 3. Comprobar si es codón de parada
        if aminoacid == 'STOP':
            print(f"[*] Codón de parada encontrado ({codon}) en la posición {i}. Finalizando traducción.")
            break
            
        amino_acids.append(aminoacid)
        i += 3
        
    return amino_acids

# --- Bloque de pruebas ---
if __name__ == "__main__":
    # Secuencia de ARN simulada: tiene basura al inicio, un AUG, codones y un STOP (UAA)
    sample_mrna = "GGCCAUGGCCGGGUUAAUGAC"
    
    print(f"Secuencia de ARN de entrada: {sample_mrna}\n")
    protein_chain = translate_mrna(sample_mrna)
    
    print("\n--- Resultado del 'Descompilador' ---")
    print("Estructura Primaria (Secuencia de aminoácidos):", "-".join(protein_chain))
    print("Longitud de la proteína (nº de aminoácidos):", len(protein_chain))
