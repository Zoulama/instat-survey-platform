-- =====================================================================
-- INSTAT Survey Platform - Mali Reference Data Population Script
-- This script populates all Mali reference tables (TableRef 01-09)
-- =====================================================================

-- Clear existing data (optional - uncomment if needed for fresh start)
-- TRUNCATE TABLE strategic_axis_results, cmr_indicators, operational_results, monitoring_indicators CASCADE;
-- TRUNCATE TABLE instat_structures, participating_structures, financing_sources CASCADE;
-- TRUNCATE TABLE mali_cercles, mali_regions CASCADE;

-- =====================================================================
-- TableRef 01: Strategic Axis Results (SDS Strategic Framework)
-- =====================================================================

INSERT INTO strategic_axis_results (result_id, strategic_axis, operational_objective, expected_result, activity) VALUES
-- Axe 1: Modernisation du système statistique national
('AXE1_OBJ1_RES1', 'Modernisation du système statistique national', 'Améliorer la qualité et la fiabilité des statistiques', 'Mise en place d''un système de contrôle qualité', 'Élaboration de procédures de contrôle qualité'),
('AXE1_OBJ1_RES2', 'Modernisation du système statistique national', 'Améliorer la qualité et la fiabilité des statistiques', 'Formation du personnel aux nouvelles méthodes', 'Organisation de sessions de formation'),
('AXE1_OBJ2_RES1', 'Modernisation du système statistique national', 'Renforcer les capacités techniques', 'Acquisition d''équipements modernes', 'Achat d''équipements informatiques et logiciels'),
('AXE1_OBJ2_RES2', 'Modernisation du système statistique national', 'Renforcer les capacités techniques', 'Développement d''applications informatiques', 'Conception de logiciels de gestion statistique'),

-- Axe 2: Développement des statistiques sectorielles
('AXE2_OBJ1_RES1', 'Développement des statistiques sectorielles', 'Améliorer les statistiques économiques', 'Production régulière des comptes nationaux', 'Collecte et traitement des données économiques'),
('AXE2_OBJ1_RES2', 'Développement des statistiques sectorielles', 'Améliorer les statistiques économiques', 'Mise à jour des nomenclatures', 'Révision des classifications économiques'),
('AXE2_OBJ2_RES1', 'Développement des statistiques sectorielles', 'Développer les statistiques sociales', 'Réalisation d''enquêtes démographiques', 'Planification et exécution d''enquêtes'),
('AXE2_OBJ2_RES2', 'Développement des statistiques sectorielles', 'Développer les statistiques sociales', 'Analyse des données d''état civil', 'Traitement des registres d''état civil'),

-- Axe 3: Renforcement de la coordination statistique
('AXE3_OBJ1_RES1', 'Renforcement de la coordination statistique', 'Améliorer la coordination inter-institutionnelle', 'Mise en place d''un comité de coordination', 'Création et animation du comité'),
('AXE3_OBJ1_RES2', 'Renforcement de la coordination statistique', 'Améliorer la coordination inter-institutionnelle', 'Harmonisation des méthodes', 'Élaboration de standards communs'),
('AXE3_OBJ2_RES1', 'Renforcement de la coordination statistique', 'Optimiser l''utilisation des ressources', 'Éviter les doubles emplois', 'Coordination des programmes de travail'),
('AXE3_OBJ2_RES2', 'Renforcement de la coordination statistique', 'Optimiser l''utilisation des ressources', 'Partage des données', 'Mise en place d''une plateforme de partage'),

-- Axe 4: Amélioration de la diffusion statistique
('AXE4_OBJ1_RES1', 'Amélioration de la diffusion statistique', 'Moderniser les canaux de diffusion', 'Développement d''un portail web', 'Conception et mise en ligne du portail'),
('AXE4_OBJ1_RES2', 'Amélioration de la diffusion statistique', 'Moderniser les canaux de diffusion', 'Production de bulletins réguliers', 'Rédaction et publication de bulletins'),
('AXE4_OBJ2_RES1', 'Amélioration de la diffusion statistique', 'Faciliter l''accès aux données', 'Création d''un centre de documentation', 'Aménagement d''espaces de consultation'),
('AXE4_OBJ2_RES2', 'Amélioration de la diffusion statistique', 'Faciliter l''accès aux données', 'Formation des utilisateurs', 'Organisation d''ateliers de formation')
ON CONFLICT (result_id) DO NOTHING;

-- =====================================================================
-- TableRef 02: INSTAT Structures
-- =====================================================================

