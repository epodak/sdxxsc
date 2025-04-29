import gradio as gr
import pandas as pd
import os
import json
from datetime import datetime
import db_models
from db_models import Product
import ai_helper

# 确保数据库初始化
db_models.init_db()

# 添加新产品
def add_product(sku_id, product_type, category, product_name, short_description, 
                base_price, pricing_model, applicable_industry, keywords):
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

# 搜索产品
def search_products(search_query="", product_type="", status=""):
    try:
        results = Product.search(search_query, product_type, status)
        
        if not results:
            return "没有找到符合条件的产品"
        
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
        return f"搜索失败: {str(e)}"

# 根据产品信息生成AI描述
def generate_ai_description(product_type, product_name, category, applicable_industry, special_features, keywords):
    try:
        # 预处理输入
        keywords_list = keywords.split(',') if keywords else []
        features_list = special_features.split(',') if special_features else []
        
        # 调用AI服务
        result = ai_helper.generate_product_description(
            product_type=product_type,
            product_name=product_name,
            keywords=keywords_list,
            category=category,
            target_audience=applicable_industry,
            special_features=features_list
        )
        
        if result.get('success'):
            # 格式化返回结果
            description = result.get('description', '')
            selling_points = '\n'.join([f"- {point}" for point in result.get('selling_points', [])])
            title_suggestions = '\n'.join([f"{i+1}. {title}" for i, title in enumerate(result.get('title_suggestions', []))])
            
            return f"""### 生成的短描述:
{description}

### 核心卖点:
{selling_points}

### 标题建议:
{title_suggestions}
"""
        else:
            return f"生成描述失败: {result.get('error', '未知错误')}"
    
    except Exception as e:
        return f"生成描述失败: {str(e)}"

# 优化产品信息以适应特定平台
def optimize_for_platform(product_name, short_description, keywords, target_platform):
    try:
        # 预处理输入
        keywords_list = keywords.split(',') if keywords else []
        
        # 构建产品数据
        product_data = {
            "product_name": product_name,
            "short_description": short_description,
            "keywords": keywords_list
        }
        
        # 调用AI服务
        result = ai_helper.optimize_product_fields(product_data, target_platform)
        
        if result.get('success'):
            # 格式化返回结果
            optimized_title = result.get('optimized_title', '')
            optimized_description = result.get('optimized_description', '')
            recommended_keywords = ', '.join(result.get('recommended_keywords', []))
            platform_suggestions = result.get('platform_suggestions', '')
            
            return f"""### {target_platform}平台优化后的标题:
{optimized_title}

### {target_platform}平台优化后的描述:
{optimized_description}

### 推荐关键词:
{recommended_keywords}

### 平台特定建议:
{platform_suggestions}
"""
        else:
            return f"优化失败: {result.get('error', '未知错误')}"
    
    except Exception as e:
        return f"优化失败: {str(e)}"

# 获取产品类型选项
def get_product_types():
    return ["Digital Service", "Field Service", "Physical Good", "Training", "Bundle"]

# 获取状态选项
def get_status_options():
    return ["Draft", "Active", "Inactive", "Discontinued"]

# 获取定价模型选项
def get_pricing_models():
    return ["One-time", "Subscription", "Tiered", "Quote", "Free"]

# 获取平台选项
def get_platform_options():
    return ["通用", "淘宝", "京东", "1688", "抖音", "小红书"]

