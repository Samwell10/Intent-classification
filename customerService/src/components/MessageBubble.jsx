import React from "react";

export default function MessageBubble({ sender, text, intent }) {
  const isUser = sender === "user";

  return (
    <div className={`message-row ${isUser ? "user-row" : "bot-row"}`}>
      <div className={`bubble ${isUser ? "user-bubble" : "bot-bubble"}`}>
        {!isUser && intent && (
          <div className="intent-tag">
            Intent: <span>{intent}</span>
          </div>
        )}
        <div>{text}</div>
      </div>
    </div>
  );
}
