"""
Mali Reference Tables Schema for INSTAT SDS Survey System
Based on MODELISATION_Fiche2_Programme_REVUE_SDS_version01_22072025_15h14.docx

TableRef 01 - 09: Reference tables for Mali statistical surveys
"""
from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from pydantic import BaseModel, Field


class TableRefType(str, Enum):
    """Reference table types"""
    GEOGRAPHIC = "geographic"
    INSTITUTIONAL = "institutional"
    ACTIVITY = "activity"
    INDICATOR = "indicator"
    FINANCIAL = "financial"
    EVALUATION = "evaluation"


# TableRef 01: Axe stratégique/Objectifs opérationnel/Résultats attendus du SDS
class StrategicAxisResult(BaseModel):
    """TableRef 01: Strategic Axis/Operational Objectives/Expected Results SDS"""
    ResultID: str = Field(alias="result_id", description="Code du résultat")
    StrategicAxis: str = Field(alias="strategic_axis", description="Axe stratégique")
    OperationalObjective: str = Field(alias="operational_objective", description="Objectifs opérationnels")
    ExpectedResult: str = Field(alias="expected_result", description="Résultats attendus")
    Activity: str = Field(alias="activity", description="Activité")
    
    class Config:
        orm_mode = True
        allow_population_by_field_name = True


# TableRef 02: Liste des Structures pour les revues SDS
class INSTATStructure(BaseModel):
    """TableRef 02: List of Structures for SDS reviews"""
    StructureID: str = Field(alias="structure_id", description="Code de la structure")
    StructureName: str = Field(alias="structure_name", description="Nom de la structure")
    Abbreviation: str = Field(alias="abbreviation", description="Abréviation")
    StructureType: str = Field(alias="structure_type", description="Type de structure")
    ResponsibleForCollection: bool = Field(alias="responsible_for_collection", default=False, description="Structure en charge de collecte")
    
    class Config:
        orm_mode = True
        allow_population_by_field_name = True


# TableRef 03: Indicateurs CMR (Cadre de Mesure de la Performance)
class CMRIndicator(BaseModel):
    """TableRef 03: CMR Performance Measurement Framework Indicators"""
    IndicatorID: str = Field(description="Code de l'indicateur")
    IndicatorName: str = Field(description="Nom de l'indicateur")
    Category: str = Field(description="Catégorie")
    MeasurementUnit: str = Field(description="Unité de mesure")
    DataSource: str = Field(description="Source des données")
    CollectionFrequency: str = Field(description="Fréquence de collecte")
    ResponsibleStructure: str = Field(description="Structure responsable")
    
    class Config:
        orm_mode = True


# TableRef 04: Résultat attendu par Objectif opérationnel et Axe
class OperationalResult(BaseModel):
    """TableRef 04: Expected Result by Operational Objective and Axis"""
    ResultCode: str = Field(description="Code du résultat")
    AxisCode: str = Field(description="Code de l'axe")
    ObjectiveCode: str = Field(description="Code de l'objectif")
    ResultDescription: str = Field(description="Description du résultat")
    PerformanceIndicators: Optional[List[str]] = Field(default=[], description="Indicateurs de performance")
    
    class Config:
        orm_mode = True


# TableRef 05: Autres structures devant participer à l'activité
class ParticipatingStructure(BaseModel):
    """TableRef 05: Other structures that should participate in the activity"""
    StructureCode: str = Field(description="Code de la structure")
    StructureName: str = Field(description="Nom de la structure")
    ParticipationType: str = Field(description="Type de participation")
    Role: str = Field(description="Rôle dans l'activité")
    ContactInfo: Optional[str] = Field(default=None, description="Informations de contact")
    
    class Config:
        orm_mode = True


# TableRef 06: Indicateur de Suivi-évaluation
class MonitoringIndicator(BaseModel):
    """TableRef 06: Monitoring and Evaluation Indicators"""
    IndicatorCode: str = Field(description="Code de l'indicateur")
    IndicatorName: str = Field(description="Nom de l'indicateur")
    Category: str = Field(description="Catégorie")
    MeasurementMethod: str = Field(description="Méthode de mesure")
    ReportingFrequency: str = Field(description="Fréquence de rapportage")
    TargetValue: Optional[str] = Field(default=None, description="Valeur cible")
    DataCollectionMethod: str = Field(description="Méthode de collecte des données")
    
    class Config:
        orm_mode = True


# TableRef 07: Sources de financement
class FinancingSource(BaseModel):
    """TableRef 07: Financing Sources"""
    SourceCode: str = Field(description="Code de la source")
    SourceName: str = Field(description="Nom de la source de financement")
    SourceType: str = Field(description="Type de source")
    Currency: str = Field(default="FCFA", description="Devise")
    MinAmount: Optional[float] = Field(default=None, description="Montant minimum")
    MaxAmount: Optional[float] = Field(default=None, description="Montant maximum")
    FinancingConditions: Optional[str] = Field(default=None, description="Conditions de financement")
    
    class Config:
        orm_mode = True


# TableRef 08: Liste des régions selon le découpage administratif du Mali
class MaliRegion(BaseModel):
    """TableRef 08: List of regions according to Mali's administrative division"""
    RegionCode: str = Field(alias="region_code", description="Code de la région")
    RegionName: str = Field(alias="region_name", description="Nom de la région")
    RegionCapital: str = Field(alias="region_capital", description="Chef-lieu de région")
    Population: Optional[int] = Field(alias="population", default=None, description="Population")
    Surface: Optional[float] = Field(alias="surface", default=None, description="Superficie en km²")
    Status: str = Field(alias="status", default="active", description="Statut")
    
    class Config:
        orm_mode = True
        allow_population_by_field_name = True