# UI接口
def create_ui():
    # 产品添加表单
    with gr.Tab("添加产品"):
        with gr.Row():
            sku_id = gr.Textbox(label="SKU ID / 产品ID", placeholder="如: IFM-SVC-HVAC-PM-Q", info="唯一标识符")
            product_type = gr.Dropdown(label="产品类型", choices=get_product_types(), info="选择产品所属大类")
        
        with gr.Row():
            category = gr.Textbox(label="产品类目", placeholder="如: Maintenance > HVAC", info="产品细分类目")
            product_name = gr.Textbox(label="产品名称", placeholder="如: 智能运维管理平台", info="面向客户的产品/服务名称")
        
        short_description = gr.Textbox(label="简要描述", placeholder="100-200字简短概述,概括核心价值", lines=3, info="用于列表页和搜索结果")
        
        with gr.Row():
            base_price = gr.Number(label="基本价格", info="起始价格或标准单价")
            pricing_model = gr.Dropdown(label="价格模式", choices=get_pricing_models(), info="定价策略")
        
        applicable_industry = gr.Textbox(label="适用行业", placeholder="输入逗号分隔的行业,如: 地产,制造,医疗", info="目标行业标签")
        keywords = gr.Textbox(label="关键词", placeholder="输入逗号分隔的关键词,如: 智能运维,楼宇自控,节能", info="用于搜索和SEO")
        
        add_btn = gr.Button("添加产品", variant="primary")
        result_msg = gr.Textbox(label="结果消息", interactive=False)
        
        add_btn.click(
            fn=add_product,
            inputs=[sku_id, product_type, category, product_name, short_description, 
                   base_price, pricing_model, applicable_industry, keywords],
            outputs=result_msg
        )
    
    # 产品搜索与浏览
    with gr.Tab("产品浏览"):
        with gr.Row():
            search_query = gr.Textbox(label="搜索", placeholder="输入产品名称,SKU或关键词")
            filter_type = gr.Dropdown(label="产品类型筛选", choices=[""] + get_product_types(), value="")
            filter_status = gr.Dropdown(label="状态筛选", choices=[""] + get_status_options(), value="")
        
        search_btn = gr.Button("搜索")
        results_table = gr.Dataframe(label="产品列表")
        
        search_btn.click(
            fn=search_products,
            inputs=[search_query, filter_type, filter_status],
            outputs=results_table
        )
    
    # AI辅助选品标签页
    with gr.Tab("AI辅助选品"):
        gr.Markdown("""
        # AI辅助选品功能
        
        使用AI功能帮助您生成产品描述,卖点和优化建议.
        """)
        
        with gr.Tabs():
            # 描述生成标签页
            with gr.Tab("产品描述生成"):
                with gr.Row():
                    ai_product_type = gr.Dropdown(label="产品类型", choices=get_product_types())
                    ai_product_name = gr.Textbox(label="产品名称", placeholder="输入产品名称")
                
                with gr.Row():
                    ai_category = gr.Textbox(label="产品类目", placeholder="如: Maintenance > HVAC")
                    ai_applicable_industry = gr.Textbox(label="目标行业/受众", placeholder="如: 地产,制造,医疗")
                
                ai_special_features = gr.Textbox(label="特色功能", placeholder="输入逗号分隔的特色功能列表", lines=2)
                ai_keywords = gr.Textbox(label="关键词", placeholder="输入逗号分隔的关键词", lines=2)
                
                generate_btn = gr.Button("生成描述", variant="primary")
                ai_result = gr.Markdown(label="AI生成结果")
                
                generate_btn.click(
                    fn=generate_ai_description,
                    inputs=[ai_product_type, ai_product_name, ai_category, 
                           ai_applicable_industry, ai_special_features, ai_keywords],
                    outputs=ai_result
                )
            
            # 平台优化标签页
            with gr.Tab("平台内容优化"):
                with gr.Row():
                    opt_product_name = gr.Textbox(label="产品名称", placeholder="输入产品名称")
                    opt_target_platform = gr.Dropdown(label="目标平台", choices=get_platform_options(), value="通用")
                
                opt_short_description = gr.Textbox(label="产品描述", placeholder="输入产品描述", lines=3)
                opt_keywords = gr.Textbox(label="关键词", placeholder="输入逗号分隔的关键词", lines=2)
                
                optimize_btn = gr.Button("优化内容", variant="primary")
                opt_result = gr.Markdown(label="优化结果")
                
                optimize_btn.click(
                    fn=optimize_for_platform,
                    inputs=[opt_product_name, opt_short_description, opt_keywords, opt_target_platform],
                    outputs=opt_result
                )
    
    # 关于与帮助标签页
    with gr.Tab("关于"):
        gr.Markdown("""
        # 选品工具 MVP
        
        这是一个用于产品信息管理的最小可行产品(MVP).基于Python和Gradio构建,使用SQLite作为数据存储.
        
        ## 主要功能
        
        - 产品信息录入与管理
        - 产品搜索与浏览
        - AI辅助内容生成
        - 平台内容优化
        
        ## 使用方法
        
        1. 在"添加产品"标签页填写产品信息并提交
        2. 在"产品浏览"标签页查看和搜索产品
        3. 在"AI辅助选品"标签页使用AI功能生成描述和优化内容
        
        ## 环境配置
        
        要启用AI功能,请设置环境变量:
        
        ```
        export OPENAI_API_KEY="你的OpenAI API密钥"
        ```
        """)

# 创建Gradio应用
demo = gr.Blocks(title="选品工具 MVP", theme=gr.themes.Soft())
with demo:
    gr.Markdown("# 选品工具 MVP")
    create_ui()

# 启动应用
if __name__ == "__main__":
    demo.launch()
