#!/usr/bin/env python3
"""
Data loader script for Mali Reference Tables
Populates the database with initial reference data for TableRef 01-09
"""
import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy.orm import Session
from src.infrastructure.database.connection import get_db
from src.infrastructure.database.mali_ref_models import (
    MaliRegionModel, MaliCercleModel, INSTATStructureModel,
    FinancingSourceModel, MonitoringIndicatorModel, CMRIndicatorModel,
    StrategicAxisResultModel, OperationalResultModel, ParticipatingStructureModel
)
from data.mali_reference_sample_data import REFERENCE_DATA


def load_reference_data():
    """Load all reference data into the database"""
    session_generator = get_db()
    session = next(session_generator)
    
    try:
        # Load Mali Regions (TableRef 08)
        print("Loading Mali regions...")
        for region_data in REFERENCE_DATA["mali_regions"]:
            existing = session.query(MaliRegionModel).filter_by(region_code=region_data["region_code"]).first()
            if not existing:
                region = MaliRegionModel(**region_data)
                session.add(region)
        session.commit()
        print(f"✓ Loaded {len(REFERENCE_DATA['mali_regions'])} regions")

        # Load Mali Cercles (TableRef 09)
        print("Loading Mali cercles...")
        for cercle_data in REFERENCE_DATA["mali_cercles"]:
            existing = session.query(MaliCercleModel).filter_by(cercle_code=cercle_data["cercle_code"]).first()
            if not existing:
                cercle = MaliCercleModel(**cercle_data)
                session.add(cercle)
        session.commit()
        print(f"✓ Loaded {len(REFERENCE_DATA['mali_cercles'])} cercles")

        # Load INSTAT Structures (TableRef 02)
        print("Loading INSTAT structures...")
        for structure_data in REFERENCE_DATA["instat_structures"]:
            existing = session.query(INSTATStructureModel).filter_by(structure_id=structure_data["structure_id"]).first()
            if not existing:
                structure = INSTATStructureModel(**structure_data)
                session.add(structure)
        session.commit()
        print(f"✓ Loaded {len(REFERENCE_DATA['instat_structures'])} structures")

        # Load Financing Sources (TableRef 07)
        print("Loading financing sources...")
        for source_data in REFERENCE_DATA["financing_sources"]:
            existing = session.query(FinancingSourceModel).filter_by(source_code=source_data["source_code"]).first()
            if not existing:
                source = FinancingSourceModel(**source_data)
                session.add(source)
        session.commit()
        print(f"✓ Loaded {len(REFERENCE_DATA['financing_sources'])} financing sources")

        # Load Monitoring Indicators (TableRef 06)
        print("Loading monitoring indicators...")
        for indicator_data in REFERENCE_DATA["monitoring_indicators"]:
            existing = session.query(MonitoringIndicatorModel).filter_by(indicator_code=indicator_data["indicator_code"]).first()
            if not existing:
                indicator = MonitoringIndicatorModel(**indicator_data)
                session.add(indicator)
        session.commit()
        print(f"✓ Loaded {len(REFERENCE_DATA['monitoring_indicators'])} monitoring indicators")

        # Load CMR Indicators (TableRef 03)
        print("Loading CMR indicators...")
        for indicator_data in REFERENCE_DATA["cmr_indicators"]:
            existing = session.query(CMRIndicatorModel).filter_by(indicator_id=indicator_data["indicator_id"]).first()
            if not existing:
                indicator = CMRIndicatorModel(**indicator_data)
                session.add(indicator)
        session.commit()
        print(f"✓ Loaded {len(REFERENCE_DATA['cmr_indicators'])} CMR indicators")

        # Load Strategic Axis Results (TableRef 01)
        print("Loading strategic axis results...")
        for result_data in REFERENCE_DATA["strategic_axis_results"]:
            existing = session.query(StrategicAxisResultModel).filter_by(result_id=result_data["result_id"]).first()
            if not existing:
                result = StrategicAxisResultModel(**result_data)
                session.add(result)
        session.commit()
        print(f"✓ Loaded {len(REFERENCE_DATA['strategic_axis_results'])} strategic axis results")

        # Load Operational Results (TableRef 04)
        print("Loading operational results...")
        for result_data in REFERENCE_DATA["operational_results"]:
            existing = session.query(OperationalResultModel).filter_by(result_code=result_data["result_code"]).first()
            if not existing:
                result = OperationalResultModel(**result_data)
                session.add(result)
        session.commit()
        print(f"✓ Loaded {len(REFERENCE_DATA['operational_results'])} operational results")

        # Load Participating Structures (TableRef 05)
        print("Loading participating structures...")
        for structure_data in REFERENCE_DATA["participating_structures"]:
            existing = session.query(ParticipatingStructureModel).filter_by(structure_code=structure_data["structure_code"]).first()
            if not existing:
                structure = ParticipatingStructureModel(**structure_data)
                session.add(structure)
        session.commit()
        print(f"✓ Loaded {len(REFERENCE_DATA['participating_structures'])} participating structures")

        print("\n🎉 All reference data loaded successfully!")
        print("\nAvailable TableRef endpoints:")
        print("  - TableRef:01: /api/v1/mali-references/strategic-results")
        print("  - TableRef:02: /api/v1/mali-references/structures")
        print("  - TableRef:03: /api/v1/mali-references/cmr-indicators")
        print("  - TableRef:04: /api/v1/mali-references/operational-results")
        print("  - TableRef:05: /api/v1/mali-references/participating-structures")
        print("  - TableRef:06: /api/v1/mali-references/monitoring-indicators")
        print("  - TableRef:07: /api/v1/mali-references/financing-sources")
        print("  - TableRef:08: /api/v1/mali-references/regions")
        print("  - TableRef:09: /api/v1/mali-references/cercles")
        print("  - Generic lookup: POST /api/v1/mali-references/lookup")

    except Exception as e:
        print(f"❌ Error loading reference data: {e}")
        session.rollback()
        raise
    finally:
        session.close()


