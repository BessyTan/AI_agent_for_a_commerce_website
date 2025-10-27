import React from 'react'
import './ProductCard.css'

interface Product {
  id: number
  name: string
  description: string
  category: string
  price: number
  image_url: string
  features: string[]
}

interface ProductCardProps {
  product: Product
}

const ProductCard: React.FC<ProductCardProps> = ({ product }) => {
  return (
    <div className="product-card">
      <div className="product-image">
        <img src={product.image_url} alt={product.name} onError={(e) => {
          (e.target as HTMLImageElement).src = 'https://via.placeholder.com/300x300?text=Product+Image';
        }} />
      </div>
      <div className="product-info">
        <div className="product-category">{product.category}</div>
        <h3 className="product-name">{product.name}</h3>
        <p className="product-description">{product.description}</p>
        {product.features && product.features.length > 0 && (
          <div className="product-features">
            {product.features.map((feature, index) => (
              <span key={index} className="feature-tag">{feature}</span>
            ))}
          </div>
        )}
        <div className="product-footer">
          <span className="product-price">${product.price.toFixed(2)}</span>
          <button className="buy-button">Add to Cart</button>
        </div>
      </div>
    </div>
  )
}

export default ProductCard

