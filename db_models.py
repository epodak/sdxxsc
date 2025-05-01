import os
import sqlite3
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from utils.decorators import print_log

# 数据库连接
@print_log()
def get_db_connection():
    """获取数据库连接"""
    # 确保data目录存在
    os.makedirs('data', exist_ok=True)
    
    # 连接数据库
    conn = sqlite3.connect('data/products.db')
    conn.row_factory = sqlite3.Row
    return conn

# 初始化数据库
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

# 产品类
@print_log()
class Product:
    """产品基本信息类"""
    
    def __init__(self, data: Dict[str, Any] = None):
        self.id = None
        self.sku_id = ""
        self.product_type = ""
        self.category = ""
        self.product_name = ""
        self.short_description = ""
        self.long_description = ""
        self.key_selling_points = []
        self.base_price = 0.0
        self.currency = "CNY"
        self.pricing_model = ""
        self.pricing_details = {}
        self.applicable_industry = []
        self.applicable_scale = ""
        self.delivery_lead_time = ""
        self.supported_channels = []
        self.status = "Draft"
        self.media_assets = []
        self.keywords = []
        self.related_skus = []
        self.effective_date = ""
        self.expiry_date = ""
        self.internal_notes = ""
        self.created_at = ""
        self.updated_at = ""
        
        # 如果提供了数据，填充对象
        if data:
            self.__dict__.update(data)
    
    def to_dict(self) -> Dict[str, Any]:
        """将对象转换为字典"""
        return self.__dict__
    
    def save(self) -> int:
        """保存产品到数据库"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 准备JSON字段
        key_selling_points = json.dumps(self.key_selling_points, ensure_ascii=False)
        pricing_details = json.dumps(self.pricing_details, ensure_ascii=False)
        applicable_industry = json.dumps(self.applicable_industry, ensure_ascii=False)
        supported_channels = json.dumps(self.supported_channels, ensure_ascii=False)
        media_assets = json.dumps(self.media_assets, ensure_ascii=False)
        keywords = json.dumps(self.keywords, ensure_ascii=False)
        related_skus = json.dumps(self.related_skus, ensure_ascii=False)
        
        # 更新时间
        current_time = datetime.now().isoformat()
        
        if self.id:  # 更新现有产品
            cursor.execute('''
            UPDATE products SET 
                product_type = ?, category = ?, product_name = ?, short_description = ?, 
                long_description = ?, key_selling_points = ?, base_price = ?, currency = ?, 
                pricing_model = ?, pricing_details = ?, applicable_industry = ?, 
                applicable_scale = ?, delivery_lead_time = ?, supported_channels = ?, 
                status = ?, media_assets = ?, keywords = ?, related_skus = ?, 
                effective_date = ?, expiry_date = ?, internal_notes = ?, updated_at = ?
            WHERE id = ?
            ''', (
                self.product_type, self.category, self.product_name, self.short_description,
                self.long_description, key_selling_points, self.base_price, self.currency,
                self.pricing_model, pricing_details, applicable_industry,
                self.applicable_scale, self.delivery_lead_time, supported_channels,
                self.status, media_assets, keywords, related_skus,
                self.effective_date, self.expiry_date, self.internal_notes, current_time,
                self.id
            ))
        else:  # 创建新产品
            cursor.execute('''
            INSERT INTO products (
                sku_id, product_type, category, product_name, short_description, 
                long_description, key_selling_points, base_price, currency, 
                pricing_model, pricing_details, applicable_industry, 
                applicable_scale, delivery_lead_time, supported_channels, 
                status, media_assets, keywords, related_skus, 
                effective_date, expiry_date, internal_notes, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.sku_id, self.product_type, self.category, self.product_name, self.short_description,
                self.long_description, key_selling_points, self.base_price, self.currency,
                self.pricing_model, pricing_details, applicable_industry,
                self.applicable_scale, self.delivery_lead_time, supported_channels,
                self.status, media_assets, keywords, related_skus,
                self.effective_date, self.expiry_date, self.internal_notes, current_time
            ))
            self.id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return self.id
    
    @staticmethod
    def get_by_id(product_id: int) -> Optional['Product']:
        """根据ID获取产品"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        result = cursor.fetchone()
        
        conn.close()
        
        if result:
            # 将行转换为字典
            product_dict = dict(result)
            
            # 处理JSON字段
            for json_field in ['key_selling_points', 'pricing_details', 'applicable_industry', 
                              'supported_channels', 'media_assets', 'keywords', 'related_skus']:
                if product_dict.get(json_field):
                    try:
                        product_dict[json_field] = json.loads(product_dict[json_field])
                    except:
                        product_dict[json_field] = []
            
            return Product(product_dict)
        
        return None
    
    @staticmethod
    def get_by_sku(sku_id: str) -> Optional['Product']:
        """根据SKU ID获取产品"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM products WHERE sku_id = ?", (sku_id,))
        result = cursor.fetchone()
        
        conn.close()
        
        if result:
            # 将行转换为字典
            product_dict = dict(result)
            
            # 处理JSON字段
            for json_field in ['key_selling_points', 'pricing_details', 'applicable_industry', 
                              'supported_channels', 'media_assets', 'keywords', 'related_skus']:
                if product_dict.get(json_field):
                    try:
                        product_dict[json_field] = json.loads(product_dict[json_field])
                    except:
                        product_dict[json_field] = []
            
            return Product(product_dict)
        
        return None
    
    @staticmethod
    def search(query: str = "", product_type: str = "", status: str = "") -> List[Dict[str, Any]]:
        """搜索产品"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        sql_query = "SELECT * FROM products WHERE 1=1"
        params = []
        
        if query:
            sql_query += " AND (sku_id LIKE ? OR product_name LIKE ? OR keywords LIKE ?)"
            search_term = f"%{query}%"
            params.extend([search_term, search_term, search_term])
        
        if product_type:
            sql_query += " AND product_type = ?"
            params.append(product_type)
        
        if status:
            sql_query += " AND status = ?"
            params.append(status)
        
        sql_query += " ORDER BY updated_at DESC LIMIT 100"
        cursor.execute(sql_query, params)
        
        results = cursor.fetchall()
        conn.close()
        
        products = []
        for row in results:
            product_dict = dict(row)
            
            # 处理JSON字段
            for json_field in ['key_selling_points', 'pricing_details', 'applicable_industry', 
                              'supported_channels', 'media_assets', 'keywords', 'related_skus']:
                if product_dict.get(json_field):
                    try:
                        product_dict[json_field] = json.loads(product_dict[json_field])
                    except:
                        product_dict[json_field] = []
            
            products.append(product_dict)
        
        return products

# 根据产品类型获取扩展信息的函数
@print_log()
def get_product_extension(sku_id: str, product_type: str) -> Dict[str, Any]:
    """根据产品类型获取扩展信息"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    table_map = {
        "Digital Service": "digital_service_details",
        "Field Service": "field_service_details",
        "Physical Good": "physical_good_details",
        "Training": "training_details",
        "Bundle": "bundle_details"
    }
    
    table_name = table_map.get(product_type)
    if not table_name:
        return {}
    
    cursor.execute(f"SELECT * FROM {table_name} WHERE sku_id = ?", (sku_id,))
    result = cursor.fetchone()
    
    conn.close()
    
    if result:
        extension_dict = dict(result)
        
        # 处理JSON字段
        for key, value in extension_dict.items():
            if value and isinstance(value, str) and (value.startswith('[') or value.startswith('{')):
                try:
                    extension_dict[key] = json.loads(value)
                except:
                    pass
        
        return extension_dict
    
    return {}

# 初始化数据库（如果需要）
init_db()