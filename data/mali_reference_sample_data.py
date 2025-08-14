"""
Sample data for Mali Reference Tables (TableRef 01-09)
This file contains initial data based on Mali's administrative structure
and statistical framework
"""

# TableRef 08: Mali Regions (Official administrative divisions)
MALI_REGIONS = [
    {
        "region_code": "01",
        "region_name": "Kayes",
        "region_capital": "Kayes",
        "population": 2540000,
        "surface": 119743.0
    },
    {
        "region_code": "02", 
        "region_name": "Koulikoro",
        "region_capital": "Koulikoro",
        "population": 2418000,
        "surface": 90120.0
    },
    {
        "region_code": "03",
        "region_name": "Sikasso", 
        "region_capital": "Sikasso",
        "population": 2625000,
        "surface": 71790.0
    },
    {
        "region_code": "04",
        "region_name": "Ségou",
        "region_capital": "Ségou", 
        "population": 2336000,
        "surface": 64821.0
    },
    {
        "region_code": "05",
        "region_name": "Mopti",
        "region_capital": "Mopti",
        "population": 2037000,
        "surface": 79017.0
    },
    {
        "region_code": "06",
        "region_name": "Tombouctou",
        "region_capital": "Tombouctou",
        "population": 681000,
        "surface": 408977.0
    },
    {
        "region_code": "07",
        "region_name": "Gao",
        "region_capital": "Gao",
        "population": 544000,
        "surface": 170572.0
    },
    {
        "region_code": "08",
        "region_name": "Kidal", 
        "region_capital": "Kidal",
        "population": 67000,
        "surface": 151430.0
    },
    {
        "region_code": "09",
        "region_name": "Bamako",
        "region_capital": "Bamako",
        "population": 2446000,
        "surface": 252.0
    },
    {
        "region_code": "10",
        "region_name": "Ménaka",
        "region_capital": "Ménaka", 
        "population": 114000,
        "surface": 81040.0
    },
    {
        "region_code": "11",
        "region_name": "Taoudéni",
        "region_capital": "Taoudéni",
        "population": 32000,
        "surface": 470967.0
    }
]

# Sample TableRef 09: Mali Cercles (Major circles by region)
MALI_CERCLES = [
    # Kayes Region
    {"cercle_code": "0101", "cercle_name": "Bafoulabé", "region_code": "01", "cercle_capital": "Bafoulabé"},
    {"cercle_code": "0102", "cercle_name": "Diéma", "region_code": "01", "cercle_capital": "Diéma"},
    {"cercle_code": "0103", "cercle_name": "Kayes", "region_code": "01", "cercle_capital": "Kayes"},
    {"cercle_code": "0104", "cercle_name": "Kéniéba", "region_code": "01", "cercle_capital": "Kéniéba"},
    {"cercle_code": "0105", "cercle_name": "Kita", "region_code": "01", "cercle_capital": "Kita"},
    {"cercle_code": "0106", "cercle_name": "Nioro du Sahel", "region_code": "01", "cercle_capital": "Nioro du Sahel"},
    {"cercle_code": "0107", "cercle_name": "Yélimané", "region_code": "01", "cercle_capital": "Yélimané"},
    
    # Koulikoro Region  
    {"cercle_code": "0201", "cercle_name": "Dioila", "region_code": "02", "cercle_capital": "Dioila"},
    {"cercle_code": "0202", "cercle_name": "Kangaba", "region_code": "02", "cercle_capital": "Kangaba"},
    {"cercle_code": "0203", "cercle_name": "Kolokani", "region_code": "02", "cercle_capital": "Kolokani"},
    {"cercle_code": "0204", "cercle_name": "Kati", "region_code": "02", "cercle_capital": "Kati"},
    {"cercle_code": "0205", "cercle_name": "Koulikoro", "region_code": "02", "cercle_capital": "Koulikoro"},
    {"cercle_code": "0206", "cercle_name": "Nara", "region_code": "02", "cercle_capital": "Nara"},
    {"cercle_code": "0207", "cercle_name": "Banamba", "region_code": "02", "cercle_capital": "Banamba"},
    
    # Sikasso Region
    {"cercle_code": "0301", "cercle_name": "Bougouni", "region_code": "03", "cercle_capital": "Bougouni"},
    {"cercle_code": "0302", "cercle_name": "Kadiolo", "region_code": "03", "cercle_capital": "Kadiolo"},
    {"cercle_code": "0303", "cercle_name": "Kolondiéba", "region_code": "03", "cercle_capital": "Kolondiéba"},
    {"cercle_code": "0304", "cercle_name": "Sikasso", "region_code": "03", "cercle_capital": "Sikasso"},
    {"cercle_code": "0305", "cercle_name": "Yanfolila", "region_code": "03", "cercle_capital": "Yanfolila"},
    {"cercle_code": "0306", "cercle_name": "Yorosso", "region_code": "03", "cercle_capital": "Yorosso"},
    
    # Bamako District
    {"cercle_code": "0901", "cercle_name": "Commune I", "region_code": "09", "cercle_capital": "Bamako"},
    {"cercle_code": "0902", "cercle_name": "Commune II", "region_code": "09", "cercle_capital": "Bamako"},
    {"cercle_code": "0903", "cercle_name": "Commune III", "region_code": "09", "cercle_capital": "Bamako"},
    {"cercle_code": "0904", "cercle_name": "Commune IV", "region_code": "09", "cercle_capital": "Bamako"},
    {"cercle_code": "0905", "cercle_name": "Commune V", "region_code": "09", "cercle_capital": "Bamako"},
    {"cercle_code": "0906", "cercle_name": "Commune VI", "region_code": "09", "cercle_capital": "Bamako"}
]