INSERT INTO instat_structures (structure_id, structure_name, abbreviation, structure_type, responsible_for_collection, contact_info) VALUES
-- Structures centrales
('INSTAT_DG', 'Direction Générale', 'DG', 'Direction centrale', FALSE, '{"phone": "+223 20 22 24 55", "email": "dg@instat.gov.ml", "address": "BP 12 Bamako, Mali"}'),
('INSTAT_DGA', 'Direction Générale Adjointe', 'DGA', 'Direction centrale', FALSE, '{"phone": "+223 20 22 24 56", "email": "dga@instat.gov.ml"}'),
('INSTAT_SG', 'Secrétariat Général', 'SG', 'Secrétariat', FALSE, '{"phone": "+223 20 22 24 57", "email": "sg@instat.gov.ml"}'),

-- Directions techniques
('INSTAT_DES', 'Direction des Enquêtes et Sondages', 'DES', 'Direction technique', TRUE, '{"phone": "+223 20 22 24 58", "email": "des@instat.gov.ml"}'),
('INSTAT_SSN', 'Direction du Système Statistique National', 'SSN', 'Direction technique', FALSE, '{"phone": "+223 20 22 24 59", "email": "ssn@instat.gov.ml"}'),
('INSTAT_SDS', 'Direction de la Synthèse et des Données Sectorielles', 'SDS', 'Direction technique', TRUE, '{"phone": "+223 20 22 24 60", "email": "sds@instat.gov.ml"}'),
('INSTAT_DPPD', 'Direction de la Prospective et de la Planification du Développement', 'DPPD', 'Direction technique', FALSE, '{"phone": "+223 20 22 24 61", "email": "dppd@instat.gov.ml"}'),

-- Directions d''appui
('INSTAT_DAF', 'Direction Administrative et Financière', 'DAF', 'Direction d''appui', FALSE, '{"phone": "+223 20 22 24 62", "email": "daf@instat.gov.ml"}'),
('INSTAT_DRH', 'Direction des Ressources Humaines', 'DRH', 'Direction d''appui', FALSE, '{"phone": "+223 20 22 24 63", "email": "drh@instat.gov.ml"}'),
('INSTAT_DSI', 'Direction des Systèmes d''Information', 'DSI', 'Direction d''appui', FALSE, '{"phone": "+223 20 22 24 64", "email": "dsi@instat.gov.ml"}'),

-- Antennes régionales
('INSTAT_KAYES', 'Antenne Régionale de Kayes', 'AR-Kayes', 'Antenne régionale', TRUE, '{"phone": "+223 25 25 25 25", "email": "kayes@instat.gov.ml"}'),
('INSTAT_KOULIKORO', 'Antenne Régionale de Koulikoro', 'AR-Koulikoro', 'Antenne régionale', TRUE, '{"phone": "+223 26 26 26 26", "email": "koulikoro@instat.gov.ml"}'),
('INSTAT_SIKASSO', 'Antenne Régionale de Sikasso', 'AR-Sikasso', 'Antenne régionale', TRUE, '{"phone": "+223 27 27 27 27", "email": "sikasso@instat.gov.ml"}'),
('INSTAT_SEGOU', 'Antenne Régionale de Ségou', 'AR-Ségou', 'Antenne régionale', TRUE, '{"phone": "+223 28 28 28 28", "email": "segou@instat.gov.ml"}'),
('INSTAT_MOPTI', 'Antenne Régionale de Mopti', 'AR-Mopti', 'Antenne régionale', TRUE, '{"phone": "+223 29 29 29 29", "email": "mopti@instat.gov.ml"}'),
('INSTAT_TOMBOUCTO', 'Antenne Régionale de Tombouctou', 'AR-Tombouctou', 'Antenne régionale', TRUE, '{"phone": "+223 30 30 30 30", "email": "tombouctou@instat.gov.ml"}'),
('INSTAT_GAO', 'Antenne Régionale de Gao', 'AR-Gao', 'Antenne régionale', TRUE, '{"phone": "+223 31 31 31 31", "email": "gao@instat.gov.ml"}'),
('INSTAT_KIDAL', 'Antenne Régionale de Kidal', 'AR-Kidal', 'Antenne régionale', TRUE, '{"phone": "+223 32 32 32 32", "email": "kidal@instat.gov.ml"}'),

-- Structures spécialisées
('INSTAT_CAPI', 'Centre d''Analyse et de Prévision des Indicateurs', 'CAPI', 'Centre spécialisé', FALSE, '{"phone": "+223 20 22 24 65", "email": "capi@instat.gov.ml"}'),
('INSTAT_CTSI', 'Centre de Traitement Statistique et Informatique', 'CTSI', 'Centre spécialisé', FALSE, '{"phone": "+223 20 22 24 66", "email": "ctsi@instat.gov.ml"}')
ON CONFLICT (structure_id) DO NOTHING;

-- =====================================================================
-- TableRef 03: CMR Indicators (Cadre de Mesure des Résultats)
-- =====================================================================

