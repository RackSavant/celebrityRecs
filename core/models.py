from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Literal
from datetime import datetime
from enum import Enum
import json

class CulturalReference(str, Enum):
    """Enum for cultural references."""
    HIP_HOP = "hip_hop"
    HIPPIE = "hippie"
    PUNK = "punk"
    VINTAGE = "vintage"
    STREETWEAR = "streetwear"
    WORKWEAR = "workwear"
    SPORTS = "sports"

class StyleEra(str, Enum):
    """Enum for preferred fashion eras."""
    VICTORIAN = "victorian"
    ROARING_20S = "roaring_20s"
    POST_WAR_50S = "post_war_50s"
    MODERN_2000S = "modern_2000s"
    FUTURE = "future"

class StyleAttribute(str, Enum):
    """Enum for style attributes."""
    CASUAL = "casual"
    FORMAL = "formal"
    SPORTY = "sporty"
    BOHEMIAN = "bohemian"
    MINIMALIST = "minimalist"
    STREET = "street"
    CLASSIC = "classic"

class Category(str, Enum):
    """Enum for clothing categories."""
    SHIRT = "shirt"
    PANTS = "pants"
    DRESS = "dress"
    JACKET = "jacket"
    SHOES = "shoes"
    ACCESSORIES = "accessories"

class StyleProfile(BaseModel):
    """User's fashion DNA profile."""
    cultural_references: List[CulturalReference] = Field(
        default_factory=list,
        description="Cultural influences in user's style"
    )
    preferred_eras: List[StyleEra] = Field(
        default_factory=list,
        description="Preferred fashion eras"
    )
    style_attributes: List[StyleAttribute] = Field(
        default_factory=list,
        description="Core style attributes"
    )
    color_preferences: List[str] = Field(
        default_factory=list,
        description="Preferred colors"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "cultural_references": ["hip_hop", "streetwear"],
                "preferred_eras": ["modern_2000s"],
                "style_attributes": ["casual", "street"],
                "color_preferences": ["black", "white", "grey"]
            }
        }

class FashionItem(BaseModel):
    """Represents a clothing item."""
    id: str = Field(..., description="Unique identifier for the item")
    name: str = Field(..., description="Item name")
    category: Category = Field(..., description="Item category")
    attributes: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional item attributes"
    )
    image_url: str = Field(..., description="URL to item image")
    brand: Optional[str] = Field(None, description="Item brand")
    price: float = Field(..., description="Item price")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "item_123",
                "name": "Classic Denim Jacket",
                "category": "jacket",
                "attributes": {
                    "material": "denim",
                    "fit": "regular",
                    "season": "all"
                },
                "image_url": "https://example.com/jacket.jpg",
                "brand": "Levi's",
                "price": 149.99
            }
        }

class ConversationContext(BaseModel):
    """Manages chat state and user preferences."""
    user_id: str = Field(..., description="Unique user identifier")
    current_topic: str = Field(..., description="Current conversation topic")
    style_profile: StyleProfile = Field(..., description="User's style preferences")
    conversation_history: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Chat history"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_123",
                "current_topic": "casual spring outfits",
                "style_profile": {
                    "cultural_references": ["hip_hop", "streetwear"],
                    "preferred_eras": ["modern_2000s"],
                    "style_attributes": ["casual", "street"],
                    "color_preferences": ["black", "white", "grey"]
                },
                "conversation_history": [
                    {"user": "Hi, I need help with an outfit", "assistant": "I'm here to help!"}
                ]
            }
        }

class TryOnRequest(BaseModel):
    """Request for virtual try-on."""
    user_image: str = Field(..., description="Base64 encoded user image")
    fashion_item_id: str = Field(..., description="ID of the fashion item to try")
    preferences: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional user preferences"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_image": "data:image/jpeg;base64,...",
                "fashion_item_id": "item_123",
                "preferences": {
                    "pose": "standing",
                    "lighting": "natural"
                }
            }
        }

class RecommendationResponse(BaseModel):
    """API response for recommendations."""
    items: List[FashionItem] = Field(..., description="Recommended items")
    confidence_score: float = Field(..., description="Confidence score of recommendations")
    reasoning: str = Field(..., description="Explanation for the recommendations")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "items": [
                    {
                        "id": "item_123",
                        "name": "Classic Denim Jacket",
                        "category": "jacket",
                        "attributes": {
                            "material": "denim",
                            "fit": "regular"
                        },
                        "image_url": "https://example.com/jacket.jpg",
                        "brand": "Levi's",
                        "price": 149.99
                    }
                ],
                "confidence_score": 0.95,
                "reasoning": "Recommended based on your casual street style preferences",
                "timestamp": "2025-06-17T19:46:57-07:00"
            }
        }
