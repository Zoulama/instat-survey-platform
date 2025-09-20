# Database Migration Guide for INSTAT Survey Platform

This guide explains how to handle database migrations, particularly for the new User table fields.

## Recent Changes

### User Table Updates
We've added two new fields to the Users table:
- `Status` (VARCHAR(50), default: 'active') - User account status
- `Department` (VARCHAR(100), nullable) - User department/division

## Migration Options

### Option 1: Fresh Deployment
If you're doing a fresh deployment, use the updated complete migration:
```bash
# Run the complete migration (includes new fields)
docker exec -i <db_container> psql -U postgres -d instat_surveys < migrations/complete_instat_platform_migration.sql
```

### Option 2: Update Existing Database
If you have an existing database, run the specific migration:
```bash
# Add the new fields to existing Users table
docker exec -i <db_container> psql -U postgres -d instat_surveys < migrations/add_user_status_department_fields.sql
```

### Option 3: Manual Database Update
You can manually add the fields:
```sql
-- Add Status column
ALTER TABLE "Users" ADD COLUMN "Status" VARCHAR(50) DEFAULT 'active';

-- Add Department column  
ALTER TABLE "Users" ADD COLUMN "Department" VARCHAR(100);

-- Update existing users
UPDATE "Users" SET "Status" = 'active' WHERE "Status" IS NULL;

-- Add indexes
CREATE INDEX IF NOT EXISTS idx_users_status ON "Users" ("Status");
CREATE INDEX IF NOT EXISTS idx_users_department ON "Users" ("Department");
```

## User Management API Changes

The following API endpoints now support the new fields:

### User Update (PUT /v1/api/admin/users/{user_id})
Request body now accepts:
```json
{
  "email": "user@example.com",
  "role": "manager", 
  "status": "active",
  "department": "Direction Générale"
}
```

### User Response
All user responses now include:
```json
{
  "user_id": 1,
  "username": "admin",
  "email": "admin@instat.gov.ml",
  "role": "admin",
  "status": "active",
  "department": "Direction Générale"
}
```

## Available User Statuses
- `active` - User can log in and access the system
- `inactive` - User account is disabled
- `suspended` - User account is temporarily suspended
- `pending` - User account awaiting activation

## Available Departments
Based on INSTAT organizational structure:
- Direction Générale
- Direction des Enquêtes et Sondages
- Direction du Système Statistique National
- Direction de la Synthèse et des Données Sectorielles
- Direction Administrative et Financière
- Direction des Ressources Humaines
- Direction des Systèmes d'Information

## Password Reset Feature

A new password reset functionality has been added:

### Endpoint: POST /v1/api/admin/users/{user_id}/reset-password

Request body:
```json
{
  "generate_temp_password": true,
  "temp_password_length": 12,
  "send_email_notification": false
}
```

Response:
```json
{
  "user_id": 1,
  "username": "john_doe",
  "temp_password": "TempPass123!",
  "reset_timestamp": "2025-09-20T15:30:00",
  "message": "Password successfully reset for user john_doe"
}
```

## Troubleshooting

### Migration Errors
If you get errors during migration:

1. **Column already exists**: This is normal if running multiple times
2. **Permission denied**: Ensure the database user has ALTER TABLE permissions
3. **Constraint violations**: Check if you have invalid data in the Users table

### API Errors
If you get schema validation errors:
1. Rebuild the Docker container: `docker compose build app`
2. Restart the application: `docker compose up -d app`
3. Check the OpenAPI schema: `curl http://localhost:8000/openapi.json`

## Verification

After migration, verify the changes:

```sql
-- Check table structure
\d "Users"

-- Check existing data
SELECT "Username", "Status", "Department" FROM "Users";

-- Test indexes
\di idx_users_*
```

The API documentation should show the new fields at: http://localhost:8000/docs