INSERT INTO cmr_indicators (indicator_id, indicator_name, category, measurement_unit, data_source, collection_frequency, responsible_structure, baseline_value, target_value) VALUES
-- Indicateurs démographiques
('CMR_DEMO_001', 'Taux de croissance démographique', 'Démographie', 'Pourcentage', 'Recensement, projections', 'Annuelle', 'INSTAT_DES', '3.1%', '2.8%'),
('CMR_DEMO_002', 'Taux de mortalité infantile', 'Démographie', 'Pour 1000', 'Enquête démographique', 'Quinquennale', 'INSTAT_DES', '75‰', '60‰'),
('CMR_DEMO_003', 'Espérance de vie à la naissance', 'Démographie', 'Années', 'Tables de mortalité', 'Quinquennale', 'INSTAT_DES', '58.5 ans', '65 ans'),
('CMR_DEMO_004', 'Taux de fécondité', 'Démographie', 'Enfants par femme', 'Enquête démographique', 'Quinquennale', 'INSTAT_DES', '6.1', '4.5'),

-- Indicateurs économiques
('CMR_ECO_001', 'Taux de croissance du PIB', 'Économie', 'Pourcentage', 'Comptes nationaux', 'Annuelle', 'INSTAT_SDS', '5.3%', '7.0%'),
('CMR_ECO_002', 'PIB par habitant', 'Économie', 'FCFA', 'Comptes nationaux', 'Annuelle', 'INSTAT_SDS', '485000', '650000'),
('CMR_ECO_003', 'Taux d''inflation', 'Économie', 'Pourcentage', 'IPC', 'Mensuelle', 'INSTAT_SDS', '2.1%', '3.0%'),
('CMR_ECO_004', 'Taux de chômage', 'Économie', 'Pourcentage', 'Enquête emploi', 'Annuelle', 'INSTAT_DES', '8.5%', '6.0%'),

-- Indicateurs sociaux
('CMR_SOC_001', 'Taux de scolarisation primaire', 'Éducation', 'Pourcentage', 'Statistiques scolaires', 'Annuelle', 'Ministère Éducation', '67%', '85%'),
('CMR_SOC_002', 'Taux d''alphabétisation', 'Éducation', 'Pourcentage', 'Enquête alphabétisation', 'Quinquennale', 'INSTAT_DES', '35%', '50%'),
('CMR_SOC_003', 'Accès à l''eau potable', 'Social', 'Pourcentage', 'Enquête ménage', 'Quinquennale', 'INSTAT_DES', '68%', '85%'),
('CMR_SOC_004', 'Couverture sanitaire', 'Santé', 'Pourcentage', 'Statistiques sanitaires', 'Annuelle', 'Ministère Santé', '45%', '70%'),

-- Indicateurs de gouvernance
('CMR_GOV_001', 'Indice de transparence', 'Gouvernance', 'Indice', 'Évaluation externe', 'Annuelle', 'INSTAT_SSN', '3.2/10', '6.0/10'),
('CMR_GOV_002', 'Participation citoyenne', 'Gouvernance', 'Pourcentage', 'Enquête gouvernance', 'Biennale', 'INSTAT_DES', '42%', '65%'),

-- Indicateurs environnementaux
('CMR_ENV_001', 'Taux de déforestation', 'Environnement', 'Pourcentage', 'Images satellites', 'Annuelle', 'Ministère Environnement', '2.8%', '1.5%'),
('CMR_ENV_002', 'Émissions de CO2', 'Environnement', 'Tonnes/hab', 'Inventaire carbone', 'Biennale', 'INSTAT_SDS', '0.3 t/hab', '0.2 t/hab')
ON CONFLICT (indicator_id) DO NOTHING;

-- =====================================================================
-- TableRef 04: Operational Results
-- =====================================================================

INSERT INTO operational_results (result_code, axis_code, objective_code, result_description, performance_indicators) VALUES
('RES_001', 'AXE1', 'OBJ1', 'Amélioration de la qualité des données statistiques', '{"indicators": ["CMR_GOV_001", "CMR_DEMO_001"], "target": "Réduction de 50% des erreurs de collecte"}'),
('RES_002', 'AXE1', 'OBJ1', 'Renforcement des capacités du personnel', '{"indicators": ["Formation"], "target": "100% du personnel formé"}'),
('RES_003', 'AXE1', 'OBJ2', 'Modernisation des équipements et infrastructures', '{"indicators": ["Équipements"], "target": "Renouvellement de 80% du matériel"}'),
('RES_004', 'AXE2', 'OBJ1', 'Production régulière des comptes nationaux', '{"indicators": ["CMR_ECO_001"], "target": "Publication dans les délais"}'),
('RES_005', 'AXE2', 'OBJ2', 'Amélioration des statistiques démographiques et sociales', '{"indicators": ["CMR_DEMO_002", "CMR_SOC_001"], "target": "Réduction des écarts avec standards internationaux"}'),
('RES_006', 'AXE3', 'OBJ1', 'Coordination effective du système statistique national', '{"indicators": ["Coordination"], "target": "90% des structures participent"}'),
('RES_007', 'AXE3', 'OBJ2', 'Harmonisation des méthodes et procédures', '{"indicators": ["Standards"], "target": "Adoption de standards communs"}'),
('RES_008', 'AXE4', 'OBJ1', 'Amélioration de l''accès aux données', '{"indicators": ["Diffusion"], "target": "Augmentation de 100% des consultations"}'),
('RES_009', 'AXE4', 'OBJ2', 'Satisfaction des utilisateurs', '{"indicators": ["Satisfaction"], "target": "Taux de satisfaction > 80%"}')
ON CONFLICT (result_code) DO NOTHING;

