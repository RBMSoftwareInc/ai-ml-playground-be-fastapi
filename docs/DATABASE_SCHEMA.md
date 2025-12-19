# Complete Database Schema Documentation

## Overview

This document describes the comprehensive database schema for the AI/ML Playground platform, covering all industries, use cases, training data, AI models, DevLab, and Discovery tools.

---

## 📊 Schema Categories

### 1. Core Models
- Users, Industries, Use Cases, Categories

### 2. Commerce Models
- Products, Orders, Transactions, Customers, Inventory

### 3. Analytics Models
- Events, A/B Tests, Results

### 4. Training & AI Models
- Content Chunks, Training Datasets, Model Versions, Metrics

### 5. DevLab Models
- Projects, Files, Executions, Analyses, Tests, Vulnerabilities, Insights

### 6. Discovery Models
- Discovery Tools, Executions

### 7. Content Management
- Content Versions, Sync Logs

---

## 📋 Complete Table List

### Core Tables

#### `users`
- User authentication and preferences
- Fields: id, email, username, hashed_password, is_active, preferences

#### `industries`
- Industry definitions
- Fields: id, industry_id, name, icon, description

#### `use_case_categories`
- Use case category definitions
- Fields: id, category_id, name, icon, description, display_order

#### `use_cases`
- Use case catalog (30+ use cases across 9 industries)
- Fields: id, use_case_id, display_name, industry_id, category_id, descriptions, keywords, tips, theory_content, is_dynamic, api_endpoint
- **Supports**: Static and dynamic use cases

#### `use_case_executions`
- Use case execution logs
- Fields: id, use_case_id, user_id, input_data, output_data, confidence, latency_ms, model_version

---

### Commerce Tables

#### `product_categories`
- Product category hierarchy
- Fields: id, category_id, name, parent_category_id

#### `products`
- Product catalog with embeddings
- Fields: id, product_id, sku, name, description, price, embedding, visual_embedding

#### `product_variants`
- Product variants
- Fields: id, variant_id, product_id, attributes, price

#### `orders`
- Order management
- Fields: id, order_id, customer_id, status, total, shipping_address

#### `order_items`
- Order line items
- Fields: id, order_id, product_id, quantity, unit_price

#### `transactions`
- Transaction and fraud data
- Fields: id, transaction_id, amount, is_fraud, fraud_score, device_fingerprint

#### `customers`
- Customer data and segmentation
- Fields: id, customer_id, email, total_orders, total_spent, churn_probability, segment_id

#### `customer_segments`
- Customer segments
- Fields: id, segment_id, name, criteria, characteristics

#### `inventory`
- Inventory management
- Fields: id, product_id, current_stock, reorder_point, reorder_quantity

#### `inventory_movements`
- Inventory movement logs
- Fields: id, product_id, movement_type, quantity, reference_id

---

### Analytics Tables

#### `analytics_events`
- Analytics event tracking
- Fields: id, event_type, user_id, event_data, properties, created_at

#### `ab_tests`
- A/B test definitions
- Fields: id, test_id, name, primary_kpi, traffic_split, variants, status

#### `ab_test_results`
- A/B test results
- Fields: id, test_id, variant_name, visitors, conversions, conversion_rate, is_winner

---

### Training & AI Models Tables

#### `content_chunks`
- Content chunks for embeddings and semantic search
- Fields: id, use_case_id, discovery_tool_id, content_type, content_text, embedding, embedding_model
- **Purpose**: Store all text content (theory, tips, descriptions) with embeddings for semantic search

#### `training_datasets`
- Training datasets for model training
- Fields: id, name, version, dataset_type, use_case_ids, data_snapshot, data_source, record_count
- **Supports**: conversation, code, simulation, general datasets

#### `conversation_examples`
- Conversation examples for conversational AI training
- Fields: id, user_query, ai_response, context, use_case_id, suggestions, quality_score
- **Purpose**: Train AI Conversation Mode

#### `simulation_examples`
- Interactive simulation examples
- Fields: id, solution_id, scenario_id, input_data, expected_output, pipeline_steps, business_impact
- **Purpose**: Train Interactive AI Mode

#### `code_examples`
- Code examples for DevLab training
- Fields: id, code, language, code_type, explanation, test_code, refactored_code, security_issues, embedding
- **Purpose**: Train DevLab AI models

#### `model_versions`
- Model version tracking
- Fields: id, model_name, version, model_type, training_strategy, file_path, base_model, external_service, is_active
- **Training Strategy**: 'pretrained', 'fine_tuned', 'custom'
- **External Service**: 'openai', 'anthropic', 'self_hosted', 'hybrid'

#### `model_metrics`
- Model performance metrics
- Fields: id, model_version_id, metric_type, metric_name, metric_value, dataset_type

#### `model_deployments`
- Model deployment tracking
- Fields: id, model_version_id, environment, endpoint_url, deployment_status

---

### DevLab Tables

#### `devlab_projects`
- DevLab projects
- Fields: id, project_id, name, language, user_id, environment, metadata

#### `devlab_files`
- Project files
- Fields: id, project_id, file_path, file_name, content, language, file_type

