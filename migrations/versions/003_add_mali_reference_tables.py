"""Add Mali reference tables for TableRef 01-09

Revision ID: 003
Revises: 002
Create Date: 2025-08-06 15:52:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '003'
down_revision = 'add_enhanced_survey_fields'
branch_labels = None
depends_on = None


def upgrade():
    # TableRef 01: Strategic Axis Results
    op.create_table(
        'strategic_axis_results',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('result_id', sa.String(50), nullable=False, comment="Code du résultat"),
        sa.Column('strategic_axis', sa.Text(), nullable=False, comment="Axe stratégique"),
        sa.Column('operational_objective', sa.Text(), nullable=False, comment="Objectifs opérationnels"),
        sa.Column('expected_result', sa.Text(), nullable=False, comment="Résultats attendus"),
        sa.Column('activity', sa.Text(), nullable=False, comment="Activité"),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('result_id')
    )

    # TableRef 02: INSTAT Structures
    op.create_table(
        'instat_structures',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('structure_id', sa.String(20), nullable=False, comment="Code de la structure"),
        sa.Column('structure_name', sa.String(255), nullable=False, comment="Nom de la structure"),
        sa.Column('abbreviation', sa.String(50), comment="Abréviation"),
        sa.Column('structure_type', sa.String(100), comment="Type de structure"),
        sa.Column('responsible_for_collection', sa.Boolean(), server_default='false', comment="Structure en charge de collecte"),
        sa.Column('contact_info', sa.JSON(), comment="Informations de contact"),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('structure_id')
    )

    # TableRef 03: CMR Indicators
    op.create_table(
        'cmr_indicators',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('indicator_id', sa.String(50), nullable=False, comment="Code de l'indicateur"),
        sa.Column('indicator_name', sa.Text(), nullable=False, comment="Nom de l'indicateur"),
        sa.Column('category', sa.String(100), comment="Catégorie"),
        sa.Column('measurement_unit', sa.String(100), comment="Unité de mesure"),
        sa.Column('data_source', sa.String(255), comment="Source des données"),
        sa.Column('collection_frequency', sa.String(50), comment="Fréquence de collecte"),
        sa.Column('responsible_structure', sa.String(100), comment="Structure responsable"),
        sa.Column('baseline_value', sa.String(100), comment="Valeur de référence"),
        sa.Column('target_value', sa.String(100), comment="Valeur cible"),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('indicator_id')
    )

    # TableRef 04: Operational Results
    op.create_table(
        'operational_results',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('result_code', sa.String(50), nullable=False, comment="Code du résultat"),
        sa.Column('axis_code', sa.String(20), comment="Code de l'axe"),
        sa.Column('objective_code', sa.String(20), comment="Code de l'objectif"),
        sa.Column('result_description', sa.Text(), nullable=False, comment="Description du résultat"),
        sa.Column('performance_indicators', sa.JSON(), comment="Indicateurs de performance"),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('result_code')
    )

    # TableRef 05: Participating Structures
    op.create_table(
        'participating_structures',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('structure_code', sa.String(20), nullable=False, comment="Code de la structure"),
        sa.Column('structure_name', sa.String(255), nullable=False, comment="Nom de la structure"),
        sa.Column('participation_type', sa.String(100), comment="Type de participation"),
        sa.Column('role', sa.Text(), comment="Rôle dans l'activité"),
        sa.Column('contact_info', sa.Text(), comment="Informations de contact"),
        sa.Column('expertise_areas', sa.JSON(), comment="Domaines d'expertise"),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('structure_code')
    )

    # TableRef 06: Monitoring Indicators
    op.create_table(
        'monitoring_indicators',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('indicator_code', sa.String(50), nullable=False, comment="Code de l'indicateur"),
        sa.Column('indicator_name', sa.Text(), nullable=False, comment="Nom de l'indicateur"),
        sa.Column('category', sa.String(100), comment="Catégorie"),
        sa.Column('measurement_method', sa.Text(), comment="Méthode de mesure"),
        sa.Column('reporting_frequency', sa.String(50), comment="Fréquence de rapportage"),
        sa.Column('target_value', sa.String(100), comment="Valeur cible"),
        sa.Column('data_collection_method', sa.Text(), comment="Méthode de collecte des données"),
        sa.Column('responsible_unit', sa.String(100), comment="Unité responsable"),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('indicator_code')
    )

    # TableRef 07: Financing Sources
    op.create_table(
        'financing_sources',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('source_code', sa.String(20), nullable=False, comment="Code de la source"),
        sa.Column('source_name', sa.String(255), nullable=False, comment="Nom de la source de financement"),
        sa.Column('source_type', sa.String(100), comment="Type de source"),
        sa.Column('currency', sa.String(10), server_default='FCFA', comment="Devise"),
        sa.Column('min_amount', sa.Float(), comment="Montant minimum"),
        sa.Column('max_amount', sa.Float(), comment="Montant maximum"),
        sa.Column('financing_conditions', sa.Text(), comment="Conditions de financement"),
        sa.Column('contact_info', sa.JSON(), comment="Informations de contact"),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('source_code')
    )

    # TableRef 08: Mali Regions
    op.create_table(
        'mali_regions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('region_code', sa.String(10), nullable=False, comment="Code de la région"),
        sa.Column('region_name', sa.String(100), nullable=False, comment="Nom de la région"),
        sa.Column('region_capital', sa.String(100), comment="Chef-lieu de région"),
        sa.Column('population', sa.Integer(), comment="Population"),
        sa.Column('surface', sa.Float(), comment="Superficie en km²"),
        sa.Column('status', sa.String(20), server_default='active', comment="Statut"),
        sa.Column('coordinates', sa.JSON(), comment="Coordonnées géographiques"),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('region_code')
    )

    # TableRef 09: Mali Cercles
    op.create_table(
        'mali_cercles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('cercle_code', sa.String(10), nullable=False, comment="Code du cercle"),
        sa.Column('cercle_name', sa.String(100), nullable=False, comment="Nom du cercle"),
        sa.Column('region_code', sa.String(10), comment="Code de la région"),
        sa.Column('cercle_capital', sa.String(100), comment="Chef-lieu de cercle"),
        sa.Column('population', sa.Integer(), comment="Population"),
        sa.Column('surface', sa.Float(), comment="Superficie en km²"),
        sa.Column('status', sa.String(20), server_default='active', comment="Statut"),
        sa.Column('coordinates', sa.JSON(), comment="Coordonnées géographiques"),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('cercle_code'),
        sa.ForeignKeyConstraint(['region_code'], ['mali_regions.region_code'])
    )

    # Survey Responses with Table References
    op.create_table(
        'survey_responses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('survey_id', sa.Integer(), nullable=False, comment="ID de l'enquête"),
        sa.Column('question_id', sa.Integer(), nullable=False, comment="ID de la question"),
        sa.Column('response_value', sa.Text(), comment="Valeur de la réponse"),
        sa.Column('table_reference', sa.String(50), comment="Reference à la table (e.g., 'TableRef:08')"),
        sa.Column('reference_code', sa.String(50), comment="Code de la table de référence"),
        sa.Column('respondent_id', sa.String(100), comment="ID du répondant"),
        sa.Column('response_date', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('is_validated', sa.Boolean(), server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )

    # SDS Activity Survey
    op.create_table(
        'sds_activity_surveys',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('fiche_number', sa.String(50), nullable=False, comment="Numéro de fiche"),
        sa.Column('order_number', sa.Integer(), nullable=False, comment="Numéro d'ordre"),
        sa.Column('total_fiches', sa.Integer(), nullable=False, comment="Nombre total de fiches"),
        sa.Column('region_code', sa.String(10), comment="Code de la région"),
        sa.Column('cercle_code', sa.String(10), comment="Code du cercle"),
        sa.Column('implementing_structure', sa.String(20), comment="Structure en charge de réalisation"),
        sa.Column('data_collection_structure', sa.String(20), comment="Structure en charge de collecte"),
        sa.Column('activity_title', sa.Text(), comment="Intitulé de l'activité"),
        sa.Column('is_data_disaggregatable', sa.Boolean(), comment="Les données sont-elles désagrégées?"),
        sa.Column('disaggregation_by_gender', sa.Boolean(), comment="Désagrégation par genre"),
        sa.Column('disaggregation_by_age', sa.Boolean(), comment="Désagrégation par âge"),
        sa.Column('disaggregation_by_sex', sa.Boolean(), comment="Désagrégation par sexe"),
        sa.Column('disaggregation_by_disability', sa.Boolean(), comment="Désagrégation par handicap"),
        sa.Column('disaggregation_by_decision_participation', sa.Boolean(), comment="Désagrégation par participation à la décision"),
        sa.Column('disaggregation_by_territory', sa.Boolean(), comment="Désagrégation territoriale"),
        sa.Column('disaggregation_by_residence_area', sa.Boolean(), comment="Désagrégation par milieu de résidence"),
        sa.Column('region_level', sa.Boolean(), comment="Niveau région"),
        sa.Column('cercle_level', sa.Boolean(), comment="Niveau cercle"),
        sa.Column('arrondissement_level', sa.Boolean(), comment="Niveau arrondissement"),
        sa.Column('commune_level', sa.Boolean(), comment="Niveau commune"),
        sa.Column('urban_area', sa.Boolean(), comment="Urbain"),
        sa.Column('rural_area', sa.Boolean(), comment="Rural"),
        sa.Column('financing_sources', sa.JSON(), comment="Sources de financement"),
        sa.Column('activity_cost', sa.Float(), comment="Coût de l'activité en FCFA"),
        sa.Column('monitoring_indicators', sa.JSON(), comment="Indicateurs de suivi"),
        sa.Column('completion_result', sa.String(10), comment="Résultat de remplissage: 1=Complet, 2=Partiel, 3=Non rempli"),
        sa.Column('created_by', sa.String(100), comment="Créé par"),
        sa.Column('reviewed_by', sa.String(100), comment="Revu par"),
        sa.Column('approved_by', sa.String(100), comment="Approuvé par"),
        sa.Column('review_date', sa.DateTime(timezone=True), comment="Date de révision"),
        sa.Column('approval_date', sa.DateTime(timezone=True), comment="Date d'approbation"),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['region_code'], ['mali_regions.region_code']),
        sa.ForeignKeyConstraint(['cercle_code'], ['mali_cercles.cercle_code']),
        sa.ForeignKeyConstraint(['implementing_structure'], ['instat_structures.structure_id']),
        sa.ForeignKeyConstraint(['data_collection_structure'], ['instat_structures.structure_id'])
    )

    # Table Reference Mappings
    op.create_table(
        'table_reference_mappings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('table_ref', sa.String(20), nullable=False, comment="Table reference (e.g., 'TableRef:08')"),
        sa.Column('table_name', sa.String(100), nullable=False, comment="Nom de la table"),
        sa.Column('model_class', sa.String(100), nullable=False, comment="Nom de la classe de modèle"),
        sa.Column('description', sa.Text(), comment="Description de la table"),
        sa.Column('display_fields', sa.JSON(), comment="Champs à afficher"),
        sa.Column('search_fields', sa.JSON(), comment="Champs de recherche"),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )

    # Insert initial table reference mappings
    op.execute("""
        INSERT INTO table_reference_mappings (table_ref, table_name, model_class, description, display_fields, search_fields) VALUES
        ('TableRef:01', 'strategic_axis_results', 'StrategicAxisResultModel', 'Axe stratégique/Objectifs opérationnel/Résultats attendus du SDS', '["result_id", "strategic_axis", "operational_objective"]', '["strategic_axis", "operational_objective", "expected_result"]'),
        ('TableRef:02', 'instat_structures', 'INSTATStructureModel', 'Liste des Structures pour les revues SDS', '["structure_id", "structure_name", "abbreviation"]', '["structure_name", "abbreviation"]'),
        ('TableRef:03', 'cmr_indicators', 'CMRIndicatorModel', 'Indicateurs CMR', '["indicator_id", "indicator_name", "category"]', '["indicator_name", "category"]'),
        ('TableRef:04', 'operational_results', 'OperationalResultModel', 'Résultat attendu par Objectif opérationnel et Axe', '["result_code", "result_description"]', '["result_description"]'),
        ('TableRef:05', 'participating_structures', 'ParticipatingStructureModel', 'Autres structures devant participer à l''activité', '["structure_code", "structure_name", "participation_type"]', '["structure_name", "participation_type"]'),
        ('TableRef:06', 'monitoring_indicators', 'MonitoringIndicatorModel', 'Indicateur de Suivi-évaluation', '["indicator_code", "indicator_name", "category"]', '["indicator_name", "category"]'),
        ('TableRef:07', 'financing_sources', 'FinancingSourceModel', 'Sources de financement', '["source_code", "source_name", "source_type"]', '["source_name", "source_type"]'),
        ('TableRef:08', 'mali_regions', 'MaliRegionModel', 'Liste des régions selon le découpage administratif du Mali', '["region_code", "region_name", "region_capital"]', '["region_name", "region_capital"]'),
        ('TableRef:09', 'mali_cercles', 'MaliCercleModel', 'Liste des cercles selon le découpage administratif du Mali', '["cercle_code", "cercle_name", "region_code"]', '["cercle_name", "cercle_capital"]');
    """)


def downgrade():
    # Drop tables in reverse order
    op.drop_table('table_reference_mappings')
    op.drop_table('sds_activity_surveys')
    op.drop_table('survey_responses')
    op.drop_table('mali_cercles')
    op.drop_table('mali_regions')
    op.drop_table('financing_sources')
    op.drop_table('monitoring_indicators')
    op.drop_table('participating_structures')
    op.drop_table('operational_results')
    op.drop_table('cmr_indicators')
    op.drop_table('instat_structures')
    op.drop_table('strategic_axis_results')
