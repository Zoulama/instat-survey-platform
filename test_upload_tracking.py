#!/usr/bin/env python3
"""
Test script for upload tracking functionality
"""
import asyncio
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, Any
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.utils.upload_tracker import upload_tracker


def test_upload_tracker_directly():
    """Test the upload tracker utility directly"""
    print("Testing UploadTracker utility directly...")
    print("=" * 50)
    
    # Create some test upload entries
    test_uploads = [
        {
            "original_filename": "test_file_1.xlsx",
            "timestamped_filename": "test_file_1_20240115_143022.xlsx",
            "upload_timestamp": datetime.utcnow().isoformat(),
            "uploaded_by": "test_user_1",
            "file_size": 2048,
            "file_path": "/uploads/test_file_1_20240115_143022.xlsx"
        },
        {
            "original_filename": "survey_data.xlsx",
            "timestamped_filename": "survey_data_20240115_143045.xlsx",
            "upload_timestamp": (datetime.utcnow() - timedelta(hours=2)).isoformat(),
            "uploaded_by": "test_user_2",
            "file_size": 4096,
            "file_path": "/uploads/survey_data_20240115_143045.xlsx"
        },
        {
            "original_filename": "report.docx",
            "timestamped_filename": "report_20240115_120000.docx",
            "upload_timestamp": (datetime.utcnow() - timedelta(days=1)).isoformat(),
            "uploaded_by": "test_user_1",
            "file_size": 8192,
            "file_path": "/uploads/report_20240115_120000.docx"
        }
    ]
    
    # Log test uploads
    print("1. Logging test uploads...")
    for upload in test_uploads:
        upload_tracker.log_upload(upload)
        print(f"   - Logged: {upload['original_filename']}")
    
    # Test getting recent uploads
    print("\n2. Getting recent uploads...")
    recent_uploads = upload_tracker.get_recent_uploads(limit=10)
    print(f"   Found {len(recent_uploads)} recent uploads:")
    for upload in recent_uploads[-3:]:  # Show last 3
        print(f"   - {upload.get('original_filename')} by {upload.get('uploaded_by')}")
    
    # Test getting uploads by user
    print("\n3. Getting uploads by user 'test_user_1'...")
    user_uploads = upload_tracker.get_uploads_by_user("test_user_1", limit=10)
    print(f"   Found {len(user_uploads)} uploads for test_user_1:")
    for upload in user_uploads:
        print(f"   - {upload.get('original_filename')}")
    
    # Test getting uploads by date range
    print("\n4. Getting uploads from the last 2 days...")
    start_date = datetime.utcnow() - timedelta(days=2)
    end_date = datetime.utcnow()
    date_uploads = upload_tracker.get_uploads_by_date_range(start_date, end_date)
    print(f"   Found {len(date_uploads)} uploads in date range:")
    for upload in date_uploads[-3:]:  # Show last 3
        print(f"   - {upload.get('original_filename')} at {upload.get('timestamp')}")
    
    # Test getting statistics
    print("\n5. Getting upload statistics...")
    stats = upload_tracker.get_upload_statistics()
    if "error" not in stats:
        print(f"   Total uploads: {stats.get('total_uploads', 0)}")
        print(f"   Unique users: {stats.get('unique_users', 0)}")
        print(f"   Total file size: {stats.get('total_file_size', 0)} bytes")
        print(f"   Average file size: {stats.get('average_file_size', 0):.2f} bytes")
        print(f"   Uploads today: {stats.get('uploads_today', 0)}")
        print(f"   Most active user: {stats.get('most_active_user', 'None')}")
    else:
        print(f"   Error getting statistics: {stats['error']}")
    
    print("\n✅ Direct upload tracker tests completed!")


