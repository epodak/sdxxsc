from typing import Dict, Any, List, Optional
from models.product import Product
from utils.decorators import print_log

@print_log()
def add_product(sku_id: str, product_type: str, category: str, product_name: str, 
                short_description: str, base_price: float, pricing_model: str, 
                applicable_industry: str, keywords: str) -> str:
    """添加新产品"""
    if not sku_id or not product_name:
        return "SKU ID和产品名称为必填项"
    
    try:
        # 检查SKU是否已存在
        existing_product = Product.get_by_sku(sku_id)
        if existing_product:
            return f"SKU ID: {sku_id} 已存在"
        
        # 创建新产品对象
        product = Product()
        product.sku_id = sku_id
        product.product_type = product_type
        product.category = category
        product.product_name = product_name
        product.short_description = short_description
        product.base_price = base_price
        product.pricing_model = pricing_model
        
        # 处理数组字段
        product.applicable_industry = applicable_industry.split(',') if applicable_industry else []
        product.keywords = keywords.split(',') if keywords else []
        
        # 保存产品
        product.save()
        
        return f"产品 {product_name} (SKU: {sku_id}) 添加成功"
    
    except Exception as e:
        return f"添加产品失败: {str(e)}"

@print_log()
def search_products(search_query: str = "", product_type: str = "", status: str = "") -> List[Dict[str, Any]]:
    """搜索产品"""
    try:
        results = Product.search(search_query, product_type, status)
        
        if not results:
            return []
        
        # 简化返回结果,只显示关键字段
        simplified_results = []
        for product in results:
            simplified_results.append({
                "id": product.get("id"),
                "sku_id": product.get("sku_id"),
                "product_type": product.get("product_type"),
                "product_name": product.get("product_name"),
                "category": product.get("category"),
                "short_description": product.get("short_description", "")[:50] + "..." if product.get("short_description", "") else "",
                "base_price": product.get("base_price"),
                "currency": product.get("currency"),
                "status": product.get("status"),
                "updated_at": product.get("updated_at")
            })
        
        return simplified_results
    except Exception as e:
        return []

# 获取产品类型选项
def get_product_types() -> List[str]:
    return ["Digital Service", "Field Service", "Physical Good", "Training", "Bundle"]

# 获取状态选项
def get_status_options() -> List[str]:
    return ["Draft", "Active", "Inactive", "Discontinued"]

# 获取定价模型选项
def get_pricing_models() -> List[str]:
    return ["One-time", "Subscription", "Tiered", "Quote", "Free"]

# 获取平台选项
def get_platform_options() -> List[str]:
    return ["通用", "淘宝", "京东", "1688", "抖音", "小红书"] 