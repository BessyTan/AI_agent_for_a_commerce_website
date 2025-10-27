"""
Commerce Agent - Core AI logic
Handles conversation, text-based recommendations, and image-based search
"""

from typing import List, Dict, Optional
import sqlite3
from database import get_all_products, search_products_by_text, search_products_by_image_similarity

class CommerceAgent:
    """
    Unified AI agent for commerce website
    Handles:
    1. General conversation
    2. Text-based product recommendations
    3. Image-based product search
    """
    
    def __init__(self):
        self.name = "ShopAssist"
        self.context = "I'm an AI shopping assistant for an e-commerce website. I can help you find products, answer questions, and recommend items based on your needs."
        
    def handle_message(self, message: str, history: List[dict] = None) -> Dict:
        """
        Handle text message and determine if it's conversation or product recommendation request
        """
        message_lower = message.lower().strip()
        
        # Check for general conversation
        if self._is_general_conversation(message_lower):
            return self._handle_conversation(message_lower, history)
        
        # Otherwise, treat as product recommendation request
        return self._handle_text_recommendation(message, history)
    
    def _is_general_conversation(self, message: str) -> bool:
        """Determine if message is general conversation vs product recommendation"""
        message_lower = message.lower()
        
        # Check for explicit product-related keywords FIRST (higher priority)
        product_keywords = [
            "recommend", "suggest", "find", "search", "show", "looking for",
            "need", "want", "buy", "price", "product", "item", "give me",
            "looking for", "t-shirt", "shirt", "shoes", "shorts", "watch", 
            "mat", "gloves", "bottle", "earbuds"
        ]
        
        for keyword in product_keywords:
            if keyword in message_lower:
                return False  # This is a product query, not general conversation
        
        # Check for general conversation keywords
        conversation_keywords = [
            "what's your name", "who are you", "what can you do", "hello", "hi", "hey",
            "how are you", "what is your purpose", "help me", "capabilities"
        ]
        
        for keyword in conversation_keywords:
            if keyword in message_lower:
                return True  # This is general conversation
        
        # Default to conversation for ambiguous queries
        return True
    
    def _handle_conversation(self, message: str, history: List[dict] = None) -> Dict:
        """Handle general conversation"""
        message_lower = message.lower()
        
        if "name" in message_lower or "who are you" in message_lower:
            response = f"Hi! I'm {self.name}, your AI shopping assistant. {self.context}"
        
        elif "what can you do" in message_lower or "capabilities" in message_lower:
            response = (
                f"I can help you with several things:\n"
                f"1. Answer general questions about the store\n"
                f"2. Recommend products based on text descriptions\n"
                f"3. Find products from images you upload\n"
                f"Just tell me what you're looking for or upload an image!"
            )
        
        elif "hello" in message_lower or "hi" in message_lower or "hey" in message_lower:
            response = f"Hello! I'm {self.name}. How can I help you today?"
        
        elif "help" in message_lower:
            response = (
                f"I'm here to help you shop! You can:\n"
                f"• Ask me questions about products\n"
                f"• Describe what you're looking for (e.g., 'Recommend me a t-shirt for sports')\n"
                f"• Upload an image to find similar products\n"
                f"What would you like to do?"
            )
        
        else:
            response = (
                f"I'm not sure how to help with that, but I can assist you with:\n"
                f"• Finding and recommending products\n"
                f"• Answering questions about our store\n"
                f"• Searching products by image\n"
                f"Try asking me to recommend a product or upload an image!"
            )
        
        return {
            "response": response,
            "products": None,
            "response_type": "conversation"
        }
    
    def _handle_text_recommendation(self, message: str, history: List[dict] = None) -> Dict:
        """Handle text-based product recommendation"""
        try:
            # Get all products
            all_products = get_all_products()
            
            # Simple keyword-based matching for recommendation
            # In production, use proper NLP/ML models
            message_lower = message.lower()
            
            # Search for relevant products
            matched_products = search_products_by_text(message, all_products)
            
            # If no matches, suggest popular items
            if not matched_products:
                matched_products = all_products[:3]  # Show first 3 as suggestions
                response = (
                    f"I couldn't find exactly what you're looking for, "
                    f"but here are some popular items you might like:"
                )
            else:
                response = f"Here are some products that match your request:"
            
            return {
                "response": response,
                "products": matched_products[:5],  # Limit to 5 products
                "response_type": "text_recommendation"
            }
        except Exception as e:
            return {
                "response": f"I encountered an error while searching: {str(e)}",
                "products": None,
                "response_type": "text_recommendation"
            }
    
    def handle_image_search(self, image_data: str, image_format: str, history: List[dict] = None) -> Dict:
        """
        Handle image-based product search from the predefined catalog
        In production, use proper computer vision models (CLIP, etc.)
        """
        try:
            # Get all products from the predefined catalog
            all_products = get_all_products()
            
            # Search products from the catalog based on image
            # In production, this would use vision models to analyze the image
            # and match against product images in the catalog
            matched_products = search_products_by_image_similarity(image_data, all_products)
            
            if not matched_products:
                # Fallback to show some products from the catalog
                matched_products = all_products[:3]
                response = "I've received your image. Here are some products from our catalog:"
            else:
                response = "I found some products from our catalog that might match your image:"
            
            return {
                "response": response,
                "products": matched_products[:5],
                "response_type": "image_search"
            }
        except Exception as e:
            return {
                "response": f"I encountered an error processing the image: {str(e)}",
                "products": None,
                "response_type": "image_search"
            }

