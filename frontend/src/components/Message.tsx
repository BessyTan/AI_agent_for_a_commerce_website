import React from 'react'
import './Message.css'

interface MessageProps {
  message: {
    role: 'user' | 'assistant'
    content: string
  }
}

const Message: React.FC<MessageProps> = ({ message }) => {
  return (
    <div className={`message ${message.role}`}>
      <div className="message-avatar">
        {message.role === 'user' ? '👤' : '🤖'}
      </div>
      <div className="message-content">
        <p>{message.content}</p>
      </div>
    </div>
  )
}

export default Message

