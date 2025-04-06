# DevOps and CI/CD Guidelines

---

## 1. Introduction

This document outlines ThinkAlike's DevOps and CI/CD (Continuous Integration/Continuous Deployment) practices. These guidelines ensure reliable, secure, and efficient deployment of our applications while maintaining high quality standards through automated processes.

---

## 2. CI/CD Pipeline Structure

### 2.1 Pipeline Stages

```yaml
# Example Azure DevOps pipeline configuration
trigger:
  branches:
    include:
      - main
      - develop
      - feature/*
      - release/*

stages:
  - stage: Build
    jobs:
      - job: BuildAndTest
        steps:
          - task: NodeTool@0
            inputs:
              versionSpec: '16.x'
          - script: |
              npm ci
              npm run lint
              npm run test
              npm run build

  - stage: SecurityScan
    jobs:
      - job: SecurityAudit
        steps:
          - task: dependency-check@1
            inputs:
              scanPath: '$(Build.SourcesDirectory)'
          - task: SonarQubePrepare@4
          - task: SonarQubeAnalyze@4

  - stage: Deploy_Staging
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/develop'))
    jobs:
      - deployment: Deploy
        environment: staging
        strategy:
          rolling:
            maxParallel: 2

  - stage: Deploy_Production
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    jobs:
      - deployment: Deploy
        environment: production
        strategy:
          rolling:
            maxParallel: 1
```

### 2.2 Environment Configuration

```yaml
# Example environment configuration
environments:
  development:
    url: https://dev.thinkalike.com
    resources:
      memory: 2Gi
      cpu: 1
    replicas: 1

  staging:
    url: https://staging.thinkalike.com
    resources:
      memory: 4Gi
      cpu: 2
    replicas: 2

  production:
    url: https://thinkalike.com
    resources:
      memory: 8Gi
      cpu: 4
    replicas: 3
```

---

## 3. Version Control Practices

### 3.1 Branching Strategy

Follow GitFlow with these branches:

* `main` - Production code
* `develop` - Integration branch
* `feature/*` - New features
* `bugfix/*` - Bug fixes
* `release/*` - Release preparation
* `hotfix/*` - Production fixes

```bash
# Creating a new feature branch
git checkout develop
git pull
git checkout -b feature/user-authentication

# Merging feature branch
git checkout develop
git merge --no-ff feature/user-authentication
git push origin develop

# Creating a release
git checkout -b release/1.2.0
# Make release-specific changes
git checkout main
git merge --no-ff release/1.2.0
git tag -a v1.2.0 -m "Version 1.2.0"
```

### 3.2 Commit Message Standards

Follow conventional commits:

```bash
# Format: <type>(<scope>): <description>
feat(auth): implement JWT authentication
fix(api): resolve user lookup timeout
docs(readme): update deployment instructions
chore(deps): update dependencies
test(auth): add unit tests for login flow
```

---

## 4. Build Process

### 4.1 Build Scripts

```javascript
// package.json build scripts
{
  "scripts": {
    "build": "npm-run-all clean build:* generate-docs",
    "build:ts": "tsc -p tsconfig.prod.json",
    "build:assets": "node scripts/build-assets.js",
    "build:styles": "sass src/styles:dist/styles",
    "clean": "rimraf dist",
    "generate-docs": "typedoc src/"
  }
}
```

### 4.2 Docker Configuration

```dockerfile
# Dockerfile
FROM node:16-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:16-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package*.json ./

ENV NODE_ENV=production
EXPOSE 3000
CMD ["npm", "start"]
```

---

## 5. Testing Strategy

### 5.1 Test Types

```yaml
# Test execution in pipeline
steps:
  - task: Npm@1
    inputs:
      command: 'custom'
      customCommand: 'run test:all'
    env:
      NODE_ENV: test

  - task: PublishTestResults@2
    inputs:
      testResultsFormat: 'JUnit'
      testResultsFiles: '**/junit.xml'
```

### 5.2 Test Configuration

```javascript
// jest.config.js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  collectCoverage: true,
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  },
  reporters: [
    'default',
    ['jest-junit', {
      outputDirectory: 'test-results',
      outputName: 'junit.xml',
    }]
  ]
};
```

---

## 6. Deployment Process

### 6.1 Kubernetes Deployment

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: thinkalike-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: thinkalike-api
  template:
    metadata:
      labels:
        app: thinkalike-api
    spec:
      containers:
        - name: api
          image: thinkalike/api:latest
          ports:
            - containerPort: 3000
          resources:
            requests:
              memory: "256Mi"
              cpu: "200m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          env:
            - name: NODE_ENV
              value: production
          readinessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 10
```

### 6.2 Database Migrations

```typescript
// migrations/20230401000000_create_users.ts
import { Knex } from 'knex';

export async function up(knex: Knex): Promise<void> {
  return knex.schema.createTable('users', table => {
    table.uuid('id').primary();
    table.string('email').unique().notNullable();
    table.string('password_hash').notNullable();
    table.timestamps(true, true);
  });
}

