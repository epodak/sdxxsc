from typing import Dict, Any, List
import ai_helper
from utils.decorators import print_log

@print_log()
def generate_ai_description(product_type: str, product_name: str, category: str, 
                          applicable_industry: str, special_features: str, keywords: str) -> str:
    """根据产品信息生成AI描述"""
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

@print_log()
def optimize_for_platform(product_name: str, short_description: str, keywords: str, target_platform: str) -> str:
    """优化产品信息以适应特定平台"""
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