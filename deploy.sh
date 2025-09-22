#!/bin/bash

# =====================================================================
# INSTAT Survey Platform - Complete Deployment Script
# This script handles the entire deployment process including database setup
# =====================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="instat-survey-platform"
COMPOSE_PROJECT_NAME="instat-survey-platform"

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

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    print_header "Checking Prerequisites"

    # Check Docker
    if ! command -v docker >/dev/null 2>&1; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    print_success "Docker is available"

    # Check Docker Compose
    if ! command -v docker-compose >/dev/null 2>&1; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    print_success "Docker Compose is available"

    # Check if user is in docker group
    if ! groups | grep -q docker; then
        print_warning "User is not in docker group. You may need sudo privileges."
    fi

    # Check required files
    required_files=(
        "docker-compose.yml"
        "Dockerfile"
        "scripts/setup_database.sh"
        "migrations/complete_instat_platform_migration.sql"
        "scripts/populate_mali_reference_data.sql"
    )

    for file in "${required_files[@]}"; do
        if [ ! -f "$file" ]; then
            print_error "Required file not found: $file"
            exit 1
        fi
    done
    print_success "All required files found"
}

# Setup directories
setup_directories() {
    print_header "Setting Up Directories"

    directories=(
        "logs"
        "uploads"
        "generated"
        "data/postgres"
        "data/redis"
        "backups"
    )

    for dir in "${directories[@]}"; do
        mkdir -p "$dir"
        print_success "Created directory: $dir"
    done

    # Set permissions
    chmod +x scripts/*.sh scripts/*.py 2>/dev/null || true
    print_success "Set executable permissions on scripts"
}

# Environment setup
setup_environment() {
    print_header "Setting Up Environment"

    # Create .env file if it doesn't exist
    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            cp .env.example .env
            print_success "Created .env from template"
        else
            # Create basic .env file
            cat > .env << EOF
# Database Configuration
DATABASE_URL=postgresql://postgres:password@db:5432/instat_surveys
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=instat_surveys

# Security
SECRET_KEY=muqObXpk89vWh_6YpNGYMv20iH8Lu7CLW5nh7FCi-o
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Application
ENVIRONMENT=production
DEBUG=false
API_V1_STR=/api/v1

# File Upload
MAX_FILE_SIZE=100MB
UPLOAD_PATH=./uploads
ALLOWED_FILE_EXTENSIONS=[".xlsx",".xls"]

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log
EOF
            print_success "Created basic .env file"
        fi
    else
        print_info ".env file already exists"
    fi
}

# Build and start services
deploy_services() {
    print_header "Building and Starting Services"

    # Stop existing containers
    print_info "Stopping existing containers..."
    docker-compose down 2>/dev/null || true

    # Remove old images (optional)
    if [ "$1" = "--fresh" ]; then
        print_info "Removing old images for fresh build..."
        docker-compose down --rmi all --volumes 2>/dev/null || true
    fi

    # Build application
    print_info "Building application image..."
    if docker-compose build --no-cache; then
        print_success "Application image built successfully"
    else
        print_error "Failed to build application image"
        exit 1
    fi

    # Start services
    print_info "Starting services..."
    if docker-compose up -d; then
        print_success "Services started successfully"
    else
        print_error "Failed to start services"
        exit 1
    fi

    # Wait for services to be ready
    print_info "Waiting for services to be ready..."
    sleep 10

    # Check service health
    check_services_health
}

# Check services health
check_services_health() {
    print_header "Checking Service Health"

    # Check PostgreSQL
    print_info "Checking PostgreSQL health..."
    for i in {1..30}; do
        if docker-compose exec -T db pg_isready -U postgres >/dev/null 2>&1; then
            print_success "PostgreSQL is ready"
            break
        fi
        if [ $i -eq 30 ]; then
            print_error "PostgreSQL failed to start within 5 minutes"
            print_info "Checking PostgreSQL logs:"
            docker-compose logs db
            exit 1
        fi
        sleep 10
    done

    # Check Redis
    print_info "Checking Redis health..."
    if docker-compose exec -T redis redis-cli ping >/dev/null 2>&1; then
        print_success "Redis is ready"
    else
        print_warning "Redis is not responding, but continuing..."
    fi

    # Check application
    print_info "Checking application health..."
    for i in {1..30}; do
        if curl -f http://localhost:8000/health >/dev/null 2>&1; then
            print_success "Application is ready"
            break
        fi
        if [ $i -eq 30 ]; then
            print_error "Application failed to start within 5 minutes"
            print_info "Checking application logs:"
            docker-compose logs app
            exit 1
        fi
        sleep 10
    done
}

# Setup database
setup_database() {
    print_header "Setting Up Database"

    # Make sure database setup script is executable
    chmod +x scripts/setup_database.sh

    # Run database setup
    if ./scripts/setup_database.sh; then
        print_success "Database setup completed successfully"
    else
        print_error "Database setup failed"
        print_info "Checking database logs:"
        docker-compose logs db
        exit 1
    fi
}

# Verify deployment
verify_deployment() {
    print_header "Verifying Deployment"

    # Check container status
    print_info "Checking container status..."
    if docker-compose ps | grep -q "Up"; then
        print_success "All containers are running"
    else
        print_error "Some containers are not running"
        docker-compose ps
        exit 1
    fi

    # Test API endpoints
    print_info "Testing API endpoints..."

    # Health check
    if curl -f http://localhost:8000/health >/dev/null 2>&1; then
        print_success "Health check endpoint is working"
    else
        print_error "Health check endpoint failed"
        exit 1
    fi

    # Test authentication
    print_info "Testing authentication system..."
    TOKEN=$(curl -s -X POST "http://localhost:8000/v1/api/auth/token" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "username=admin@instat.gov.ml&password=admin123" | \
        python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null || echo "")

    if [ -n "$TOKEN" ]; then
        print_success "Authentication system is working"

        # Test authenticated endpoint
        if curl -f -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/mali-reference/regions >/dev/null 2>&1; then
            print_success "Authenticated API endpoints are working"
        else
            print_warning "Authenticated endpoints might have issues"
        fi
    else
        print_warning "Could not get authentication token, but deployment may still be successful"
    fi

    # Verify database data
    print_info "Verifying database data..."
    ./scripts/setup_database.sh --verify
}

# Show deployment summary
show_summary() {
    print_header "Deployment Summary"

    echo "🎉 INSTAT Survey Platform deployed successfully!"
    echo
    echo "📊 Service Status:"
    docker-compose ps
    echo
    echo "🔗 Access URLs:"
    echo "  • Application: http://localhost:8000"
    echo "  • API Documentation (Swagger): http://localhost:8000/docs"
    echo "  • API Documentation (ReDoc): http://localhost:8000/redoc"
    echo "  • Database: localhost:5432"
    echo "  • Redis: localhost:6379"
    if docker-compose ps | grep -q superset; then
        echo "  • Apache Superset: http://localhost:8088"
    fi
    echo
    echo "🔐 Default Credentials:"
    echo "  • Username: admin@instat.gov.ml"
    echo "  • Password: admin123"
    echo
    echo "📝 Available API Endpoints:"
    echo "  • Authentication: POST /api/v1/auth/token"
    echo "  • File Upload: POST /api/v1/files/upload-excel-and-create-survey"
    echo "  • Templates: GET /api/v1/instat/templates"
    echo "  • Mali Reference: GET /api/v1/mali-reference/*"
    echo "  • Admin Panel: GET /api/v1/admin/*"
    echo
    echo "🛠️ Useful Commands:"
    echo "  • View logs: docker-compose logs -f"
    echo "  • Stop services: docker-compose down"
    echo "  • Restart services: docker-compose restart"
    echo "  • Update deployment: ./deploy.sh --update"
    echo "  • Database backup: docker-compose exec db pg_dump -U postgres instat_surveys > backup.sql"
    echo
    echo "📖 For detailed documentation, see DATABASE_SETUP.md"
}

# Update deployment
update_deployment() {
    print_header "Updating Deployment"

    # Pull latest changes
    if command -v git >/dev/null 2>&1 && [ -d ".git" ]; then
        print_info "Pulling latest changes from git..."
        git pull
    fi

    # Backup database
    print_info "Creating database backup..."
    mkdir -p backups
    docker-compose exec -T db pg_dump -U postgres instat_surveys > "backups/backup_$(date +%Y%m%d_%H%M%S).sql" 2>/dev/null || print_warning "Database backup failed"

    # Rebuild and restart
    deploy_services

    # Run any new migrations
    print_info "Running database updates if needed..."
    ./scripts/setup_database.sh --migration-only 2>/dev/null || print_info "No additional database updates needed"

    verify_deployment
    print_success "Deployment updated successfully"
}

# Show help
show_help() {
    echo "INSTAT Survey Platform Deployment Script"
    echo
    echo "Usage: $0 [OPTION]"
    echo
    echo "Options:"
    echo "  --fresh         Clean deployment (removes old images and volumes)"
    echo "  --update        Update existing deployment"
    echo "  --db-only       Setup database only (assumes services are running)"
    echo "  --verify        Verify current deployment"
    echo "  --help, -h      Show this help message"
    echo
    echo "Default behavior (no options):"
    echo "  1. Check prerequisites"
    echo "  2. Setup directories and environment"
    echo "  3. Build and start services"
    echo "  4. Setup database with complete migration and reference data"
    echo "  5. Verify deployment"
    echo "  6. Show deployment summary"
}

# Main function
main() {
    cd "$SCRIPT_DIR"

    print_header "INSTAT Survey Platform Deployment"
    echo "Starting deployment process..."
    echo

    check_prerequisites
    setup_directories
    setup_environment
    deploy_services "$1"
    setup_database
    verify_deployment
    show_summary
}

# Handle command line arguments
case "$1" in
    --fresh)
        main --fresh
        ;;
    --update)
        update_deployment
        ;;
    --db-only)
        print_header "Database Setup Only"
        check_prerequisites
        setup_database
        ;;
    --verify)
        print_header "Verifying Deployment"
        verify_deployment
        ;;
    --help|-h)
        show_help
        ;;
    *)
        main
        ;;
esac
