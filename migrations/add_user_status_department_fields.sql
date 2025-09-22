-- =====================================================================
-- Migration: Add Status, Department, FirstName, and LastName fields to Users table
-- This migration adds the Status, Department, FirstName, and LastName fields to existing Users tables
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

-- Add FirstName column if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'Users' AND column_name = 'FirstName') THEN
        ALTER TABLE "Users" ADD COLUMN "FirstName" VARCHAR(100) NOT NULL DEFAULT '';
        RAISE NOTICE 'Added FirstName column to Users table';
    ELSE
        RAISE NOTICE 'FirstName column already exists in Users table';
    END IF;
END $$;

-- Add LastName column if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'Users' AND column_name = 'LastName') THEN
        ALTER TABLE "Users" ADD COLUMN "LastName" VARCHAR(100) NOT NULL DEFAULT '';
        RAISE NOTICE 'Added LastName column to Users table';
    ELSE
        RAISE NOTICE 'LastName column already exists in Users table';
    END IF;
END $$;

-- Update existing users to have active status
UPDATE "Users" SET "Status" = 'active' WHERE "Status" IS NULL;

-- Add indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_status ON "Users" ("Status");
CREATE INDEX IF NOT EXISTS idx_users_role ON "Users" ("Role");
CREATE INDEX IF NOT EXISTS idx_users_department ON "Users" ("Department");

-- Update existing admin user with department, firstname, lastname if not set
UPDATE "Users" 
SET "Department" = 'IT',
    "FirstName" = 'Admin',
    "LastName" = 'User'
WHERE "Username" = 'admin' AND ("Department" IS NULL OR "Department" = '');

-- Update any existing users to ensure they have FirstName and LastName
UPDATE "Users" 
SET "FirstName" = COALESCE(NULLIF("FirstName", ''), 'User'),
    "LastName" = COALESCE(NULLIF("LastName", ''), SPLIT_PART("Email", '@', 1))
WHERE "FirstName" = '' OR "LastName" = '' OR "FirstName" IS NULL OR "LastName" IS NULL;

-- Add indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_firstname ON "Users" ("FirstName");
CREATE INDEX IF NOT EXISTS idx_users_lastname ON "Users" ("LastName");

-- Final success messages
DO $$
BEGIN
    RAISE NOTICE 'Successfully added Status, Department, FirstName, and LastName fields to Users table';
    RAISE NOTICE 'All existing users set to active status';
    RAISE NOTICE 'Admin user updated with default values';
    RAISE NOTICE 'All users now have FirstName and LastName values';
END $$;
