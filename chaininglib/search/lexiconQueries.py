import chaininglib.utils.stringutils as stringutils

    
def lexicon_query(word, pos, lexicon):
    '''
    This function builds a query for getting the paradigm etc. of a given lemma out of a given lexicon.
    The resulting query string is to be used in LexiconQuery.search() 
    
    Args:
        word: a lemma/wordform to build the query with
        pos: a part-of-speech to build the query with
        lexicon: a lexicon to build the query for
    Returns:
        a query string to be used as a parameter of pattern() 
    '''
  
    if word is None:
        return _lexicon_query_alllemmata(lexicon, pos)
    
    if (lexicon=="anw"):
        # part-of-speech filter not supported for this lexicon
        if (pos is not None and pos != ''):
            print('Filtering by part-of-speech is not (yet) supported in the \''+lexicon+'\' lexicon')
        # exact or fuzzy search
        exactsearch = (not stringutils.containsRegex(word))
        subpart = """FILTER ( regex(?lemma, \""""+word+"""\") || regex(?definition, \""""+word+"""\") ) . """
        if (exactsearch == True):
              subpart =  """
                { { ?lemId rdfs:label ?lemma .  
                values ?lemma { \""""+word+"""\"@nl \""""+word+"""\" } }                 
                UNION
                { ?definitionId lemon:value ?definition .
                values ?definition { \""""+word+"""\"@nl \""""+word+"""\" } } } .
                """               
        query = """PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#>
                  PREFIX anw: <http://rdf.ivdnt.org/lexica/anw>
                  PREFIX anwsch: <http://rdf.ivdnt.org/schema/anw/>
                  PREFIX lemon: <http://lemon-model.net/lemon#>
                  
                  SELECT ?lemId ?lemma ?writtenForm ?definition concat('', ?definitionComplement) as ?definitionComplement
                  FROM <http://rdf.ivdnt.org/lexica/anw>
                  WHERE {
                      ?lemId rdfs:label ?lemma .
                      ?lemId ontolex:sense ?senseId .
                      ?senseId lemon:definition ?definitionId .
                      ?definitionId lemon:value ?definition .
                      OPTIONAL { ?definitionId anwsch:definitionComplement ?definitionComplement .}
                      OPTIONAL { ?lemId ontolex:canonicalForm ?lemCFId . 
                          ?lemCFId ontolex:writtenRepresentation ?writtenForm . }
                      """+subpart+"""
                      }"""
    elif (lexicon=="diamant"):
        # part-of-speech filter not supported for this lexicon
        if (pos is not None and pos != ''):
            print('Filtering by part-of-speech is not (yet) supported in the \''+lexicon+'\' lexicon')
        # exact or fuzzy search
        exactsearch = (not stringutils.containsRegex(word))
        subpart1 = """?n_form ontolex:writtenRep ?n_ontolex_writtenRep . 
            FILTER regex(?n_ontolex_writtenRep, \""""+word+"""\") . """
        subpart2 = """?n_syndef diamant:definitionText ?n_syndef_definitionText .  
            FILTER regex(?n_ontolex_writtenRep, \""""+word+"""\") . """
        if (exactsearch == True):
            subpart1 =  """
                { ?n_form ontolex:writtenRep ?n_ontolex_writtenRep . 
                values ?n_ontolex_writtenRep { \""""+word+"""\"@nl \""""+word+"""\" } } 
                """                
            subpart2 = """
                { ?n_syndef diamant:definitionText ?n_syndef_definitionText . 
                values ?n_syndef_definitionText { \""""+word+"""\"@nl \""""+word+"""\" } } 
                """
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
            """ + subpart1 + """
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
            """ + subpart2 + """
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
    elif (lexicon=="molex"):
        # exact or fuzzy search
        exactsearch = (not stringutils.containsRegex(word))
        subpart1 = """"""
        subpart2 = """"""
        subpartPos = """"""
        if (word != ''):
            if (exactsearch == True):
                subpart1 =  """
                    { ?lemCFId ontolex:writtenRep ?lemma . 
                    values ?lemma { \""""+word+"""\"@nl \""""+word+"""\" } } 
                    UNION
                    { ?wordformId ontolex:writtenRep ?wordform . 
                    values ?wordform { \""""+word+"""\"@nl \""""+word+"""\" } } .
                    """        
            else:
                subpart2 = """FILTER ( regex(?lemma, \""""+word+"""\") || regex(?wordform, \""""+word+"""\") ) . """
        if (pos is not None and pos != ''):
            subpartPos = """FILTER ( regex(?lemPos, \""""+pos+"""$\") ) ."""
        query = """
            PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#>
            PREFIX UD: <http://universaldependencies.org/u/>
            PREFIX diamant: <http://rdf.ivdnt.org/schema/diamant#>
            
            SELECT ?lemEntryId ?lemma ?lemPos ?wordformId ?wordform ?hyphenation ?wordformPos ?Gender ?Number
            FROM <http://rdf.ivdnt.org/lexica/molex>
            WHERE
            {
            ?lemEntryId ontolex:canonicalForm ?lemCFId .
            ?lemCFId ontolex:writtenRep ?lemma .
            """+subpart1+"""
            OPTIONAL {?lemEntryId UD:Gender ?Gender .}
            OPTIONAL {?lemEntryId UD:VerbForm ?verbform .}
            ?lemEntryId UD:pos ?lemPos .
            """+subpartPos+"""
            ?lemEntryId ontolex:lexicalForm ?wordformId .
            ?wordformId UD:pos ?wordformPos .
            OPTIONAL {?wordformId UD:Number ?Number .}
            OPTIONAL {?wordformId ontolex:writtenRep ?wordform .}
            OPTIONAL {?wordformId diamant:hyphenation ?hyphenation .}
            """+subpart2+"""
            }
        """
    elif (lexicon=="duelme"):
        # part-of-speech filter not supported for this lexicon
        if (pos is not None and pos != ''):
            print('Filtering by part-of-speech is not (yet) supported in the \''+lexicon+'\' lexicon')
        # exact or fuzzy search
        exactsearch = (not stringutils.containsRegex(word))
        subpart = """FILTER ( regex(?lemma, \""""+word+"""\") || regex(?wordform, \""""+word+"""\") ) ."""
        if (exactsearch == True):
            subpart =  """
                { ?y lmf:hasLemma ?dl .  
                values ?dl { \""""+word+"""\"@nl \""""+word+"""\" } }                 
                """        
        query = """
            PREFIX duelme: <http://rdf.ivdnt.org/lexica/duelme>
            PREFIX intskos: <http://ivdnt.org/schema/lexica#>
            PREFIX lmf: <http://www.lexinfo.net/lmf>
            PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#>
            PREFIX UD: <http://rdf.ivdnt.org/vocabs/UniversalDependencies2#>
            
            SELECT ?exampleSentence ?lemma ?gender ?number
            WHERE  {
                  ?d intskos:ExampleSentence ?exampleSentence .
                  ?d lmf:ListOfComponents [lmf:Component ?y] .
                  ?y lmf:hasLemma ?lemma . 
                  OPTIONAL {?y UD:Gender ?gender}
                  OPTIONAL {?y UD:Number ?number}
            """+subpart+"""
            }
        """
    elif (lexicon=="celex"):
        # part-of-speech filter not supported for this lexicon
        if (pos is not None and pos != ''):
            print('Filtering by part-of-speech is not (yet) supported in the \''+lexicon+'\' lexicon')
        # exact or fuzzy search
        exactsearch = (not stringutils.containsRegex(word))
        subpart = """FILTER ( regex(?lemma, \""""+word+"""\") ) . """
        if (exactsearch == True):
            subpart =  """
                { ?lemmaId ontolex:canonicalForm [ontolex:writtenRep ?lemma] .  
                values ?lemma { \""""+word+"""\"@nl \""""+word+"""\" } }                 
                """        
        query = """
            PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#>
            PREFIX celex: <http://rdf.ivdnt.org/lexica/celex>
            PREFIX UD: <http://rdf.ivdnt.org/vocabs/UniversalDependencies2#>
            PREFIX decomp: <http://www.w3.org/ns/lemon/decomp#>
            PREFIX gold: <http://purl.org/linguistics/gold#>
            
            SELECT DISTINCT ?lemmaId ?lemma ?wordformId ?wordform ?number ?gender concat('', ?subLemmata) AS ?subLemmata
            WHERE  {
                ?lemmaId ontolex:canonicalForm [ontolex:writtenRep ?lemma] .
                """+subpart+"""
                BIND( ?lemmaId AS ?lemmaIdIRI ).
                ?lemmaId ontolex:lexicalForm ?wordformId .
                ?wordformId ontolex:writtenRep ?wordform .
                OPTIONAL {?wordformId UD:Number ?number} .
                OPTIONAL {
                    ?lemmaId UD:Gender ?g . 
                        bind( 
                            if(?g = UD:Fem_Gender, 
                            UD:Com_Gender, 
                                if(?g = UD:Masc_Gender,
                                    UD:Com_Gender,
                                    UD:Neut_Gender
                                )
                            )
                            AS ?gender
                        )
                }
                OPTIONAL {
                    SELECT ?lemmaIdIRI (group_concat(DISTINCT concat(?partNr,":",?subLemma);separator=" + ") as ?subLemmata)
                    WHERE {
                        SELECT ?lemmaIdIRI ?celexComp ?aWordformId ?subLemma ?partNr
                        WHERE {
                                {
                                ?lemmaIdIRI ontolex:lexicalForm ?aWordformId . 
                                ?lemmaIdIRI decomp:constituent ?celexComp .
                                OPTIONAL { ?celexComp gold:stem [ontolex:writtenRep ?subLemma] . }
                                OPTIONAL { ?celexComp decomp:correspondsTo [ ontolex:canonicalForm [ontolex:writtenRep ?subLemma]] . }
                                }
                                {
                                    {
                                        {?lemmaIdIRI <http://www.w3.org/1999/02/22-rdf-syntax-ns#_1> ?celexComp .}
                                        UNION
                                        {?lemmaIdIRI <http://www.w3.org/1999/02/22-rdf-syntax-ns#_2> ?celexComp .}
                                        UNION
                                        {?lemmaIdIRI <http://www.w3.org/1999/02/22-rdf-syntax-ns#_3> ?celexComp .}
                                        UNION
                                        {?lemmaIdIRI <http://www.w3.org/1999/02/22-rdf-syntax-ns#_4> ?celexComp .}
                                        UNION
                                        {?lemmaIdIRI <http://www.w3.org/1999/02/22-rdf-syntax-ns#_5> ?celexComp .}
                                        UNION
                                        {?lemmaIdIRI <http://www.w3.org/1999/02/22-rdf-syntax-ns#_6> ?celexComp .}                                        
                                    }
                                ?lemmaIdIRI ?rdfsynt ?celexComp .
                                BIND(IF(STRSTARTS(str(?rdfsynt), "http://www.w3.org/1999/02/22-rdf-syntax-ns#"), replace(STRAFTER(str(?rdfsynt), "#"), "_", ""), "999") AS ?partNr) .
                                MINUS {
                                    ?lemmaIdIRI <http://www.w3.org/1999/02/22-rdf-syntax-ns#0> ?celexComp .
                                    }
                                }
                            FILTER (?partNr != "999") .
                            }
                            ORDER BY ?partNr
                            }
                        GROUP BY ?aWordformId ?lemmaIdIRI
                    }
            }
        """
    else:
        raise ValueError("Lexicon " + lexicon + " unknown!")
        
    return query