# TableRef 02: INSTAT Structures
INSTAT_STRUCTURES = [
    {
        "structure_id": "1000",
        "structure_name": "Institut National de la Statistique du Mali",
        "abbreviation": "INSTAT",
        "structure_type": "Institut National",
        "responsible_for_collection": True,
        "contact_info": {
            "address": "BP 12, Bamako, Mali", 
            "phone": "+223 20 22 24 86",
            "email": "instat@instat.gov.ml"
        }
    },
    {
        "structure_id": "1001", 
        "structure_name": "Direction Nationale de la Statistique et de l'Informatique",
        "abbreviation": "DNSI",
        "structure_type": "Direction Nationale",
        "responsible_for_collection": True
    },
    {
        "structure_id": "2001",
        "structure_name": "Ministère de l'Économie et des Finances",
        "abbreviation": "MEF", 
        "structure_type": "Ministère",
        "responsible_for_collection": False
    },
    {
        "structure_id": "2002",
        "structure_name": "Ministère de la Santé et des Affaires Sociales",
        "abbreviation": "MSAS",
        "structure_type": "Ministère", 
        "responsible_for_collection": False
    },
    {
        "structure_id": "3001",
        "structure_name": "Direction Régionale de la Statistique - Kayes",
        "abbreviation": "DRS-Kayes",
        "structure_type": "Direction Régionale",
        "responsible_for_collection": True
    },
    {
        "structure_id": "3002",
        "structure_name": "Direction Régionale de la Statistique - Koulikoro", 
        "abbreviation": "DRS-Koulikoro",
        "structure_type": "Direction Régionale",
        "responsible_for_collection": True
    }
]

# TableRef 07: Financing Sources
FINANCING_SOURCES = [
    {
        "source_code": "BM01",
        "source_name": "Banque Mondiale",
        "source_type": "Bailleur International",
        "currency": "USD",
        "min_amount": 100000.0,
        "max_amount": 50000000.0,
        "financing_conditions": "Conformité aux standards internationaux"
    },
    {
        "source_code": "AFD01", 
        "source_name": "Agence Française de Développement",
        "source_type": "Bailleur Bilatéral",
        "currency": "EUR",
        "min_amount": 50000.0,
        "max_amount": 10000000.0
    },
    {
        "source_code": "GVM01",
        "source_name": "Budget National du Mali",
        "source_type": "Financement National",
        "currency": "FCFA",
        "min_amount": 1000000.0,
        "max_amount": 5000000000.0
    },
    {
        "source_code": "UE01",
        "source_name": "Union Européenne",
        "source_type": "Bailleur International",
        "currency": "EUR",
        "min_amount": 75000.0,
        "max_amount": 25000000.0
    },
    {
        "source_code": "USAID01",
        "source_name": "USAID Mali",
        "source_type": "Bailleur Bilatéral", 
        "currency": "USD",
        "min_amount": 25000.0,
        "max_amount": 15000000.0
    }
]

# TableRef 06: Monitoring Indicators (Sample)
MONITORING_INDICATORS = [
    {
        "indicator_code": "M001",
        "indicator_name": "Taux d'exécution du budget statistique",
        "category": "Performance Budgétaire",
        "measurement_method": "Pourcentage du budget exécuté par rapport au budget alloué",
        "reporting_frequency": "Trimestrielle",
        "target_value": "85%",
        "data_collection_method": "Rapports financiers"
    },
    {
        "indicator_code": "M002", 
        "indicator_name": "Nombre d'enquêtes réalisées",
        "category": "Production Statistique",
        "measurement_method": "Décompte des enquêtes terminées",
        "reporting_frequency": "Mensuelle",
        "target_value": "12 par an",
        "data_collection_method": "Registre des enquêtes"
    },
    {
        "indicator_code": "M003",
        "indicator_name": "Taux de couverture géographique",
        "category": "Couverture",
        "measurement_method": "Pourcentage de régions couvertes", 
        "reporting_frequency": "Semestrielle",
        "target_value": "100%",
        "data_collection_method": "Cartes de couverture"
    }
]

