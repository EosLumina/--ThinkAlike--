# Database Design Guidelines

---

## 1. Introduction

Defines database design patterns, best practices, and standards for ensuring data consistency and performance.

---

## 2. Database Architecture

### 2.1 Schema Design

```mermaid
erDiagram
    USER {
        uuid id PK
        string email
        string password_hash
        timestamp created_at
    }
    PROFILE {
        uuid id PK
        uuid user_id FK
        jsonb preferences
    }
    USER ||--o| PROFILE : has
```

---

## 2. Database Design Principles

### 2.1 Core Principles

* **Single Source of Truth**: Store each piece of data in one place
* **Normalization**: Structure data to minimize redundancy
* **Performance**: Design for query efficiency and scalability
* **Integrity**: Enforce data consistency through constraints
* **Security**: Apply the principle of least privilege
* **Maintainability**: Design for clarity and ease of modification

### 2.2 Technology Choices

ThinkAlike uses the following database technologies:

* **Primary Database**: PostgreSQL (relational)
* **Caching Layer**: Redis
* **Search Engine**: Elasticsearch
* **Time-Series Data**: InfluxDB (for metrics and analytics)
* **Graph Relationships**: Neo4j (for social/connection features)

---

## 3. Schema Design

### 3.1 Naming Conventions

* Use **snake_case** for all database objects (tables, columns, indexes)
* Use **plural nouns** for table names (e.g., `users`, `preferences`)
* Use **singular nouns** for column names (e.g., `first_name`, `created_at`)
* Prefix join tables with joined table names (e.g., `users_teams`)
* Use consistent prefixes for related tables

```sql
-- Example of proper naming conventions
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE users_teams (
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    team_id INTEGER NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL DEFAULT 'member',
    joined_at TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (user_id, team_id)
);
```

### 3.2 Data Types

* Choose the **most appropriate data type** for each column
* Use **fixed-length** types when the length is known
* Consider **storage requirements** and **query performance**
* Use **domain-specific types** when available (e.g., UUID, JSONB, ARRAY)

| Data Category | Preferred Type | Notes |
|---------------|---------------|-------|
| Identifiers | INTEGER, BIGINT, UUID | Use UUID for distributed systems |
| Short Text | VARCHAR(n) | Specify appropriate length |
| Long Text | TEXT | For variable-length content |
| Dates and Times | TIMESTAMP WITH TIME ZONE | Always store in UTC |
| Booleans | BOOLEAN | Not NULL with default |
| Floating Point | NUMERIC | For financial calculations |
| Enumerated Values | ENUM or CHECK constraint | For fixed sets of values |
| JSON Data | JSONB | For flexible schema content |
| Binary Data | BYTEA | For files, consider external storage |

```sql
-- Example proper data type usage
CREATE TABLE content_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    body TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'draft'
        CHECK (status IN ('draft', 'published', 'archived')),
    view_count INTEGER NOT NULL DEFAULT 0,
    metadata JSONB,
    published_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);
```

### 3.3 Relationships

* Define **foreign keys** to enforce referential integrity
* Consider **cascading operations** for related data
* Use **join tables** for many-to-many relationships
* Include **relationship metadata** when needed (e.g., role, status)

```sql
-- Example relationships
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    content_item_id UUID NOT NULL REFERENCES content_items(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    parent_comment_id INTEGER REFERENCES comments(id) ON DELETE SET NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_comments_content_item ON comments(content_item_id);
CREATE INDEX idx_comments_user ON comments(user_id);
CREATE INDEX idx_comments_parent ON comments(parent_comment_id);
```

---

## 4. Indexing Strategy

### 4.1 Index Types

* **Primary Key**: Define for all tables
* **Unique Index**: For columns with uniqueness constraints
* **Foreign Key Index**: Create indexes for all foreign keys
* **Composite Index**: For queries with multiple conditions
* **Partial Index**: For filtering on specific values
* **Expression Index**: For transformed data lookups

### 4.2 Indexing Guidelines

* Index columns used in **WHERE, JOIN, and ORDER BY** clauses
* Consider the **selectivity** of the indexed columns
* Balance between **query performance** and **write overhead**
* Monitor and adjust indexes based on **query patterns**
* Name indexes consistently: `idx_[table]_[column(s)]`