def test_file_upload_with_tracking():
    """Test file upload endpoints to verify tracking integration"""
    print("\nTesting file upload with tracking integration...")
    print("=" * 50)
    
    # This would require a running server and authentication
    # For now, just check if the integration is properly set up
    
    try:
        from src.api.v1.file_upload import router as upload_router
        print("✅ File upload router imported successfully")
        
        # Check if upload_tracker is imported
        import src.api.v1.file_upload as upload_module
        if hasattr(upload_module, 'upload_tracker'):
            print("✅ upload_tracker is properly imported in file upload module")
        else:
            print("❌ upload_tracker not found in file upload module")
            
    except ImportError as e:
        print(f"❌ Error importing file upload module: {e}")
    
    try:
        from src.api.v1.upload_tracking import router as tracking_router
        print("✅ Upload tracking router imported successfully")
        
        # Check router configuration
        print(f"   Router prefix: {tracking_router.prefix}")
        print(f"   Router tags: {tracking_router.tags}")
        print(f"   Number of routes: {len(tracking_router.routes)}")
        
        # List available endpoints
        print("   Available endpoints:")
        for route in tracking_router.routes:
            if hasattr(route, 'path') and hasattr(route, 'methods'):
                methods = ', '.join(route.methods) if route.methods else 'GET'
                print(f"     {methods} {route.path}")
                
    except ImportError as e:
        print(f"❌ Error importing upload tracking module: {e}")


def test_api_endpoints_structure():
    """Test API endpoints structure and documentation"""
    print("\nTesting API endpoints structure...")
    print("=" * 50)
    
    try:
        # Import the main FastAPI app
        from main import app
        print("✅ Main FastAPI app imported successfully")
        
        # Check if all routers are included
        router_prefixes = []
        for route in app.routes:
            if hasattr(route, 'path_regex'):
                # Extract prefix from path
                path = str(route.path_regex.pattern)
                if '/v1/api/' in path:
                    prefix = path.split('/v1/api/')[1].split('/')[0].replace('\\', '')
                    if prefix and prefix not in router_prefixes:
                        router_prefixes.append(prefix)
        
        print(f"   Found API prefixes: {router_prefixes}")
        
        # Check if upload tracking is included
        if 'uploads' in router_prefixes:
            print("✅ Upload tracking endpoints are registered")
        else:
            print("❌ Upload tracking endpoints not found in registered routes")
            
        # Count total routes
        total_routes = len([r for r in app.routes if hasattr(r, 'path_regex')])
        print(f"   Total API routes: {total_routes}")
        
    except Exception as e:
        print(f"❌ Error testing API structure: {e}")


def cleanup_test_data():
    """Clean up test data"""
    print("\nCleaning up test data...")
    print("=" * 50)
    
    try:
        # Remove test log file if it exists
        import os
        from pathlib import Path
        
        log_file = Path("logs/uploads.json")
        if log_file.exists():
            # Read current data
            with open(log_file, 'r') as f:
                data = json.load(f)
            
            # Filter out test entries
            filtered_data = [
                item for item in data 
                if not item.get('uploaded_by', '').startswith('test_user')
            ]
            
            # Write back filtered data
            with open(log_file, 'w') as f:
                json.dump(filtered_data, f, indent=2)
            
            print(f"✅ Cleaned up test data from {log_file}")
            print(f"   Removed {len(data) - len(filtered_data)} test entries")
        else:
            print("   No log file found to clean up")
            
    except Exception as e:
        print(f"❌ Error cleaning up test data: {e}")


def main():
    """Run all tests"""
    print("INSTAT Survey Platform - Upload Tracking Tests")
    print("=" * 60)
    
    try:
        # Test 1: Direct utility testing
        test_upload_tracker_directly()
        
        # Test 2: Integration testing
        test_file_upload_with_tracking()
        
        # Test 3: API structure testing
        test_api_endpoints_structure()
        
        print("\n" + "=" * 60)
        print("🎉 All tests completed!")
        print("\nNew upload tracking features:")
        print("  • Upload history logging with timestamps")
        print("  • File upload statistics and analytics")
        print("  • User-specific upload tracking")
        print("  • Date range filtering for uploads")
        print("  • Automatic file cleanup utilities")
        print("  • RESTful API endpoints for upload management")
        
        print("\nAPI Endpoints added:")
        print("  • GET  /v1/api/uploads/recent - Recent uploads")
        print("  • GET  /v1/api/uploads/my-uploads - Current user's uploads")
        print("  • GET  /v1/api/uploads/today - Today's uploads")
        print("  • GET  /v1/api/uploads/by-user/{username} - User-specific uploads")
        print("  • GET  /v1/api/uploads/by-date-range - Date-filtered uploads")
        print("  • GET  /v1/api/uploads/statistics - Upload statistics")
        print("  • POST /v1/api/uploads/cleanup - Admin cleanup utility")
        
    finally:
        # Clean up test data
        cleanup_test_data()


if __name__ == "__main__":
    main()