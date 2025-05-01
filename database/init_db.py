from utils.decorators import print_log
from database.connection import get_db_connection

@print_log()
def init_db():
    """初始化数据库表结构"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 创建产品基本信息表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sku_id TEXT UNIQUE NOT NULL,
        product_type TEXT NOT NULL,
        category TEXT NOT NULL,
        product_name TEXT NOT NULL,
        short_description TEXT,
        long_description TEXT,
        key_selling_points TEXT,  -- JSON格式存储
        base_price REAL,
        currency TEXT DEFAULT 'CNY',
        pricing_model TEXT,
        pricing_details TEXT,  -- JSON格式存储
        applicable_industry TEXT,  -- JSON格式存储
        applicable_scale TEXT,
        delivery_lead_time TEXT,
        supported_channels TEXT,  -- JSON格式存储
        status TEXT DEFAULT 'Draft',
        media_assets TEXT,  -- JSON格式存储
        keywords TEXT,  -- JSON格式存储
        related_skus TEXT,  -- JSON格式存储
        effective_date TEXT,
        expiry_date TEXT,
        internal_notes TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT
    )
    ''')
    
    # 创建数字化服务扩展信息表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS digital_service_details (
        sku_id TEXT PRIMARY KEY,
        deployment_model TEXT,
        supported_terminals TEXT,  -- JSON格式存储
        feature_list TEXT,  -- JSON格式存储
        integration_capabilities TEXT,  -- JSON格式存储
        license_model TEXT,
        service_level_agreement TEXT,  -- JSON格式存储
        version_info TEXT,
        deliverables TEXT,  -- JSON格式存储
        support_hours TEXT,
        FOREIGN KEY (sku_id) REFERENCES products (sku_id) ON DELETE CASCADE
    )
    ''')
    
    # 创建现场执行服务扩展信息表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS field_service_details (
        sku_id TEXT PRIMARY KEY,
        service_scope TEXT,
        service_delivery_method TEXT,
        geographic_coverage TEXT,
        service_frequency TEXT,
        service_time_window TEXT,
        service_content_items TEXT,  -- JSON格式存储
        technician_qualifications TEXT,  -- JSON格式存储
        team_configuration TEXT,
        response_time_sla TEXT,
        resolution_time_sla TEXT,
        safety_standards TEXT,
        historical_cases TEXT,  -- JSON格式存储
        required_client_input TEXT,
        requires_site_survey INTEGER DEFAULT 0,  -- 布尔值
        deliverables TEXT,  -- JSON格式存储
        support_hours TEXT,
        FOREIGN KEY (sku_id) REFERENCES products (sku_id) ON DELETE CASCADE
    )
    ''')
    
    # 创建软硬一体产品扩展信息表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS physical_good_details (
        sku_id TEXT PRIMARY KEY,
        hardware_model TEXT,
        dimensions TEXT,  -- JSON格式存储
        weight TEXT,  -- JSON格式存储
        material TEXT,
        technical_specifications TEXT,  -- JSON格式存储
        software_features TEXT,  -- JSON格式存储
        connectivity TEXT,  -- JSON格式存储
        data_frequency TEXT,
        operating_environment TEXT,
        certifications TEXT,  -- JSON格式存储
        warranty_period TEXT,
        maintenance_requirements TEXT,
        requires_software_subscription INTEGER DEFAULT 0,  -- 布尔值
        installation_required INTEGER DEFAULT 0,  -- 布尔值
        installation_guide_url TEXT,
        associated_software_sku TEXT,
        associated_service_sku TEXT,
        FOREIGN KEY (sku_id) REFERENCES products (sku_id) ON DELETE CASCADE
    )
    ''')
    
    # 创建培训课程扩展信息表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS training_details (
        sku_id TEXT PRIMARY KEY,
        course_format TEXT,
        duration TEXT,
        location TEXT,
        course_outline TEXT,  -- JSON格式存储
        learning_objectives TEXT,  -- JSON格式存储
        instructor_info TEXT,  -- JSON格式存储
        certification_included INTEGER DEFAULT 0,  -- 布尔值
        certification_type TEXT,
        certification_body TEXT,
        schedule_details TEXT,  -- JSON格式存储
        prerequisites TEXT,
        max_class_size INTEGER,
        provided_materials TEXT,
        FOREIGN KEY (sku_id) REFERENCES products (sku_id) ON DELETE CASCADE
    )
    ''')
    
    # 创建组合套餐扩展信息表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bundle_details (
        sku_id TEXT PRIMARY KEY,
        included_items TEXT,  -- JSON格式存储
        bundle_savings TEXT,
        customization_support TEXT,
        overall_sla TEXT,
        validity_period TEXT,
        renewal_terms TEXT,
        FOREIGN KEY (sku_id) REFERENCES products (sku_id) ON DELETE CASCADE
    )
    ''')
    
    conn.commit()
    conn.close() 