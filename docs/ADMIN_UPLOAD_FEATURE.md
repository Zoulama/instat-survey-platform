# Admin-Only Upload Feature

## Overview

The file upload and import functionality in the INSTAT Survey Platform is now restricted to administrators only. This security measure ensures that only authorized users can import Excel files and create survey structures, maintaining data integrity and system security.

## Permission System

### User Roles & Scopes

The system uses a combination of roles and scopes to control access:

#### Admin Roles
- `admin` - Full administrative access
- `super_admin` - Super administrator access  
- `system_admin` - System administrator access

#### Scopes
- `admin:read` - Read administrative data
- `admin:write` - Create/modify administrative data
- `admin:delete` - Delete administrative data
- `upload:admin` - Administrative upload permissions
- `upload:read` - Read upload data
- `upload:write` - Basic upload permissions (deprecated for file imports)

### Permission Levels

1. **Admin** - Full access to all features
2. **Upload Admin** - Can upload files and access admin upload features
3. **Read Admin** - Can view all uploads and statistics
4. **User** - Can only view their own uploads
5. **Basic** - Limited access

## Restricted Endpoints

### File Upload (Admin Only)
```
POST /v1/api/files/upload-excel-and-create-survey
POST /v1/api/files/upload-excel-and-create-survey-with-template
```

**Required Permission**: `admin:write` scope or admin role
**Description**: Upload Excel files and automatically create survey structures

### Upload Management (Admin Only)
```
GET  /v1/api/uploads/recent
GET  /v1/api/uploads/by-user/{username}
GET  /v1/api/uploads/by-date-range
GET  /v1/api/uploads/statistics
GET  /v1/api/uploads/today
POST /v1/api/uploads/cleanup
```

**Required Permission**: `admin:read` or `admin:write` scope

### User Accessible Endpoints
```
GET /v1/api/uploads/my-uploads
GET /v1/api/uploads/permissions
```

**Required Permission**: `upload:read` scope

## Implementation Details

### Admin Permission Checking

The system implements multiple layers of security:

1. **Scope-based Authorization**: FastAPI `require_scopes()` decorator
2. **Custom Admin Checks**: `AdminPermissions` utility class
3. **Runtime Validation**: Additional permission checks in endpoint handlers

```python
# Example permission check
admin_permissions.require_upload_admin_access(current_user)
```

### Upload Tracking

All uploads are tracked with:
- Timestamp of upload
- User information
- File metadata
- Upload path
- File size

### Error Responses

Non-admin users attempting to access restricted endpoints will receive:

```json
{
  "detail": "Admin access required for file upload operations. Contact your administrator for access.",
  "status_code": 403
}
```

## API Usage Examples

### Check User Permissions
```bash
curl -X GET "/v1/api/uploads/permissions" \
  -H "Authorization: Bearer {token}"
```

Response:
```json
{
  "username": "john.doe",
  "permission_level": "user",
  "can_upload_files": false,
  "can_view_all_uploads": false,
  "can_manage_uploads": false,
  "accessible_endpoints": [
    "GET /v1/api/uploads/my-uploads",
    "GET /v1/api/uploads/permissions"
  ]
}
```

### Admin File Upload
```bash
curl -X POST "/v1/api/files/upload-excel-and-create-survey" \
  -H "Authorization: Bearer {admin_token}" \
  -F "file=@survey_template.xlsx" \
  -F "create_template=true"
```

### View Upload Statistics (Admin Only)
```bash
curl -X GET "/v1/api/uploads/statistics" \
  -H "Authorization: Bearer {admin_token}"
```

Response:
```json
{
  "total_uploads": 25,
  "unique_users": 3,
  "total_file_size": 1048576,
  "average_file_size": 41943.04,
  "uploads_today": 2,
  "uploads_this_week": 8,
  "uploads_this_month": 25,
  "most_active_user": "admin"
}
```

## Security Features

### Upload Timestamping
All uploaded files are automatically timestamped to prevent filename conflicts:
```
original_file.xlsx → original_file_20240925_143022.xlsx
```

### Audit Trail
Complete audit trail of all uploads including:
- Original filename
- Timestamped filename  
- Upload timestamp
- User information
- File size and path

### Access Control
- JWT-based authentication
- Role-based access control (RBAC)
- Scope-based permissions
- Runtime permission validation

### File Cleanup
Automated cleanup utilities for managing old files:
```bash
POST /v1/api/uploads/cleanup?days_old=30
```

## Configuration

### Environment Variables
```bash
# Upload directory
UPLOAD_DIR=/path/to/uploads

# Allowed file extensions
ALLOWED_FILE_EXTENSIONS=['.xlsx', '.xls']

# Admin roles
ADMIN_ROLES=admin,super_admin,system_admin
```

### Database Schema
Upload tracking is stored in JSON log files at `logs/uploads.json` with automatic rotation.

## Migration Guide

### For Existing Users
1. Contact your administrator to request upload permissions
2. Administrators need to assign `admin:write` scope or admin role
3. Use `/v1/api/uploads/permissions` to verify access level

### For Administrators
1. Ensure users have appropriate scopes in the authentication system
2. Monitor uploads via statistics endpoints
3. Regularly clean up old files using cleanup utilities

## Troubleshooting

### Common Issues

**403 Forbidden Error**
- **Cause**: User lacks admin permissions
- **Solution**: Contact administrator for access or verify JWT token contains required scopes

**File Upload Fails**
- **Cause**: Invalid file format or size limits
- **Solution**: Ensure file is Excel format (.xlsx, .xls) and within size limits

**Upload Not Tracked**
- **Cause**: Upload tracker logging failure
- **Solution**: Check logs directory permissions and disk space

### Support
For technical support or permission requests, contact your system administrator.