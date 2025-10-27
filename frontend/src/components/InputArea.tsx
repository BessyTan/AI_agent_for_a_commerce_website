import React, { useState, useRef } from 'react'
import './InputArea.css'

interface InputAreaProps {
  onSendMessage: (message: string) => void
  onImageUpload: (file: File) => void
}

const InputArea: React.FC<InputAreaProps> = ({ onSendMessage, onImageUpload }) => {
  const [input, setInput] = useState('')
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (input.trim()) {
      onSendMessage(input)
      setInput('')
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  const handleImageClick = () => {
    fileInputRef.current?.click()
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      onImageUpload(file)
      // Reset input
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
    }
  }

  return (
    <div className="input-area">
      <div className="input-actions">
        <button
          type="button"
          className="action-button"
          onClick={handleImageClick}
          title="Upload image for search"
        >
          📷
        </button>
      </div>
      <form onSubmit={handleSubmit} className="input-form">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type a message or upload an image..."
          className="input-field"
        />
        <button type="submit" className="send-button" disabled={!input.trim()}>
          Send
        </button>
      </form>
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        style={{ display: 'none' }}
      />
    </div>
  )
}

export default InputArea

