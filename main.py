from database.init_db import init_db
from services.product_service import (
    add_product, search_products, 
    get_product_types, get_status_options, 
    get_pricing_models, get_platform_options
)
from services.ai_service import generate_ai_description, optimize_for_platform
from ui import demo

# 确保数据库初始化
init_db()

# 启动应用
if __name__ == "__main__":
    demo.launch()
