#!/bin/bash

# =====================================================================
# INSTAT Survey Platform - Database Setup Script
# This script runs the complete database migration and populates Mali reference data
# =====================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-instat_surveys}"
DB_USER="${DB_USER:-postgres}"
DB_PASSWORD="${DB_PASSWORD:-password}"

# Docker container name (if running in Docker)
DOCKER_CONTAINER="${DOCKER_CONTAINER:-instat-survey-platform_postgres_1}"

# Script paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MIGRATION_FILE="$PROJECT_ROOT/migrations/complete_instat_platform_migration.sql"
POPULATION_FILE="$PROJECT_ROOT/scripts/populate_mali_reference_data.sql"

# Functions
print_header() {
    echo -e "${BLUE}===========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}===========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

check_file_exists() {
    if [ ! -f "$1" ]; then
        print_error "Required file not found: $1"
        exit 1
    fi
}

# Check if running in Docker or local
check_database_connection() {
    if docker ps | grep -q "$DOCKER_CONTAINER"; then
        print_success "Docker container '$DOCKER_CONTAINER' is running"
        USE_DOCKER=true
        DB_COMMAND="docker exec -i $DOCKER_CONTAINER psql -U $DB_USER -d $DB_NAME"
    else
        print_warning "Docker container not found, attempting local connection..."
        USE_DOCKER=false

        # Test local connection
        if command -v psql >/dev/null 2>&1; then
            if PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1;" >/dev/null 2>&1; then
                print_success "Local PostgreSQL connection successful"
                DB_COMMAND="PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME"
            else
                print_error "Cannot connect to PostgreSQL database locally"
                print_error "Please ensure PostgreSQL is running and connection parameters are correct"
                echo "Connection parameters:"
                echo "  Host: $DB_HOST"
                echo "  Port: $DB_PORT"
                echo "  Database: $DB_NAME"
                echo "  User: $DB_USER"
                exit 1
            fi
        else
            print_error "psql command not found"
            print_error "Please install PostgreSQL client or run in Docker environment"
            exit 1
        fi
    fi
}

run_sql_file() {
    local file_path="$1"
    local description="$2"

    print_header "$description"

    if [ "$USE_DOCKER" = true ]; then
        echo "Executing via Docker container: $DOCKER_CONTAINER"
        if docker exec -i "$DOCKER_CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" < "$file_path"; then
            print_success "$description completed successfully"
        else
            print_error "$description failed"
            return 1
        fi
    else
        echo "Executing via local PostgreSQL connection"
        if PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -f "$file_path"; then
            print_success "$description completed successfully"
        else
            print_error "$description failed"
            return 1
        fi
    fi
}

# Backup existing data (optional)
create_backup() {
    print_header "Creating Database Backup (Optional)"

    local backup_dir="$PROJECT_ROOT/backups"
    local backup_file="$backup_dir/backup_$(date +%Y%m%d_%H%M%S).sql"

    mkdir -p "$backup_dir"

    if [ "$USE_DOCKER" = true ]; then
        if docker exec "$DOCKER_CONTAINER" pg_dump -U "$DB_USER" "$DB_NAME" > "$backup_file"; then
            print_success "Backup created: $backup_file"
        else
            print_warning "Backup creation failed, continuing anyway..."
        fi
    else
        if PGPASSWORD="$DB_PASSWORD" pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" "$DB_NAME" > "$backup_file"; then
            print_success "Backup created: $backup_file"
        else
            print_warning "Backup creation failed, continuing anyway..."
        fi
    fi
}

# Verify data population
verify_data() {
    print_header "Verifying Database Setup"

    local verify_sql="
SELECT
    'Users' as table_name, COUNT(*) as record_count FROM \"Users\"
UNION ALL
SELECT 'Mali Regions', COUNT(*) FROM mali_regions
UNION ALL
SELECT 'Mali Cercles', COUNT(*) FROM mali_cercles
UNION ALL
SELECT 'INSTAT Structures', COUNT(*) FROM instat_structures
UNION ALL
SELECT 'Strategic Axis Results', COUNT(*) FROM strategic_axis_results
UNION ALL
SELECT 'CMR Indicators', COUNT(*) FROM cmr_indicators
UNION ALL
SELECT 'Monitoring Indicators', COUNT(*) FROM monitoring_indicators
UNION ALL
SELECT 'Financing Sources', COUNT(*) FROM financing_sources
UNION ALL
SELECT 'Table Reference Mappings', COUNT(*) FROM table_reference_mappings;
"

    echo "Database record counts:"
    if [ "$USE_DOCKER" = true ]; then
        docker exec -i "$DOCKER_CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" -c "$verify_sql"
    else
        PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "$verify_sql"
    fi
}

# Main execution
main() {
    print_header "INSTAT Survey Platform Database Setup"

    echo "This script will:"
    echo "1. Check database connection"
    echo "2. Create backup (optional)"
    echo "3. Run complete database migration"
    echo "4. Populate Mali reference data"
    echo "5. Verify setup"
    echo

    # Check required files exist
    print_header "Checking Required Files"
    check_file_exists "$MIGRATION_FILE"
    check_file_exists "$POPULATION_FILE"
    print_success "All required files found"

    # Check database connection
    print_header "Checking Database Connection"
    check_database_connection

    # Ask for backup
    echo
    read -p "Create backup before migration? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        create_backup
    fi

    # Run migration
    if run_sql_file "$MIGRATION_FILE" "Running Complete Database Migration"; then
        echo

        # Run data population
        if run_sql_file "$POPULATION_FILE" "Populating Mali Reference Data"; then
            echo

            # Verify setup
            verify_data

            # Final success message
            print_header "Setup Complete!"
            print_success "INSTAT Survey Platform database is ready!"
            echo
            echo "Next steps:"
            echo "1. Start the application server"
            echo "2. Test authentication with admin/admin123!"
            echo "3. Upload Excel files to test parsing"
            echo "4. Access admin panel at /api/v1/admin/audit-logs"
            echo
            echo "API endpoints available:"
            echo "- Authentication: /api/v1/auth/token"
            echo "- File upload: /api/v1/files/upload-excel-and-create-survey"
            echo "- Templates: /api/v1/instat/templates"
            echo "- Mali reference: /api/v1/mali-reference/*"
            echo "- Admin panel: /api/v1/admin/*"

        else
            print_error "Data population failed!"
            exit 1
        fi
    else
        print_error "Database migration failed!"
        exit 1
    fi
}

# Handle script arguments
case "$1" in
    --migration-only)
        print_header "Running Migration Only"
        check_database_connection
        run_sql_file "$MIGRATION_FILE" "Running Complete Database Migration"
        ;;
    --data-only)
        print_header "Running Data Population Only"
        check_database_connection
        run_sql_file "$POPULATION_FILE" "Populating Mali Reference Data"
        ;;
    --verify)
        print_header "Verifying Database Setup"
        check_database_connection
        verify_data
        ;;
    --help|-h)
        echo "INSTAT Survey Platform Database Setup Script"
        echo
        echo "Usage: $0 [OPTION]"
        echo
        echo "Options:"
        echo "  --migration-only    Run database migration only"
        echo "  --data-only        Run data population only"
        echo "  --verify          Verify database setup"
        echo "  --help, -h        Show this help message"
        echo
        echo "Environment variables:"
        echo "  DB_HOST           Database host (default: localhost)"
        echo "  DB_PORT           Database port (default: 5432)"
        echo "  DB_NAME           Database name (default: instat_surveys)"
        echo "  DB_USER           Database user (default: postgres)"
        echo "  DB_PASSWORD       Database password (default: password)"
        echo "  DOCKER_CONTAINER  Docker container name (default: instat-survey-platform_postgres_1)"
        ;;
    *)
        main
        ;;
esac
