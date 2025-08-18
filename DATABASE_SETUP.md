# INSTAT Survey Platform - Database Setup Guide

This document provides comprehensive guidance for setting up the INSTAT Survey Platform database with complete migration and Mali reference data population.

## 📋 Overview

The database setup includes:
- **Complete database migration** with all tables and structures
- **OAuth2 authentication system** with role-based access control
- **Audit logging system** for administrative actions
- **Mali reference data** (TableRef 01-09) with real data
- **Parsing results storage** with rolling retention
- **Performance indexes** and triggers

## 🎯 Quick Start

### Automated Setup Script (Recommended)

```bash
# Make script executable
chmod +x scripts/setup_database.sh

# Or with specific options
./scripts/setup_database.sh --migration-only
./scripts/setup_database.sh --data-only

NEW_HASH=$(docker exec -i instat-survey-platform-app-1 python3 -c "
import bcrypt
password = 'admin123!'
password_bytes = password.encode('utf-8')
salt = bcrypt.gensalt(rounds=12)
hashed = bcrypt.hashpw(password_bytes, salt)
print(hashed.decode('utf-8'))
")
docker exec -i instat-survey-platform-db-1 psql -U postgres -d instat_surveys -c "INSERT INTO \"Users\" (\"Username\", \"Email\", \"Role\", \"HashedPassword\") VALUES ('admin', 'admin@instat.gov.ml', 'admin', '$NEW_HASH');"


./scripts/setup_database.sh --verify
```

## 📁 File Structure

```
├── migrations/
│   └── complete_instat_platform_migration.sql  # Complete database schema
├── scripts/
│   ├── setup_database.sh                       # Automated setup script
│   └── populate_mali_reference_data.sql        # Mali reference data
└── DATABASE_SETUP.md                           # This documentation
```

## 🗄️ Database Schema

### Core Survey Tables
- **Users** - User management with OAuth2 support
- **Roles** - Role-based access control
- **Surveys** - Base survey structure
- **INSTATSurveys** - INSTAT-specific survey fields
- **SurveyTemplates** - Reusable survey templates
- **Sections/Subsections** - Survey structure
- **Questions/AnswerOptions** - Survey questions
- **Responses/ResponseDetails** - Survey responses

### Security & Audit Tables
- **audit_logs** - Complete audit trail
- **parsing_results** - File parsing history (rolling retention)
- **parsing_statistics** - Parsing performance metrics

### Mali Reference Tables (TableRef 01-09)
- **strategic_axis_results** - SDS strategic framework
- **instat_structures** - INSTAT organizational structure
- **cmr_indicators** - Performance measurement indicators
- **operational_results** - Operational objectives and results
- **participating_structures** - Partner organizations
- **monitoring_indicators** - Monitoring and evaluation indicators
- **financing_sources** - Funding sources and partners
- **mali_regions** - Mali administrative regions
- **mali_cercles** - Mali administrative circles
- **table_reference_mappings** - Reference table metadata

## 📊 Mali Reference Data Details

### TableRef 01: Strategic Axis Results (17 records)
Strategic axes, operational objectives, and expected results from Mali's Statistical Development Strategy (SDS).

### TableRef 02: INSTAT Structures (20 records)
Complete organizational structure including:
- Central directorates (DG, DGA, SG)
- Technical directions (DES, SSN, SDS, DPPD)
- Support directions (DAF, DRH, DSI)
- Regional antennas (8 regions)
- Specialized centers (CAPI, CTSI)

### TableRef 03: CMR Indicators (16 records)
Results Measurement Framework indicators covering:
- Demographic indicators
- Economic indicators  
- Social indicators
- Governance indicators
- Environmental indicators

### TableRef 04: Operational Results (9 records)
Expected results by operational objective and strategic axis.

### TableRef 05: Participating Structures (18 records)
Partner organizations including:
- Government ministries
- Regulatory institutions
- Development organizations
- Private sector representatives
- Academic institutions

### TableRef 06: Monitoring Indicators (16 records)
Performance monitoring indicators for:
- NSS performance
- Capacity building
- Quality assurance
- Data dissemination

### TableRef 07: Financing Sources (17 records)
Funding sources including:
- National budget
- Bilateral cooperation (France, Germany, USA, Japan)
- Multilateral organizations (World Bank, African Development Bank, EU, UNDP)
- Regional organizations (BCEAO, UEMOA, ECOWAS)
- Private foundations and partnerships

### TableRef 08: Mali Regions (10 records)
All administrative regions with geographic coordinates:
- Kayes, Koulikoro, Sikasso, Ségou, Mopti
- Tombouctou, Gao, Kidal, Bamako District
- Taoudénit (newest region)

### TableRef 09: Mali Cercles (65 records)
All administrative circles with demographic data:
- Complete coverage of Mali's administrative divisions
- Population and surface area data
- Capital cities and geographic relationships

