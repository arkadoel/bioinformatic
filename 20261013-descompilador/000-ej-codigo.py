from genomic_parser import Chromosome, Gene, Exon, Intron, IntergenicRegion, Transposon

@chromosome(name="Chromosome_X", total_base_pairs=150000000)
def complete_dna_decompilation():
    """
    Representación completa de un fragmento de ADN: 
    Incluye código activo (Exones), código preprocesado (Intrones) 
    y código muerto / estructural (ADN Basura / Intergénico).
    """

    # -------------------------------------------------------------
    # 1. ZONA NO CODIFICANTE / INTERGÉNICAS ("ADN Basura" o Legacy Code)
    # -------------------------------------------------------------
    with IntergenicRegion(start=1, end=45200, classification="junk_spacer"):
        # Equivalente a bloques de comentarios masivos o código comentado de versiones antiguas
        notes = "Región espaciadora sin transcripción conocida. Alta densidad de repeticiones."
        element_type = "Satellite_DNA"


    # -------------------------------------------------------------
    # 2. BLOQUE DE UN GEN ACTIVO (Con Exones e Intrones)
    # -------------------------------------------------------------
    @gene(id="GENE_4201", symbol="Kinase_Complex_A", strand="+")
    def target_gene():
        
        # Cabecera / Promotor (El punto de entrada del sistema de transcripción)
        promoter(start=45201, end=45350, sequence="TATAAA...")

        # El ARN Mensajero preliminar (Pre-mRNA antes del "Splicing")
        with PreMRTranscript(start=45351, end=52000):
            
            # EXÓN 1: Fragmento de código que SÍ sobrevive a la compilación
            exon(index=1, start=45351, end=45500, sequence="ATGAAG...", role="coding_start")
            
            # INTRÓN 1: Bloque intermedio. Se elimina antes de generar la proteína final.
            # Equivalente a una directiva de preprocesador o una macro que se borra en tiempo de compilación.
            intron(index=1, start=45501, end=46800, sequence="GT...AG", status="spliced_out")
            
            # EXÓN 2: Siguiente fragmento de código funcional
            exon(index=2, start=46801, end=47100, sequence="CCAGTC...", role="coding_middle")
            
            # INTRÓN 2: Otro bloque descartado en el filtrado de ARN
            intron(index=2, start=47101, end=50500, sequence="GT...AG", status="spliced_out")
            
            # EXÓN 3: Bloque final del gen
            exon(index=3, start=50501, end=52000, sequence="GCCC...", role="coding_end")

        terminator(start=52001, end=52050)


    # -------------------------------------------------------------
    # 3. ELEMENTOS MÓVILES / TRANSPOSONES (El "código espagueti" o virus insertados)
    # -------------------------------------------------------------
    with Transposon(start=52051, end=65000, classification="retrotransposon_Alu"):
        # Bloques de ADN que se autorreplicaban y se metieron ahí por error histórico.
        # En informática sería código copiado y pegado de otro programa antiguo que ya no hace nada.
        status = "inactive_genomic_parasite"
        mutation_rate = "high"