-- =====================================================================
-- TableRef 05: Participating Structures
-- =====================================================================

INSERT INTO participating_structures (structure_code, structure_name, participation_type, role, contact_info, expertise_areas) VALUES
-- Ministères et institutions publiques
('MEF', 'Ministère de l''Économie et des Finances', 'Ministère', 'Partenaire institutionnel et financier', 'BP 234 Bamako', '["finances_publiques", "politique_economique"]'),
('MENA', 'Ministère de l''Éducation Nationale', 'Ministère', 'Fournisseur de données éducatives', 'BP 71 Bamako', '["education", "formation"]'),
('MSAS', 'Ministère de la Santé et des Affaires Sociales', 'Ministère', 'Fournisseur de données sanitaires', 'BP 232 Bamako', '["sante", "protection_sociale"]'),
('MATD', 'Ministère de l''Administration Territoriale et de la Décentralisation', 'Ministère', 'Coordination territoriale', 'BP 78 Bamako', '["administration", "decentralisation"]'),

-- Institutions de régulation et contrôle
('BCEAO', 'Banque Centrale des États de l''Afrique de l''Ouest', 'Institution régionale', 'Fournisseur de données monétaires et financières', 'BP 206 Bamako', '["politique_monetaire", "systeme_financier"]'),
('DGI', 'Direction Générale des Impôts', 'Administration fiscale', 'Fournisseur de données fiscales', 'BP 182 Bamako', '["fiscalite", "revenus"]'),
('DGD', 'Direction Générale des Douanes', 'Administration douanière', 'Fournisseur de données du commerce extérieur', 'BP 234 Bamako', '["commerce_exterieur", "douanes"]'),

-- Organismes de développement
('PNUD', 'Programme des Nations Unies pour le Développement', 'Organisation internationale', 'Appui technique et financier', 'BP 120 Bamako', '["developpement", "capacites"]'),
('BM', 'Banque Mondiale', 'Institution financière internationale', 'Financement et assistance technique', 'BP 1864 Bamako', '["financement", "politique_developpement"]'),
('BAD', 'Banque Africaine de Développement', 'Institution financière régionale', 'Financement des projets statistiques', 'Representative Bamako', '["financement", "integration_africaine"]'),
('AFD', 'Agence Française de Développement', 'Agence de développement', 'Appui technique et financier', 'BP 32 Bamako', '["cooperation", "financement"]'),
('UE', 'Union Européenne', 'Organisation supranationale', 'Financement et assistance technique', 'BP 115 Bamako', '["cooperation", "politique_developpement"]'),

-- Société civile et secteur privé
('CCIM', 'Chambre de Commerce et d''Industrie du Mali', 'Chambre consulaire', 'Représentation du secteur privé', 'BP 46 Bamako', '["secteur_prive", "commerce"]'),
('APCAM', 'Assemblée Permanente des Chambres d''Agriculture du Mali', 'Organisation professionnelle', 'Représentation du secteur agricole', 'BP 1566 Bamako', '["agriculture", "elevage"]'),
('CNPM', 'Conseil National du Patronat du Mali', 'Organisation patronale', 'Représentation des entreprises', 'BP 3462 Bamako', '["patronat", "emploi"]'),

-- Institutions académiques et de recherche
('USTTB', 'Université des Sciences, des Techniques et des Technologies de Bamako', 'Université', 'Formation et recherche', 'BP E 3206 Bamako', '["formation", "recherche"]'),
('IER', 'Institut d''Économie Rurale', 'Institut de recherche', 'Recherche en économie rurale', 'BP 258 Bamako', '["recherche_agricole", "economie_rurale"]'),
('ISFRA', 'Institut Supérieur de Formation et de Recherche Appliquée', 'Institut', 'Formation statistique', 'BP 2041 Bamako', '["formation_statistique", "recherche_appliquee"]')
ON CONFLICT (structure_code) DO NOTHING;