export async function down(knex: Knex): Promise<void> {
  return knex.schema.dropTable('users');
}
```

---

## 7. Monitoring and Logging

### 7.1 Logging Configuration

```typescript
// src/config/logger.ts
import winston from 'winston';

export const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  defaultMeta: { service: 'thinkalike-api' },
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});
```

### 7.2 Metrics Collection

```typescript
// src/middleware/metrics.ts
import prometheus from 'prom-client';

const httpRequestDurationMicroseconds = new prometheus.Histogram({
  name: 'http_request_duration_ms',
  help: 'Duration of HTTP requests in ms',
  labelNames: ['method', 'route', 'code'],
  buckets: [0.1, 5, 15, 50, 100, 500]
});

export const metricsMiddleware = (req, res, next) => {
  const start = process.hrtime();

  res.on('finish', () => {
    const duration = process.hrtime(start);
    const durationMs = duration[0] * 1000 + duration[1] / 1000000;

    httpRequestDurationMicroseconds
      .labels(req.method, req.route.path, res.statusCode.toString())
      .observe(durationMs);
  });

  next();
};
```

---

## 8. Security Practices

### 8.1 Secret Management

```yaml
# Azure Key Vault configuration
apiVersion: secrets-store.csi.x-k8s.io/v1
kind: SecretProviderClass
metadata:
  name: azure-kvname
spec:
  provider: azure
  parameters:
    usePodIdentity: "true"
    keyvaultName: "thinkalike-kv"
    objects: |
      array:
        - |
          objectName: DatabasePassword
          objectType: secret
        - |
          objectName: JWTSecret
          objectType: secret
    tenantId: "your-tenant-id"
```

### 8.2 Security Scanning

```yaml
# Security scan configuration
steps:
  - task: dependency-check@1
    inputs:
      scanPath: '$(Build.SourcesDirectory)'
      format: 'HTML'

  - task: WhiteSource@21
    inputs:
      cwd: '$(Build.SourcesDirectory)'

  - task: ContainerScan@0
    inputs:
      imageName: 'thinkalike/api:$(Build.BuildId)'
```

---

## 9. Disaster Recovery

### 9.1 Backup Procedures

```bash
# Database backup script
#!/bin/bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"

# Backup database
pg_dump -Fc thinkalike > "$BACKUP_DIR/db_$TIMESTAMP.dump"

# Upload to cloud storage
az storage blob upload \
  --container-name backups \
  --file "$BACKUP_DIR/db_$TIMESTAMP.dump" \
  --name "db_$TIMESTAMP.dump"

# Clean old backups
find "$BACKUP_DIR" -type f -mtime +7 -delete
```

### 9.2 Recovery Procedures

```bash
# Database restore script
#!/bin/bash
BACKUP_FILE=$1

# Download from cloud storage
az storage blob download \
  --container-name backups \
  --name "$BACKUP_FILE" \
  --file "./restore.dump"

# Restore database
pg_restore -d thinkalike_new "./restore.dump"

# Verify restoration
psql -d thinkalike_new -c "SELECT COUNT(*) FROM users;"
```

---

## 10. Documentation

### 10.1 API Documentation

```yaml
# Swagger configuration
openapi: 3.0.0
info:
  title: ThinkAlike API
  version: 1.0.0
  description: API documentation for ThinkAlike platform
servers:
  - url: https://api.thinkalike.com/v1
paths:
  /users:
    get:
      summary: Get users
      responses:
        '200':
          description: List of users
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
```

### 10.2 System Documentation

```markdown
# System Architecture

## Components
- Frontend: React SPA
- Backend: Node.js API
- Database: PostgreSQL
- Cache: Redis
- Message Queue: RabbitMQ

## Infrastructure
- Cloud: Azure
- Container Orchestration: AKS
- CDN: Azure CDN
- Load Balancer: Azure Load Balancer
```

---

## 11. Performance Optimization

### 11.1 Load Testing

```javascript
// k6 load test script
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '5m', target: 100 },   // Ramp up
    { duration: '10m', target: 100 },  // Stay at peak
    { duration: '5m', target: 0 },     // Ramp down
  ],
};

export default function() {
  const res = http.get('https://api.thinkalike.com/health');
  check(res, { 'status is 200': (r) => r.status === 200 });
  sleep(1);
}
```

### 11.2 Performance Monitoring

```javascript
// src/middleware/performance.ts
import { performance } from 'perf_hooks';

export const performanceMiddleware = (req, res, next) => {
  const start = performance.now();

  res.on('finish', () => {
    const duration = performance.now() - start;
    logger.info('Request completed', {
      method: req.method,
      path: req.path,
      duration,
      statusCode: res.statusCode
    });

    if (duration > 1000) {
      logger.warn('Slow request detected', {
        method: req.method,
        path: req.path,
        duration
      });
    }
  });

  next();
};
```

---

By following these DevOps and CI/CD guidelines, ThinkAlike ensures reliable, secure, and efficient deployment of our applications while maintaining high quality standards through automated processes.
