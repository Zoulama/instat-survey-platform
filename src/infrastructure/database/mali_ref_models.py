"""
Database models for Mali Reference Tables (TableRef 01-09)
SQLAlchemy models for the INSTAT SDS Survey System
"""
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.infrastructure.database.base import Base


# TableRef 01: Strategic Axis Results
class StrategicAxisResultModel(Base):
    __tablename__ = 'strategic_axis_results'
    
    id = Column(Integer, primary_key=True)
    result_id = Column(String(50), unique=True, nullable=False, comment="Code du résultat")
    strategic_axis = Column(Text, nullable=False, comment="Axe stratégique")
    operational_objective = Column(Text, nullable=False, comment="Objectifs opérationnels")
    expected_result = Column(Text, nullable=False, comment="Résultats attendus")
    activity = Column(Text, nullable=False, comment="Activité")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# TableRef 02: INSTAT Structures
class INSTATStructureModel(Base):
    __tablename__ = 'instat_structures'
    
    id = Column(Integer, primary_key=True)
    structure_id = Column(String(20), unique=True, nullable=False, comment="Code de la structure")
    structure_name = Column(String(255), nullable=False, comment="Nom de la structure")
    abbreviation = Column(String(50), comment="Abréviation")
    structure_type = Column(String(100), comment="Type de structure")
    responsible_for_collection = Column(Boolean, default=False, comment="Structure en charge de collecte")
    contact_info = Column(JSON, comment="Informations de contact")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# TableRef 03: CMR Indicators
class CMRIndicatorModel(Base):
    __tablename__ = 'cmr_indicators'
    
    id = Column(Integer, primary_key=True)
    indicator_id = Column(String(50), unique=True, nullable=False, comment="Code de l'indicateur")
    indicator_name = Column(Text, nullable=False, comment="Nom de l'indicateur")
    category = Column(String(100), comment="Catégorie")
    measurement_unit = Column(String(100), comment="Unité de mesure")
    data_source = Column(String(255), comment="Source des données")
    collection_frequency = Column(String(50), comment="Fréquence de collecte")
    responsible_structure = Column(String(100), comment="Structure responsable")
    baseline_value = Column(String(100), comment="Valeur de référence")
    target_value = Column(String(100), comment="Valeur cible")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# TableRef 04: Operational Results
class OperationalResultModel(Base):
    __tablename__ = 'operational_results'
    
    id = Column(Integer, primary_key=True)
    result_code = Column(String(50), unique=True, nullable=False, comment="Code du résultat")
    axis_code = Column(String(20), comment="Code de l'axe")
    objective_code = Column(String(20), comment="Code de l'objectif")
    result_description = Column(Text, nullable=False, comment="Description du résultat")
    performance_indicators = Column(JSON, comment="Indicateurs de performance")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# TableRef 05: Participating Structures
class ParticipatingStructureModel(Base):
    __tablename__ = 'participating_structures'
    
    id = Column(Integer, primary_key=True)
    structure_code = Column(String(20), unique=True, nullable=False, comment="Code de la structure")
    structure_name = Column(String(255), nullable=False, comment="Nom de la structure")
    participation_type = Column(String(100), comment="Type de participation")
    role = Column(Text, comment="Rôle dans l'activité")
    contact_info = Column(Text, comment="Informations de contact")
    expertise_areas = Column(JSON, comment="Domaines d'expertise")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# TableRef 06: Monitoring Indicators
class MonitoringIndicatorModel(Base):
    __tablename__ = 'monitoring_indicators'
    
    id = Column(Integer, primary_key=True)
    indicator_code = Column(String(50), unique=True, nullable=False, comment="Code de l'indicateur")
    indicator_name = Column(Text, nullable=False, comment="Nom de l'indicateur")
    category = Column(String(100), comment="Catégorie")
    measurement_method = Column(Text, comment="Méthode de mesure")
    reporting_frequency = Column(String(50), comment="Fréquence de rapportage")
    target_value = Column(String(100), comment="Valeur cible")
    data_collection_method = Column(Text, comment="Méthode de collecte des données")
    responsible_unit = Column(String(100), comment="Unité responsable")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# TableRef 07: Financing Sources
class FinancingSourceModel(Base):
    __tablename__ = 'financing_sources'
    
    id = Column(Integer, primary_key=True)
    source_code = Column(String(20), unique=True, nullable=False, comment="Code de la source")
    source_name = Column(String(255), nullable=False, comment="Nom de la source de financement")
    source_type = Column(String(100), comment="Type de source")
    currency = Column(String(10), default="FCFA", comment="Devise")
    min_amount = Column(Float, comment="Montant minimum")
    max_amount = Column(Float, comment="Montant maximum")
    financing_conditions = Column(Text, comment="Conditions de financement")
    contact_info = Column(JSON, comment="Informations de contact")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# TableRef 08: Mali Regions
class MaliRegionModel(Base):
    __tablename__ = 'mali_regions'
    
    id = Column(Integer, primary_key=True)
    region_code = Column(String(10), unique=True, nullable=False, comment="Code de la région")
    region_name = Column(String(100), nullable=False, comment="Nom de la région")
    region_capital = Column(String(100), comment="Chef-lieu de région")
    population = Column(Integer, comment="Population")
    surface = Column(Float, comment="Superficie en km²")
    status = Column(String(20), default="active", comment="Statut")
    coordinates = Column(JSON, comment="Coordonnées géographiques")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship to cercles
    cercles = relationship("MaliCercleModel", back_populates="region")