-- =====================================================================
-- TableRef 06: Monitoring Indicators
-- =====================================================================

INSERT INTO monitoring_indicators (indicator_code, indicator_name, category, measurement_method, reporting_frequency, target_value, data_collection_method, responsible_unit) VALUES
-- Indicateurs de performance du SSN
('IND_PERF_001', 'Taux de couverture statistique territoriale', 'Performance SSN', 'Ratio structures/territoire', 'Semestrielle', '95%', 'Recensement des structures', 'INSTAT_SSN'),
('IND_PERF_002', 'Délai moyen de publication des statistiques', 'Performance SSN', 'Calcul de moyennes', 'Trimestrielle', '3 mois', 'Suivi des publications', 'INSTAT_SSN'),
('IND_PERF_003', 'Taux de mise à jour des données', 'Performance SSN', 'Ratio données actualisées', 'Mensuelle', '90%', 'Audit des bases de données', 'INSTAT_DSI'),
('IND_PERF_004', 'Niveau de satisfaction des utilisateurs', 'Performance SSN', 'Enquête de satisfaction', 'Annuelle', '80%', 'Enquête par questionnaire', 'INSTAT_SSN'),

-- Indicateurs de capacité
('IND_CAP_001', 'Nombre de statisticiens formés', 'Capacités', 'Comptage', 'Annuelle', '50 personnes', 'Registre des formations', 'INSTAT_DRH'),
('IND_CAP_002', 'Taux d''équipement informatique', 'Capacités', 'Ratio équipements/personnel', 'Annuelle', '100%', 'Inventaire matériel', 'INSTAT_DSI'),
('IND_CAP_003', 'Budget exécuté pour les statistiques', 'Capacités', 'Pourcentage du budget total', 'Annuelle', '2% du budget national', 'Suivi budgétaire', 'INSTAT_DAF'),
('IND_CAP_004', 'Nombre de logiciels statistiques disponibles', 'Capacités', 'Comptage', 'Annuelle', '10 logiciels', 'Inventaire logiciels', 'INSTAT_DSI'),

-- Indicateurs de qualité
('IND_QUAL_001', 'Taux d''erreur dans les données publiées', 'Qualité', 'Audit qualité', 'Trimestrielle', '<2%', 'Contrôle qualité', 'INSTAT_SDS'),
('IND_QUAL_002', 'Conformité aux standards internationaux', 'Qualité', 'Évaluation externe', 'Annuelle', '90%', 'Audit externe', 'INSTAT_SSN'),
('IND_QUAL_003', 'Taux de réponse aux enquêtes', 'Qualité', 'Ratio répondants/échantillon', 'Par enquête', '85%', 'Suivi des enquêtes', 'INSTAT_DES'),
('IND_QUAL_004', 'Délai de traitement des données', 'Qualité', 'Mesure temporelle', 'Mensuelle', '15 jours', 'Chronométrage', 'INSTAT_CTSI'),

-- Indicateurs de diffusion
('IND_DIFF_001', 'Nombre de publications produites', 'Diffusion', 'Comptage', 'Trimestrielle', '20 publications/trimestre', 'Suivi éditorial', 'INSTAT_SSN'),
('IND_DIFF_002', 'Taux d''utilisation du portail web', 'Diffusion', 'Statistiques web', 'Mensuelle', '10000 visites/mois', 'Analytics web', 'INSTAT_DSI'),
('IND_DIFF_003', 'Nombre de médias utilisant les statistiques', 'Diffusion', 'Veille médiatique', 'Mensuelle', '50 articles/mois', 'Revue de presse', 'INSTAT_SSN'),
('IND_DIFF_004', 'Taux de téléchargement des données', 'Diffusion', 'Statistiques de téléchargement', 'Mensuelle', '1000 téléchargements/mois', 'Logs serveur', 'INSTAT_DSI')
ON CONFLICT (indicator_code) DO NOTHING;

-- =====================================================================
-- TableRef 07: Financing Sources
-- =====================================================================

INSERT INTO financing_sources (source_code, source_name, source_type, currency, min_amount, max_amount, financing_conditions, contact_info) VALUES
-- Sources nationales
('BN_MALI', 'Budget National du Mali', 'Public national', 'FCFA', 500000000, 5000000000, 'Allocation budgétaire annuelle selon la loi de finances', '{"entity": "Ministère des Finances", "contact": "budgetstat@finances.gov.ml"}'),
('CTL_MALI', 'Collectivités Territoriales', 'Public local', 'FCFA', 10000000, 500000000, 'Contribution des régions et communes aux activités statistiques locales', '{"entity": "MATD", "contact": "collectivites@matd.gov.ml"}'),

