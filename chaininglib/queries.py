
def get_query(word, lexicon):
    if (lexicon=="anw"):
        subpart = 'FILTER ( regex(?lemma, "'+word+'") || regex(?definition, "'+word+'") ) .\n'
        query = """PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#>\n
                  PREFIX anw: <http://rdf.ivdnt.org/lexica/anw>\n
                  PREFIX anwsch: <http://rdf.ivdnt.org/schema/anw/>\n
                  PREFIX lemon: <http://lemon-model.net/lemon#>\n
                  \n
                  SELECT ?lemId ?lemma ?writtenForm ?definition ?definitionComplement\n
                  FROM <http://rdf.ivdnt.org/lexica/anw>\n
                  WHERE {\n
                      ?lemId rdfs:label ?lemma .\n
                      ?lemId ontolex:sense ?senseId .\n
                      ?senseId lemon:definition ?definitionId .\n
                      ?definitionId lemon:value ?definition .\n
                      OPTIONAL { ?definitionId anwsch:definitionComplement ?definitionComplement .}\n
                      OPTIONAL { ?lemId ontolex:canonicalForm ?lemCFId . \n
                          ?lemCFId ontolex:writtenRepresentation ?writtenForm . }\n
                      """+subpart+"""\n
                      }\n"""
    elif (lexicon=="diamant"):
        query = """
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        prefix prov: <http://www.w3.org/ns/prov#>
        prefix diamant: <http://rdf.ivdnt.org/schema/diamant#>
        prefix lexinfo: <http://www.lexinfo.net/ontology/2.0/lexinfo#>
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        prefix lemon: <http://lemon-model.net/lemon#>
        prefix ontolex: <http://www.w3.org/ns/lemon/ontolex#>
        prefix ud: <http://universaldependencies.org/u/pos/>
        prefix skos: <http://www.w3.org/2004/02/skos/core#>
        prefix dcterms: <http://purl.org/dc/terms/>
        prefix dc: <http://purl.org/dc/terms/>

        select ?n_entry ?n_form ?n_ontolex_writtenRep ?n_syndef ?n_sensedef ?n_sensedef_definitionText ?n_syndef_definitionText ?n_sense ?inputMode ?wy_f_show ?wy_t_show
        where
        {
        graph ?g
        {
        {
            { ?n_form ontolex:writtenRep ?n_ontolex_writtenRep .
              values ?n_ontolex_writtenRep  { \"""" + word + """\" } } .
            { ?n_entry a ontolex:LexicalEntry} .
            { ?n_form a ontolex:Form} .
            { ?n_sense a ontolex:LexicalSense} .
            { ?n_syndef a diamant:SynonymDefinition} .
            { ?n_sensedef a lemon:SenseDefinition} .
            { ?n_syndef diamant:definitionText ?n_syndef_definitionText } .
            { ?n_sensedef diamant:definitionText ?n_sensedef_definitionText } .
            { ?n_entry ontolex:canonicalForm ?n_form } .
            { ?n_entry ontolex:sense ?n_sense } .
            { ?n_sense lemon:definition ?n_syndef } .
            { ?n_sense lemon:definition ?n_sensedef } .
              ?n_sense diamant:attestation ?n_attest_show .
              ?n_sense diamant:attestation ?n_attest_filter .
              ?n_attest_show diamant:text ?n_q_show .
              ?n_attest_filter diamant:text ?n_q_filter .
              ?n_attest_show a diamant:Attestation .
              ?n_attest_filter a diamant:Attestation .
              ?n_q_filter a diamant:Quotation .
              ?n_q_show a diamant:Quotation .
              ?n_q_filter diamant:witnessYearFrom ?wy_f_filter .
              ?n_q_filter diamant:witnessYearTo ?wy_t_filter .
              ?n_q_show diamant:witnessYearFrom ?wy_f_show .
              ?n_q_show diamant:witnessYearTo ?wy_t_show .
              FILTER (xsd:integer(?wy_f_show) >= 1200)
              FILTER (xsd:integer(?wy_t_show) >= 1200)
              FILTER (xsd:integer(?wy_f_show) <= 2018)
              FILTER (xsd:integer(?wy_t_show) <= 2018)
            { bind("lemma" as ?inputMode) } .
            } UNION
          {
            { ?n_syndef diamant:definitionText ?n_syndef_definitionText .
            values ?n_syndef_definitionText  { \"""" + word + """\" } } .
            { ?n_sense a ontolex:LexicalSense} .
            { ?n_syndef a diamant:SynonymDefinition} .
            { ?n_sensedef a lemon:SenseDefinition} .
            { ?n_form a ontolex:Form} .
            { ?n_form ontolex:writtenRep ?n_ontolex_writtenRep } .  { ?n_entry a ontolex:LexicalEntry} .
            { ?n_entry ontolex:sense ?n_sense } .
            { ?n_sense lemon:definition ?n_syndef } .
            { ?n_sense lemon:definition ?n_sensedef } .
            { ?n_sensedef diamant:definitionText ?n_sensedef_definitionText } .
            { ?n_entry ontolex:canonicalForm ?n_form } .
            ?n_sense diamant:attestation ?n_attest_show .
            ?n_sense diamant:attestation ?n_attest_filter .
            ?n_attest_filter diamant:text ?n_q_filter .
            ?n_attest_show diamant:text ?n_q_show .
            ?n_q_filter diamant:witnessYearFrom ?wy_f_filter .
            ?n_q_filter diamant:witnessYearTo ?wy_t_filter .
            ?n_q_show diamant:witnessYearFrom ?wy_f_show .
            ?n_q_show diamant:witnessYearTo ?wy_t_show .
            ?n_attest_show a diamant:Attestation .
            ?n_attest_filter a diamant:Attestation .
            ?n_q_filter a diamant:Quotation .
            ?n_q_show a diamant:Quotation .
            FILTER (xsd:integer(?wy_f_show) >= 1200)
            FILTER (xsd:integer(?wy_t_show) >= 1200)
            FILTER (xsd:integer(?wy_f_show) <= 2018)
            FILTER (xsd:integer(?wy_t_show) <= 2018)
          { bind("defText" as ?inputMode) } .
            }
        }
        }"""

        return query