## 🚀 Features Enabled

### OAuth2 Security System
- JWT-based authentication
- Role-based access control (admin, manager, data_scientist, readonly, write)
- Secure password hashing with bcrypt
- Token expiration and refresh mechanisms

### Audit Logging
- Complete action tracking for administrative operations
- IP address and user agent logging
- Success/failure tracking with error messages
- JSON detail storage for complex operations

### Parsing Results Storage
- Rolling retention (last 100 uploads automatically maintained)
- File integrity verification with SHA-256 hashing
- Processing time and performance metrics
- Comprehensive metadata tracking

### Performance Optimizations
- Indexes on frequently queried columns
- Automatic timestamp updates
- Foreign key constraints for data integrity
- Triggers for rolling retention and maintenance

## 🔐 Default Credentials

**Admin User:**
- Username: `admin`
- Password: `admin123!`
- Role: `admin` (full access)

**Default Roles:**
- `admin` - Full administrative access
- `manager` - Management permissions
- `data_scientist` - Analysis permissions
- `readonly` - Read-only access
- `write` - General write access

## 🛠️ Environment Configuration

### Database Connection
```bash
export DB_HOST="localhost"
export DB_PORT="5432"
export DB_NAME="instat_surveys"
export DB_USER="postgres"
export DB_PASSWORD="your_password"
```

### Docker Environment
```bash
export DOCKER_CONTAINER="instat-survey-platform_postgres_1"
```

## 🧪 Testing the Setup

### 1. Verify Database Connection
```bash
./scripts/setup_database.sh --verify
```

### 2. Test Authentication
```bash
curl -X POST "http://localhost:8000/v1/api/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123!"
```

### 3. Test Reference Data
```bash
# Get Mali regions
curl -X GET "http://localhost:8000/v1/api/mali-reference/regions" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get INSTAT structures
curl -X GET "http://localhost:8000/v1/api/mali-reference/structures" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 4. Test File Upload
```bash
curl -X POST "http://localhost:8000/v1/api/files/upload-excel-and-create-survey" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@sample_survey.xlsx"
```

## 🔧 Maintenance

### Database Backup
```bash
# Using Docker
docker exec postgres_container pg_dump -U postgres instat_surveys > backup.sql

# Local PostgreSQL
pg_dump -h localhost -U postgres instat_surveys > backup.sql
```

### Rolling Retention Cleanup
The parsing results table automatically maintains only the last 100 upload records. This is handled by database triggers.

### Performance Monitoring
```sql
-- Check audit log growth
SELECT COUNT(*), DATE(timestamp) FROM audit_logs GROUP BY DATE(timestamp);

-- Check parsing results statistics
SELECT status, COUNT(*) FROM parsing_results GROUP BY status;

-- Monitor table sizes
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(tablename::regclass)) 
FROM pg_tables WHERE schemaname = 'public' ORDER BY pg_total_relation_size(tablename::regclass) DESC;
```

## 🚨 Troubleshooting

### Common Issues

**1. Connection Failed**
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Check connection parameters
psql -h localhost -p 5432 -U postgres -d instat_surveys -c "SELECT 1;"
```

**2. Permission Denied**
```bash
# Make sure script is executable
chmod +x scripts/setup_database.sh

# Check database permissions
GRANT ALL PRIVILEGES ON DATABASE instat_surveys TO postgres;
```

**3. Migration Errors**
```sql
-- Check if tables already exist
\dt

-- Drop specific table if needed (CAREFUL!)
DROP TABLE IF EXISTS table_name CASCADE;
```

**4. Data Population Issues**
```sql
-- Check reference data counts
SELECT 'mali_regions' as table_name, COUNT(*) FROM mali_regions
UNION ALL
SELECT 'instat_structures', COUNT(*) FROM instat_structures;
```

### Reset Database (if needed)
```sql
-- DANGER: This will delete all data
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
```

## 📞 Support

For technical support with database setup:

1. Check the troubleshooting section above
2. Review the setup logs for specific error messages
3. Ensure all prerequisites are met (PostgreSQL, Docker if applicable)
4. Verify network connectivity and firewall settings

## 📈 Next Steps After Setup

1. **Configure Application**: Update application configuration files
2. **Start Services**: Launch the FastAPI application server
3. **Test Authentication**: Verify OAuth2 token generation
4. **Upload Test Data**: Test Excel file parsing functionality
5. **Access Admin Panel**: Use audit logging and user management features
6. **Configure Monitoring**: Set up log monitoring and alerting
7. **Backup Strategy**: Implement regular database backups
8. **SSL Configuration**: Enable HTTPS for production deployment

The database is now ready for full INSTAT Survey Platform operations with comprehensive security, audit trails, and Mali-specific reference data!