# TableRef 09: Liste des cercles selon le découpage administratif du Mali
class MaliCercle(BaseModel):
    """TableRef 09: List of circles according to Mali's administrative division"""
    CercleCode: str = Field(alias="cercle_code", description="Code du cercle")
    CercleName: str = Field(alias="cercle_name", description="Nom du cercle")
    RegionCode: str = Field(alias="region_code", description="Code de la région")
    CercleCapital: str = Field(alias="cercle_capital", description="Chef-lieu de cercle")
    Population: Optional[int] = Field(alias="population", default=None, description="Population")
    Surface: Optional[float] = Field(alias="surface", default=None, description="Superficie en km²")
    Status: str = Field(alias="status", default="active", description="Statut")
    
    class Config:
        orm_mode = True
        allow_population_by_field_name = True


# Survey Response Models with Table References
class SurveyResponse(BaseModel):
    """Survey response model with table reference support"""
    ResponseID: Optional[int] = None
    SurveyID: int
    QuestionID: int
    ResponseValue: str
    TableReference: Optional[str] = Field(default=None, description="Reference to table (e.g., 'TableRef:08')")
    ReferenceCode: Optional[str] = Field(default=None, description="Code from reference table")
    
    class Config:
        orm_mode = True


# Question model with table reference support
class QuestionWithTableRef(BaseModel):
    """Question model with table reference support"""
    QuestionID: Optional[int] = None
    QuestionText: str
    QuestionType: str
    TableReference: Optional[str] = Field(default=None, description="Reference to table")
    ReferenceTableType: Optional[TableRefType] = None
    IsRequired: bool = False
    SectionNumber: Optional[str] = None
    QuestionNumber: Optional[str] = None
    
    # Multi-language support
    QuestionTextFR: Optional[str] = None
    QuestionTextEN: Optional[str] = None
    
    class Config:
        orm_mode = True


# Mali SDS Survey specific models
class SDSActivitySurvey(BaseModel):
    """SDS Activity Programming Survey Model"""
    # Header information
    FicheNumber: str = Field(description="Numéro de fiche")
    OrderNumber: int = Field(description="Numéro d'ordre")
    TotalFiches: int = Field(description="Nombre total de fiches")
    
    # Section 1: Identification
    RegionCode: str = Field(description="Code de la région (@TableRef:08)")
    CercleCode: str = Field(description="Code du cercle (@TableRef:09)")
    ImplementingStructure: str = Field(description="Structure en charge de réalisation (@TableRef:02)")
    DataCollectionStructure: str = Field(description="Structure en charge de collecte (@TableRef:02)")
    ActivityTitle: str = Field(description="Intitulé de l'activité (@TableRef:01)")
    
    # Section 2: Activity Characteristics
    IsDataDisaggregatable: bool = Field(description="Les données sont-elles désagrégées?")
    
    # Disaggregation details (if applicable)
    DisaggregationByGender: Optional[bool] = None
    DisaggregationByAge: Optional[bool] = None
    DisaggregationBySex: Optional[bool] = None
    DisaggregationByDisability: Optional[bool] = None
    DisaggregationByDecisionParticipation: Optional[bool] = None
    DisaggregationByTerritory: Optional[bool] = None
    DisaggregationByResidenceArea: Optional[bool] = None
    
    # Territorial level disaggregation
    RegionLevel: Optional[bool] = None
    CercleLevel: Optional[bool] = None
    ArrondissementLevel: Optional[bool] = None
    CommuneLevel: Optional[bool] = None
    
    # Residence area
    UrbanArea: Optional[bool] = None
    RuralArea: Optional[bool] = None
    
    # Financial information
    FinancingSources: Optional[List[str]] = Field(default=[], description="Sources de financement (@TableRef:07)")
    ActivityCost: Optional[float] = Field(description="Coût de l'activité en FCFA")
    
    # Monitoring indicators
    MonitoringIndicators: Optional[List[str]] = Field(default=[], description="Indicateurs de suivi (@TableRef:06)")
    
    # Completion status
    CompletionResult: Optional[str] = Field(description="Résultat de remplissage: 1=Complètement rempli, 2=Partiellement rempli, 3=Non rempli")
    
    class Config:
        orm_mode = True


# Reference Table Container
class ReferenceTableData(BaseModel):
    """Container for all reference table data"""
    strategic_results: List[StrategicAxisResult] = []
    structures: List[INSTATStructure] = []
    cmr_indicators: List[CMRIndicator] = []
    operational_results: List[OperationalResult] = []
    participating_structures: List[ParticipatingStructure] = []
    monitoring_indicators: List[MonitoringIndicator] = []
    financing_sources: List[FinancingSource] = []
    regions: List[MaliRegion] = []
    cercles: List[MaliCercle] = []
    
    class Config:
        orm_mode = True


# API Response Models
class ReferenceTableResponse(BaseModel):
    """API response for reference tables"""
    table_id: str
    table_name: str
    data: List[Dict[str, Any]]
    total_records: int
    last_updated: Optional[datetime] = None
    
    class Config:
        orm_mode = True


class TableRefLookupRequest(BaseModel):
    """Request model for table reference lookup"""
    table_ref: str = Field(description="Table reference (e.g., 'TableRef:08')")
    search_term: Optional[str] = Field(default=None, description="Search term for filtering")
    limit: Optional[int] = Field(default=100, description="Limit results")


class TableRefLookupResponse(BaseModel):
    """Response model for table reference lookup"""
    table_ref: str
    results: List[Dict[str, Any]]
    total_found: int
    filtered: bool
