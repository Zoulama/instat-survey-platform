"""
Upload tracking utility for logging and managing file uploads
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class UploadTracker:
    """Track file uploads with timestamps and metadata"""
    
    def __init__(self, log_file_path: str = "logs/uploads.json"):
        self.log_file = Path(log_file_path)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize log file if it doesn't exist
        if not self.log_file.exists():
            self._write_log([])
    
    def log_upload(self, upload_info: Dict[str, Any]) -> None:
        """Log a file upload with timestamp and metadata"""
        try:
            # Read existing logs
            uploads = self._read_log()
            
            # Add new upload entry
            upload_entry = {
                "id": len(uploads) + 1,
                "timestamp": datetime.utcnow().isoformat(),
                **upload_info
            }
            uploads.append(upload_entry)
            
            # Keep only the last 1000 uploads to prevent log file from growing too large
            if len(uploads) > 1000:
                uploads = uploads[-1000:]
            
            # Write back to file
            self._write_log(uploads)
            
            logger.info(f"Logged upload: {upload_info.get('timestamped_filename', 'unknown')}")
            
        except Exception as e:
            logger.error(f"Failed to log upload: {e}")
    
    def get_recent_uploads(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent uploads, most recent first"""
        try:
            uploads = self._read_log()
            return uploads[-limit:] if uploads else []
        except Exception as e:
            logger.error(f"Failed to read upload log: {e}")
            return []
    
    def get_uploads_by_user(self, username: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get uploads by specific user"""
        try:
            uploads = self._read_log()
            user_uploads = [u for u in uploads if u.get('uploaded_by') == username]
            return user_uploads[-limit:] if user_uploads else []
        except Exception as e:
            logger.error(f"Failed to read upload log for user {username}: {e}")
            return []
    
    def get_uploads_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get uploads within a date range"""
        try:
            uploads = self._read_log()
            filtered_uploads = []
            
            for upload in uploads:
                upload_time = datetime.fromisoformat(upload.get('timestamp', ''))
                if start_date <= upload_time <= end_date:
                    filtered_uploads.append(upload)
            
            return filtered_uploads
        except Exception as e:
            logger.error(f"Failed to filter uploads by date range: {e}")
            return []
    
    def get_upload_statistics(self) -> Dict[str, Any]:
        """Get upload statistics"""
        try:
            uploads = self._read_log()
            
            if not uploads:
                return {
                    "total_uploads": 0,
                    "unique_users": 0,
                    "total_file_size": 0,
                    "uploads_today": 0,
                    "uploads_this_week": 0,
                    "uploads_this_month": 0
                }
            
            # Calculate statistics
            total_uploads = len(uploads)
            unique_users = len(set(u.get('uploaded_by') for u in uploads if u.get('uploaded_by')))
            total_file_size = sum(u.get('file_size', 0) for u in uploads)
            
            # Date-based statistics
            now = datetime.utcnow()
            today = now.date()
            week_ago = now.replace(day=now.day-7) if now.day > 7 else now.replace(month=now.month-1, day=30-7+now.day)
            month_ago = now.replace(month=now.month-1) if now.month > 1 else now.replace(year=now.year-1, month=12)
            
            uploads_today = len([u for u in uploads 
                               if datetime.fromisoformat(u.get('timestamp', '')).date() == today])
            uploads_this_week = len([u for u in uploads 
                                   if datetime.fromisoformat(u.get('timestamp', '')) >= week_ago])
            uploads_this_month = len([u for u in uploads 
                                    if datetime.fromisoformat(u.get('timestamp', '')) >= month_ago])
            
            return {
                "total_uploads": total_uploads,
                "unique_users": unique_users,
                "total_file_size": total_file_size,
                "average_file_size": total_file_size / total_uploads if total_uploads > 0 else 0,
                "uploads_today": uploads_today,
                "uploads_this_week": uploads_this_week,
                "uploads_this_month": uploads_this_month,
                "most_active_user": self._get_most_active_user(uploads)
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate upload statistics: {e}")
            return {"error": str(e)}
    
    def cleanup_old_files(self, days_old: int = 30) -> int:
        """Clean up uploaded files older than specified days"""
        try:
            uploads = self._read_log()
            cutoff_date = datetime.utcnow().replace(day=datetime.utcnow().day - days_old)
            
            files_deleted = 0
            remaining_uploads = []
            
            for upload in uploads:
                upload_time = datetime.fromisoformat(upload.get('timestamp', ''))
                
                if upload_time < cutoff_date:
                    # Delete the file if it exists
                    file_path = Path(upload.get('file_path', ''))
                    if file_path.exists():
                        file_path.unlink()
                        files_deleted += 1
                        logger.info(f"Deleted old file: {file_path}")
                else:
                    remaining_uploads.append(upload)
            
            # Update log with remaining uploads
            self._write_log(remaining_uploads)
            
            return files_deleted
            
        except Exception as e:
            logger.error(f"Failed to cleanup old files: {e}")
            return 0
    
    def _read_log(self) -> List[Dict[str, Any]]:
        """Read upload log from file"""
        try:
            if self.log_file.exists():
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Failed to read upload log: {e}")
            return []
    
    def _write_log(self, uploads: List[Dict[str, Any]]) -> None:
        """Write upload log to file"""
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(uploads, f, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            logger.error(f"Failed to write upload log: {e}")
    
    def _get_most_active_user(self, uploads: List[Dict[str, Any]]) -> Optional[str]:
        """Get the most active user from uploads"""
        try:
            user_counts = {}
            for upload in uploads:
                user = upload.get('uploaded_by')
                if user:
                    user_counts[user] = user_counts.get(user, 0) + 1
            
            if user_counts:
                return max(user_counts.items(), key=lambda x: x[1])[0]
            return None
            
        except Exception as e:
            logger.error(f"Failed to get most active user: {e}")
            return None


# Global tracker instance
upload_tracker = UploadTracker()