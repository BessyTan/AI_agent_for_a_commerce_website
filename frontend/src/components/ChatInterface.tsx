import React, { useState, useRef, useEffect } from 'react'
import axios from 'axios'
import Message from './Message'
import ProductCard from './ProductCard'
import InputArea from './InputArea'
import './ChatInterface.css'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

interface Product {
  id: number
  name: string
  description: string
  category: string
  price: number
  image_url: string
  features: string[]
}

interface AgentResponse {
  response: string
  products: Product[] | null
  response_type: 'conversation' | 'text_recommendation' | 'image_search'
}

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: "Hello! I'm ShopAssist, your AI shopping assistant. I can help you find products, recommend items based on your needs, or search by image. How can I help you today?"
    }
  ])
  const [products, setProducts] = useState<Product[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, products])

  const handleSendMessage = async (content: string) => {
    if (!content.trim()) return

    // Add user message
    const userMessage: Message = { role: 'user', content }
    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)

    try {
      // Get conversation history (last 10 messages)
      const history = messages.slice(-10).map(msg => ({
        role: msg.role,
        content: msg.content
      }))

      const response = await axios.post<AgentResponse>(
        `${API_BASE_URL}/chat`,
        {
          message: content,
          conversation_history: history
        }
      )

      const agentMessage: Message = { role: 'assistant', content: response.data.response }
      setMessages(prev => [...prev, agentMessage])

      // Update products if returned
      if (response.data.products && response.data.products.length > 0) {
        setProducts(response.data.products)
      } else {
        setProducts([])
      }
    } catch (error) {
      console.error('Error sending message:', error)
      const errorMessage: Message = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.'
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleImageUpload = async (file: File) => {
    setIsLoading(true)

    try {
      const formData = new FormData()
      formData.append('image', file)

      const response = await axios.post<AgentResponse>(
        `${API_BASE_URL}/image-search`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      )

      const imageMessage: Message = {
        role: 'user',
        content: `[Image: ${file.name}]`
      }
      setMessages(prev => [...prev, imageMessage])

      const agentMessage: Message = {
        role: 'assistant',
        content: response.data.response
      }
      setMessages(prev => [...prev, agentMessage])

      // Update products
      if (response.data.products && response.data.products.length > 0) {
        setProducts(response.data.products)
      } else {
        setProducts([])
      }
    } catch (error) {
      console.error('Error uploading image:', error)
      const errorMessage: Message = {
        role: 'assistant',
        content: 'Sorry, I couldn\'t process the image. Please try again.'
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h1>ShopAssist</h1>
        <p>Your AI Shopping Assistant</p>
      </div>

      <div className="chat-messages">
        {messages.map((message, index) => (
          <Message key={index} message={message} />
        ))}
        {isLoading && (
          <div className="message assistant">
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {products.length > 0 && (
        <div className="products-section">
          <h3>Recommended Products</h3>
          <div className="products-grid">
            {products.map(product => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        </div>
      )}

      <InputArea onSendMessage={handleSendMessage} onImageUpload={handleImageUpload} />
    </div>
  )
}

export default ChatInterface