# TableRef 03: CMR Indicators (Sample Performance Measurement Framework)
CMR_INDICATORS = [
    {
        "indicator_id": "CMR001",
        "indicator_name": "Taux d'accès à l'eau potable",
        "category": "Social",
        "measurement_unit": "Pourcentage",
        "data_source": "Enquête MICS/DHS", 
        "collection_frequency": "Annuelle",
        "responsible_structure": "INSTAT",
        "baseline_value": "69.6%",
        "target_value": "85%"
    },
    {
        "indicator_id": "CMR002",
        "indicator_name": "Taux de pauvreté",
        "category": "Économique", 
        "measurement_unit": "Pourcentage",
        "data_source": "Enquête EMOP",
        "collection_frequency": "Annuelle", 
        "responsible_structure": "INSTAT",
        "baseline_value": "47.7%",
        "target_value": "35%"
    },
    {
        "indicator_id": "CMR003",
        "indicator_name": "Taux de scolarisation primaire",
        "category": "Éducation",
        "measurement_unit": "Pourcentage",
        "data_source": "Annuaire statistique de l'éducation",
        "collection_frequency": "Annuelle",
        "responsible_structure": "MEN",
        "baseline_value": "78.3%", 
        "target_value": "95%"
    }
]

# TableRef 01: Strategic Axis Results (Sample SDS Framework)
STRATEGIC_AXIS_RESULTS = [
    {
        "result_id": "AXE1-OBJ1-RES1",
        "strategic_axis": "Axe 1: Amélioration de la gestion du SSN",
        "operational_objective": "Objectif 1.1: Renforcer le cadre institutionnel et organisationnel",
        "expected_result": "Le cadre institutionnel et organisationnel du SSN est renforcé",
        "activity": "Révision des textes réglementaires du SSN"
    },
    {
        "result_id": "AXE1-OBJ2-RES1", 
        "strategic_axis": "Axe 1: Amélioration de la gestion du SSN",
        "operational_objective": "Objectif 1.2: Développer les capacités humaines",
        "expected_result": "Les capacités humaines du SSN sont développées",
        "activity": "Formation du personnel statistique"
    },
    {
        "result_id": "AXE2-OBJ1-RES1",
        "strategic_axis": "Axe 2: Production statistique de qualité",
        "operational_objective": "Objectif 2.1: Améliorer la production des statistiques",
        "expected_result": "La production statistique est améliorée et de qualité", 
        "activity": "Réalisation d'enquêtes statistiques"
    }
]

# TableRef 04: Operational Results (Sample)
OPERATIONAL_RESULTS = [
    {
        "result_code": "R111",
        "axis_code": "A1", 
        "objective_code": "O11",
        "result_description": "Le cadre réglementaire du SSN est actualisé et opérationnel",
        "performance_indicators": ["Nombre de textes révisés", "Taux d'application des textes"]
    },
    {
        "result_code": "R211",
        "axis_code": "A2",
        "objective_code": "O21", 
        "result_description": "Les enquêtes statistiques sont réalisées selon les standards internationaux",
        "performance_indicators": ["Nombre d'enquêtes réalisées", "Taux de conformité aux standards"]
    }
]

# TableRef 05: Participating Structures (Sample)
PARTICIPATING_STRUCTURES = [
    {
        "structure_code": "P001",
        "structure_name": "OCHA Mali",
        "participation_type": "Technique",
        "role": "Appui technique en coordination humanitaire",
        "contact_info": "ocha-mali@un.org"
    },
    {
        "structure_code": "P002",
        "structure_name": "UNICEF Mali", 
        "participation_type": "Financier et Technique",
        "role": "Financement et appui technique pour les enquêtes sociales",
        "contact_info": "bamako@unicef.org"
    }
]

# Complete data dictionary for easy loading
REFERENCE_DATA = {
    "mali_regions": MALI_REGIONS,
    "mali_cercles": MALI_CERCLES, 
    "instat_structures": INSTAT_STRUCTURES,
    "financing_sources": FINANCING_SOURCES,
    "monitoring_indicators": MONITORING_INDICATORS,
    "cmr_indicators": CMR_INDICATORS,
    "strategic_axis_results": STRATEGIC_AXIS_RESULTS,
    "operational_results": OPERATIONAL_RESULTS, 
    "participating_structures": PARTICIPATING_STRUCTURES
}
