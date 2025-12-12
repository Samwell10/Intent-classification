import React from "react";
import MessageBubble from "./MessageBubble.jsx";

export default function ChatLayout({ messages, input, setInput, loading, onSend }) {
  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (!loading && input.trim()) onSend();
    }
  };

  return (
    <div className="app-container">
      <div className="chat-card">
        <header className="chat-header">
          <div className="chat-title">Banking Intent Assistant</div>
          <div className="chat-subtitle">
            Type a question like: <span>“My card isn't working”</span>
          </div>
        </header>

        <main className="chat-body">
          {messages.length === 0 && (
            <div className="empty-state">
              Start by typing a message below. The assistant will predict your intent
              and provide a support-style answer.
            </div>
          )}

          {messages.map((msg, index) => (
            <MessageBubble
              key={index}
              sender={msg.sender}
              text={msg.text}
              intent={msg.intent}
            />
          ))}
        </main>

        <footer className="chat-footer">
          <textarea
            className="chat-input"
            placeholder="Ask something about your card, transfers, top-ups..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={2}
          />
          <button
            className="send-button"
            onClick={onSend}
            disabled={loading || !input.trim()}
          >
            {loading ? "Thinking..." : "Send"}
          </button>
        </footer>
      </div>
    </div>
  );
}