def verify_data():
    """Verify that the data was loaded correctly"""
    session_generator = get_db()
    session = next(session_generator)
    
    try:
        # Check counts for each table
        region_count = session.query(MaliRegionModel).count()
        cercle_count = session.query(MaliCercleModel).count()
        structure_count = session.query(INSTATStructureModel).count()
        financing_count = session.query(FinancingSourceModel).count()
        monitoring_count = session.query(MonitoringIndicatorModel).count()
        cmr_count = session.query(CMRIndicatorModel).count()
        strategic_count = session.query(StrategicAxisResultModel).count()
        operational_count = session.query(OperationalResultModel).count()
        participating_count = session.query(ParticipatingStructureModel).count()
        
        print("\nData verification:")
        print(f"  - Regions: {region_count}")
        print(f"  - Cercles: {cercle_count}")
        print(f"  - Structures: {structure_count}")
        print(f"  - Financing sources: {financing_count}")
        print(f"  - Monitoring indicators: {monitoring_count}")
        print(f"  - CMR indicators: {cmr_count}")
        print(f"  - Strategic results: {strategic_count}")
        print(f"  - Operational results: {operational_count}")
        print(f"  - Participating structures: {participating_count}")
        
        # Test a few sample queries
        print("\nSample data verification:")
        
        # Check if Bamako region exists
        bamako = session.query(MaliRegionModel).filter_by(region_name="Bamako").first()
        if bamako:
            print(f"  ✓ Bamako region found: {bamako.region_code}")
        
        # Check if INSTAT structure exists
        instat = session.query(INSTATStructureModel).filter_by(abbreviation="INSTAT").first()
        if instat:
            print(f"  ✓ INSTAT structure found: {instat.structure_id}")
        
        # Check cercles in Bamako
        bamako_cercles = session.query(MaliCercleModel).filter_by(region_code="09").count()
        print(f"  ✓ Bamako has {bamako_cercles} communes")
        
        return True
    
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False
    finally:
        session.close()


if __name__ == "__main__":
    print("🚀 Loading Mali reference data into the database...")
    print("=" * 60)
    
    # Load the data
    load_reference_data()
    
    # Verify the data
    verify_data()
    
    print("\n" + "=" * 60)
    print("✅ Mali reference data loading complete!")
    print("\nYou can now use the Mali reference tables in your surveys.")
    print("The tables support TableRef:01 through TableRef:09 as specified")
    print("in the MODELISATION document.")
