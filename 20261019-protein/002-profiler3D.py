import py3Dmol

# Crear un visor 3D y cargar una proteína real por su código ID universal (ej. la Insulina, código 1TRZ)
view = py3Dmol.view(query='pdb:1TRZ')
view.setStyle({'cartoon': {'color': 'spectrum'}}) # Estilo de cinta de colores
view.show()

'''
pip install jupyter
jupyter lab
'''