```sql
-- Example indexing strategy
CREATE TABLE user_activities (
    id BIGSERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    activity_type VARCHAR(50) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id VARCHAR(36) NOT NULL,
    data JSONB,
    ip_address INET,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Index for user-specific activity queries
CREATE INDEX idx_user_activities_user_id ON user_activities(user_id);

-- Composite index for filtered activity queries
CREATE INDEX idx_user_activities_type_entity ON user_activities(activity_type, entity_type, entity_id);

-- Index for recent activity queries
CREATE INDEX idx_user_activities_created_at ON user_activities(created_at DESC);

-- Partial index for specific activity types
CREATE INDEX idx_user_activities_logins ON user_activities(user_id, created_at)
WHERE activity_type = 'login';

-- Expression index for JSON queries
CREATE INDEX idx_user_activities_data_source ON user_activities((data->>'source'));
```

### 4.3 Index Monitoring

* Regularly review index usage statistics
* Identify missing or unused indexes
* Rebuild indexes periodically to reduce fragmentation
* Consider index maintenance during off-peak hours

```sql
-- Query to find unused indexes
SELECT
    s.schemaname,
    s.relname AS tablename,
    i.indexrelname AS indexname,
    pg_size_pretty(pg_relation_size(i.indexrelid)) AS index_size,
    idx_scan AS index_scans
FROM
    pg_stat_user_indexes i
JOIN
    pg_stat_user_tables s ON i.relid = s.relid
WHERE
    idx_scan = 0 -- Unused indexes
ORDER BY
    pg_relation_size(i.indexrelid) DESC;
```

---

## 5. Performance Optimization

### 5.1 Query Optimization

* Write **efficient queries** that minimize data retrieval
* Use **appropriate joins** instead of multiple queries
* Apply **filtering early** in the query
* Optimize **sorting and grouping** operations
* Consider **pagination** for large result sets

```sql
-- Example optimized query with filtering, joining, and pagination
SELECT
    p.id,
    p.title,
    p.content_summary,
    u.username AS author_name,
    COUNT(c.id) AS comment_count
FROM
    posts p
    JOIN users u ON p.author_id = u.id
    LEFT JOIN comments c ON c.post_id = p.id
WHERE
    p.status = 'published'
    AND p.published_at > (NOW() - INTERVAL '30 days')
GROUP BY
    p.id, p.title, p.content_summary, u.username
ORDER BY
    p.published_at DESC
LIMIT 20 OFFSET 40;
```

### 5.2 Database Connection Management

* Use **connection pooling** to manage database connections
* Set appropriate **pool sizes** based on workload
* Monitor **connection usage** and adjust as needed
* Implement **connection timeout** and **retry logic**

```python
# Example SQLAlchemy connection pool configuration
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:password@localhost/dbname"

engine = create_engine(
    DATABASE_URL,
    # Connection pool settings
    pool_size=10,  # Maximum connections in pool
    max_overflow=20,  # Maximum overflow connections
    pool_timeout=30,  # Seconds to wait for connection
    pool_recycle=1800,  # Recycle connections after 30 minutes
    echo=False,  # Set to True for query logging
)

Session = sessionmaker(bind=engine)
```

### 5.3 Caching Strategy

* Cache **frequently accessed** and **slow-changing** data
* Implement **cache invalidation** strategies
* Consider **multi-level caching** (application, distributed, database)
* Monitor **cache hit ratios** and adjust caching policies

```python
# Example Redis caching implementation
import redis
import json
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_result(ttl_seconds=300):
    """Cache function results in Redis."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Create a cache key based on function name and arguments
            key_parts = [func.__name__]
            key_parts.extend([str(arg) for arg in args])
            key_parts.extend([f"{k}:{v}" for k, v in sorted(kwargs.items())])
            cache_key = "cache:" + ":".join(key_parts)

            # Try to get from cache
            cached_result = redis_client.get(cache_key)
            if cached_result:
                return json.loads(cached_result)

            # If not in cache, call the function
            result = await func(*args, **kwargs)

            # Cache the result
            redis_client.setex(
                cache_key,
                ttl_seconds,
                json.dumps(result)
            )

            return result
        return wrapper
    return decorator

# Usage example
@cache_result(ttl_seconds=60)
async def get_user_recommendations(user_id: int, limit: int = 10):
    # Expensive database query to generate recommendations
    # ...
    return recommendations
```

