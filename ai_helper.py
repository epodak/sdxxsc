import os
import openai
from typing import List, Dict, Any, Optional

# 从环境变量获取API密钥
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

# 初始化OpenAI客户端
def get_openai_client():
    if not OPENAI_API_KEY:
        raise ValueError("请设置OPENAI_API_KEY环境变量")
    
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    return client

# 生成产品描述
def generate_product_description(
    product_type: str,
    product_name: str,
    keywords: List[str],
    category: str,
    target_audience: str,
    special_features: Optional[List[str]] = None,
    tone: str = "专业",
    max_length: int = 200
) -> Dict[str, Any]:
    """
    根据产品信息生成产品描述
    
    参数:
        product_type: 产品类型
        product_name: 产品名称
        keywords: 关键词列表
        category: 产品类目
        target_audience: 目标受众/行业
        special_features: 特色功能列表
        tone: 文案风格
        max_length: 最大字符数
        
    返回:
        Dict 包含生成的描述、卖点和标题建议
    """
    try:
        client = get_openai_client()
        
        # 构建提示词
        prompt = f"""
        请根据以下信息生成一个简洁、吸引人的产品描述:
        
        产品类型: {product_type}
        产品名称: {product_name}
        产品类目: {category}
        目标受众/行业: {target_audience}
        关键词: {', '.join(keywords)}
        特色功能: {', '.join(special_features) if special_features else '无特别指定'}
        
        要求:
        1. 简短描述不超过{max_length}字符
        2. 使用{tone}的语气
        3. 突出产品核心价值和差异性
        4. 同时提供3-5条核心卖点(每条15-30字)
        5. 提供2-3个优化后的产品标题建议
        
        输出格式:
        简短描述: [产品简短描述]
        核心卖点:
        - [卖点1]
        - [卖点2]
        - [卖点3]
        
        标题建议:
        1. [标题建议1]
        2. [标题建议2]
        """
        
        # 调用API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个专业的产品文案撰写专家，擅长创建简洁、有吸引力的产品描述。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        
        # 解析结果
        result_text = response.choices[0].message.content
        
        # 简单解析文本结果
        sections = {}
        current_section = None
        
        for line in result_text.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('简短描述:'):
                current_section = 'description'
                sections[current_section] = line.replace('简短描述:', '').strip()
            elif line.startswith('核心卖点:'):
                current_section = 'selling_points'
                sections[current_section] = []
            elif line.startswith('标题建议:'):
                current_section = 'title_suggestions'
                sections[current_section] = []
            elif line.startswith('-') and current_section == 'selling_points':
                sections[current_section].append(line.replace('-', '').strip())
            elif line[0].isdigit() and line[1] == '.' and current_section == 'title_suggestions':
                sections[current_section].append(line[2:].strip())
        
        return {
            'description': sections.get('description', ''),
            'selling_points': sections.get('selling_points', []),
            'title_suggestions': sections.get('title_suggestions', []),
            'success': True
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

# 优化产品信息
def optimize_product_fields(product_data: Dict[str, Any], target_platform: str = "通用") -> Dict[str, Any]:
    """
    优化产品信息以适应不同平台或场景
    
    参数:
        product_data: 产品信息字典
        target_platform: 目标平台(如"淘宝","京东","抖音"等)
        
    返回:
        Dict 包含优化后的产品字段
    """
    try:
        client = get_openai_client()
        
        # 构建提示词
        prompt = f"""
        请根据以下产品信息，针对{target_platform}平台优化各字段以提高转化率:
        
        产品类型: {product_data.get('product_type', '')}
        产品名称: {product_data.get('product_name', '')}
        产品描述: {product_data.get('short_description', '')}
        关键词: {product_data.get('keywords', [])}
        
        请提供以下优化后的内容:
        1. 平台友好的产品标题(限制在60个字符内)
        2. 优化后的短描述(根据平台特性调整语言风格)
        3. 推荐的搜索关键词(5-10个)
        4. 其他平台特定建议
        """
        
        # 调用API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个专业的电商平台优化专家，熟悉各大电商平台的内容策略和优化方法。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        
        # 获取结果
        result_text = response.choices[0].message.content
        
        # 简单解析结果
        sections = {}
        current_section = None
        
        for line in result_text.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('1. 平台友好的产品标题'):
                current_section = 'optimized_title'
                sections[current_section] = line.split(':', 1)[1].strip() if ':' in line else ''
            elif line.startswith('2. 优化后的短描述'):
                current_section = 'optimized_description'
                sections[current_section] = line.split(':', 1)[1].strip() if ':' in line else ''
            elif line.startswith('3. 推荐的搜索关键词'):
                current_section = 'recommended_keywords'
                keyword_text = line.split(':', 1)[1].strip() if ':' in line else ''
                sections[current_section] = [k.strip() for k in keyword_text.split(',')]
            elif line.startswith('4. 其他平台特定建议'):
                current_section = 'platform_suggestions'
                sections[current_section] = line.split(':', 1)[1].strip() if ':' in line else ''
            elif current_section:
                if current_section == 'recommended_keywords' and not line.startswith('4.'):
                    if isinstance(sections[current_section], list):
                        sections[current_section].extend([k.strip() for k in line.split(',')])
                    else:
                        sections[current_section] = [k.strip() for k in line.split(',')]
                elif current_section in ['optimized_title', 'optimized_description', 'platform_suggestions']:
                    sections[current_section] += ' ' + line
        
        return {
            'optimized_title': sections.get('optimized_title', ''),
            'optimized_description': sections.get('optimized_description', ''),
            'recommended_keywords': sections.get('recommended_keywords', []),
            'platform_suggestions': sections.get('platform_suggestions', ''),
            'success': True,
            'target_platform': target_platform
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'target_platform': target_platform
        } 