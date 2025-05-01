from typing import List, Optional
from pydantic import BaseModel, Field

class ProductDescription(BaseModel):
    """产品描述AI生成结果"""
    description: str = Field(..., description="生成的产品描述")
    selling_points: List[str] = Field(default_factory=list, description="产品卖点列表")
    title_suggestions: List[str] = Field(default_factory=list, description="标题建议列表")

class PlatformOptimization(BaseModel):
    """平台优化AI生成结果"""
    optimized_title: str = Field(..., description="优化后的标题")
    optimized_description: str = Field(..., description="优化后的描述")
    recommended_keywords: List[str] = Field(default_factory=list, description="推荐的关键词列表")
    platform_suggestions: str = Field(..., description="平台特定的优化建议")

class ProductAIResponse(BaseModel):
    """AI响应的基础模型"""
    success: bool = Field(default=True, description="是否成功")
    error: Optional[str] = Field(default=None, description="错误信息")
    description: Optional[ProductDescription] = Field(default=None, description="产品描述结果")
    optimization: Optional[PlatformOptimization] = Field(default=None, description="平台优化结果") 