---

## 6. Data Migration and Evolution

### 6.1 Schema Migrations

* Use a **migration framework** to manage schema changes
* Write **reversible migrations** when possible
* Separate **data migrations** from schema changes
* Test migrations with **production-like data volumes**

```python
# Example Alembic migration script
"""Add user preferences table

Revision ID: 3a7e8bcf01d2
Revises: 2b5ef815d23e
Create Date: 2023-04-10 14:27:32.651987

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '3a7e8bcf01d2'
down_revision = '2b5ef815d23e'
branch_labels = None
depends_on = None

def upgrade():
    # Create new table
    op.create_table(
        'user_preferences',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('preference_key', sa.String(length=100), nullable=False),
        sa.Column('preference_value', sa.Text(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes
    op.create_index('idx_user_preferences_user_id', 'user_preferences', ['user_id'])
    op.create_unique_constraint('uq_user_preferences_user_key', 'user_preferences', ['user_id', 'preference_key'])

def downgrade():
    # Drop table and constraints
    op.drop_index('idx_user_preferences_user_id')
    op.drop_table('user_preferences')
```

### 6.2 Migration Best Practices

* Schedule migrations during **low-traffic periods**
* Implement **zero-downtime migrations** for production
* Create **backup points** before major migrations
* Monitor **database performance** during and after migrations
* Have a **rollback plan** for failed migrations

### 6.3 Versioning

* Maintain **backward compatibility** when possible
* Document **breaking changes** thoroughly
* Consider **schema versioning** for major changes
* Use **feature flags** to gradually roll out changes

---

## 7. Database Security

### 7.1 Access Control

* Apply the **principle of least privilege**
* Create **separate database users** for different access patterns
* Use **role-based access control**
* Revoke unnecessary permissions
* Regularly audit database access

```sql
-- Example database role and permission setup
CREATE ROLE app_readonly;
CREATE ROLE app_readwrite;
CREATE ROLE app_admin;

-- Grant appropriate permissions
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_readonly;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_readwrite;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_readwrite;

-- Grant admin permissions
GRANT ALL PRIVILEGES ON SCHEMA public TO app_admin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO app_admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO app_admin;

-- Create application users
CREATE USER app_api_user WITH PASSWORD 'secure_password';
GRANT app_readwrite TO app_api_user;

CREATE USER reporting_user WITH PASSWORD 'another_secure_password';
GRANT app_readonly TO reporting_user;
```

### 7.2 Data Encryption

* Encrypt **sensitive data** at rest
* Use **transport layer security** (TLS/SSL) for connections
* Implement **column-level encryption** for PII
* Store **encryption keys** separately from the data
* Regularly rotate encryption keys

```sql
-- Example of column-level encryption function
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Function to encrypt data
CREATE OR REPLACE FUNCTION encrypt_pii(input_text TEXT)
RETURNS TEXT AS $$
BEGIN
    RETURN pgp_sym_encrypt(
        input_text,
        current_setting('app.encryption_key')
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to decrypt data
CREATE OR REPLACE FUNCTION decrypt_pii(encrypted_text TEXT)
RETURNS TEXT AS $$
BEGIN
    RETURN pgp_sym_decrypt(
        encrypted_text::bytea,
        current_setting('app.encryption_key')
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Example table with encrypted columns
CREATE TABLE customer_data (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    ssn TEXT, -- Will store encrypted value
    credit_card_number TEXT, -- Will store encrypted value
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Example usage
INSERT INTO customer_data (customer_id, ssn, credit_card_number)
VALUES (
    123,
    encrypt_pii('123-45-6789'),
    encrypt_pii('4111-1111-1111-1111')
);
```

### 7.3 Auditing

* Enable **database audit logging**
* Track **schema changes**
* Monitor **suspicious query patterns**
* Implement **row-level change tracking**
* Store audit logs securely

