import React from "react";
import "./ChatWindow.css";
import ChatMessage from "./ChatMessage";

const ChatWindow = ({ messages, isLoading, chatWindowRef }) => {
  return (
    <div className="chat-window" ref={chatWindowRef}>
      {messages.map((msg, index) => (
        <ChatMessage key={index} message={msg} />
      ))}
      {isLoading && <div className="loading">Loading...</div>}
    </div>
  );
};

export default ChatWindow;