-- Sources bilatérales
('AFD_FRANCE', 'Agence Française de Développement', 'Bilatéral', 'EUR', 100000, 5000000, 'Projets de coopération technique, taux préférentiel 2%', '{"entity": "AFD Mali", "contact": "afdmali@afd.fr", "website": "www.afd.fr"}'),
('GIZ_ALL', 'Deutsche Gesellschaft für Internationale Zusammenarbeit', 'Bilatéral', 'EUR', 50000, 2000000, 'Assistance technique et formation', '{"entity": "GIZ Mali", "contact": "giz-mali@giz.de"}'),
('USAID_USA', 'United States Agency for International Development', 'Bilatéral', 'USD', 100000, 3000000, 'Programmes de renforcement des capacités', '{"entity": "USAID Mali", "contact": "usaidmali@usaid.gov"}'),
('JICA_JPN', 'Japan International Cooperation Agency', 'Bilatéral', 'JPY', 5000000, 200000000, 'Coopération technique et équipements', '{"entity": "JICA Mali", "contact": "jica-mali@jica.go.jp"}'),

-- Sources multilatérales
('BM_WORLD', 'Banque Mondiale', 'Multilatéral', 'USD', 500000, 50000000, 'Prêts concessionnels et dons pour projets statistiques', '{"entity": "Banque Mondiale Mali", "contact": "mali@worldbank.org"}'),
('BAD_AFR', 'Banque Africaine de Développement', 'Multilatéral', 'USD', 200000, 20000000, 'Financement des projets d''intégration statistique africaine', '{"entity": "BAD", "contact": "mali@afdb.org"}'),
('UE_EUROPE', 'Union Européenne', 'Multilatéral', 'EUR', 300000, 15000000, 'Programme d''appui institutionnel et sectoriel', '{"entity": "Délégation UE Mali", "contact": "delegation-mali@eeas.europa.eu"}'),
('PNUD_ONU', 'Programme des Nations Unies pour le Développement', 'Multilatéral', 'USD', 100000, 5000000, 'Appui aux programmes de développement des capacités', '{"entity": "PNUD Mali", "contact": "registry.ml@undp.org"}'),

-- Sources régionales et organisations spécialisées
('BCEAO_REG', 'Banque Centrale des États de l''Afrique de l''Ouest', 'Régional', 'FCFA', 50000000, 1000000000, 'Financement des projets statistiques monétaires et financiers', '{"entity": "BCEAO", "contact": "bceao@bceao.int"}'),
('UEMOA_REG', 'Union Économique et Monétaire Ouest Africaine', 'Régional', 'FCFA', 100000000, 2000000000, 'Harmonisation statistique régionale', '{"entity": "UEMOA", "contact": "commission@uemoa.int"}'),
('CEDEAO_REG', 'Communauté Économique des États de l''Afrique de l''Ouest', 'Régional', 'USD', 50000, 3000000, 'Intégration statistique sous-régionale', '{"entity": "CEDEAO", "contact": "info@ecowas.int"}'),

-- Fondations et ONG
('FGATES', 'Fondation Bill et Melinda Gates', 'Fondation privée', 'USD', 100000, 10000000, 'Projets de santé et développement avec composante statistique', '{"entity": "Gates Foundation", "contact": "info@gatesfoundation.org"}'),
('OSISA', 'Open Society Initiative for Southern Africa', 'ONG internationale', 'USD', 25000, 500000, 'Gouvernance et transparence statistique', '{"entity": "Open Society", "contact": "info@osisa.org"}'),

-- Secteur privé et partenariats
('PART_PRIVE', 'Partenariats Public-Privé', 'Partenariat', 'FCFA', 25000000, 1000000000, 'Financement conjoint pour enquêtes sectorielles', '{"entity": "CNPM", "contact": "partenariat@cnpm.org.ml"}'),
('SERV_STAT', 'Services Statistiques Payants', 'Commercial', 'FCFA', 1000000, 100000000, 'Prestations statistiques spécialisées', '{"entity": "INSTAT", "contact": "services@instat.gov.ml"}')
ON CONFLICT (source_code) DO NOTHING;

-- =====================================================================
-- TableRef 08: Mali Regions (Administrative Divisions)
-- =====================================================================

