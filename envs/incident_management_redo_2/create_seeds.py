#!/usr/bin/env python3
"""
CREATE SEEDS - Incident Management Data Generator

This script contains ALL business rules for generating seed data.
It generates realistic test data following the Standard Operating Procedures (SOP).

USAGE:
    cd envs/incident_management_redo/
    python3 create_seeds.py

OUTPUT:
    - Deletes all existing JSON files in ./data/
    - Generates fresh data with all business rules
    - Creates ~25 JSON files with complete dataset

CONTAINS:
    ✓ All business rules from SOP
    ✓ User role distributions and authorizations
    ✓ SLA configurations per tier
    ✓ Incident workflows and escalations
    ✓ Change management and approvals
    ✓ Attachments, metrics, reports, audits
    
NOTE:
    - This script is self-contained (no dependencies on other seed scripts)
    - For database loading, use scripts in ../../scripts/seeds_utils/infra/
    - Data is generated with fixed seed (42) for reproducibility
"""

import json
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()
Faker.seed(42)

# Fixed reference date for reproducibility (2025-10-07 12:00:00 UTC)
# This ensures all generated data is relative to this fixed point in time
REFERENCE_DATE = datetime(2025, 10, 7, 12, 0, 0)
MAX_DATE = REFERENCE_DATE  # Maximum date for any timestamp
random.seed(42)

# ============================================================================
# CONFIGURATION & CONSTANTS
# ============================================================================

EMAIL_DOMAINS = ['gmail.com', 'outlook.com', 'yahoo.com', 'company.com', 'techcorp.com']

# SLA Configuration per Tier and Severity (from SOP 1.3)
# Each entry has min-max ranges for response and resolution times
SLA_MATRIX = {
    'premium': {
        'P1': {'response': (15, 30), 'resolution': (120, 240)},      # 15-30min, 2-4h
        'P2': {'response': (60, 120), 'resolution': (480, 1440)},    # 1-2h, 8-24h
        'P3': {'response': (240, 480), 'resolution': (2880, 4320)},  # 4-8h, 48-72h
        'P4': {'response': (1440, 2880), 'resolution': (7680, 7680)} # 24-48h, 128h
    },
    'standard': {
        'P1': {'response': (60, 120), 'resolution': (480, 1440)},    # 1-2h, 8-24h
        'P2': {'response': (240, 480), 'resolution': (1440, 2880)},  # 4-8h, 24-48h
        'P3': {'response': (1440, 1440), 'resolution': (4320, 7200)}, # 24h, 72-120h
        'P4': {'response': (2880, 4320), 'resolution': (10080, 10080)} # 48-72h, 168h
    },
    'basic': {
        'P1': {'response': (240, 480), 'resolution': (1440, 2880)},   # 4-8h, 24-48h
        'P2': {'response': (1440, 1440), 'resolution': (4320, 7200)}, # 24h, 72-120h
        'P3': {'response': (2880, 4320), 'resolution': (7200, 14400)}, # 48-72h, 5-10 days
        'P4': {'response': (7200, 10080), 'resolution': (20160, 20160)} # 5-7 days, 2 weeks
    }
}

# Availability Guarantee per Tier
AVAILABILITY_GUARANTEE = {
    'premium': 99.9,
    'standard': 99.5,
    'basic': 99.0
}

# Role distributions (780 total users: 700 active + 80 inactive)
# This ensures 700 active users available for operations
USER_ROLE_DISTRIBUTION = {
    'incident_manager': 80,      # ~10% (approvers for many requests)
    'technical_support': 234,    # ~30% (largest group, creates many requests)
    'account_manager': 80,       # ~10%
    'executive': 55,             # ~7% (senior approvers)
    'vendor_contact': 78,        # ~10%
    'system_administrator': 100, # ~13% (technical work, approvals)
    'client_contact': 153        # ~20% (client-side users)
}