```sql
-- Example audit trail implementation
CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    operation VARCHAR(10) NOT NULL,
    record_id INTEGER NOT NULL,
    old_data JSONB,
    new_data JSONB,
    changed_by VARCHAR(100) NOT NULL,
    changed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Example trigger function for auditing
CREATE OR REPLACE FUNCTION audit_trigger_func()
RETURNS TRIGGER AS $$
DECLARE
    audit_row audit_log;
    include_old BOOLEAN;
    include_new BOOLEAN;
BEGIN
    audit_row = ROW(
        nextval('audit_log_id_seq'),
        TG_TABLE_NAME,
        TG_OP,
        NULL, -- Will be replaced with actual ID
        NULL, -- Will hold old data if relevant
        NULL, -- Will hold new data if relevant
        current_setting('app.current_user', TRUE),
        NOW()
    );

    IF TG_OP = 'DELETE' THEN
        audit_row.record_id = OLD.id;
        audit_row.old_data = to_jsonb(OLD);
    ELSIF TG_OP = 'UPDATE' THEN
        audit_row.record_id = NEW.id;
        audit_row.old_data = to_jsonb(OLD);
        audit_row.new_data = to_jsonb(NEW);
    ELSIF TG_OP = 'INSERT' THEN
        audit_row.record_id = NEW.id;
        audit_row.new_data = to_jsonb(NEW);
    END IF;

    INSERT INTO audit_log VALUES (audit_row.*);
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Apply audit trigger to a table
CREATE TRIGGER user_audit
AFTER INSERT OR UPDATE OR DELETE ON users
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_func();
```

---

## 8. Database Maintenance and Operations

### 8.1 Backup and Recovery

* Implement **regular backups** with verified restore procedures
* Use **point-in-time recovery** capabilities
* Define appropriate **backup retention policies**
* Test **recovery procedures** regularly
* Store backups in **geographically distributed locations**

```bash
# Example PostgreSQL backup script
#!/bin/bash

# Configuration
DB_NAME="thinkalike"
BACKUP_DIR="/var/backups/postgres"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_${TIMESTAMP}.sql.gz"
LOG_FILE="${BACKUP_DIR}/backup_log.txt"

# Ensure backup directory exists
mkdir -p ${BACKUP_DIR}

# Execute backup
echo "Starting backup of ${DB_NAME} at $(date)" >> ${LOG_FILE}
pg_dump -U postgres -d ${DB_NAME} -F c -b -v -f ${BACKUP_FILE}.tmp && \
mv ${BACKUP_FILE}.tmp ${BACKUP_FILE}

# Check if backup was successful
if [ $? -eq 0 ]; then
    echo "Backup completed successfully: ${BACKUP_FILE}" >> ${LOG_FILE}

    # Cleanup old backups (keep last 14 days)
    find ${BACKUP_DIR} -name "${DB_NAME}_*.sql.gz" -type f -mtime +14 -delete
else
    echo "Backup failed!" >> ${LOG_FILE}
fi
```

### 8.2 Monitoring and Alerting

* Monitor **database performance metrics**
* Set up alerts for **unusual activity patterns**
* Track **resource usage** (CPU, memory, disk, connections)
* Monitor **long-running queries**
* Check for **deadlocks** and **lock contention**

```yaml
# Example Prometheus alerting rules for PostgreSQL
groups:
- name: PostgresqlAlerts
  rules:
  - alert: PostgresqlHighConnections
    expr: sum by (instance) (pg_stat_activity_count) > 200
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High number of PostgreSQL connections"
      description: "PostgreSQL instance {{ $labels.instance }} has {{ $value }} connections"

  - alert: PostgresqlSlowQueries
    expr: pg_stat_activity_max_tx_duration{datname!~"template.*|postgres"} > 300
    for: 2m
    labels:
      severity: warning
    annotations:
      summary: "PostgreSQL slow queries"
      description: "PostgreSQL instance has a query running for more than 5 minutes in database {{ $labels.datname }}"

  - alert: PostgresqlHighReplicationLag
    expr: pg_replication_lag > 600
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "PostgreSQL high replication lag"
      description: "PostgreSQL replication lag is {{ $value }} seconds on {{ $labels.instance }}"
```

### 8.3 Database Health Checks

* Implement **automatic health checks**
* Check for **database corruption**
* Analyze **index fragmentation**
* Run **regular vacuum** operations
* Monitor **table bloat**