INSERT INTO mali_regions (region_code, region_name, region_capital, population, surface, coordinates) VALUES
('01', 'Kayes', 'Kayes', 2418400, 119743, '{"latitude": 14.4469, "longitude": -11.4456, "bounds": {"north": 16.0, "south": 12.5, "east": -9.0, "west": -12.3}}'),
('02', 'Koulikoro', 'Koulikoro', 2796000, 90120, '{"latitude": 12.8622, "longitude": -7.5589, "bounds": {"north": 15.5, "south": 11.0, "east": -4.5, "west": -9.0}}'),
('03', 'Sikasso', 'Sikasso', 2999400, 71790, '{"latitude": 11.3175, "longitude": -5.6672, "bounds": {"north": 13.5, "south": 9.0, "east": -3.0, "west": -7.5}}'),
('04', 'Ségou', 'Ségou', 2752200, 64821, '{"latitude": 13.4317, "longitude": -6.2139, "bounds": {"north": 16.0, "south": 12.0, "east": -3.0, "west": -7.5}}'),
('05', 'Mopti', 'Mopti', 2542000, 79017, '{"latitude": 14.4947, "longitude": -4.1969, "bounds": {"north": 17.0, "south": 12.5, "east": -1.0, "west": -6.5}}'),
('06', 'Tombouctou', 'Tombouctou', 755600, 408977, '{"latitude": 16.7666, "longitude": -3.0026, "bounds": {"north": 21.0, "south": 14.5, "east": 1.5, "west": -7.5}}'),
('07', 'Gao', 'Gao', 684000, 170572, '{"latitude": 16.2719, "longitude": -0.0447, "bounds": {"north": 21.0, "south": 14.0, "east": 4.5, "west": -2.0}}'),
('08', 'Kidal', 'Kidal', 84000, 151430, '{"latitude": 18.4411, "longitude": 1.4078, "bounds": {"north": 25.0, "south": 17.0, "east": 4.5, "west": -2.0}}'),
('BKO', 'Bamako', 'Bamako', 2929000, 267, '{"latitude": 12.6392, "longitude": -8.0029, "bounds": {"north": 12.75, "south": 12.45, "east": -7.8, "west": -8.2}}'),
('TA', 'Taoudénit', 'Taoudénit', 65000, 307024, '{"latitude": 22.6776, "longitude": -3.9835, "bounds": {"north": 25.0, "south": 20.0, "east": 0.5, "west": -7.5}}')
ON CONFLICT (region_code) DO NOTHING;

-- =====================================================================
-- TableRef 09: Mali Cercles
-- =====================================================================

INSERT INTO mali_cercles (cercle_code, cercle_name, region_code, cercle_capital, population, surface) VALUES
-- Région de Kayes
('0101', 'Bafoulabé', '01', 'Bafoulabé', 285000, 22823),
('0102', 'Diéma', '01', 'Diéma', 222000, 9204),
('0103', 'Kéniéba', '01', 'Kéniéba', 199000, 9145),
('0104', 'Kita', '01', 'Kita', 407000, 34454),
('0105', 'Kayes', '01', 'Kayes', 513000, 12061),
('0106', 'Nioro du Sahel', '01', 'Nioro du Sahel', 275000, 16859),
('0107', 'Yélimané', '01', 'Yélimané', 517000, 15197),

-- Région de Koulikoro
('0201', 'Dioila', '02', 'Dioila', 291000, 5247),
('0202', 'Kangaba', '02', 'Kangaba', 173000, 7126),
('0203', 'Kolokani', '02', 'Kolokani', 284000, 14380),
('0204', 'Kati', '02', 'Kati', 693000, 9921),
('0205', 'Koulikoro', '02', 'Koulikoro', 296000, 8900),
('0206', 'Nara', '02', 'Nara', 258000, 30714),
('0207', 'Banamba', '02', 'Banamba', 345000, 13832),

-- Région de Sikasso
('0301', 'Bougouni', '03', 'Bougouni', 389000, 8910),
('0302', 'Kadiolo', '03', 'Kadiolo', 198000, 2010),
('0303', 'Kolondiéba', '03', 'Kolondiéba', 160000, 4607),
('0304', 'Koutiala', '03', 'Koutiala', 704000, 18169),
('0305', 'Sikasso', '03', 'Sikasso', 788000, 19787),
('0306', 'Yanfolila', '03', 'Yanfolila', 204000, 6285),
('0307', 'Yorosso', '03', 'Yorosso', 556000, 12022),

-- Région de Ségou
('0401', 'Barouéli', '04', 'Barouéli', 295000, 4744),
('0402', 'Bla', '04', 'Bla', 370000, 4723),
('0403', 'Macina', '04', 'Macina', 299000, 12015),
('0404', 'Niono', '04', 'Niono', 330000, 13895),
('0405', 'San', '04', 'San', 598000, 17264),
('0406', 'Ségou', '04', 'Ségou', 859000, 12180),
('0407', 'Tominian', '04', 'Tominian', 218000, 8000),

-- Région de Mopti
('0501', 'Bandiagara', '05', 'Bandiagara', 473000, 9974),
('0502', 'Bankass', '05', 'Bankass', 318000, 9370),
('0503', 'Djenné', '05', 'Djenné', 237000, 4194),
('0504', 'Douentza', '05', 'Douentza', 381000, 17110),
('0505', 'Koro', '05', 'Koro', 367000, 10156),
('0506', 'Mopti', '05', 'Mopti', 445000, 8500),
('0507', 'Tenenkou', '05', 'Ténenkou', 197000, 5700),
('0508', 'Youwarou', '05', 'Youwarou', 325000, 23213),

