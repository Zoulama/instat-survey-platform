# INSTAT Digital Platform for Managing Statistical Activities

## Overview

This is a comprehensive digital platform designed for INSTAT (National Institute of Statistics) to manage the entire statistical production chain. The platform consists of five main modules that handle different aspects of statistical survey management and data processing.

## Platform Modules

1. **Metadata Management** - Manage definitions, classifications, indicators, and statistical foundations
2. **Form Designer** - Visual drag-and-drop form editor with conditional logic
3. **Data Collection** - Multi-device responsive data entry interface with offline capability
4. **Data Processing** - Generic data processing with validation rules and Superset integration
5. **Dissemination** - Publishing and sharing results with access control

## Architecture

- **Backend**: Python with FastAPI framework
- **Database**: PostgreSQL with multiple schemas for different macro-activities
- **Authentication**: JWT-based authentication with role-based access control
- **Deployment**: Docker containers with docker-compose
- **Data Processing**: Apache Superset integration for analytics

## Database Schemas

The platform supports three main macro-activities, each with dedicated database schemas:
- `survey_program` - Program management surveys
- `survey_balance` - Balance sheet surveys  
- `survey_diagnostic` - Diagnostic surveys

## 🚀 Quick Deployment

For rapid deployment with complete database setup and Mali reference data:

```bash
# Clone the repository
git clone https://github.com/your-org/instat-survey-platform.git
cd instat-survey-platform

# Build and start all services
docker compose down && docker compose build app && docker compose up -d

# Wait for services to start, then set up database
sleep 10 && DOCKER_CONTAINER=instat-survey-platform-db-1 ./scripts/setup_database.sh

# Create admin user with proper password hash
NEW_HASH=$(docker exec -i instat-survey-platform-app-1 python3 -c "
import bcrypt
password = 'admin123!'
password_bytes = password.encode('utf-8')
salt = bcrypt.gensalt(rounds=12)
hashed = bcrypt.hashpw(password_bytes, salt)
print(hashed.decode('utf-8'))
")
docker exec -i instat-survey-platform-db-1 psql -U postgres -d instat_surveys -c "INSERT INTO \"Users\" (\"Username\", \"Email\", \"Role\", \"HashedPassword\") VALUES ('admin', 'admin@instat.gov.ml', 'admin', '$NEW_HASH');"

# Verify database setup
DOCKER_CONTAINER=instat-survey-platform-db-1 ./scripts/setup_database.sh --verify
```

**Access the platform:**
- Application: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Admin Login: `username=admin`, `password=admin123!`

## Features

### Core Features
- Multi-device responsive forms (mobile, tablet, desktop)
- Offline-first data collection with sync capabilities
- Real-time form validation and conditional logic
- Excel/Word document parsing and form generation
- Hierarchical form structure management
- Role-based access control (Admin, Manager, Data Scientist, ReadOnly, Write)

### Advanced Features
- **OAuth2 Authentication** with JWT tokens and role-based permissions
- **Comprehensive Audit Logging** for all administrative actions
- **Mali Reference Data** with complete administrative divisions
- **File Upload Tracking** with rolling retention (last 100 uploads)
- AI-powered form generation
- Big Data and AI pipeline for data cleaning
- Automated anomaly detection
- Integration with existing tools (CSPro, SPSS, KoBoToolbox)
- Multi-language support
- WCAG accessibility compliance

## On-Premise Deployment Guide

### Prerequisites

Before deploying the INSTAT Survey Platform on-premise, ensure your server meets these requirements:

#### System Requirements
- **Operating System**: Linux (Ubuntu 20.04+ recommended) or CentOS/RHEL 8+
- **Memory**: Minimum 8GB RAM (16GB+ recommended for production)
- **Storage**: Minimum 50GB free disk space (SSD recommended)
- **CPU**: Minimum 4 cores (8+ cores recommended for production)
- **Network**: Internet access for initial setup and updates

#### Software Dependencies
- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 2.0 or higher
- **Git**: For cloning the repository
- **curl/wget**: For health checks and testing

### Step 1: Install System Dependencies

#### On Ubuntu/Debian:
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y git curl wget unzip

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Logout and login again for Docker group changes
newgrp docker
```

#### On CentOS/RHEL:
```bash
# Update system packages
sudo yum update -y

