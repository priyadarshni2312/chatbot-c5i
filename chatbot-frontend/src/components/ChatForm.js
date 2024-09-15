import React, { useState } from "react";
import "./ChatForm.css";

const ChatForm = ({ onSendMessage }) => {
  const [input, setInput] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (input.trim()) {
      onSendMessage(input); // Send user's message to parent component
      setInput("");
    }
  };

  return (
    <form className="chat-form" onSubmit={handleSubmit}>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type your message..."
      />
      <button type="submit">Send</button>
    </form>
  );
};

export default ChatForm;