```sql
-- Example health check queries
-- 1. Check for bloated tables
SELECT
    schemaname,
    tablename,
    pg_size_pretty(table_size) AS table_size,
    pg_size_pretty(bloat_size) AS bloat_size,
    round(100*bloat_size/table_size) AS bloat_percentage
FROM (
    SELECT
        schemaname,
        tablename,
        pg_table_size(schemaname || '.' || tablename) AS table_size,
        pg_table_size(schemaname || '.' || tablename) -
            pg_relation_size(schemaname || '.' || tablename) AS bloat_size
    FROM pg_tables
    WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
) AS a
WHERE
    bloat_size > 1048576 -- 1MB
    AND round(100*bloat_size/table_size) > 10 -- 10% bloat
ORDER BY bloat_size DESC;

-- 2. Check for unused indexes
SELECT
    schemaname || '.' || relname AS table,
    indexrelname AS index,
    pg_size_pretty(pg_relation_size(i.indexrelid)) AS index_size,
    idx_scan AS scans
FROM
    pg_stat_user_indexes ui
JOIN
    pg_index i ON ui.indexrelid = i.indexrelid
WHERE
    idx_scan = 0 -- Index has never been used
    AND 0 != (SELECT count(*) FROM pg_constraint WHERE conindid = i.indexrelid)
    AND i.indisunique IS FALSE -- Not a unique constraint
ORDER BY
    pg_relation_size(i.indexrelid) DESC;
```

---

## 9. Transaction Management

### 9.1 ACID Properties

* Ensure **atomicity** for related operations
* Maintain **consistency** in database state
* Implement **isolation** between concurrent transactions
* Guarantee **durability** of committed transactions

### 9.2 Transaction Guidelines

* Keep transactions **short and focused**
* Set appropriate **isolation levels** for different operations
* Avoid **long-running transactions**
* Implement **retry logic** for deadlocks
* Be aware of **transaction costs** in distributed systems

```python
# Example transaction handling with retry logic
import time
from sqlalchemy.exc import OperationalError

def with_transaction_retry(session, max_retries=3, retry_delay=0.1):
    """Execute a function within a transaction with retry logic."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            while True:
                try:
                    result = func(session, *args, **kwargs)
                    session.commit()
                    return result
                except OperationalError as e:
                    session.rollback()
                    retries += 1
                    if retries > max_retries:
                        raise
                    # Exponential backoff
                    sleep_time = retry_delay * (2 ** (retries - 1))
                    time.sleep(sleep_time)
        return wrapper
    return decorator

# Usage example
@with_transaction_retry(db.session, max_retries=3)
def transfer_funds(session, from_account_id, to_account_id, amount):
    # Get accounts with row-level locking
    from_account = session.query(Account).with_for_update().get(from_account_id)
    to_account = session.query(Account).with_for_update().get(to_account_id)

    if from_account.balance < amount:
        raise InsufficientFundsError("Insufficient funds")

    # Update balances
    from_account.balance -= amount
    to_account.balance += amount

    # Record transaction
    transaction = Transaction(
        from_account_id=from_account_id,
        to_account_id=to_account_id,
        amount=amount,
        status='completed'
    )
    session.add(transaction)

    return transaction
```

---

## 10. Scaling Strategies

### 10.1 Vertical Scaling

* Increase **hardware resources** for database servers
* Optimize for **higher concurrency**
* Consider **hardware limitations** and cost implications
* Monitor **resource utilization** to inform scaling decisions

### 10.2 Horizontal Scaling

* Implement **read replicas** for read-heavy workloads
* Consider **database sharding** for write-heavy workloads
* Design for **distributed transactions** if needed
* Plan for **cross-shard queries** and reporting