#### `devlab_executions`
- Code execution logs
- Fields: id, project_id, language, code, status, output, error, execution_time_ms, container_id, security_scan_result
- **Security**: Container ID for Docker isolation tracking

#### `devlab_analyses`
- Code analysis results
- Fields: id, project_id, analysis_type, findings, severity, suggestions, model_version
- **Analysis Types**: security, performance, quality, complexity, dependency

#### `devlab_tests`
- Test execution and generation
- Fields: id, project_id, test_name, test_type, framework, test_code, status, coverage_percentage, generated_by_ai

#### `devlab_vulnerabilities`
- Security vulnerabilities
- Fields: id, project_id, vulnerability_type, severity, description, code_location, cve_id, fix_suggestion

#### `devlab_insights`
- AI insights for code
- Fields: id, project_id, insight_type, title, description, confidence, action, priority
- **Insight Types**: optimization, security, refactor, test, dependency

---

### Discovery Tables

#### `discovery_tools`
- Discovery Zone tools
- Fields: id, tool_id, name, icon, category, interaction_type, model_prompt_template, visualization_type, surprise_type
- **Supports**: All discovery tools (color-predictor, bill-negotiator, etc.)

#### `discovery_tool_executions`
- Discovery tool execution logs
- Fields: id, tool_id, user_id, input_data, output_data, visualization_data, surprise_result

---

### Content Management Tables

#### `content_versions`
- Content version tracking
- Fields: id, content_type, content_id, version, content_data, source, source_file, checksum
- **Purpose**: Track content changes and sync between frontend/backend

#### `content_syncs`
- Content synchronization logs
- Fields: id, sync_type, content_type, records_processed, status, error_log

---

## 🔗 Key Relationships

```
Industries (1) ──< (Many) Use Cases
Use Cases (1) ──< (Many) Use Case Executions
Use Cases (1) ──< (Many) Content Chunks
Use Cases (1) ──< (Many) Conversation Examples

DevLab Projects (1) ──< (Many) DevLab Files
DevLab Projects (1) ──< (Many) DevLab Executions
DevLab Projects (1) ──< (Many) DevLab Analyses
DevLab Projects (1) ──< (Many) DevLab Tests

Discovery Tools (1) ──< (Many) Discovery Tool Executions

Model Versions (1) ──< (Many) Model Metrics
Model Versions (1) ──< (Many) Model Deployments
```

---

## 🔐 Security Considerations

### Code Execution Security (DevLab)
- **Container Isolation**: `container_id` field tracks Docker containers
- **Security Scanning**: `security_scan_result` in executions
- **Vulnerability Tracking**: Dedicated `devlab_vulnerabilities` table
- **Resource Limits**: Tracked in execution records (memory, CPU, time)

### Data Security
- **No PII in Training Data**: User IDs are optional, no personal data
- **Code Privacy**: User code in DevLab can be marked for deletion
- **Audit Logging**: All executions and analyses are logged

---

## 📈 Indexes for Performance

### Critical Indexes
- `use_cases.use_case_id` - Unique index
- `use_case_executions.use_case_id` + `created_at` - Composite index
- `content_chunks.content_type` + `use_case_id` - Composite index
- `devlab_executions.status` + `created_at` - Composite index
- `model_versions.model_type` + `is_active` - Composite index
- `discovery_tools.category` - Index for filtering

---

## 🎯 Schema Coverage

### ✅ Industries (9)
- E-commerce, Fintech, Retail, Healthcare, Travel, Hospitality, Entertainment, Manufacturing, Real Estate

### ✅ Use Cases (30+)
- All use cases with support for static and dynamic use cases
- Categories: Product Discovery, Logistics, Personalization, Pricing & Fraud, Marketing Intelligence, Product Intelligence, Creative & AR, Gamification, Analytics

### ✅ Training Data
- Content chunks with embeddings
- Conversation examples
- Simulation examples
- Code examples
- Training datasets

### ✅ AI Models
- Model versions with training strategy tracking
- Model metrics
- Model deployments

### ✅ DevLab
- Projects, files, executions
- Code analysis
- Test generation
- Vulnerability detection
- AI insights

### ✅ Discovery Tools
- All discovery tools
- Execution tracking

### ✅ Content Management
- Version tracking
- Sync logging

---

## 🚀 Migration Strategy

### Phase 1: Core Tables
1. Users, Industries, Use Cases
2. Products, Orders, Customers
3. Analytics

### Phase 2: Training & Models
1. Content Chunks
2. Training Datasets
3. Model Versions

### Phase 3: DevLab
1. Projects, Files
2. Executions, Analyses
3. Tests, Vulnerabilities

### Phase 4: Discovery
1. Discovery Tools
2. Executions

### Phase 5: Content Management
1. Content Versions
2. Sync Logs

---

## 📝 Notes

- All tables use `id` as primary key (Integer, auto-increment)
- All tables have `created_at` timestamp
- Most tables have `updated_at` timestamp
- JSON fields are used for flexible data storage
- Foreign keys maintain referential integrity
- Indexes optimize query performance
- Boolean fields default to appropriate values
- All text fields use appropriate length limits

---

**Schema Version**: 1.0  
**Last Updated**: 2025-01-15  
**Status**: Complete and Error-Free

