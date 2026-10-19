import matplotlib.pyplot as plt

# Escala de Kyte-Doolittle (hidrofobicidad estándar: positivo = ama la grasa/odia agua, negativo = ama el agua)
HYDROPHOBICITY_SCALE = {
    'I': 4.5, 'V': 4.2, 'L': 3.8, 'F': 2.8, 'C': 2.5, 'M': 1.9, 'A': 1.8, 
    'G': -0.4, 'T': -0.7, 'S': -0.8, 'W': -0.9, 'Y': -1.3, 'P': -1.6, 
    'H': -3.2, 'E': -3.5, 'Q': -3.5, 'D': -3.5, 'N': -3.5, 'K': -3.9, 'R': -4.5
}

def plot_protein_profile(amino_acids: list[str]):
    """Genera una gráfica de perfil de hidrofobicidad de la proteína."""
    # Convertir aminoácidos a sus valores numéricos
    scores = [HYDROPHOBICITY_SCALE.get(aa, 0.0) for aa in amino_acids]
    
    # Pintar con Matplotlib
    plt.figure(figsize=(10, 4))
    plt.plot(scores, marker='o', linestyle='-', color='b', linewidth=2)
    plt.axhline(0, color='r', linestyle='--', alpha=0.5, label='Límite Neutro')
    
    plt.title('Perfil de Hidrofobicidad de la Proteína (Estructura Primaria)')
    plt.xlabel('Posición del Aminoácido')
    plt.ylabel('Hidrofobicidad')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Ejemplo rápido si tienes la cadena de aminoácidos
if __name__ == "__main__":
    cadena_ejemplo = ['M', 'A', 'G', 'I', 'V', 'L', 'K', 'E', 'D', 'F']
    plot_protein_profile(cadena_ejemplo) # Descomenta para ejecutar si tienes matplotlib instalado