# TableRef 09: Mali Cercles
class MaliCercleModel(Base):
    __tablename__ = 'mali_cercles'
    
    id = Column(Integer, primary_key=True)
    cercle_code = Column(String(10), unique=True, nullable=False, comment="Code du cercle")
    cercle_name = Column(String(100), nullable=False, comment="Nom du cercle")
    region_code = Column(String(10), ForeignKey('mali_regions.region_code'), comment="Code de la région")
    cercle_capital = Column(String(100), comment="Chef-lieu de cercle")
    population = Column(Integer, comment="Population")
    surface = Column(Float, comment="Superficie en km²")
    status = Column(String(20), default="active", comment="Statut")
    coordinates = Column(JSON, comment="Coordonnées géographiques")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship to region
    region = relationship("MaliRegionModel", back_populates="cercles")


# Survey Response Model with Table References
class SurveyResponseModel(Base):
    __tablename__ = 'survey_responses'
    
    id = Column(Integer, primary_key=True)
    survey_id = Column(Integer, nullable=False, comment="ID de l'enquête")
    question_id = Column(Integer, nullable=False, comment="ID de la question")
    response_value = Column(Text, comment="Valeur de la réponse")
    table_reference = Column(String(50), comment="Reference à la table (e.g., 'TableRef:08')")
    reference_code = Column(String(50), comment="Code de la table de référence")
    respondent_id = Column(String(100), comment="ID du répondant")
    response_date = Column(DateTime(timezone=True), server_default=func.now())
    is_validated = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# SDS Activity Survey Model
class SDSActivitySurveyModel(Base):
    __tablename__ = 'sds_activity_surveys'
    
    id = Column(Integer, primary_key=True)
    
    # Header information
    fiche_number = Column(String(50), nullable=False, comment="Numéro de fiche")
    order_number = Column(Integer, nullable=False, comment="Numéro d'ordre")
    total_fiches = Column(Integer, nullable=False, comment="Nombre total de fiches")
    
    # Section 1: Identification
    region_code = Column(String(10), ForeignKey('mali_regions.region_code'), comment="Code de la région")
    cercle_code = Column(String(10), ForeignKey('mali_cercles.cercle_code'), comment="Code du cercle")
    implementing_structure = Column(String(20), ForeignKey('instat_structures.structure_id'), 
                                    comment="Structure en charge de réalisation")
    data_collection_structure = Column(String(20), ForeignKey('instat_structures.structure_id'),
                                      comment="Structure en charge de collecte")
    activity_title = Column(Text, comment="Intitulé de l'activité")
    
    # Section 2: Activity Characteristics
    is_data_disaggregatable = Column(Boolean, comment="Les données sont-elles désagrégées?")
    
    # Disaggregation details
    disaggregation_by_gender = Column(Boolean, comment="Désagrégation par genre")
    disaggregation_by_age = Column(Boolean, comment="Désagrégation par âge")
    disaggregation_by_sex = Column(Boolean, comment="Désagrégation par sexe")
    disaggregation_by_disability = Column(Boolean, comment="Désagrégation par handicap")
    disaggregation_by_decision_participation = Column(Boolean, comment="Désagrégation par participation à la décision")
    disaggregation_by_territory = Column(Boolean, comment="Désagrégation territoriale")
    disaggregation_by_residence_area = Column(Boolean, comment="Désagrégation par milieu de résidence")
    
    # Territorial levels
    region_level = Column(Boolean, comment="Niveau région")
    cercle_level = Column(Boolean, comment="Niveau cercle")
    arrondissement_level = Column(Boolean, comment="Niveau arrondissement")
    commune_level = Column(Boolean, comment="Niveau commune")
    
    # Residence areas
    urban_area = Column(Boolean, comment="Urbain")
    rural_area = Column(Boolean, comment="Rural")
    
    # Financial information
    financing_sources = Column(JSON, comment="Sources de financement")
    activity_cost = Column(Float, comment="Coût de l'activité en FCFA")
    
    # Monitoring
    monitoring_indicators = Column(JSON, comment="Indicateurs de suivi")
    
    # Completion
    completion_result = Column(String(10), comment="Résultat de remplissage: 1=Complet, 2=Partiel, 3=Non rempli")
    
    # Metadata
    created_by = Column(String(100), comment="Créé par")
    reviewed_by = Column(String(100), comment="Revu par")
    approved_by = Column(String(100), comment="Approuvé par")
    review_date = Column(DateTime(timezone=True), comment="Date de révision")
    approval_date = Column(DateTime(timezone=True), comment="Date d'approbation")
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    region = relationship("MaliRegionModel")
    cercle = relationship("MaliCercleModel")
    implementing_org = relationship("INSTATStructureModel", foreign_keys=[implementing_structure])
    collection_org = relationship("INSTATStructureModel", foreign_keys=[data_collection_structure])


# Table Reference Mapping
class TableReferenceMapping(Base):
    __tablename__ = 'table_reference_mappings'
    
    id = Column(Integer, primary_key=True)
    table_ref = Column(String(20), nullable=False, comment="Table reference (e.g., 'TableRef:08')")
    table_name = Column(String(100), nullable=False, comment="Nom de la table")
    model_class = Column(String(100), nullable=False, comment="Nom de la classe de modèle")
    description = Column(Text, comment="Description de la table")
    display_fields = Column(JSON, comment="Champs à afficher")
    search_fields = Column(JSON, comment="Champs de recherche")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