def _lexicon_query_alllemmata(lexicon, pos):
    '''
    This function builds a query for getting all lemmata of a lexicon, if needed restricted to a given part-of-speech.
    The resulting query string is to be used as a parameter of search_lexicon().
    
    Args:
        lexicon: a lexicon name 
        pos: (optional) a part-of-speech
    Returns:
        a lexicon query string
    '''
    
    if (lexicon=="anw"):
        # part-of-speech filter not supported for this lexicon
        if (pos is not None and pos != ''):
            print('Filtering by part-of-speech is not (yet) supported in the \''+lexicon+'\' lexicon')
        query = """PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#>
                  PREFIX anw: <http://rdf.ivdnt.org/lexica/anw>                  
                  SELECT DISTINCT ?writtenForm
                  FROM <http://rdf.ivdnt.org/lexica/anw>
                  WHERE {
                      ?lemId rdfs:label ?lemma .
                      ?lemId ontolex:canonicalForm ?lemCFId . 
                      ?lemCFId ontolex:writtenRepresentation ?writtenForm .
                      }
                      ORDER BY ?writtenForm"""
    elif (lexicon=="celex"):
        # part-of-speech filter not supported for this lexicon
        if (pos is not None and pos != ''):
            print('Filtering by part-of-speech is not (yet) supported in the \''+lexicon+'\' lexicon')
        query = """
            PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#>
            
            SELECT DISTINCT ?lemma AS ?writtenForm
            WHERE  {
                ?lemmaId ontolex:canonicalForm [ontolex:writtenRep ?lemma] .                
                }
            ORDER BY ?lemma"""
    elif (lexicon=="diamant"):
        # part-of-speech filter not supported for this lexicon
        if (pos is not None and pos != ''):
            print('Filtering by part-of-speech is not (yet) supported in the \''+lexicon+'\' lexicon')
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

        select DISTINCT ?n_ontolex_writtenRep AS ?writtenForm
        where
        {
        graph ?g
        {
        {
            { ?n_form ontolex:writtenRep ?n_ontolex_writtenRep} .
            { ?n_form a ontolex:Form} .
        }
        }
        }
        ORDER BY ?n_ontolex_writtenRep
        LIMIT 10000
        """
    elif (lexicon=="duelme"):
        # part-of-speech filter not supported for this lexicon
        if (pos is not None and pos != ''):
            print('Filtering by part-of-speech is not (yet) supported in the \''+lexicon+'\' lexicon')
        query = """
            PREFIX lmf: <http://www.lexinfo.net/lmf>            
            SELECT DISTINCT ?lemma AS ?writtenForm
            WHERE  {
                  ?y lmf:hasLemma ?lemma . 
            }
            ORDER BY ?lemma"""
    elif (lexicon=="molex"):
        # part-of-speech filter
        pos_condition = """"""
        if pos is not None and pos != '':
            pos_condition = """
            {?lemEntryId UD:pos ?lemPos .
            FILTER regex(?lemPos, '"""+pos+"""') } .
            """
        query = """
                PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#>
                PREFIX UD: <http://universaldependencies.org/u/>
                SELECT DISTINCT ?lemma AS ?writtenForm
                FROM <http://rdf.ivdnt.org/lexica/molex>
                WHERE
                {
                ?lemEntryId ontolex:canonicalForm ?lemCFId .
                ?lemCFId ontolex:writtenRep ?lemma .  
                """+pos_condition+"""
                }
                 ORDER BY ?lemma"""
    else:
        raise ValueError("Lexicon " + lexicon + " not supported for querying all words.")
        
    #print(query)
    return query