```yaml
# Example database cluster configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: postgres-cluster-config
data:
  postgresql.conf: |
    max_connections = 500
    shared_buffers = 4GB
    effective_cache_size = 12GB
    work_mem = 16MB
    maintenance_work_mem = 1GB
    max_worker_processes = 8
    max_parallel_workers_per_gather = 4
    max_parallel_workers = 8
    wal_level = replica
    max_wal_senders = 10
    max_replication_slots = 10
    hot_standby = on
    hot_standby_feedback = on

---

apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres-primary
spec:
  serviceName: postgres-primary
  replicas: 1
  template:
    spec:
      containers:
      - name: postgres
        image: postgres:14
        env:
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: postgres-secrets
              key: username
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secrets
              key: password
        - name: POSTGRES_DB
          value: thinkalike
        - name: PGDATA
          value: /var/lib/postgresql/data/pgdata
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: postgres-primary-data
          mountPath: /var/lib/postgresql/data
        - name: postgres-config
          mountPath: /etc/postgresql/postgresql.conf
          subPath: postgresql.conf
  volumeClaimTemplates:
  - metadata:
      name: postgres-primary-data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 100Gi

---

apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres-replica
spec:
  serviceName: postgres-replica
  replicas: 3
  template:
    spec:
      containers:
      - name: postgres
        image: postgres:14
        env:
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: postgres-secrets
              key: username
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secrets
              key: password
        - name: POSTGRES_DB
          value: thinkalike
        - name: PGDATA
          value: /var/lib/postgresql/data/pgdata
        - name: PRIMARY_HOST
          value: postgres-primary
        command:
        - bash
        - -c
        - |
          until pg_isready -h $PRIMARY_HOST -p 5432; do
            echo "Waiting for primary to be ready"
            sleep 2
          done
          # Configure as a replica
          pg_basebackup -h $PRIMARY_HOST -D $PGDATA -U $POSTGRES_USER -P -v -R
          exec postgres
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: postgres-replica-data
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: postgres-replica-data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 100Gi
```

### 10.3 Database Federation

* Split databases by **functional domain**
* Define clear **domain boundaries**
* Implement **cross-database communication** patterns
* Consider eventual consistency challenges

---

## 11. Multi-Tenancy

### 11.1 Tenancy Models

* **Separate databases**: One database per tenant
* **Separate schemas**: One schema per tenant within shared database
* **Shared schema**: Shared tables with tenant identifier

| Approach | Isolation | Resource Usage | Management Complexity | Data Size |
|----------|-----------|---------------|---------------------|-----------|
| Separate databases | High | High | High | Any size |
| Separate schemas | Medium | Medium | Medium | Medium |
| Shared schema | Low | Low | Low | Small-Medium |

### 11.2 Implementation Guidelines

* Use **tenant identifiers** consistently
* Implement **row-level security** for shared schema approach
* Consider **data isolation requirements**
* Plan for **tenant-specific customizations**
* Design for **tenant provisioning/deprovisioning**

```sql
-- Example row-level security implementation for multi-tenancy
CREATE TABLE tenant_users (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES tenants(id),
    username VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Enable row-level security
ALTER TABLE tenant_users ENABLE ROW LEVEL SECURITY;

-- Create a policy that limits access to the current tenant
CREATE POLICY tenant_isolation ON tenant_users
    USING (tenant_id = current_setting('app.current_tenant_id')::INTEGER);

-- Function to set the current tenant context
CREATE OR REPLACE FUNCTION set_tenant_context(p_tenant_id INTEGER)
RETURNS VOID AS $$
BEGIN
    PERFORM set_config('app.current_tenant_id', p_tenant_id::TEXT, FALSE);
END;
$$ LANGUAGE plpgsql;

-- Usage example
SELECT set_tenant_context(1);
SELECT * FROM tenant_users; -- Will only see tenant_id = 1 records
```

---

## 12. Database Documentation

### 12.1 Schema Documentation

* Document **table purposes** and relationships
* Describe **column meanings** and constraints
* Document **indexing strategy**
* Maintain **entity-relationship diagrams**
* Keep documentation **in sync with schema changes**

### 12.2 Documentation Tools

* Use automated tools to generate schema documentation
* Include database documentation in the overall project documentation
* Maintain living documentation that evolves with the schema
* Document query patterns and access methods

```bash
# Example schema documentation generation using SchemaSpy
java -jar schemaspy.jar \
  -t pgsql \
  -db thinkalike \
  -host localhost \
  -port 5432 \
  -u documentationuser \
  -p documentationpassword \
  -o ./database-docs \
  -dp postgresql-42.2.23.jar
```

---

**Document Details**
- Title: Database Design Guidelines
- Type: Development Guide
- Version: 1.0.0
- Last Updated: 2025-04-05

---

End of Database Design Guidelines

---



