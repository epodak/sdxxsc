from typing import Dict, Any, List, Optional
from datetime import datetime
import json
from database.connection import get_db_connection
from utils.decorators import print_log

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
        
        cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        row = cursor.fetchone()
        
        if row:
            # 将行转换为字典
            product_dict = dict(row)
            # 解析JSON字段
            for field in ['key_selling_points', 'pricing_details', 'applicable_industry', 
                         'supported_channels', 'media_assets', 'keywords', 'related_skus']:
                if product_dict.get(field):
                    product_dict[field] = json.loads(product_dict[field])
            
            return Product(product_dict)
        
        return None

    @staticmethod
    def get_by_sku(sku_id: str) -> Optional['Product']:
        """根据SKU获取产品"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM products WHERE sku_id = ?', (sku_id,))
        row = cursor.fetchone()
        
        if row:
            # 将行转换为字典
            product_dict = dict(row)
            # 解析JSON字段
            for field in ['key_selling_points', 'pricing_details', 'applicable_industry', 
                         'supported_channels', 'media_assets', 'keywords', 'related_skus']:
                if product_dict.get(field):
                    product_dict[field] = json.loads(product_dict[field])
            
            return Product(product_dict)
        
        return None

    @staticmethod
    def search(query: str = "", product_type: str = "", status: str = "") -> List[Dict[str, Any]]:
        """搜索产品"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 构建查询条件
        conditions = []
        params = []
        
        if query:
            conditions.append('''(
                sku_id LIKE ? OR 
                product_name LIKE ? OR 
                short_description LIKE ? OR
                keywords LIKE ?
            )''')
            search_term = f"%{query}%"
            params.extend([search_term] * 4)
        
        if product_type:
            conditions.append("product_type = ?")
            params.append(product_type)
        
        if status:
            conditions.append("status = ?")
            params.append(status)
        
        # 组合SQL语句
        sql = "SELECT * FROM products"
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        
        # 转换结果
        results = []
        for row in rows:
            product_dict = dict(row)
            # 解析JSON字段
            for field in ['key_selling_points', 'pricing_details', 'applicable_industry', 
                         'supported_channels', 'media_assets', 'keywords', 'related_skus']:
                if product_dict.get(field):
                    product_dict[field] = json.loads(product_dict[field])
            results.append(product_dict)
        
        return results 