# Authorized roles for specific actions (from SOP and validation rules)
AUTHORIZED_ROLES = {
    'incident_assignment': ['technical_support', 'system_administrator'],  # SOP 4.1: Only technical_support and system_administrator
    'change_approval': ['incident_manager', 'executive'],
    'sla_creation': ['incident_manager'],
    'escalation_target': ['incident_manager', 'executive'],
    'bridge_host': ['incident_manager'],  # SOP 4.5: Only incident_manager can host bridges
    'work_order_assignment': ['technical_support', 'system_administrator']
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def generate_email(first_name, last_name, used_emails):
    """Generate unique realistic email addresses"""
    domain = random.choice(EMAIL_DOMAINS)
    counter = 1
    while True:
        if counter == 1:
            email = f"{first_name.lower()}.{last_name.lower()}@{domain}"
        else:
            email = f"{first_name.lower()}.{last_name.lower()}{counter}@{domain}"
        
        if email not in used_emails:
            used_emails.add(email)
            return email
        counter += 1

def generate_phone():
    """Generate realistic phone numbers"""
    area_codes = ['201', '212', '310', '415', '617', '720', '202', '312', '404', '713']
    return f"+1{random.choice(area_codes)}{random.randint(1000000, 9999999)}"

def format_timestamp(dt):
    """Format datetime to YYYY-MM-DDTHH:MM:SS (without microseconds)"""
    return dt.strftime('%Y-%m-%dT%H:%M:%S')

def generate_timestamp(start_date=None, end_date=None):
    """Generate random timestamp within range (never exceeds REFERENCE_DATE)"""
    # Use fixed REFERENCE_DATE for reproducibility
    
    if start_date is None:
        start_date = REFERENCE_DATE - timedelta(days=365)  # 1 year before reference date
    if end_date is None:
        end_date = MAX_DATE
    
    # Ensure we never generate dates in the future
    if end_date > MAX_DATE:
        end_date = MAX_DATE
    
    time_between = end_date - start_date
    total_seconds = int(time_between.total_seconds())
    
    if total_seconds <= 0:
        return start_date
    
    # Generate random offset in seconds
    random_seconds_offset = random.randrange(total_seconds)
    result = start_date + timedelta(seconds=random_seconds_offset)
    
    # Double-check: ensure result never exceeds reference date
    if result > REFERENCE_DATE:
        result = REFERENCE_DATE
    
    return result

def generate_timestamps(max_age_days=90):
    """
    Generate created_at and updated_at with proper ordering (never in the future)
    
    Args:
        max_age_days: Maximum age in days from today (default: 90 days = 3 months)
    """
    start = MAX_DATE - timedelta(days=max_age_days)
    # Ensure created is before MAX_DATE
    end_for_created = MAX_DATE - timedelta(hours=1)  # Leave room for updated
    created = generate_timestamp(start, end_for_created)
    # Ensure updated is between created and MAX_DATE, but never exceeds MAX_DATE
    updated = generate_timestamp(created, MAX_DATE)
    return format_timestamp(created), format_timestamp(updated)

def get_users_by_role(users, role):
    """Get list of user IDs with specific role"""
    return [uid for uid, u in users.items() if u['role'] == role]

def get_authorized_user(users, action_type):
    """Get a random authorized user for specific action"""
    authorized_roles = AUTHORIZED_ROLES.get(action_type, [])
    candidates = [uid for uid, u in users.items() if u['role'] in authorized_roles]
    return random.choice(candidates) if candidates else None

# ============================================================================
# DATA GENERATION FUNCTIONS
# ============================================================================

def generate_vendors(n=8):
    """Generate vendor companies"""
    vendors = {}
    
    for i in range(1, n + 1):
        # Vendors can be older (1-3 years old companies)
        created, _ = generate_timestamps(max_age_days=random.randint(365, 1095))
        vendors[str(i)] = {
            "vendor_id": str(i),
            "vendor_name": fake.company(),
            "contact_email": f"support@vendor{i}.com",
            "contact_phone": generate_phone(),
            "status": random.choice(['active', 'active', 'inactive']),
            "created_at": created
        }
    return vendors

def generate_clients(n=25):
    """Generate 25 client companies"""
    clients = {}
    company_types = ['enterprise', 'mid_market', 'smb', 'startup']
    support_coverage = ['24x7', 'business_hours', 'on_call']
    communication = ['email', 'portal', 'phone', 'slack']
    
    for i in range(1, n + 1):
        # Clients can be older (6-18 months)
        created, updated = generate_timestamps(max_age_days=random.randint(180, 540))
        clients[str(i)] = {
            "client_id": str(i),
            "client_name": fake.company(),
            "registration_number": f"REG{random.randint(100000, 999999)}",
            "company_type": random.choice(company_types),
            "address": fake.address().replace('\n', ', '),
            "contact_phone": generate_phone(),
            "contact_email": f"contact@client{i}.com",
            "support_coverage": random.choice(support_coverage),
            "preferred_communication": random.choice(communication),
            "status": random.choice(['active', 'active', 'active', 'inactive']),
            "created_at": created,
            "updated_at": updated
        }
    return clients

def generate_users(client_count, vendor_count):
    """Generate users with role-based distribution"""
    users = {}
    user_id = 1
    used_emails = set()
    
    for role, count in USER_ROLE_DISTRIBUTION.items():
        for _ in range(count):
            first_name = fake.first_name()
            last_name = fake.last_name()
            # Users can be moderately old (3-12 months)
            created, updated = generate_timestamps(max_age_days=random.randint(90, 365))
            
            user_data = {
                "user_id": str(user_id),
                "first_name": first_name,
                "last_name": last_name,
                "email": generate_email(first_name, last_name, used_emails),
                "role": role,
                "timezone": random.choice(['America/New_York', 'America/Los_Angeles', 'America/Chicago', 
                                          'Europe/London', 'Asia/Tokyo']),
                "status": random.choice(['active'] * 9 + ['inactive']),  # 90% active (700 out of 780), 10% inactive (80)
                "client_id": None,
                "vendor_id": None,
                "created_at": created,
                "updated_at": updated
            }
            
            # Assign client_id for client_contact role
            if role == 'client_contact':
                user_data["client_id"] = str(random.randint(1, client_count))
            
            # Assign vendor_id for vendor_contact role
            if role == 'vendor_contact':
                user_data["vendor_id"] = str(random.randint(1, vendor_count))
            
            users[str(user_id)] = user_data
            user_id += 1
    
    return users

def generate_products(n=15):
    """Generate products with realistic descriptions"""
    products = {}
    product_data = [
        ("CloudCore Platform", "Enterprise cloud infrastructure platform providing scalable computing resources, storage, and networking services. Supports multi-region deployments with built-in high availability."),
        ("DataSync Pro", "Real-time data synchronization and integration platform for seamless data flow across multiple systems. Features automated conflict resolution and data validation."),
        ("SecureAuth Gateway", "Multi-factor authentication and identity management solution. Provides SSO capabilities, adaptive authentication, and comprehensive audit logging for compliance."),
        ("Analytics Engine", "Advanced analytics and business intelligence platform with real-time data processing. Includes predictive analytics, custom dashboards, and automated reporting capabilities."),
        ("API Manager", "Comprehensive API gateway and management platform for designing, publishing, and monitoring APIs. Features rate limiting, caching, and detailed analytics."),
        ("Monitoring Suite", "Infrastructure and application monitoring platform with intelligent alerting. Provides real-time metrics, distributed tracing, and automated incident detection."),
        ("Payment Gateway", "PCI-DSS compliant payment processing platform supporting multiple payment methods. Includes fraud detection, tokenization, and international currency support."),
        ("Content Delivery Network", "Global CDN service for fast content delivery with edge caching. Features DDoS protection, SSL/TLS management, and real-time analytics."),
        ("Database Cluster", "Managed relational database service with automated backups and failover. Supports read replicas, point-in-time recovery, and performance optimization."),
        ("Message Queue Service", "Distributed message queue for reliable asynchronous communication. Provides message ordering, dead-letter queues, and delivery guarantees."),
        ("Storage Service", "Object storage platform with unlimited scalability and 99.99% durability. Features versioning, lifecycle policies, and encryption at rest."),
        ("Container Orchestration", "Kubernetes-based container orchestration platform for deploying and managing containerized applications. Includes auto-scaling, rolling updates, and service mesh integration."),
        ("Email Service", "Transactional and marketing email platform with high deliverability. Features template management, bounce handling, and detailed delivery analytics."),
        ("Search Engine", "Full-text search and analytics engine for fast data retrieval. Provides relevance tuning, faceted search, and real-time indexing capabilities."),
        ("Workflow Automation", "Business process automation platform for designing and executing complex workflows. Features visual workflow designer, approval routing, and integration with external systems.")
    ]
    
    for i in range(1, n + 1):
        # Products can be older (6 months to 2 years)
        created, _ = generate_timestamps(max_age_days=random.randint(180, 730))
        name, description = product_data[i-1]
        products[str(i)] = {
            "product_id": str(i),
            "product_name": name,
            "product_code": f"PRD-{1000 + i}",
            "description": description,
            "status": random.choice(['active', 'active', 'active', 'deprecated']),
            "created_at": created
        }
    return products

def generate_configuration_items(products, target_total=50):
    """Generate 50 configuration items distributed across products"""
    configuration_items = {}
    ci_id = 1
    ci_types = ['server', 'application', 'database', 'network', 'storage', 'service']
    environments = ['production', 'staging', 'development', 'testing']
    
    # Calculate CIs per product to reach target (with some variation)
    num_products = len(products)
    base_cis_per_product = target_total // num_products
    remaining = target_total % num_products
    
    for idx, product_id in enumerate(products.keys()):
        # Distribute remaining CIs across first few products
        num_cis = base_cis_per_product + (1 if idx < remaining else 0)
        ci_counter = 1  # Counter to ensure uniqueness within product
        
        for _ in range(num_cis):
            # CIs are recent (last 6 months)
            created, updated = generate_timestamps(max_age_days=random.randint(30, 180))
            ci_type = random.choice(ci_types)
            environment = random.choice(environments)
            
            # Use counter to ensure unique name per product
            configuration_items[str(ci_id)] = {
                "ci_id": str(ci_id),
                "ci_name": f"{products[product_id]['product_name']}-{ci_type}-{environment[:4]}-{ci_counter:02d}",
                "product_id": product_id,
                "ci_type": ci_type,
                "environment": environment,
                "location": random.choice(['us-east-1', 'us-west-2', 'eu-west-1', 'ap-southeast-1']),
                "operational_status": random.choice(['operational', 'operational', 'operational', 'degraded', 'down']),
                "created_at": created,
                "updated_at": updated
            }
            ci_id += 1
            ci_counter += 1
    
    return configuration_items

def generate_subscriptions(clients, target_total=28):
    """Generate 28 subscriptions for clients (some clients have multiple)"""
    subscriptions = {}
    subscription_id = 1
    
    client_list = list(clients.items())
    
    # First, give each client one subscription
    for client_id, client in client_list:
        created, updated = generate_timestamps(max_age_days=random.randint(90, 365))
        # Subscription start date should be before created_at
        created_dt = datetime.fromisoformat(created)
        start_date = generate_timestamp(created_dt - timedelta(days=random.randint(30, 365)), created_dt).date()
        
        # Assign tier based on company type (from SOP)
        if client['company_type'] == 'enterprise':
            tier = 'premium'
        elif client['company_type'] == 'mid_market':
            tier = 'standard'
        else:  # smb, startup
            tier = 'basic'
        
        # 80% active, 20% expired
        if random.random() < 0.8:
            status = 'active'
            end_date_val = None
        else:
            status = 'expired'
            end_date_val = generate_timestamp(
                datetime.combine(start_date, datetime.min.time()),
                MAX_DATE
            ).date()
        
        subscriptions[str(subscription_id)] = {
            "subscription_id": str(subscription_id),
            "client_id": client_id,
            "tier": tier,
            "start_date": format_timestamp(start_date),
            "end_date": format_timestamp(end_date_val) if end_date_val else None,
            "status": status,
            "created_at": created,
            "updated_at": updated
        }
        subscription_id += 1
    
    # Add additional subscriptions to reach target (some clients get 2nd subscription with different tier)
    remaining = target_total - len(client_list)
    for _ in range(remaining):
        client_id, client = random.choice(client_list)
        created, updated = generate_timestamps(max_age_days=random.randint(90, 365))
        # Subscription start date should be before created_at
        created_dt = datetime.fromisoformat(created)
        start_date = generate_timestamp(created_dt - timedelta(days=random.randint(30, 365)), created_dt).date()
        
        # Different tier for 2nd subscription
        tier = random.choice(['premium', 'standard', 'basic'])
        
        if random.random() < 0.8:
            status = 'active'
            end_date_val = None
        else:
            status = 'expired'
            end_date_val = generate_timestamp(
                datetime.combine(start_date, datetime.min.time()),
                MAX_DATE
            ).date()
        
        subscriptions[str(subscription_id)] = {
            "subscription_id": str(subscription_id),
            "client_id": client_id,
            "tier": tier,
            "start_date": format_timestamp(start_date),
            "end_date": format_timestamp(end_date_val) if end_date_val else None,
            "status": status,
            "created_at": created,
            "updated_at": updated
        }
        subscription_id += 1
    
    return subscriptions

def generate_sla_agreements(subscriptions, users):
    """Generate SLA agreements based on tier and severity (from SOP 1.3)"""
    sla_agreements = {}
    sla_id = 1
    
    # Get incident managers for created_by
    incident_managers = get_users_by_role(users, 'incident_manager')
    
    for sub_id, sub in subscriptions.items():
        tier = sub['tier']
        
        # Each subscription gets SLAs for all severity levels
        for severity in ['P1', 'P2', 'P3', 'P4']:
            # SLA created shortly after subscription (1-30 days later)
            sub_created = datetime.fromisoformat(sub['created_at'])
            sla_created = generate_timestamp(sub_created, sub_created + timedelta(days=random.randint(1, 30)))
            created = format_timestamp(sla_created)
            
            # Get SLA times from matrix
            # IMPORTANT: Keep original generation logic to not affect random sequence
            # The correct ranges will be applied in post-processing
            sla_config = SLA_MATRIX[tier][severity]
            response_min, response_max = sla_config['response']
            resolution_min, resolution_max = sla_config['resolution']
            
            sla_agreements[str(sla_id)] = {
                "sla_id": str(sla_id),
                "subscription_id": sub_id,
                "severity_level": severity,
                "response_time_minutes": response_min,  # Will be adjusted in post-processing
                "resolution_time_minutes": resolution_min,  # Will be adjusted in post-processing
                "availability_guarantee": round(random.uniform(99.0, 99.99), 2),  # Keep random to preserve sequence, will be fixed in post-processing
                "created_by": random.choice(incident_managers) if incident_managers else "1",
                "created_at": created
            }
            sla_id += 1
    
    return sla_agreements

def generate_problem_tickets(clients, users, n=20):
    """Generate 20 problem tickets with realistic descriptions"""
    problems = {}
    
    # Realistic problem templates
    problem_templates = [
        ("Recurring authentication failures", "Multiple incidents reported regarding authentication failures affecting {count} clients. Pattern observed: failures occurring primarily during peak hours. Root cause under investigation."),
        ("Performance degradation on production database", "Recurring issue with database query performance causing service degradation. Multiple clients experiencing slow response times (>5s). Investigation shows connection pool exhaustion."),
        ("Memory leak in application server", "Systematic memory leak detected in production application servers. Issue affects {count} instances across multiple clients. Memory usage gradually increases until restart required."),
        ("Intermittent network timeouts", "Pattern of intermittent network connectivity issues reported by multiple clients in {region} region. Affects approximately {count} clients. Network team investigating routing issues."),
        ("API rate limiting false positives", "Multiple incidents related to incorrect API rate limiting triggers. Legitimate traffic being blocked. Affects {count} clients using high-volume API integrations."),
        ("Email delivery delays", "Recurring email delivery delays reported by {count} clients. Investigation shows mail queue backlog. Requires infrastructure scaling."),
        ("Session timeout issues", "User sessions expiring prematurely across multiple applications. Affects {count} clients. Configuration inconsistency suspected between load balancers."),
        ("Backup job failures", "Systematic backup job failures observed across {count} production environments. Storage capacity and network bandwidth under investigation."),
        ("Certificate renewal failures", "Automated SSL certificate renewal process failing for multiple domains. Manual intervention required. Affects {count} client domains."),
        ("Cache invalidation delays", "CDN cache invalidation not propagating correctly. Stale content being served to users. Multiple clients affected ({count} reported)."),
        ("Load balancer health check failures", "False positive health check failures causing unnecessary instance restarts. Pattern affects {count} backend services."),
        ("Data synchronization lag", "Recurring data replication lag between primary and secondary databases. Impacts read performance for {count} clients in disaster recovery configuration."),
        ("Disk space alerts ignored", "Systematic issue with disk space monitoring alerts not triggering properly. Multiple instances reached critical levels before manual detection. {count} servers affected."),
        ("Login page redirect loop", "Users experiencing infinite redirect loop on login page. Browser-specific issue affects Safari users. Reported by {count} clients."),
        ("File upload size limit errors", "Configuration inconsistency causing file upload failures. Different size limits across environments. Affects {count} users attempting large file uploads."),
        ("Webhook delivery failures", "Recurring webhook notification delivery failures. Retry mechanism not functioning correctly. {count} integration partners affected."),
        ("Search functionality degradation", "Search engine indexing delays causing stale search results. Multiple clients reporting missing recent data. {count} indexes require rebuild."),
        ("Mobile app crash on startup", "Pattern of mobile application crashes on cold start. Affects specific device models. {count} users reporting issue across multiple clients."),
        ("Payment processing timeouts", "Recurring payment gateway timeout issues during peak hours. Transaction success rate dropped below SLA. Affects {count} clients."),
        ("Report generation performance", "Large report generation jobs timing out. Resource contention suspected. Queue backlog growing. {count} scheduled reports failing daily.")
    ]
    
    for i in range(1, n + 1):
        created, updated = generate_timestamps(max_age_days=random.randint(30, 60))
        title, desc_template = problem_templates[i-1]
        
        # Fill in template variables
        description = desc_template.format(
            count=random.randint(3, 15),
            region=random.choice(['US-EAST', 'US-WEST', 'EU-WEST', 'AP-SOUTHEAST'])
        )
        
        problems[str(i)] = {
            "problem_id": str(i),
            "problem_number": f"PRB{str(i).zfill(7)}",
            "client_id": random.choice(list(clients.keys())),
            "title": title,
            "description": description,
            "status": random.choice(['open', 'investigating', 'resolved', 'closed']),
            "reported_by": random.choice(list(users.keys())),
            "created_at": created,
            "updated_at": updated
        }
    
    return problems

def generate_incidents(clients, cis, users, subscriptions, problems, incident_count=100):
    """
    Generate incidents with:
    - Proper severity-impact-urgency alignment
    - Authorized assignments
    - Realistic timestamps
    - Well-distributed temporal pattern (last 30 days, 40%+ in last 21 days)
    """
    incidents = {}
    categories = ['inquiry/help', 'software', 'hardware', 'Network', 'Database']
    
    # Severity alignment (from validation rules)
    severity_alignment = {
        'P1': {'impact': 'critical', 'urgency': 'critical'},
        'P2': {'impact': 'high', 'urgency': 'high'},
        'P3': {'impact': 'medium', 'urgency': 'medium'},
        'P4': {'impact': 'low', 'urgency': 'low'}
    }
    
    # Get clients with active subscriptions only (Client-Subscription Chain rule)
    clients_with_active_subs = [
        sub['client_id'] for sub in subscriptions.values() 
        if sub['status'] == 'active'
    ]
    
    if not clients_with_active_subs:
        # Fallback: use all clients if no active subscriptions
        clients_with_active_subs = list(clients.keys())
    
    # Generate incidents with proper temporal distribution:
    # - Period: Last 30 days (from 2025-09-13 to 2025-10-13)
    # - 45% in last 21 days (to ensure >= 40% threshold)
    # - 55% distributed across first 9 days
    # - Max 15 incidents per day
    end_date = MAX_DATE
    start_date = end_date - timedelta(days=30)  # Last 30 days
    recent_cutoff = end_date - timedelta(days=21)  # Last 21 days
    
    # Calculate how many incidents should be recent
    recent_count = int(incident_count * 0.45)  # 45% to ensure we pass 40% threshold
    older_count = incident_count - recent_count
    
    detection_times = []
    
    # Generate recent incidents (last 21 days: 2025-09-22 to 2025-10-13)
    for i in range(recent_count):
        days_offset = random.uniform(0, 21)
        detection_time = recent_cutoff + timedelta(
            days=days_offset,
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        # Ensure detection_time never exceeds reference date
        if detection_time > end_date:
            detection_time = end_date - timedelta(hours=random.randint(1, 24))
        detection_times.append(detection_time)
    
    # Generate older incidents (first 9 days: 2025-09-13 to 2025-09-21)
    older_period_days = (recent_cutoff - start_date).days
    for i in range(older_count):
        days_offset = random.uniform(0, older_period_days)
        detection_time = start_date + timedelta(
            days=days_offset,
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        detection_times.append(detection_time)
    
    # Shuffle to avoid patterns
    random.shuffle(detection_times)
    
    for i in range(1, incident_count + 1):
        detection_time = detection_times[i - 1]
        
        # Generate created_at and updated_at relative to detection_time
        # created_at should be AFTER detection_time (incident is logged after being detected)
        # updated_at should be after created_at (last modification time)
        created = detection_time + timedelta(minutes=random.randint(1, 15))
        updated = created + timedelta(minutes=random.randint(0, 120))
        # Ensure timestamps don't exceed reference date
        if created > REFERENCE_DATE:
            created = REFERENCE_DATE - timedelta(hours=1)
        if updated > REFERENCE_DATE:
            updated = REFERENCE_DATE
        
        severity = random.choice(['P1', 'P2', 'P3', 'P4'])
        
        # Calculate time until reference date to determine possible status
        time_until_max = (REFERENCE_DATE - detection_time).total_seconds() / 3600  # hours
        
        # Choose status based on available time
        if time_until_max < 1:
            status = 'open'  # Not enough time for any progression
        elif time_until_max < 2:
            status = random.choice(['open', 'in_progress'])
        elif time_until_max < 4:
            status = random.choice(['open', 'in_progress', 'monitoring'])
        else:
            status = random.choice(['open', 'in_progress', 'monitoring', 'resolved', 'closed'])
        
        # Generate timestamps based on status, ensuring proper ordering and MAX_DATE compliance
        acknowledged_at = None
        resolved_at = None
        closed_at = None
        
        if status in ['in_progress', 'monitoring', 'resolved', 'closed']:
            ack_time = detection_time + timedelta(minutes=min(random.randint(5, 60), time_until_max * 60 * 0.1))
            acknowledged_at = format_timestamp(ack_time)
        
        if status in ['resolved', 'closed']:
            res_time = detection_time + timedelta(hours=min(random.randint(1, 48), time_until_max * 0.5))
            resolved_at = format_timestamp(res_time)
        
        if status == 'closed':
            resolved_time = datetime.fromisoformat(resolved_at) if resolved_at else detection_time
            remaining_time = (REFERENCE_DATE - resolved_time).total_seconds() / 3600
            cls_time = resolved_time + timedelta(hours=min(random.randint(1, 24), remaining_time * 0.8))
            closed_at = format_timestamp(cls_time)
        
        # Generate realistic category-specific title and description
        ci_id = str(random.randint(1, len(cis)))
        component_name = cis[ci_id]['ci_name']
        category = random.choice(categories)
        
        # Category-specific incident templates
        if category == 'software':
            if severity == 'P1':
                title = random.choice([
                    f"Application crash: {component_name} service down",
                    f"Critical: Login failures on {component_name}",
                    f"Software failure: {component_name} throwing exceptions"
                ])
                description = f"""CRITICAL SOFTWARE FAILURE

Application: {component_name}
Impact: Service completely unavailable - all user requests failing
Users Affected: {random.randint(100, 1000)}+

Error Details:
- NullPointerException in authentication module
- Application crash detected at {detection_time.strftime('%H:%M')}
- Stack trace indicates memory corruption in user session handler
- All active sessions terminated

Immediate Actions:
- Failover to backup instance initiated
- Development team notified for emergency patch"""
            elif severity == 'P2':
                title = f"High: Performance degradation on {component_name} application"
                description = f"""Software Performance Issue

Application: {component_name}
Impact: Slow response times affecting user experience
Users Affected: {random.randint(50, 200)}

Issue:
- API response time increased from 200ms to {random.randint(2, 8)}s
- Database connection pool exhaustion detected
- Memory leak suspected in background job processor
- Error rate: {random.randint(10, 30)}%

Investigation:
- Analyzing heap dumps
- Reviewing recent code deployments"""
            else:
                title = f"Software bug: {component_name} intermittent errors"
                description = f"Minor software issue affecting {component_name}. {random.choice(['UI rendering inconsistency', 'Form validation error', 'Report export formatting issue'])} reported by users. Low priority fix scheduled for next sprint."
        
        elif category == 'hardware':
            if severity == 'P1':
                title = random.choice([
                    f"Critical: Server {component_name} hardware failure",
                    f"Disk failure on {component_name}",
                    f"Emergency: {component_name} unresponsive - hardware issue"
                ])
                description = f"""CRITICAL HARDWARE FAILURE

Server: {component_name}
Impact: Complete system failure
Location: {cis[ci_id]['location']}

Hardware Status:
- Primary disk array failed - RAID controller error
- System unresponsive to ping
- Data center technician dispatched
- Failover to secondary system {random.choice(['completed', 'in progress'])}

Data Center Response:
- Physical inspection required
- Estimated hardware replacement: 4-6 hours"""
            elif severity == 'P2':
                title = f"Hardware: {component_name} disk space critical"
                description = f"""Hardware Resource Issue

Server: {component_name}
Issue: Critical disk space shortage
Environment: {cis[ci_id]['environment']}

Status:
- Disk usage: {random.randint(92, 99)}%
- Log files consuming {random.randint(20, 50)}GB
- Database growth exceeding projections
- Risk of service degradation if not addressed

Action Plan:
- Emergency cleanup of temp files
- Log rotation policy adjustment
- Capacity planning review scheduled"""
            else:
                title = f"Hardware: {component_name} temperature warning"
                description = f"Server {component_name} reporting elevated temperature. CPU temp at {random.randint(75, 85)}°C. Cooling system operating normally. Monitoring for escalation. Non-critical."
        
        elif category == 'Network':
            if severity == 'P1':
                title = random.choice([
                    f"Critical: Network outage affecting {component_name}",
                    f"Complete connectivity loss to {component_name}",
                    f"Emergency: Network partition - {component_name} unreachable"
                ])
                description = f"""CRITICAL NETWORK OUTAGE

Affected Service: {component_name}
Impact: Complete network connectivity loss
Region: {cis[ci_id]['location']}
Users Affected: {random.randint(500, 2000)}+

Network Status:
- All traffic to {cis[ci_id]['location']} timing out
- BGP route flapping detected
- Multiple availability zones affected
- Primary and backup paths both down

Network Team Actions:
- ISP escalation opened
- Traffic being rerouted through {random.choice(['EU-WEST', 'US-EAST', 'AP-SOUTHEAST'])}
- Estimated restoration: 2-4 hours"""
            elif severity == 'P2':
                title = f"Network: High latency on {component_name}"
                description = f"""Network Performance Degradation

Service: {component_name}
Issue: Increased network latency
Location: {cis[ci_id]['location']}

Metrics:
- Latency increased from 15ms to {random.randint(150, 500)}ms
- Packet loss: {random.randint(3, 10)}%
- DNS resolution delays observed
- Affecting cross-region replication

Investigation:
- Network path analysis in progress
- Coordinating with ISP on circuit issues"""
            else:
                title = f"Network: Intermittent connectivity to {component_name}"
                description = f"Sporadic network timeout errors reported for {component_name}. Issue appears intermittent. Network monitoring shows no major anomalies. Investigating potential route optimization."
        
        elif category == 'Database':
            if severity == 'P1':
                title = random.choice([
                    f"Critical: Database {component_name} unavailable",
                    f"Database failure: {component_name} connection refused",
                    f"Emergency: {component_name} database crashed"
                ])
                description = f"""CRITICAL DATABASE FAILURE

Database: {component_name}
Impact: All database operations failing
Dependent Services: {random.randint(5, 20)} services affected

Error Status:
- Primary database instance crashed at {detection_time.strftime('%H:%M')}
- Connection pool exhausted - max connections reached
- Automatic failover initiated to read replica
- Transaction logs corrupted - recovery in progress

DBA Actions:
- Point-in-time recovery initiated
- Analyzing transaction logs
- Expected RTO: {random.randint(30, 120)} minutes"""
            elif severity == 'P2':
                title = f"Database: Query performance degradation on {component_name}"
                description = f"""Database Performance Issue

Database: {component_name}
Issue: Slow query performance
Environment: {cis[ci_id]['environment']}

Performance Metrics:
- Average query time increased from 50ms to {random.randint(2, 10)}s
- Lock wait timeouts increasing
- Table scan operations detected on large tables
- Connection pool at {random.randint(80, 95)}% capacity

Actions:
- Analyzing slow query log
- Index optimization required
- Query plan review in progress"""
            else:
                title = f"Database: {component_name} connection pool warning"
                description = f"Database connection pool for {component_name} reaching capacity limits. Current utilization: {random.randint(70, 85)}%. No immediate impact but monitoring for potential escalation. Consider connection pool tuning."
        
        else:  # inquiry/help
            if severity == 'P1':
                title = f"Critical: User lockout issue - {component_name}"
                description = f"Multiple users unable to access {component_name} service. Authentication system returning errors. {random.randint(200, 500)} active users affected. Emergency investigation in progress."
            elif severity == 'P2':
                title = f"Help request: Access issues on {component_name}"
                description = f"Users reporting access difficulties with {component_name}. Intermittent authentication failures. Working with security team to investigate. {random.randint(20, 100)} users affected."
            else:
                title = f"User inquiry: {component_name} feature question"
                description = f"User inquiry regarding {component_name} functionality. {random.choice(['Feature request for enhanced reporting', 'Question about API usage limits', 'Request for additional user permissions', 'Clarification on data export format'])}. Standard support response provided."
        
        # Ensure incident client has an active subscription (Client-Subscription Chain rule)
        client_id = random.choice(clients_with_active_subs)
        
        # Link to problem ticket (SOP 4.1: multiple incidents can share same problem)
        # About 40% of incidents are linked to problems
        problem_id = random.choice(list(problems.keys())) if random.random() > 0.6 else None
        
        incidents[str(i)] = {
            "incident_id": str(i),
            "problem_id": problem_id,
            "incident_number": f"INC{str(i).zfill(7)}",
            "title": title,
            "description": description,
            "category": category,
            "client_id": client_id,
            "affected_ci_id": ci_id,
            "severity": severity,
            "impact": severity_alignment[severity]['impact'],
            "urgency": severity_alignment[severity]['urgency'],
            "status": status,
            "reported_by": random.choice(list(users.keys())),
            "assigned_to": get_authorized_user(users, 'incident_assignment') if status != 'open' else None,
            "detection_time": format_timestamp(detection_time),
            "acknowledged_at": acknowledged_at,
            "resolved_at": resolved_at,
            "closed_at": closed_at,
            "created_at": format_timestamp(created),
            "updated_at": format_timestamp(updated)
        }
    
    return incidents

def generate_work_notes(incidents, users):
    """Generate contextual work notes"""
    work_notes = {}
    note_id = 1
    
    investigation_notes = [
        "Analyzing system logs from {start_time} to {end_time}. Initial findings indicate {issue} affecting {component}.",
        "Reproduced the issue in {env} environment. Root cause appears to be related to {cause}.",
        "Monitoring dashboards show {metric} increased significantly at {time}. Correlating with other system events."
    ]
    
    resolution_notes = [
        "Applied hotfix version {version} to {component}. Monitoring system stability for {duration}.",
        "Restarted affected services on {servers}. All services restored at {time}.",
        "Updated configuration parameter {param} from {old_val} to {new_val}. System responding normally."
    ]
    
    monitoring_notes = [
        "All metrics returned to baseline levels. Monitoring for {duration} before closing.",
        "System performance stable for past {hours} hours. No anomalies detected.",
        "Error rate dropped to {percent}% (within acceptable threshold of {threshold}%)."
    ]
    
    for incident_id, incident in list(incidents.items())[:95]:
        incident_status = incident['status']
        num_notes = random.randint(1, 3)
        
        for _ in range(num_notes):
            # Generate work note timestamp relative to incident timestamps
            incident_created = datetime.fromisoformat(incident['created_at'])
            incident_updated = datetime.fromisoformat(incident['updated_at'])
            created = generate_timestamp(incident_created, incident_updated)
            
            if incident_status == 'open':
                note_template = random.choice(investigation_notes)
            elif incident_status in ['resolved', 'closed']:
                note_template = random.choice(resolution_notes + monitoring_notes)
            else:
                note_template = random.choice(investigation_notes)
            
            note_text = note_template.format(
                start_time=created.strftime('%H:%M'),
                end_time=(created + timedelta(hours=2)).strftime('%H:%M'),
                issue=random.choice(['timeout errors', 'high memory usage']),
                component=incident['title'][:30],
                env=random.choice(['staging', 'production', 'test']),
                cause=random.choice(['configuration mismatch', 'resource exhaustion']),
                metric=random.choice(['error_rate', 'response_time']),
                time=created.strftime('%H:%M'),
                version=f"v{random.randint(1,5)}.{random.randint(0,9)}.{random.randint(0,20)}",
                duration=f"{random.randint(30, 180)} minutes",
                servers=f"srv-{random.randint(1,99):02d}",
                param=random.choice(['max_connections', 'timeout_seconds']),
                old_val=random.randint(100, 500),
                new_val=random.randint(500, 2000),
                hours=random.randint(24, 72),
                percent=random.randint(0, 3),
                threshold=5
            )
            
            work_notes[str(note_id)] = {
                "note_id": str(note_id),
                "incident_id": incident_id,
                "note_text": note_text,
                "created_by": random.choice(list(users.keys())),
                "created_at": format_timestamp(created)
            }
            note_id += 1
    
    return work_notes

# NOTE: incident_attachments removed - replaced by generic attachments table
# Use generate_attachments.py script to create attachments for multiple reference types

def generate_escalations(incidents, users):
    """
    Generate escalations with proper authorization flow
    Following SOP 4.3 and Approval Request Flow by Role table
    """
    escalations = {}
    escalation_id = 1
    
    escalation_reason_templates = {
        'L1_to_L2': [
            "Issue complexity beyond L1 support capabilities. Requires advanced troubleshooting expertise.",
            "Unable to resolve within SLA timeframe. Escalating to L2 for specialized technical support."
        ],
        'L2_to_L3': [
            "Potential code-level bug identified. Requires engineering team investigation and fix.",
            "Multiple components involved. Need cross-team coordination at L3 level."
        ],
        'L3_to_management': [
            "Critical business impact requiring management decision on resource allocation.",
            "SLA breach imminent. Management notification required per escalation policy."
        ],
        'management_to_executive': [
            "Major incident with widespread customer impact. Executive awareness required.",
            "Extended outage affecting revenue. Executive decision needed on communication strategy."
        ]
    }
    
    for incident_id in list(incidents.keys())[:25]:
        incident = incidents[incident_id]
        num_escalations = random.randint(1, 2)
        for _ in range(num_escalations):
            # Escalation requested between incident created and updated
            incident_created = datetime.fromisoformat(incident['created_at'])
            incident_updated = datetime.fromisoformat(incident['updated_at'])
            requested = generate_timestamp(incident_created, incident_updated)
            status = random.choice(['pending', 'approved', 'denied', 'cancelled'])
            responded_at = format_timestamp(requested + timedelta(hours=random.randint(1, 12))) if status != 'pending' else None
            
            escalation_level = random.choice(['L1_to_L2', 'L2_to_L3', 'L3_to_management', 'management_to_executive'])
            escalation_reason = random.choice(escalation_reason_templates[escalation_level])
            
            # Escalated_to must be incident_manager or executive (from validation rules)
            escalated_to = get_authorized_user(users, 'escalation_target')
            
            escalations[str(escalation_id)] = {
                "escalation_id": str(escalation_id),
                "incident_id": incident_id,
                "escalated_from": random.choice(list(users.keys())),
                "escalated_to": escalated_to if escalated_to else "1",
                "escalation_level": escalation_level,
                "escalation_reason": escalation_reason,
                "status": status,
                "requested_at": format_timestamp(requested),
                "responded_at": responded_at
            }
            escalation_id += 1
    
    return escalations

def generate_bridges(incidents, users):
    """
    Generate bridges with authorized hosts
    Bridge host must be incident_manager or system_administrator (from validation rules)
    """
    bridges = {}
    bridge_id = 1
    
    for incident_id in list(incidents.keys())[:15]:
        # Bridge should be created after incident
        incident = incidents[incident_id]
        incident_created = datetime.fromisoformat(incident['created_at'])
        incident_updated = datetime.fromisoformat(incident['updated_at'])
        created = format_timestamp(generate_timestamp(incident_created, incident_updated))
        start_time = generate_timestamp(incident_created, incident_updated)
        status = random.choice(['active', 'closed', 'closed'])
        end_time = format_timestamp(start_time + timedelta(hours=random.randint(1, 8))) if status == 'closed' else None
        
        # Bridge host must be authorized
        bridge_host = get_authorized_user(users, 'bridge_host')
        
        bridges[str(bridge_id)] = {
            "bridge_id": str(bridge_id),
            "bridge_number": f"BRG{str(bridge_id).zfill(7)}",
            "incident_id": incident_id,
            "bridge_type": random.choice(['major_incident', 'coordination', 'technical']),
            "bridge_host": bridge_host if bridge_host else "1",
            "start_time": format_timestamp(start_time),
            "end_time": end_time,
            "status": status,
            "created_at": created
        }
        bridge_id += 1
    
    return bridges

def generate_bridge_participants(bridges, users):
    """Generate bridge participants"""
    bridge_participants = {}
    participant_id = 1
    
    for b_id in bridges.keys():
        bridge = bridges[b_id]
        bridge_start = datetime.fromisoformat(bridge['start_time'])
        bridge_end = datetime.fromisoformat(bridge['end_time']) if bridge['end_time'] else REFERENCE_DATE
        
        num_participants = random.randint(2, 5)
        for _ in range(num_participants):
            # Participants join between bridge start and end
            joined = format_timestamp(generate_timestamp(bridge_start, bridge_end))
            bridge_participants[str(participant_id)] = {
                "participant_id": str(participant_id),
                "bridge_id": b_id,
                "user_id": random.choice(list(users.keys())),
                "role_in_bridge": random.choice(['host', 'technical_support', 'account_manager', 'vendor', 'executive']),
                "joined_at": joined
            }
            participant_id += 1
    
    return bridge_participants

def generate_change_requests(incidents, users):
    """
    Generate change requests with proper approval flow
    Following SOP 6.1 and Approval Request Flow by Role
    """
    change_requests = {}
    change_id = 1
    
    change_title_templates = {
        'emergency': [
            "Emergency: Implement hotfix for {component} critical vulnerability",
            "Emergency: Restore {component} service from backup"
        ],
        'normal': [
            "Upgrade {component} to version {version}",
            "Implement {component} performance optimization"
        ],
        'standard': [
            "Apply {component} monthly security updates",
            "Update {component} configuration parameters"
        ]
    }
    
    for incident_id in list(incidents.keys())[:30]:
        # Change requests are recent (last 45 days)
        created, updated = generate_timestamps(max_age_days=random.randint(15, 45))
        status = random.choice(['requested', 'approved', 'denied', 'scheduled', 'implemented', 'cancelled'])
        change_type = random.choice(['standard', 'normal', 'emergency'])
        
        # Risk level correlates with change type
        risk_mapping = {
            'emergency': random.choice(['high', 'critical']),
            'normal': random.choice(['medium', 'high']),
            'standard': random.choice(['low', 'medium'])
        }
        risk_level = risk_mapping[change_type]
        
        component = random.choice(['Application Server', 'Database', 'Load Balancer'])
        version = f"{random.randint(1,5)}.{random.randint(0,9)}.{random.randint(0,20)}"
        
        title = random.choice(change_title_templates[change_type]).format(
            component=component,
            version=version
        )
        
        # Approved_by must be incident_manager or executive (from validation rules)
        approved_by = get_authorized_user(users, 'change_approval') if status in ['approved', 'scheduled', 'implemented'] else None
        
        change_requests[str(change_id)] = {
            "change_id": str(change_id),
            "change_number": f"CHG{str(change_id).zfill(7)}",
            "incident_id": incident_id if random.random() > 0.3 else None,
            "title": title,
            "description": f"Change request to modify {component}",
            "change_type": change_type,
            "risk_level": risk_level,
            "requested_by": random.choice(list(users.keys())),
            "approved_by": approved_by,
            "status": status,
            "implementation_date": format_timestamp(generate_timestamp(datetime.fromisoformat(created), REFERENCE_DATE)) if status in ['scheduled', 'implemented'] else None,
            "created_at": created,
            "updated_at": updated
        }
        change_id += 1
    
    return change_requests

def generate_rollback_requests(change_requests, incidents, users):
    """Generate rollback requests following SOP 6.2"""
    rollback_requests = {}
    rollback_id = 1
    
    rollback_reason_templates = [
        """Change implementation caused unexpected side effects:
- Error rate increased to {error_rate}%
- Performance degradation of {degradation}%

Immediate rollback required to restore service stability.""",
        
        """Post-implementation validation failed:
- Critical functionality broken: {broken_feature}
- Monitoring alerts triggered: {alert_count}

Initiating emergency rollback procedure."""
    ]
    
    for c_id in list(change_requests.keys())[:10]:
        # Rollback created after the change request
        change = change_requests[c_id]
        change_created = datetime.fromisoformat(change['created_at'])
        created = generate_timestamp(change_created, REFERENCE_DATE)
        status = random.choice(['requested', 'approved', 'executed', 'failed'])
        
        change = change_requests[c_id]
        title = f"Rollback: {change['title']}"
        
        rollback_reason = random.choice(rollback_reason_templates).format(
            error_rate=random.randint(15, 45),
            degradation=random.randint(30, 80),
            broken_feature=random.choice(['user login', 'payment processing']),
            alert_count=random.randint(10, 100)
        )
        
        rollback_requests[str(rollback_id)] = {
            "rollback_id": str(rollback_id),
            "rollback_number": f"RBK{str(rollback_id).zfill(7)}",
            "change_id": c_id,
            "incident_id": random.choice(list(incidents.keys())),
            "title": title,
            "rollback_reason": rollback_reason,
            "requested_by": random.choice(list(users.keys())),
            "status": status,
            "executed_at": format_timestamp(created + timedelta(hours=random.randint(1, 6))) if status in ['executed', 'failed'] else None,
            "created_at": format_timestamp(created)
        }
        rollback_id += 1
    
    return rollback_requests

def generate_work_orders(change_requests, incidents, users):
    """
    Generate work orders with authorized assignments
    Assigned_to must be technical_support or system_administrator (from validation rules)
    """
    work_orders = {}
    work_order_id = 1
    
    for i in range(1, 41):
        # Work orders are recent (within last 60 days)
        created = generate_timestamp(REFERENCE_DATE - timedelta(days=60), REFERENCE_DATE)
        status = random.choice(['pending', 'in_progress', 'completed', 'cancelled'])
        
        component = random.choice(['Application Server', 'Database', 'Load Balancer'])
        title = f"Maintenance: {component} security patching"
        
        # Assigned_to must be authorized
        assigned_to = get_authorized_user(users, 'work_order_assignment')
        
        work_orders[str(work_order_id)] = {
            "work_order_id": str(work_order_id),
            "work_order_number": f"WO{str(work_order_id).zfill(7)}",
            "change_id": random.choice(list(change_requests.keys())) if random.random() > 0.5 else None,
            "incident_id": random.choice(list(incidents.keys())) if random.random() > 0.5 else None,
            "title": title,
            "description": f"Scheduled maintenance task for {component}",
            "assigned_to": assigned_to if assigned_to else "1",
            "status": status,
            "scheduled_date": format_timestamp(created + timedelta(days=random.randint(1, 30))),
            "completed_at": format_timestamp(created + timedelta(days=random.randint(1, 7))) if status == 'completed' else None,
            "created_at": format_timestamp(created)
        }
        work_order_id += 1
    
    return work_orders

def generate_approval_requests(escalations, bridges, change_requests, rollback_requests, users, incidents):
    """
    Generate approval requests following SOP 4.8 Approval Request Flow by Role
    Rules:
    - Technical Support: P3/P4 escalation/bridge/rollback -> Incident Manager AND Executive (one from either)
    - Account Manager: SLA breach escalation -> Incident Manager AND Executive (one from either)
    - System Administrator: P3/P4 bridge -> Incident Manager only
    - System Administrator: Rollback/High-Risk Change -> Incident Manager AND Executive (one from either)
    - Incident Manager: Emergency change -> Executive only
    """
    approval_requests = {}
    approval_id = 1
    
    # Get users by role
    tech_support = get_users_by_role(users, 'technical_support')
    account_managers = get_users_by_role(users, 'account_manager')
    sys_admins = get_users_by_role(users, 'system_administrator')
    incident_managers = get_users_by_role(users, 'incident_manager')
    executives = get_users_by_role(users, 'executive')
    
    # Create approval requests for ALL P3/P4 escalations (per SOP)
    for esc_id, esc in escalations.items():
        incident = incidents.get(str(esc['incident_id']))
        if not incident:
            continue
        
        severity = incident['severity']
        
        # Only P3/P4 escalations need approval per SOP
        if severity not in ['P3', 'P4']:
            # P1/P2 don't need approval per SOP (automatic)
            continue
        
        # Approval requested between incident created and updated
        incident_created = datetime.fromisoformat(incident['created_at']) if incident else (REFERENCE_DATE - timedelta(days=30))
        incident_updated = datetime.fromisoformat(incident['updated_at']) if incident else REFERENCE_DATE
        requested = generate_timestamp(incident_created, incident_updated)
        status = random.choice(['pending', 'approved', 'approved', 'denied'])  # 60% approved
        
        # Technical Support or Account Manager -> Incident Manager AND Executive (one from either)
        requester = random.choice(tech_support + account_managers) if (tech_support + account_managers) else random.choice(list(users.keys()))
        approver = random.choice(incident_managers + executives) if (incident_managers + executives) else random.choice(list(users.keys()))
        
        responded_at = format_timestamp(requested + timedelta(hours=random.randint(1, 48))) if status != 'pending' else None
        
        approval_requests[str(approval_id)] = {
            "approval_id": str(approval_id),
            "reference_id": esc_id,
            "reference_type": 'escalations',
            "requested_by": requester,
            "requested_action": "create_escalation",
            "approver": approver,  # Always set approver (pre-assigned for pending, actual for approved/denied)
            "status": status,
            "requested_at": format_timestamp(requested),
            "responded_at": responded_at
        }
        approval_id += 1
    
    # Create approval requests for bridges (P3/P4 only per SOP)
    for bridge_id, bridge in list(bridges.items())[:10]:
        incident = incidents.get(str(bridge['incident_id']))
        severity = incident['severity'] if incident else 'P3'
        
        if severity in ['P3', 'P4']:  # Only P3/P4 need approval
            # Use bridge created_at as base
            bridge_created = datetime.fromisoformat(bridge['created_at'])
            requested = generate_timestamp(bridge_created, bridge_created + timedelta(hours=12))
            status = random.choice(['pending', 'approved', 'approved', 'denied'])
            
            # System Administrator -> Incident Manager only
            requester = random.choice(sys_admins) if sys_admins else random.choice(list(users.keys()))
            approver = random.choice(incident_managers) if incident_managers else random.choice(list(users.keys()))
            
            responded_at = format_timestamp(requested + timedelta(hours=random.randint(1, 24))) if status != 'pending' else None
            
            approval_requests[str(approval_id)] = {
                "approval_id": str(approval_id),
                "reference_id": bridge_id,
                "reference_type": 'bridges',
                "requested_by": requester,
                "requested_action": "initiate_bridge",
                "approver": approver,  # Always set approver (pre-assigned for pending, actual for approved/denied)
                "status": status,
                "requested_at": format_timestamp(requested),
                "responded_at": responded_at
            }
            approval_id += 1
    
    # Create approval requests for change requests (High Risk/Emergency)
    for cr_id, cr in list(change_requests.items())[:15]:
        # Use change request created_at as base
        cr_created = datetime.fromisoformat(cr['created_at'])
        requested = generate_timestamp(cr_created, cr_created + timedelta(hours=24))
        status = random.choice(['pending', 'approved', 'approved', 'denied'])
        
        if cr['risk_level'] in ['high', 'critical'] or cr['change_type'] == 'emergency':
            # System Administrator or Incident Manager -> Incident Manager AND Executive (one from either)
            if cr['change_type'] == 'emergency' and cr['requested_by'] in incident_managers:
                # Incident Manager -> Executive only
                requester = cr['requested_by']
                approver = random.choice(executives) if executives else random.choice(list(users.keys()))
            else:
                # System Administrator -> Incident Manager AND Executive (one from either)
                requester = random.choice(sys_admins) if sys_admins else cr['requested_by']
                approver = random.choice(incident_managers + executives) if (incident_managers + executives) else random.choice(list(users.keys()))
            
            responded_at = format_timestamp(requested + timedelta(hours=random.randint(1, 72))) if status != 'pending' else None
            
            approval_requests[str(approval_id)] = {
                "approval_id": str(approval_id),
                "reference_id": cr_id,
                "reference_type": 'change_requests',
                "requested_by": requester,
                "requested_action": "create_change_request",
                "approver": approver,  # Always set approver (pre-assigned for pending, actual for approved/denied)
                "status": status,
                "requested_at": format_timestamp(requested),
                "responded_at": responded_at
            }
            approval_id += 1
    
    # Create approval requests for rollbacks
    for rb_id, rb in list(rollback_requests.items())[:8]:
        # Use rollback created_at as base
        rb_created = datetime.fromisoformat(rb['created_at'])
        requested = generate_timestamp(rb_created, rb_created + timedelta(hours=12))
        status = random.choice(['pending', 'approved', 'approved', 'denied'])
        
        # Technical Support or System Administrator -> Incident Manager AND Executive (one from either)
        requester = random.choice(tech_support + sys_admins) if (tech_support + sys_admins) else random.choice(list(users.keys()))
        approver = random.choice(incident_managers + executives) if (incident_managers + executives) else random.choice(list(users.keys()))
        
        responded_at = format_timestamp(requested + timedelta(hours=random.randint(1, 24))) if status != 'pending' else None
        
        approval_requests[str(approval_id)] = {
            "approval_id": str(approval_id),
            "reference_id": rb_id,
            "reference_type": 'rollback_requests',
            "requested_by": requester,
            "requested_action": "create_rollback_request",
            "approver": approver,  # Always set approver (pre-assigned for pending, actual for approved/denied)
            "status": status,
            "requested_at": format_timestamp(requested),
            "responded_at": responded_at
        }
        approval_id += 1
    
    # Fill remaining with RCA and incident closure approvals to reach 700
    while approval_id <= 700:
        # Generate recent approval requests (last 60 days)
        requested = generate_timestamp(REFERENCE_DATE - timedelta(days=60), REFERENCE_DATE)
        status = random.choice(['pending', 'approved', 'approved', 'denied'])
        ref_type = random.choice(['root_cause_analyses', 'incidents'])
        
        # RCA/Incident Closure: Incident Manager -> Executive
        requester = random.choice(incident_managers) if incident_managers else random.choice(list(users.keys()))
        approver = random.choice(executives) if executives else random.choice(list(users.keys()))
        
        responded_at = format_timestamp(requested + timedelta(hours=random.randint(1, 48))) if status != 'pending' else None
        
        # Use correct range for reference_id based on type
        if ref_type == 'root_cause_analyses':
            # 25 RCAs exist (based on generate_root_cause_analyses output)
            reference_id = str(random.randint(1, 25))
        else:  # incidents
            # 100 incidents exist
            reference_id = str(random.randint(1, len(incidents)))
        
        # Determine action based on type
        if ref_type == 'root_cause_analyses':
            action = 'conduct_rca'
        else:
            action = 'close_incident'
        
        approval_requests[str(approval_id)] = {
            "approval_id": str(approval_id),
            "reference_id": reference_id,
            "reference_type": ref_type,
            "requested_by": requester,
            "requested_action": action,
            "approver": approver,  # Always set approver (pre-assigned for pending, actual for approved/denied)
            "status": status,
            "requested_at": format_timestamp(requested),
            "responded_at": responded_at
        }
        approval_id += 1
    
    return approval_requests

def generate_communications(incidents, users):
    """Generate communications for incidents"""
    communications = {}
    comm_id = 1
    
    for incident_id in list(incidents.keys())[:60]:
        incident = incidents[incident_id]
        num_comms = random.randint(1, 3)
        
        for _ in range(num_comms):
            # Communication created between incident created and updated
            incident_created = datetime.fromisoformat(incident['created_at'])
            incident_updated = datetime.fromisoformat(incident['updated_at'])
            created = generate_timestamp(incident_created, incident_updated)
            delivery_status = random.choice(['pending', 'sent', 'delivered', 'failed'])
            sent_at = format_timestamp(created + timedelta(minutes=random.randint(1, 30))) if delivery_status in ['sent', 'delivered'] else None
            
            comm_type = random.choice(['status_update', 'resolution_notice', 'escalation_notice', 'bridge_invitation'])
            
            if comm_type == 'status_update':
                message_content = f"Incident {incident['incident_number']}: {incident['title'][:50]} - Status: {incident['status'].upper()}"
            elif comm_type == 'resolution_notice':
                message_content = f"RESOLVED: Incident {incident['incident_number']} has been resolved."
            elif comm_type == 'escalation_notice':
                message_content = f"Incident {incident['incident_number']} has been escalated. Immediate attention required."
            else:
                message_content = f"Conference Bridge Invitation for Incident {incident['incident_number']}"
            
            communications[str(comm_id)] = {
                "communication_id": str(comm_id),
                "incident_id": incident_id,
                "communication_type": comm_type,
                "recipient_type": random.choice(['client', 'internal', 'vendor', 'executive']),
                "sender": random.choice(list(users.keys())),
                "recipient": random.choice(list(users.keys())) if random.random() > 0.3 else None,
                "delivery_method": random.choice(['email', 'portal', 'sms', 'phone']),
                "message_content": message_content,
                "delivery_status": delivery_status,
                "sent_at": sent_at,
                "created_at": format_timestamp(created)
            }
            comm_id += 1
    
    return communications

def generate_performance_metrics(incidents, users):
    """Generate performance metrics for closed incidents"""
    performance_metrics = {}
    metric_id = 1
    
    for incident_id in list(incidents.keys())[:70]:
        incident = incidents[incident_id]
        num_metrics = random.randint(1, 3)
        metric_types_used = random.sample(['MTTA', 'MTTD', 'MTTR', 'MTTM', 'FTR'], num_metrics)
        for metric_type in metric_types_used:
            # Performance metric recorded between incident created and resolved/closed
            incident_created = datetime.fromisoformat(incident['created_at'])
            incident_resolved = datetime.fromisoformat(incident.get('resolved_at') or incident.get('closed_at') or incident['updated_at'])
            recorded = format_timestamp(generate_timestamp(incident_created, incident_resolved))
            performance_metrics[str(metric_id)] = {
                "metric_id": str(metric_id),
                "incident_id": incident_id,
                "metric_type": metric_type,
                "calculated_value_minutes": random.randint(10, 2000),
                "sla_target_minutes": random.randint(30, 2400),
                "recorded_by": random.choice(list(users.keys())),
                "recorded_date": recorded
            }
            metric_id += 1
    
    return performance_metrics

def generate_incident_reports(incidents, users):
    """Generate incident reports with realistic content following SOP 7.2"""
    incident_reports = {}
    report_id = 1
    
    for incident_id in list(incidents.keys())[:30]:
        incident = incidents[incident_id]
        # Report generated after incident is resolved/closed
        incident_created = datetime.fromisoformat(incident['created_at'])
        incident_resolved = datetime.fromisoformat(incident.get('resolved_at') or incident.get('closed_at') or incident['updated_at'])
        generation_date = generate_timestamp(incident_resolved, incident_resolved + timedelta(days=random.randint(1, 7)))
        report_type = random.choice(['post_incident_review', 'client_impact', 'compliance'])
        
        report_title = f"{report_type.replace('_', ' ').title()} - {incident['incident_number']}"
        
        # Generate report_content based on report_type
        if report_type == 'post_incident_review':
            report_content = f"""POST-INCIDENT REVIEW REPORT

Incident: {incident['incident_number']}
Title: {incident['title']}
Date: {incident['detection_time']}
Severity: {incident['severity']}

EXECUTIVE SUMMARY:
This report provides a comprehensive analysis of incident {incident['incident_number']} which occurred on {incident['detection_time'][:10]}. The incident impacted {random.choice(['customer-facing services', 'internal systems', 'critical infrastructure', 'production environment'])} and was classified as {incident['severity']}.

INCIDENT TIMELINE:
- {incident['detection_time'][:16]} - Incident detected and logged
- {(incident.get('acknowledged_at') or 'N/A')[:16] if incident.get('acknowledged_at') else 'N/A'} - Incident acknowledged by support team
- {(incident.get('resolved_at') or 'N/A')[:16] if incident.get('resolved_at') else 'N/A'} - Resolution implemented
- {(incident.get('closed_at') or 'N/A')[:16] if incident.get('closed_at') else 'N/A'} - Incident closed after verification

ROOT CAUSE:
The incident was caused by {random.choice(['configuration error', 'software bug', 'hardware failure', 'capacity exhaustion', 'network issue'])}. {random.choice(['Investigation revealed inadequate monitoring', 'Analysis showed missing alerting thresholds', 'Review identified insufficient capacity planning'])}.

IMPACT ASSESSMENT:
- Service Availability: {random.randint(85, 99)}%
- Users Affected: {random.randint(10, 500)}
- Duration: {random.randint(30, 240)} minutes
- Revenue Impact: {random.choice(['Minimal', 'Low', 'Medium', 'High'])}

LESSONS LEARNED:
1. {random.choice(['Monitoring gaps identified in critical system components', 'Alert thresholds need adjustment', 'Documentation requires updates'])}
2. {random.choice(['Response time can be improved with better runbooks', 'Escalation procedures need clarification', 'Communication channels need optimization'])}
3. {random.choice(['Capacity planning process needs enhancement', 'Disaster recovery procedures validated', 'Backup systems performed as expected'])}

ACTION ITEMS:
1. Update monitoring configuration [{random.choice(['HIGH', 'MEDIUM'])} Priority]
2. Enhance runbook documentation [{random.choice(['HIGH', 'MEDIUM'])} Priority]
3. Conduct team training on incident response [MEDIUM Priority]
4. Review and update capacity thresholds [MEDIUM Priority]

RECOMMENDATIONS:
- Implement additional monitoring for early detection
- Conduct regular disaster recovery drills
- Review and update SLA commitments
- Enhance automated failover capabilities"""
        
        elif report_type == 'client_impact':
            report_content = f"""CLIENT IMPACT ASSESSMENT REPORT

Incident Reference: {incident['incident_number']}
Assessment Date: {generation_date.strftime('%Y-%m-%d')}
Severity Classification: {incident['severity']}

INCIDENT OVERVIEW:
On {incident['detection_time'][:10]}, our monitoring systems detected {incident['title'].lower()}. This incident affected {random.choice(['multiple client environments', 'a subset of clients', 'all clients in affected region'])}.

CLIENT IMPACT SUMMARY:
Affected Clients: {random.randint(1, 25)}
Total Users Impacted: {random.randint(50, 1000)}
Impact Classification: {incident['impact'].upper()}
Business Functions Affected: {random.choice(['Transaction Processing', 'Data Access', 'Reporting Services', 'Authentication Services'])}

SERVICE IMPACT:
During the incident window, clients experienced {random.choice(['complete service unavailability', 'performance degradation', 'intermittent connectivity issues', 'delayed transaction processing'])}. The impact lasted approximately {random.randint(15, 180)} minutes from initial detection to full service restoration.

RESPONSE AND RESOLUTION:
Our incident response team was mobilized immediately upon detection. {random.choice(['Emergency procedures were activated', 'Escalation protocols were followed', 'War room was established'])} and resolution efforts began within {random.randint(5, 30)} minutes.

Resolution steps included:
1. Immediate failover to backup systems
2. Root cause identification and remediation
3. Service restoration and verification
4. Post-incident monitoring for stability

CLIENT COMMUNICATION:
- Initial notification sent: {random.randint(15, 45)} minutes after detection
- Status updates provided: Every {random.randint(30, 60)} minutes
- Resolution notification: Upon service restoration
- Follow-up communication: Within 24 hours

FINANCIAL IMPACT:
Based on SLA commitments and service credits policy:
- Estimated service credits: {random.choice(['None required', 'Under review', '$X,XXX'])}
- SLA compliance: {random.choice(['Met', 'Breach - credits applicable'])}

PREVENTIVE MEASURES:
To prevent recurrence, we are implementing:
1. Enhanced monitoring and alerting
2. Additional redundancy in affected systems
3. Improved automation for faster recovery
4. Regular testing of disaster recovery procedures

CUSTOMER SATISFACTION:
Post-incident survey results (where applicable):
- Response Time: {random.choice(['Satisfactory', 'Needs Improvement', 'Excellent'])}
- Communication Quality: {random.choice(['Satisfactory', 'Good', 'Excellent'])}
- Resolution Speed: {random.choice(['Satisfactory', 'Good', 'Excellent'])}"""
        
        else:  # compliance
            # Pre-compute values to avoid f-string bracket issues
            regulatory_checkbox_1 = random.choice(['✓', '○'])
            regulatory_checkbox_2 = random.choice(['✓', '○'])
            compliance_attestation = random.choice([
                'No material compliance violations identified', 
                'Minor control deficiency noted - remediation in progress', 
                'Full compliance maintained throughout incident'
            ])
            
            report_content = f"""COMPLIANCE INCIDENT REPORT

Report ID: RPT{str(report_id).zfill(7)}
Incident Reference: {incident['incident_number']}
Report Date: {generation_date.strftime('%Y-%m-%d')}
Classification: {incident['severity']}

REGULATORY CONTEXT:
This report has been prepared in accordance with {random.choice(['SOC 2 Type II requirements', 'ISO 27001 standards', 'GDPR Article 33', 'HIPAA breach notification rules', 'PCI-DSS incident response requirements'])}.

INCIDENT CLASSIFICATION:
Severity: {incident['severity']}
Category: {incident['category']}
Security Impact: {random.choice(['No security impact', 'Potential security implications under investigation', 'Confirmed security incident'])}
Data Breach: {random.choice(['No', 'Under Investigation', 'Yes - details in separate addendum'])}

TIMELINE OF EVENTS:
Detection: {incident['detection_time']}
Acknowledgment: {incident.get('acknowledged_at') or 'N/A'}
Containment: {random.choice(['Within 1 hour', 'Within 2 hours', 'Within 4 hours'])}
Resolution: {incident.get('resolved_at') or 'N/A'}
Closure: {incident.get('closed_at') or 'N/A'}

AFFECTED SYSTEMS:
- System Classification: {random.choice(['Production', 'Customer-Facing', 'Internal', 'Critical Infrastructure'])}
- Data Classification: {random.choice(['Public', 'Internal', 'Confidential', 'Restricted'])}
- Compliance Scope: {random.choice(['In-scope for SOC 2', 'In-scope for ISO 27001', 'In-scope for PCI-DSS'])}

DATA PROTECTION IMPACT:
Personal Data Affected: {random.choice(['None', 'Potentially - under investigation', 'Yes - details documented'])}
Data Categories: {random.choice(['N/A', 'User account information', 'Transaction records', 'System logs only'])}
Number of Records: {random.choice(['0', '<1,000', '<10,000'])}
Notification Required: {random.choice(['No', 'Under legal review', 'Yes - in progress'])}

COMPLIANCE OBLIGATIONS MET:
✓ Incident logged in compliance register
✓ Incident response team notified
✓ Senior management informed
✓ Documentation retained per policy
✓ Root cause analysis initiated
{regulatory_checkbox_1} Regulatory notification completed (if required)
{regulatory_checkbox_2} Customer notification completed (if required)

CONTROL EFFECTIVENESS:
Detection Controls: {random.choice(['Effective - detected within SLA', 'Partially effective - manual detection required'])}
Response Controls: {random.choice(['Effective - response within defined timeframe', 'Effective - all procedures followed'])}
Recovery Controls: {random.choice(['Effective - RTO/RPO met', 'Effective - systems restored per plan'])}

CORRECTIVE ACTIONS:
1. Control enhancement: {random.choice(['Monitoring threshold adjustment', 'Alert rule creation', 'Access control review'])}
2. Process improvement: {random.choice(['Runbook update', 'Training delivery', 'Procedure documentation'])}
3. Technical remediation: {random.choice(['Software patch', 'Configuration change', 'Infrastructure upgrade'])}

AUDIT TRAIL:
All actions during incident response have been logged and are available for audit review. Evidence retention period: {random.choice(['7 years', '10 years', 'Per retention policy'])}.

COMPLIANCE ATTESTATION:
This incident has been reviewed for compliance impact. {compliance_attestation}."""
        
        incident_reports[str(report_id)] = {
            "report_id": str(report_id),
            "report_number": f"RPT{str(report_id).zfill(7)}",
            "report_title": report_title,
            "incident_id": incident_id,
            "report_type": report_type,
            "report_content": report_content,
            "generated_by": random.choice(list(users.keys())),
            "generation_date": format_timestamp(generation_date),
            "report_status": random.choice(['draft', 'completed', 'approved', 'archived'])
        }
        report_id += 1
    
    return incident_reports

def generate_root_cause_analyses(incidents, users):
    """Generate RCA records following SOP 7.3"""
    root_cause_analyses = {}
    rca_id = 1
    
    # RCA analysis methods
    analysis_methods = ['5_whys', 'fishbone', 'timeline', 'fault_tree', 'kepner_tregoe']
    
    # Root cause summary templates by method
    rca_summaries = {
        '5_whys': [
            """Root Cause Analysis using 5 Whys Method:

WHY 1: Why did the {component} fail?
- {reason1}

WHY 2: Why did {reason1} occur?
- {reason2}

WHY 3: Why was {reason2} not detected earlier?
- {reason3}

WHY 4: Why were monitoring alerts not configured?
- {reason4}

WHY 5: Why was the alert configuration incomplete?
- ROOT CAUSE: {root_cause}

Corrective Actions:
1. {action1}
2. {action2}
3. {action3}""",
        ],
        'fishbone': [
            """Root Cause Analysis using Fishbone (Ishikawa) Diagram:

PROBLEM: {component} {problem_type}

PEOPLE:
- Insufficient training on {skill}
- Lack of {expertise} expertise during {time}

PROCESS:
- Inadequate {process} procedures
- Missing validation step in {workflow}

TECHNOLOGY:
- {tech_issue}
- Outdated {tech_component} version

ENVIRONMENT:
- {env_factor}
- Resource constraints during peak load

ROOT CAUSE: {root_cause}

Preventive Measures:
- {prevention1}
- {prevention2}""",
        ],
        'timeline': [
            """Root Cause Analysis - Timeline Method:

INCIDENT TIMELINE:
{start_time} - Initial symptom detected: {symptom}
{time1} - {event1}
{time2} - {event2}
{time3} - Contributing factor identified: {factor}
{time4} - Root cause confirmed: {root_cause}

CAUSAL CHAIN:
{trigger} → {intermediate1} → {intermediate2} → FAILURE

ROOT CAUSE: {root_cause}

Recommendations:
1. {recommendation1}
2. {recommendation2}""",
        ],
        'fault_tree': [
            """Root Cause Analysis - Fault Tree Analysis:

TOP EVENT: {component} Complete Failure

PRIMARY CAUSES (OR Gate):
├─ Hardware Failure (P=0.{prob1})
│  └─ {hw_cause}
├─ Software Defect (P=0.{prob2})
│  └─ {sw_cause}
└─ Configuration Error (P=0.{prob3})
   └─ {config_cause}

CRITICAL PATH IDENTIFIED:
{path}

ROOT CAUSE: {root_cause}

Risk Mitigation:
- {mitigation1}
- {mitigation2}""",
        ],
        'kepner_tregoe': [
            """Root Cause Analysis - Kepner-Tregoe Method:

SITUATION ANALYSIS:
What: {component} {problem_type}
Where: {location}
When: {when}
Extent: {extent}

IS / IS NOT Analysis:
IS: {is_condition}
IS NOT: {is_not_condition}
Distinction: {distinction}

PROBABLE CAUSE TESTING:
Hypothesis 1: {hypothesis1} - REJECTED
Hypothesis 2: {hypothesis2} - CONFIRMED

ROOT CAUSE: {root_cause}

Decision Analysis:
Action: {decision}
Expected Outcome: {outcome}""",
        ]
    }
    
    for incident_id in list(incidents.keys())[:25]:
        incident = incidents[incident_id]
        # RCAs are recent (last 30 days)
        created, updated = generate_timestamps(max_age_days=random.randint(7, 30))
        due_date_dt = datetime.fromisoformat(created) + timedelta(days=random.randint(7, 30))
        status = random.choice(['assigned', 'in_progress', 'completed', 'approved'])
        
        component = random.choice(['Application Server', 'Database', 'Load Balancer', 'Network Gateway', 'Storage System'])
        rca_title = f"RCA Report: {incident['incident_number']} - {component} Failure"
        
        # Select analysis method
        analysis_method = random.choice(analysis_methods)
        
        # Generate root_cause_summary only for completed/approved RCAs
        root_cause_summary = None
        if status in ['completed', 'approved']:
            template = random.choice(rca_summaries[analysis_method])
            
            # Fill template with realistic content
            root_cause_summary = template.format(
                component=component,
                problem_type=random.choice(['service degradation', 'complete outage', 'intermittent failures']),
                reason1=random.choice(['excessive memory consumption', 'connection pool exhaustion', 'disk space depletion']),
                reason2=random.choice(['memory leak in application code', 'unclosed database connections', 'log rotation failure']),
                reason3=random.choice(['insufficient monitoring coverage', 'alert threshold too high', 'monitoring service down']),
                reason4=random.choice(['lack of documentation', 'incomplete deployment checklist', 'missing runbook']),
                root_cause=random.choice([
                    'Inadequate resource monitoring and alerting configuration',
                    'Unhandled edge case in error recovery logic',
                    'Race condition in concurrent connection handling',
                    'Memory leak in third-party library (version 2.3.1)',
                    'Configuration drift between environments'
                ]),
                action1='Implement comprehensive monitoring for memory, connections, and disk usage',
                action2='Update deployment checklist to include resource validation',
                action3='Schedule quarterly review of monitoring alert thresholds',
                skill=random.choice(['system monitoring', 'performance tuning', 'incident response']),
                expertise=random.choice(['database optimization', 'network troubleshooting', 'capacity planning']),
                time=random.choice(['peak hours', 'weekend deployment', 'maintenance window']),
                process=random.choice(['change management', 'deployment validation', 'capacity planning']),
                workflow=random.choice(['pre-deployment testing', 'rollback procedures', 'health checks']),
                tech_issue=random.choice(['Memory leak in daemon process', 'Inefficient query execution', 'Connection timeout misconfiguration']),
                tech_component=random.choice(['operating system', 'database driver', 'load balancer']),
                env_factor=random.choice(['High CPU utilization during peak', 'Network latency spikes', 'Insufficient memory allocation']),
                prevention1='Implement automated resource monitoring with proactive alerts',
                prevention2='Conduct regular capacity planning reviews',
                start_time='09:15',
                symptom=random.choice(['high response times', 'connection timeouts', 'service errors']),
                time1='09:30',
                event1='Error rate increased to 15%',
                time2='09:45',
                event2='Memory usage reached 95%',
                time3='10:00',
                factor='Memory leak identified in background process',
                time4='10:30',
                trigger=random.choice(['Scheduled batch job started', 'Traffic spike occurred', 'Configuration change deployed']),
                intermediate1='Resource exhaustion',
                intermediate2='Service degradation',
                recommendation1='Upgrade to patched version with memory leak fix',
                recommendation2='Implement circuit breaker pattern for external dependencies',
                prob1=random.randint(15, 35),
                prob2=random.randint(40, 60),
                prob3=random.randint(10, 25),
                hw_cause='Disk I/O bottleneck under load',
                sw_cause='Unhandled exception in error recovery code',
                config_cause='Incorrect connection pool size configuration',
                path='Config Error → Pool Exhaustion → Connection Failures → Service Down',
                mitigation1='Implement connection pool monitoring and auto-scaling',
                mitigation2='Add graceful degradation for connection failures',
                location=random.choice(['Production datacenter', 'Primary region', 'All availability zones']),
                when=random.choice(['During peak traffic hours', 'After deployment', 'Weekend maintenance']),
                extent=random.choice(['30% of users affected', 'Complete service outage', 'Intermittent for 2 hours']),
                is_condition='Failures occurred on primary database connections',
                is_not_condition='Read replica connections remained stable',
                distinction='Primary database was running older driver version',
                hypothesis1='Network connectivity issue',
                hypothesis2='Driver version incompatibility causing connection leaks',
                decision='Upgrade database driver to latest stable version',
                outcome='Eliminate connection leak and improve stability'
            )
        
        # SOP 7.3: RCAs conducted by incident_manager or technical_support
        rca_conductor = random.choice(get_users_by_role(users, 'incident_manager') + get_users_by_role(users, 'technical_support'))
        # Approved by executives (SOP)
        approved_by_user = random.choice(get_users_by_role(users, 'executive')) if status == 'approved' and get_users_by_role(users, 'executive') else None
        
        root_cause_analyses[str(rca_id)] = {
            "rca_id": str(rca_id),
            "rca_number": f"RCA{str(rca_id).zfill(7)}",
            "rca_title": rca_title,
            "incident_id": incident_id,
            "assigned_to": rca_conductor,
            "status": status,
            "analysis_method": analysis_method,
            "root_cause_summary": root_cause_summary,
            "due_date": format_timestamp(due_date_dt),
            "completed_at": format_timestamp(datetime.fromisoformat(created) + timedelta(days=random.randint(3, 21))) if status in ['completed', 'approved'] else None,
            "approved_by": approved_by_user,
            "created_at": created,
            "updated_at": updated
        }
        rca_id += 1
    
    return root_cause_analyses

def generate_post_incident_reviews(incidents, users):
    """Generate PIR records following SOP 7.4"""
    post_incident_reviews = {}
    review_id = 1
    
    for incident_id in list(incidents.keys())[:20]:
        # PIR scheduled after incident is closed (P1/P2 only)
        incident = incidents[incident_id]
        incident_closed = datetime.fromisoformat(incident.get('closed_at') or incident['updated_at'])
        created = generate_timestamp(incident_closed, incident_closed + timedelta(days=random.randint(1, 3)))
        scheduled_date = created + timedelta(days=random.randint(3, 14))
        status = random.choice(['scheduled', 'completed', 'cancelled'])
        
        # Generate realistic content for completed PIRs
        if status == 'completed':
            severity = incident.get('severity', 'P3')
            
            # Review notes
            review_notes = f"""Post-Incident Review - {incident['incident_number']}

Attendees: Incident Manager, Technical Leads, Account Manager, {random.randint(3, 8)} team members
Duration: {random.randint(45, 90)} minutes

Timeline Review:
- Detection: {incident.get('detection_time', 'N/A')[:16]}
- Acknowledged: {incident.get('acknowledged_at', 'N/A')[:16] if incident.get('acknowledged_at') else 'N/A'}
- Resolved: {incident.get('resolved_at', 'N/A')[:16] if incident.get('resolved_at') else 'N/A'}
- Total Duration: {random.randint(2, 48)} hours

Key Discussion Points:
1. Initial response effectiveness
2. Communication clarity during incident
3. Escalation procedures followed
4. Technical resolution approach
5. Customer impact mitigation

Team Performance: {random.choice(['Excellent coordination', 'Good response time', 'Room for improvement in communication', 'Effective collaboration'])}"""

            # Lessons learned
            lessons_templates = [
                f"Early detection systems proved effective. {random.choice(['Monitoring alerts', 'Automated checks', 'User reports'])} identified the issue within {random.randint(5, 30)} minutes.",
                f"Communication protocols worked well. Status updates were provided every {random.randint(15, 60)} minutes to stakeholders.",
                f"Escalation to {random.choice(['executive level', 'technical experts', 'vendor support'])} could have been faster. Consider lowering escalation thresholds for {severity} incidents.",
                f"Documentation was {random.choice(['comprehensive', 'adequate', 'incomplete'])}. {random.choice(['Continue current practices', 'Need better real-time documentation', 'Implement structured templates'])}.",
                f"Cross-team collaboration was {random.choice(['seamless', 'effective', 'challenging'])}. {random.choice(['Bridge calls', 'Slack channels', 'Email threads'])} facilitated coordination.",
                f"Root cause analysis completed within SLA. {random.choice(['Technical investigation', 'Log analysis', 'System diagnostics'])} identified the underlying issue.",
                f"Customer communication was {random.choice(['timely', 'delayed', 'proactive'])}. Consider implementing automated status page updates.",
                f"Post-incident procedures followed as documented. Recovery time met expectations for {severity} severity."
            ]
            
            lessons_learned = "\n".join([f"• {random.choice(lessons_templates)}" for _ in range(random.randint(4, 6))])
            
            # Action items
            action_templates = [
                f"Update runbook for {random.choice(['database failover', 'network recovery', 'service restart', 'cache invalidation'])} procedures - Assigned to: Tech Lead - Due: {random.randint(7, 30)} days",
                f"Implement additional monitoring for {random.choice(['memory usage', 'connection pools', 'API latency', 'disk space'])} - Assigned to: DevOps - Due: {random.randint(14, 45)} days",
                f"Review and update escalation thresholds for {severity} incidents - Assigned to: Incident Manager - Due: {random.randint(7, 21)} days",
                f"Conduct training session on {random.choice(['incident response', 'bridge call protocols', 'communication templates', 'RCA techniques'])} - Assigned to: Training Team - Due: {random.randint(30, 60)} days",
                f"Enhance customer communication templates for {severity} severity - Assigned to: Account Management - Due: {random.randint(14, 30)} days",
                f"Implement automated {random.choice(['health checks', 'alerting rules', 'backup verification', 'capacity monitoring'])} - Assigned to: Engineering - Due: {random.randint(21, 60)} days",
                f"Schedule vendor review meeting to discuss {random.choice(['SLA compliance', 'support responsiveness', 'escalation procedures'])} - Assigned to: Vendor Manager - Due: {random.randint(7, 14)} days",
                f"Update disaster recovery documentation - Assigned to: Architecture Team - Due: {random.randint(30, 90)} days"
            ]
            
            action_items = "\n".join([f"{i+1}. {random.choice(action_templates)}" for i in range(random.randint(3, 6))])
        else:
            # For scheduled/cancelled, leave fields empty or minimal
            review_notes = "" if status == 'scheduled' else "Review cancelled - incident reclassified as non-critical"
            lessons_learned = ""
            action_items = ""
        
        post_incident_reviews[str(review_id)] = {
            "review_id": str(review_id),
            "incident_id": incident_id,
            "scheduled_date": format_timestamp(scheduled_date),
            "facilitator": random.choice(list(users.keys())),
            "review_notes": review_notes,
            "lessons_learned": lessons_learned,
            "action_items": action_items,
            "status": status,
            "created_at": format_timestamp(created)
        }
        review_id += 1
    
    return post_incident_reviews

def generate_audit_trails(users, clients, vendors, subscriptions, sla_agreements, products, 
                          configuration_items, incidents, escalations, bridges, change_requests, 
                          rollback_requests, work_orders, n=200):
    """
    Generate audit trail records with valid reference_id and field_name values.
    Each audit trail must:
    1. Reference an existing entity (valid reference_id)
    2. Use a field name that exists in that entity's schema
    3. Have created_at >= parent entity's created_at
    """
    audit_trails = {}
    
    # Map reference types to their data collections and valid field names (based on actual schema)
    entity_mapping = {
        'user': {
            'collection': users,
            'fields': ['status', 'role', 'email', 'timezone']  # Valid user fields
        },
        'client': {
            'collection': clients,
            'fields': ['status', 'company_type', 'support_coverage', 'preferred_communication', 'contact_email']
        },
        'vendor': {
            'collection': vendors,
            'fields': ['status', 'contact_email', 'contact_phone']
        },
        'subscription': {
            'collection': subscriptions,
            'fields': ['status', 'tier', 'start_date', 'end_date']
        },
        'sla': {
            'collection': sla_agreements,
            'fields': ['severity_level', 'response_time_minutes', 'resolution_time_minutes', 'availability_guarantee']
        },
        'product': {
            'collection': products,
            'fields': ['status', 'product_name', 'description']
        },
        'ci': {
            'collection': configuration_items,
            'fields': ['operational_status', 'ci_type', 'environment', 'location']
        },
        'incident': {
            'collection': incidents,
            'fields': ['status', 'severity', 'impact', 'urgency', 'assigned_to', 'description', 'title', 'category']
        },
        'escalation': {
            'collection': escalations,
            'fields': ['status', 'escalation_level', 'escalation_reason']
        },
        'bridge': {
            'collection': bridges,
            'fields': ['status', 'bridge_type', 'bridge_host']
        },
        'change': {
            'collection': change_requests,
            'fields': ['status', 'risk_level', 'change_type', 'description']
        },
        'rollback': {
            'collection': rollback_requests,
            'fields': ['status', 'rollback_reason', 'title']
        },
        'work_order': {
            'collection': work_orders,
            'fields': ['status', 'assigned_to', 'description', 'title']
        }
    }
    
    # Generate audit trails
    audit_id = 1
    for ref_type, config in entity_mapping.items():
        collection = config['collection']
        valid_fields = config['fields']
        
        if not collection:
            continue
        
        # Generate multiple audit records for this entity type
        num_audits = min(n // len(entity_mapping), len(collection) * 2)  # At most 2 audits per entity
        
        for _ in range(num_audits):
            if audit_id > n:
                break
            
            # Pick a random entity from this collection
            entity_id = random.choice(list(collection.keys()))
            entity = collection[entity_id]
            
            # Get parent created_at to ensure audit is after it
            parent_created_at = entity.get('created_at')
            if parent_created_at:
                if isinstance(parent_created_at, str):
                    parent_created_dt = datetime.fromisoformat(parent_created_at)
                else:
                    parent_created_dt = parent_created_at
                
                # Audit must happen after parent creation
                audit_created = generate_timestamp(parent_created_dt, REFERENCE_DATE)
            else:
                # Fallback if no created_at (recent audit trail)
                audit_created = generate_timestamp(REFERENCE_DATE - timedelta(days=60), REFERENCE_DATE)
            
            # Pick a valid field name for this entity type
            field_name = random.choice(valid_fields)
            
            # Generate realistic old/new values based on field type
            if 'status' in field_name:
                old_value = random.choice(['pending', 'active', 'open'])
                new_value = random.choice(['approved', 'completed', 'closed'])
            elif field_name in ['email', 'contact_email']:
                old_value = fake.email()
                new_value = fake.email()
            elif 'time' in field_name.lower() or 'date' in field_name.lower():
                old_value = str(random.randint(10, 100))
                new_value = str(random.randint(10, 100))
            elif 'assigned_to' in field_name or 'host' in field_name:
                old_value = str(random.randint(1, 50))
                new_value = str(random.randint(1, 50))
            else:
                old_value = fake.word()
                new_value = fake.word()
            
            audit_trails[str(audit_id)] = {
                "audit_id": str(audit_id),
                "reference_id": entity_id,
                "reference_type": ref_type,
                "action": random.choice(['create', 'update', 'update', 'update']),  # 75% update, 25% create
                "user_id": random.choice(list(users.keys())),
                "field_name": field_name,
                "old_value": old_value if audit_trails.get(str(audit_id - 1), {}).get('action') != 'create' else None,
                "new_value": new_value,
                "created_at": format_timestamp(audit_created)
            }
            audit_id += 1
            
            if audit_id > n:
                break
    
    return audit_trails

def fix_audit_trail_values(audit_trails):
    """
    Post-process audit trails to fix old_value and new_value to be realistic.
    This function is called AFTER all data generation to avoid affecting random seed sequence.
    """
    # Use a completely separate random generator for fixing values
    import random as fix_random
    fix_rng = fix_random.Random(99)  # Different seed to not interfere
    
    # Map field names to valid values
    field_value_map = {
        'status': ['pending', 'active', 'open', 'in_progress', 'resolved', 'closed', 'approved', 'rejected'],
        'severity': ['P1', 'P2', 'P3', 'P4'],
        'impact': ['low', 'medium', 'high', 'critical'],
        'urgency': ['low', 'medium', 'high', 'critical'],
        'priority': ['P1', 'P2', 'P3', 'P4'],
        'role': ['technical_support', 'incident_manager', 'account_manager', 'executive', 'system_administrator', 'client_contact'],
        'tier': ['basic', 'standard', 'premium'],
        'operational_status': ['operational', 'degraded', 'offline', 'maintenance'],
        'ci_type': ['server', 'database', 'application', 'network'],
        'environment': ['production', 'staging', 'development', 'test'],
        'category': ['inquiry/help', 'software', 'hardware', 'Network', 'Database'],
        'escalation_level': ['L1', 'L2', 'L3', 'management'],
        'risk_level': ['low', 'medium', 'high', 'critical'],
        'change_type': ['standard', 'emergency', 'major', 'minor'],
        'company_type': ['enterprise', 'smb', 'startup'],
        'support_coverage': ['24/7', 'business_hours', 'extended_hours'],
        'preferred_communication': ['email', 'phone', 'chat', 'portal'],
        'timezone': ['UTC', 'America/New_York', 'America/Los_Angeles', 'Europe/London', 'Asia/Tokyo'],
        'bridge_type': ['war_room', 'status_update', 'customer_briefing', 'post_mortem'],
        'escalation_reason': ['SLA breach', 'Critical severity', 'Customer request', 'Complexity requires expertise', 'Multiple failures']
    }
    
    print(f"   Fixing {len(audit_trails)} audit trail values to be realistic...")
    
    for audit_id, audit in audit_trails.items():
        field_name = audit['field_name']
        action = audit['action']
        
        # Generate realistic values based on field type
        if field_name in field_value_map:
            # Use predefined valid values
            valid_values = field_value_map[field_name]
            new_value = fix_rng.choice(valid_values)
            if action != 'create':
                old_value = fix_rng.choice([v for v in valid_values if v != new_value] or valid_values)
            else:
                old_value = None
        elif 'time' in field_name.lower() and 'minutes' in field_name.lower():
            # Time in minutes
            new_value = str(fix_rng.choice([15, 30, 60, 120, 240, 480, 1440]))
            old_value = str(fix_rng.choice([15, 30, 60, 120, 240, 480, 1440])) if action != 'create' else None
        elif 'assigned_to' in field_name or 'host' in field_name or field_name.endswith('_by'):
            # User IDs
            new_value = str(fix_rng.randint(1, 100))
            old_value = str(fix_rng.randint(1, 100)) if action != 'create' else None
        elif 'availability_guarantee' in field_name:
            # Percentage
            new_value = str(fix_rng.choice([99.0, 99.5, 99.9, 99.95, 99.99]))
            old_value = str(fix_rng.choice([99.0, 99.5, 99.9, 99.95, 99.99])) if action != 'create' else None
        else:
            # Keep original values for fields we don't have mappings for
            continue
        
        # Update the audit trail with fixed values
        audit['old_value'] = old_value
        audit['new_value'] = new_value
    
    return audit_trails

def fix_sla_values(sla_agreements, subscriptions):
    """
    Post-process SLA agreements to set correct response/resolution times and availability.
    This function is called AFTER all data generation to avoid affecting random seed sequence.
    """
    # Use a completely separate random generator
    import random as fix_random
    fix_rng = fix_random.Random(88)  # Different seed
    
    print(f"   Fixing {len(sla_agreements)} SLA agreements with correct ranges...")
    
    for sla_id, sla in sla_agreements.items():
        sub_id = sla['subscription_id']
        subscription = subscriptions.get(sub_id, {})
        tier = subscription.get('tier', 'standard')
        severity = sla['severity_level']
        
        # Get ranges for this tier/severity
        if tier in SLA_MATRIX and severity in SLA_MATRIX[tier]:
            sla_config = SLA_MATRIX[tier][severity]
            response_min, response_max = sla_config['response']
            resolution_min, resolution_max = sla_config['resolution']
            
            # Generate random values within ranges
            sla['response_time_minutes'] = fix_rng.randint(response_min, response_max)
            sla['resolution_time_minutes'] = fix_rng.randint(resolution_min, resolution_max)
            sla['availability_guarantee'] = AVAILABILITY_GUARANTEE.get(tier, 99.0)
    
    return sla_agreements

def clean_orphaned_attachments(attachments, incidents, change_requests, root_cause_analyses, 
                               incident_reports, post_incident_reviews, communications, 
                               work_orders, problem_tickets):
    """
    Remove attachments that reference non-existent entities.
    This ensures data integrity after generation.
    """
    # Map reference types to their collections
    reference_collections = {
        'incident': incidents,
        'change': change_requests,
        'rca': root_cause_analyses,
        'report': incident_reports,
        'pir': post_incident_reviews,
        'communication': communications,
        'work_order': work_orders,
        'problem': problem_tickets
    }
    
    print(f"   Validating {len(attachments)} attachments for orphaned references...")
    
    valid_attachments = {}
    orphaned_count = 0
    
    for att_id, attachment in attachments.items():
        ref_type = attachment['reference_type']
        ref_id = attachment['reference_id']
        
        # Check if reference exists
        collection = reference_collections.get(ref_type, {})
        if ref_id in collection:
            valid_attachments[att_id] = attachment
        else:
            orphaned_count += 1
            # print(f"   ⚠️  Removing orphaned attachment {att_id}: {ref_type}/{ref_id} not found")
    
    if orphaned_count > 0:
        print(f"   ✅ Removed {orphaned_count} orphaned attachments")
    else:
        print(f"   ✅ No orphaned attachments found")
    
    return valid_attachments

def save_to_json(data, filename, output_dir='data'):
    """Save data to JSON file in specified directory"""
    import os
    
    # Create data directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Save to data/ directory
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"  ✅ {filename}: {len(data)} records")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def generate_realistic_filename(reference_type):
    """Generate realistic file names based on reference type"""
    extensions = {
        'incident': ['.log', '.txt', '.csv', '.xlsx', '.pdf'],
        'change': ['.pdf', '.docx', '.xlsx', '.zip'],
        'rca': ['.pdf', '.docx', '.pptx', '.xlsx'],
        'report': ['.pdf', '.xlsx', '.docx', '.html'],
        'pir': ['.pdf', '.docx', '.pptx'],
        'communication': ['.pdf', '.eml', '.msg', '.txt'],
        'work_order': ['.pdf', '.docx', '.xlsx'],
        'problem': ['.log', '.txt', '.pdf', '.docx']
    }
    
    templates = {
        'incident': [
            'error_log_{id}', 'stack_trace_{id}', 'system_metrics_{id}', 
            'incident_screenshot_{id}', 'diagnostic_report_{id}'
        ],
        'change': [
            'change_plan_{id}', 'rollback_procedure_{id}', 'test_results_{id}',
            'approval_form_{id}', 'implementation_guide_{id}'
        ],
        'rca': [
            'root_cause_analysis_{id}', 'fishbone_diagram_{id}', '5_whys_{id}',
            'timeline_analysis_{id}', 'fault_tree_{id}'
        ],
        'report': [
            'incident_report_{id}', 'impact_assessment_{id}', 'compliance_report_{id}',
            'executive_summary_{id}'
        ],
        'pir': [
            'pir_meeting_notes_{id}', 'lessons_learned_{id}', 'action_items_{id}',
            'pir_presentation_{id}'
        ],
        'communication': [
            'client_notification_{id}', 'status_update_{id}', 'escalation_email_{id}',
            'resolution_notice_{id}'
        ],
        'work_order': [
            'work_order_{id}', 'completion_certificate_{id}', 'maintenance_log_{id}'
        ],
        'problem': [
            'problem_investigation_{id}', 'workaround_doc_{id}', 'affected_systems_{id}'
        ]
    }
    
    template = random.choice(templates.get(reference_type, ['file_{id}']))
    ext = random.choice(extensions.get(reference_type, ['.pdf']))
    
    # Generate unique identifier
    unique_id = f"{random.randint(1000, 9999)}"
    filename = template.replace('{id}', unique_id) + ext
    
    return filename

def generate_attachments(incidents, change_requests, root_cause_analyses, incident_reports,
                        post_incident_reviews, communications, work_orders, problem_tickets, users):
    """
    Generate attachments for various reference types
    Attachments can reference: incident, change, rca, report, pir, communication, work_order, problem
    """
    # Map reference types to their collections
    reference_collections = {
        'incident': incidents,
        'change': change_requests,
        'rca': root_cause_analyses,
        'report': incident_reports,
        'pir': post_incident_reviews,
        'communication': communications,
        'work_order': work_orders,
        'problem': problem_tickets
    }
    
    # Generate attachments
    attachments = {}
    attachment_id = 1
    
    # Configuration: how many attachments per entity (average)
    attachments_config = {
        'incident': (2, 4),      # 2-4 attachments per incident
        'change': (3, 5),        # 3-5 attachments per change
        'rca': (2, 4),           # 2-4 attachments per RCA
        'report': (1, 3),        # 1-3 attachments per report
        'pir': (2, 3),           # 2-3 attachments per PIR
        'communication': (1, 2), # 1-2 attachments per communication (30%)
        'work_order': (1, 3),    # 1-3 attachments per work order (50%)
        'problem': (1, 3),       # 1-3 attachments per problem
    }
    
    print("\n" + "="*80)
    print("📎 GENERATING ATTACHMENTS")
    print("="*80 + "\n")
    
    for ref_type, collection in reference_collections.items():
        min_att, max_att = attachments_config.get(ref_type, (1, 2))
        
        # For some types, not all entities have attachments
        if ref_type == 'communication':
            # Only 30% of communications have attachments
            entities_with_attachments = random.sample(list(collection.keys()), 
                                                     k=int(len(collection) * 0.3))
        elif ref_type == 'work_order':
            # Only 50% of work orders have attachments
            entities_with_attachments = random.sample(list(collection.keys()), 
                                                     k=int(len(collection) * 0.5))
        else:
            # All other entities have attachments
            entities_with_attachments = list(collection.keys())
        
        for entity_id in entities_with_attachments:
            entity = collection[entity_id]
            num_attachments = random.randint(min_att, max_att)
            
            for _ in range(num_attachments):
                # Get entity's created_at for timestamp
                entity_created_at_str = entity.get('created_at', '2024-01-01T00:00:00')
                entity_created_at = datetime.fromisoformat(entity_created_at_str) if isinstance(entity_created_at_str, str) else entity_created_at_str
                
                uploaded_at = generate_timestamp(entity_created_at, REFERENCE_DATE)
                
                # Generate realistic filename
                file_name = generate_realistic_filename(ref_type)
                file_size_bytes = random.randint(1024, 10485760)  # 1KB to 10MB
                
                # Determine file type based on extension
                from pathlib import Path
                ext = Path(file_name).suffix
                file_type_map = {
                    '.pdf': 'pdf',
                    '.docx': 'docx',
                    '.xlsx': 'xlsx',
                    '.pptx': 'pptx',
                    '.log': 'log',
                    '.txt': 'txt',
                    '.csv': 'csv',
                    '.zip': 'zip',
                    '.eml': 'eml',
                    '.msg': 'msg',
                    '.html': 'html'
                }
                file_type = file_type_map.get(ext, 'unknown')
                
                # Generate realistic S3-style file URL
                bucket_name = 'incident-mgmt-attachments'
                date_path = uploaded_at.strftime('%Y/%m/%d')
                file_url = f"https://s3.amazonaws.com/{bucket_name}/{date_path}/{ref_type}/{entity_id}/{file_name}"
                
                # Use integer attachment_id (schema compliant)
                attachments[str(attachment_id)] = {
                    "attachment_id": str(attachment_id),
                    "reference_id": entity_id,
                    "reference_type": ref_type,
                    "file_name": file_name,
                    "file_url": file_url,
                    "file_type": file_type,
                    "file_size_bytes": file_size_bytes,
                    "uploaded_by": random.choice(list(users.keys())),
                    "uploaded_at": uploaded_at.isoformat()
                }
                
                attachment_id += 1
        
        print(f"  ✅ {ref_type}: {len([a for a in attachments.values() if a['reference_type'] == ref_type])} attachments")
    
    print("\n" + "="*80)
    print(f"✅ TOTAL: Generated {len(attachments)} attachments")
    print("="*80 + "\n")
    
    return attachments

def main():
    import sys
    import os
    import glob
    from pathlib import Path
    
    # Always use local data/ directory (relative to this script)
    script_dir = Path(__file__).parent
    output_dir = script_dir / 'data'
    output_dir.mkdir(exist_ok=True)  # Create data/ if doesn't exist
    output_dir = str(output_dir)
    
    print("\n" + "="*80)
    print("🎯 INCIDENT MANAGEMENT SEED DATA GENERATOR")
    print("="*80)
    print(f"\n📂 Output directory: {output_dir}")
    
    # Clean existing JSON files
    print("\n🗑️  Cleaning existing JSON files...")
    json_files = glob.glob(os.path.join(output_dir, "*.json"))
    if json_files:
        for json_file in json_files:
            os.remove(json_file)
        print(f"   Deleted {len(json_files)} existing JSON files")
    else:
        print("   No existing files to delete")
    
    print("\n📋 Generating data with business rules from SOP...")
    
    # Generate in dependency order
    print("\n1. Base entities...")
    vendors = generate_vendors(8)
    clients = generate_clients(25)  # Increased from 15 to 25
    users = generate_users(len(clients), len(vendors))  # Now generates 150 users
    products = generate_products(15)  # Increased from 6 to 15
    configuration_items = generate_configuration_items(products)
    
    print("\n2. Subscriptions and SLAs...")
    subscriptions = generate_subscriptions(clients)
    sla_agreements = generate_sla_agreements(subscriptions, users)
    
    print("\n3. Problem Tickets and Incidents...")
    problem_tickets = generate_problem_tickets(clients, users, 20)  # Increased from 15 to 20
    incidents = generate_incidents(clients, configuration_items, users, subscriptions, problem_tickets, 100)
    
    print("\n4. Incident support...")
    work_notes = generate_work_notes(incidents, users)
    escalations = generate_escalations(incidents, users)
    bridges = generate_bridges(incidents, users)
    bridge_participants = generate_bridge_participants(bridges, users)
    
    print("\n5. Change management...")
    change_requests = generate_change_requests(incidents, users)
    rollback_requests = generate_rollback_requests(change_requests, incidents, users)
    work_orders = generate_work_orders(change_requests, incidents, users)
    
    print("\n6. Approvals and communications...")
    approval_requests = generate_approval_requests(escalations, bridges, change_requests, 
                                                   rollback_requests, users, incidents)
    communications = generate_communications(incidents, users)
    
    print("\n7. Metrics and reporting...")
    performance_metrics = generate_performance_metrics(incidents, users)
    incident_reports = generate_incident_reports(incidents, users)
    root_cause_analyses = generate_root_cause_analyses(incidents, users)
    post_incident_reviews = generate_post_incident_reviews(incidents, users)
    audit_trails = generate_audit_trails(users, clients, vendors, subscriptions, sla_agreements, products, 
                                         configuration_items, incidents, escalations, bridges, change_requests, 
                                         rollback_requests, work_orders, 200)
    
    print("\n8. Attachments...")
    attachments = generate_attachments(incidents, change_requests, root_cause_analyses, incident_reports,
                                      post_incident_reviews, communications, work_orders, problem_tickets, users)
    
    # Post-process data (doesn't affect random sequence since it's after generation)
    print("\n" + "="*80)
    print("🔧 POST-PROCESSING")
    print("="*80 + "\n")
    sla_agreements = fix_sla_values(sla_agreements, subscriptions)
    audit_trails = fix_audit_trail_values(audit_trails)
    attachments = clean_orphaned_attachments(attachments, incidents, change_requests, root_cause_analyses,
                                            incident_reports, post_incident_reviews, communications,
                                            work_orders, problem_tickets)
    
    # Save all data
    print("\n" + "="*80)
    print("💾 SAVING TO JSON FILES")
    print("="*80 + "\n")
    
    save_to_json(vendors, 'vendors.json', output_dir)
    save_to_json(clients, 'clients.json', output_dir)
    save_to_json(users, 'users.json', output_dir)
    save_to_json(products, 'products.json', output_dir)
    save_to_json(configuration_items, 'configuration_items.json', output_dir)
    save_to_json(subscriptions, 'subscriptions.json', output_dir)
    save_to_json(sla_agreements, 'sla_agreements.json', output_dir)
    save_to_json(problem_tickets, 'problem_tickets.json', output_dir)
    save_to_json(incidents, 'incidents.json', output_dir)
    save_to_json(work_notes, 'work_notes.json', output_dir)
    save_to_json(attachments, 'attachments.json', output_dir)
    save_to_json(escalations, 'escalations.json', output_dir)
    save_to_json(bridges, 'bridges.json', output_dir)
    save_to_json(bridge_participants, 'bridge_participants.json', output_dir)
    save_to_json(change_requests, 'change_requests.json', output_dir)
    save_to_json(rollback_requests, 'rollback_requests.json', output_dir)
    save_to_json(work_orders, 'work_orders.json', output_dir)
    save_to_json(approval_requests, 'approval_requests.json', output_dir)
    save_to_json(communications, 'communications.json', output_dir)
    save_to_json(performance_metrics, 'performance_metrics.json', output_dir)
    save_to_json(incident_reports, 'incident_reports.json', output_dir)
    save_to_json(root_cause_analyses, 'root_cause_analyses.json', output_dir)
    save_to_json(post_incident_reviews, 'post_incident_reviews.json', output_dir)
    save_to_json(audit_trails, 'audit_trails.json', output_dir)
    
    print("\n" + "="*80)
    print("✅ DATA GENERATION COMPLETE!")
    print("="*80)
    total_records = (len(configuration_items) + len(clients) + len(users) + len(subscriptions) + 
                     len(sla_agreements) + len(products) + len(problem_tickets) + len(incidents) + 
                     len(work_notes) + len(attachments) + len(escalations) + len(bridges) + 
                     len(bridge_participants) + len(change_requests) + len(rollback_requests) + 
                     len(work_orders) + len(approval_requests) + len(communications) + 
                     len(performance_metrics) + len(incident_reports) + len(root_cause_analyses) + 
                     len(post_incident_reviews) + len(audit_trails) + len(vendors))
    
    print(f"\n📊 Summary: Generated {total_records:,} total records across 25 tables")
    print(f"   All business rules and data generation completed!\n")

if __name__ == "__main__":
    main()

