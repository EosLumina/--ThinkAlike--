-- Create Events table (if not exists)
CREATE TABLE IF NOT EXISTS Events (
    event_id VARCHAR(255) PRIMARY KEY,
    community_id VARCHAR(255) NOT NULL,
    event_name VARCHAR(255) NOT NULL,
    description TEXT,
    location VARCHAR(255),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    geofence_parameters JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (community_id) REFERENCES Communities(community_id)
);

-- Create LiveLocationShares table
CREATE TABLE IF NOT EXISTS LiveLocationShares (
    share_id UUID PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    recipient_id VARCHAR(255) NOT NULL,
    start_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    -- Note: recipient_id could reference either Users or Communities
    -- This is simplified here but would need proper handling in application logic
    
    -- Add indexes for common queries
    INDEX (user_id, active),
    INDEX (recipient_id, active)
);

-- Create EventProximityOptIns table
CREATE TABLE IF NOT EXISTS EventProximityOptIns (
    event_id VARCHAR(255) NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    opt_in_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    opt_out_time TIMESTAMP NULL,
    PRIMARY KEY (event_id, user_id),
    FOREIGN KEY (event_id) REFERENCES Events(event_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    
    -- Add index for common queries
    INDEX (event_id, opt_out_time)
);

-- Create audit trigger for location sharing
CREATE OR REPLACE FUNCTION audit_location_sharing()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO AuditLog (
        action_type,
        table_name,
        record_id,
        user_id,
        timestamp,
        details
    ) VALUES (
        TG_OP,
        TG_TABLE_NAME,
        NEW.share_id::text,
        NEW.user_id,
        CURRENT_TIMESTAMP,
        jsonb_build_object(
            'recipient_id', NEW.recipient_id,
            'duration_minutes', EXTRACT(EPOCH FROM (NEW.end_time - NEW.start_time))/60
        )
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER location_sharing_audit
AFTER INSERT OR UPDATE OR DELETE ON LiveLocationShares
FOR EACH ROW EXECUTE FUNCTION audit_location_sharing();

-- Add location-related fields to Profiles table
ALTER TABLE Profiles
ADD COLUMN IF NOT EXISTS static_location_city VARCHAR(255),
ADD COLUMN IF NOT EXISTS static_location_country VARCHAR(255);