# Install required packages
sudo yum install -y git curl wget unzip

# Install Docker
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install -y docker-ce docker-ce-cli containerd.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Logout and login again for Docker group changes
newgrp docker
```

### Step 2: Clone and Prepare the Application

```bash
# Clone the repository
git clone https://github.com/your-org/instat-survey-platform.git
cd instat-survey-platform

# Create necessary directories
mkdir -p logs
mkdir -p data/postgres
mkdir -p data/redis
mkdir -p uploads
mkdir -p generated

# Set proper permissions
sudo chown -R $USER:$USER .
chmod +x scripts/*.py
```

### Step 3: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit environment configuration
nano .env
```

**Key environment variables to configure:**
```env
# Database Configuration
DATABASE_URL=postgresql://postgres:your_secure_password@db:5432/instat_survey_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=instat_survey_db

# Redis Configuration
REDIS_URL=redis://redis:6379/0

# Security
SECRET_KEY=your_very_secure_secret_key_here_minimum_32_characters
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Application
ENVIRONMENT=production
DEBUG=false
API_V1_STR=/v1

# CORS Settings
ALLOWED_HOSTS=["localhost","127.0.0.1","your-domain.com"]
CORS_ORIGINS=["http://localhost:3000","https://your-domain.com"]

# File Upload
MAX_FILE_SIZE=100MB
UPLOAD_PATH=./uploads

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log
```

### Step 4: Build and Deploy with Docker

```bash
# Build the application image
docker-compose build --no-cache

# Start all services in detached mode
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f app
```

### Step 5: Initialize Database with Complete Setup

```bash
# Wait for database to be ready (about 30 seconds)
sleep 30

# Check database connectivity
docker-compose exec db pg_isready -U postgres

# Run the automated database setup script (RECOMMENDED)
./scripts/setup_database.sh

# OR run manual setup if needed:
# 1. Run complete database migration
docker exec -i $(docker-compose ps -q db) psql -U postgres -d instat_surveys < migrations/complete_instat_platform_migration.sql

# 2. Populate Mali reference data
docker exec -i $(docker-compose ps -q db) psql -U postgres -d instat_surveys < scripts/populate_mali_reference_data.sql

# Verify the setup was successful
./scripts/setup_database.sh --verify
```

### Step 6: Verify Database Setup

```bash
# Check that all tables were created and data populated
docker-compose exec db psql -U postgres -d instat_surveys -c "
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
SELECT 'Financing Sources', COUNT(*) FROM financing_sources
UNION ALL
SELECT 'Table Reference Mappings', COUNT(*) FROM table_reference_mappings;
"

# Expected output should show:
# Users: 1 (admin user)
# Mali Regions: 10
# Mali Cercles: 65
# INSTAT Structures: 20
# Strategic Axis Results: 17
# CMR Indicators: 16
# Financing Sources: 17
# Table Reference Mappings: 9
```

### Step 7: Test Authentication System

```bash
# Test the OAuth2 authentication system
# The admin user is automatically created by the migration
# Default credentials: username=admin, password=admin123!

# Get authentication token
curl -X POST "http://localhost:8000/api/v1/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123!"

# Test authenticated endpoint (replace YOUR_TOKEN with the token from above)
curl -X GET "http://localhost:8000/api/v1/admin/audit-logs" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Test Mali reference data endpoints
curl -X GET "http://localhost:8000/api/v1/mali-reference/regions" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Step 8: Configure Reverse Proxy (Optional but Recommended)

For production deployments, use Nginx as a reverse proxy:

```bash
# Install Nginx
sudo apt install -y nginx  # Ubuntu/Debian
# OR
sudo yum install -y nginx   # CentOS/RHEL

# Create Nginx configuration
sudo tee /etc/nginx/sites-available/instat-survey > /dev/null <<EOF
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    client_max_body_size 100M;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }
    
    location /static {
        alias /var/www/instat-survey/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# Enable the site
sudo ln -s /etc/nginx/sites-available/instat-survey /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl enable nginx
```

### Step 9: Configure SSL/TLS (Recommended)

```bash
# Install Certbot for Let's Encrypt
sudo apt install -y certbot python3-certbot-nginx  # Ubuntu/Debian
# OR
sudo yum install -y certbot python3-certbot-nginx   # CentOS/RHEL

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Test automatic renewal
sudo certbot renew --dry-run
```

### Step 10: Setup System Services (Optional)

Create systemd services for automatic startup:

```bash
# Create service file
sudo tee /etc/systemd/system/instat-survey.service > /dev/null <<EOF
[Unit]
Description=INSTAT Survey Platform
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/\$USER/instat-survey-platform
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
TimeoutStartSec=0
User=\$USER
Group=\$USER

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
sudo systemctl enable instat-survey.service
sudo systemctl start instat-survey.service
```

### Step 11: Verification and Testing

```bash
# Check all containers are running
docker-compose ps

# Test API endpoints
curl -f http://localhost:8000/health
curl -f http://localhost:8000/v1/

# Test database connectivity
docker-compose exec db psql -U postgres -d instat_survey_db -c "SELECT COUNT(*) FROM alembic_version;"

# Test Redis connectivity
docker-compose exec redis redis-cli ping

# Test file upload (create a small test file)
echo "test" > test.txt
curl -X POST -F "file=@test.txt" http://localhost:8000/v1/files/upload
rm test.txt
```

### Step 12: Monitoring and Maintenance

```bash
# View application logs
docker-compose logs -f app

# Monitor resource usage
docker stats

# Backup database
docker-compose exec db pg_dump -U postgres -d instat_survey_db > backup_$(date +%Y%m%d).sql

# Update application
git pull
docker-compose build --no-cache
docker-compose up -d
```

### Troubleshooting

#### Common Issues:

1. **Port conflicts**: Ensure ports 8000, 5432, 6379 are available
   ```bash
   sudo netstat -tulpn | grep :8000
   sudo netstat -tulpn | grep :5432
   sudo netstat -tulpn | grep :6379
   ```

2. **Permission issues**: Fix file permissions
   ```bash
   sudo chown -R $USER:$USER .
   chmod 755 scripts/*.py
   ```

3. **Database connection issues**: Check PostgreSQL status
   ```bash
   docker-compose logs db
   docker-compose exec db psql -U postgres -c "\l"
   ```

4. **Memory issues**: Monitor Docker resource usage
   ```bash
   docker system df
   docker system prune -a  # Clean unused images
   ```

#### Health Checks:

- **API Health**: `http://localhost:8000/health`
- **Database**: `docker-compose exec db pg_isready -U postgres`
- **Redis**: `docker-compose exec redis redis-cli ping`
- **Application**: `docker-compose exec app python -c "import requests; print(requests.get('http://localhost:8000/health').status_code)"`

### Performance Tuning

For production environments:

1. **PostgreSQL tuning**:
   ```bash
   # Edit postgresql.conf in container
   docker-compose exec db bash -c "echo 'shared_buffers = 256MB' >> /var/lib/postgresql/data/postgresql.conf"
   docker-compose exec db bash -c "echo 'effective_cache_size = 1GB' >> /var/lib/postgresql/data/postgresql.conf"
   docker-compose restart db
   ```

2. **Application scaling**:
   ```yaml
   # In docker-compose.yml, scale the app service
   app:
     deploy:
       replicas: 3
   ```

3. **Resource limits**:
   ```yaml
   # Add resource limits to docker-compose.yml
   deploy:
     resources:
       limits:
         cpus: '2.0'
         memory: 4G
       reservations:
         memory: 2G
   ```

## Development Setup

For development purposes, you can also run the application locally:

```bash
# Clone the repository
git clone https://github.com/your-org/instat-survey-platform.git
cd instat-survey-platform

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Set up local PostgreSQL and Redis
# Configure .env file with local database settings

# Run database migrations
alembic upgrade head

# Start development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Directory Structure

```
instat-survey-platform/
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── docker-compose.yml     # Docker services configuration
├── database/              # Database schemas and migrations
├── src/
│   ├── api/              # API endpoints
│   ├── domain/           # Business logic and entities
│   ├── infrastructure/   # External services and storage
│   └── utils/            # Helper utilities
├── schemas/              # Pydantic models
├── static/               # Static files
└── templates/            # HTML templates
```

## License

This project is licensed under the MIT License.
