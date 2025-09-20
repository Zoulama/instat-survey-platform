-- =====================================================================
-- Migration: Add Status and Department fields to Users table
-- This migration adds the Status and Department fields to existing Users tables
-- =====================================================================

-- Add Status column if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'Users' AND column_name = 'Status') THEN
        ALTER TABLE "Users" ADD COLUMN "Status" VARCHAR(50) DEFAULT 'active';
        RAISE NOTICE 'Added Status column to Users table';
    ELSE
        RAISE NOTICE 'Status column already exists in Users table';
    END IF;
END $$;

-- Add Department column if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'Users' AND column_name = 'Department') THEN
        ALTER TABLE "Users" ADD COLUMN "Department" VARCHAR(100);
        RAISE NOTICE 'Added Department column to Users table';
    ELSE
        RAISE NOTICE 'Department column already exists in Users table';
    END IF;
END $$;

-- Update existing users to have active status
UPDATE "Users" SET "Status" = 'active' WHERE "Status" IS NULL;

-- Add indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_status ON "Users" ("Status");
CREATE INDEX IF NOT EXISTS idx_users_role ON "Users" ("Role");
CREATE INDEX IF NOT EXISTS idx_users_department ON "Users" ("Department");

-- Update existing admin user with department if not set
UPDATE "Users" 
SET "Department" = 'Direction Générale' 
WHERE "Username" = 'admin' AND ("Department" IS NULL OR "Department" = '');

-- Final success messages
DO $$
BEGIN
    RAISE NOTICE 'Successfully added Status and Department fields to Users table';
    RAISE NOTICE 'All existing users set to active status';
    RAISE NOTICE 'Admin user assigned to Direction Générale';
END $$;
