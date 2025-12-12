import { useState } from 'react'
import './App.css'
import ChatLayout from './components/ChatLayout';
import { predictIntent } from './api';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    const trimmed = input.trim();
    if (!trimmed) return;

    // Add user message
    const userMessage = { sender: "user", text: trimmed };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const result = await predictIntent(trimmed);
      const botMessage = {
        sender: "bot",
        text: result.response,
        intent: result.intent,
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        sender: "bot",
        text: ` Error: ${error.message}`,
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <p>HELPPP</p>
      <ChatLayout
        messages={messages}
        input={input}
        setInput={setInput}
        loading={loading}
        onSend={handleSend}
      />
    </>
  )
}

export default App