-- Région de Tombouctou
('0601', 'Diré', '06', 'Diré', 157000, 8781),
('0602', 'Goundam', '06', 'Goundam', 155000, 51781),
('0603', 'Niafunké', '06', 'Niafunké', 184000, 49572),
('0604', 'Tombouctou', '06', 'Tombouctou', 165000, 90611),
('0605', 'Gourma-Rharous', '06', 'Gourma-Rharous', 94600, 208232),

-- Région de Gao
('0701', 'Ansongo', '07', 'Ansongo', 162000, 54394),
('0702', 'Bourem', '07', 'Bourem', 93000, 52648),
('0703', 'Gao', '07', 'Gao', 307000, 42973),
('0704', 'Ménaka', '07', 'Ménaka', 122000, 20551),

-- Région de Kidal
('0801', 'Abeïbara', '08', 'Abeïbara', 23000, 51981),
('0802', 'Kidal', '08', 'Kidal', 37000, 53265),
('0803', 'Tin-Essako', '08', 'Tin-Essako', 24000, 46184),

-- District de Bamako
('BK01', 'Commune I', 'BKO', 'Commune I', 335000, 35),
('BK02', 'Commune II', 'BKO', 'Commune II', 160000, 17),
('BK03', 'Commune III', 'BKO', 'Commune III', 128000, 23),
('BK04', 'Commune IV', 'BKO', 'Commune IV', 600000, 37),
('BK05', 'Commune V', 'BKO', 'Commune V', 341000, 41),
('BK06', 'Commune VI', 'BKO', 'Commune VI', 1365000, 114),

-- Région de Taoudénit
('TA01', 'Taoudénit', 'TA', 'Taoudénit', 65000, 307024)
ON CONFLICT (cercle_code) DO NOTHING;

-- =====================================================================
-- FINAL STATUS MESSAGE
-- =====================================================================

DO $$
BEGIN
    RAISE NOTICE '==========================================';
    RAISE NOTICE 'Mali Reference Data Population COMPLETED';
    RAISE NOTICE '==========================================';
    RAISE NOTICE 'TableRef 01: % Strategic Axis Results inserted', (SELECT COUNT(*) FROM strategic_axis_results);
    RAISE NOTICE 'TableRef 02: % INSTAT Structures inserted', (SELECT COUNT(*) FROM instat_structures);
    RAISE NOTICE 'TableRef 03: % CMR Indicators inserted', (SELECT COUNT(*) FROM cmr_indicators);
    RAISE NOTICE 'TableRef 04: % Operational Results inserted', (SELECT COUNT(*) FROM operational_results);
    RAISE NOTICE 'TableRef 05: % Participating Structures inserted', (SELECT COUNT(*) FROM participating_structures);
    RAISE NOTICE 'TableRef 06: % Monitoring Indicators inserted', (SELECT COUNT(*) FROM monitoring_indicators);
    RAISE NOTICE 'TableRef 07: % Financing Sources inserted', (SELECT COUNT(*) FROM financing_sources);
    RAISE NOTICE 'TableRef 08: % Mali Regions inserted', (SELECT COUNT(*) FROM mali_regions);
    RAISE NOTICE 'TableRef 09: % Mali Cercles inserted', (SELECT COUNT(*) FROM mali_cercles);
    RAISE NOTICE '==========================================';
    RAISE NOTICE 'All Mali reference tables populated successfully!';
    RAISE NOTICE 'System ready for survey operations with complete reference data.';
END $$;

-- =====================================================================
-- FIX: Set is_active = TRUE for all reference data records
-- This ensures all records are visible through API endpoints
-- =====================================================================

UPDATE mali_regions SET is_active = TRUE;
UPDATE mali_cercles SET is_active = TRUE;
UPDATE financing_sources SET is_active = TRUE;
UPDATE instat_structures SET is_active = TRUE;
UPDATE strategic_axis_results SET is_active = TRUE;
UPDATE monitoring_indicators SET is_active = TRUE;
UPDATE cmr_indicators SET is_active = TRUE;
UPDATE operational_results SET is_active = TRUE WHERE is_active IS NULL;
UPDATE participating_structures SET is_active = TRUE WHERE is_active IS NULL;

-- Notify completion of activation
DO $$
BEGIN
    RAISE NOTICE '==========================================';
    RAISE NOTICE 'Reference Data Activation COMPLETED';
    RAISE NOTICE '==========================================';
    RAISE NOTICE 'All reference data records set to is_active = TRUE';
    RAISE NOTICE 'Mali reference endpoints should now return data properly';
END $$;
