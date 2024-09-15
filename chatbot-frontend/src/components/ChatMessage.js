import React from "react";
import "./ChatMessage.css"; // If you have specific styles for messages

const ChatMessage = ({ message }) => {
  // Function to convert newlines to <br/> tags
  const formatText = (text) => {
    return text.split("\n").map((part, index) => (
      <React.Fragment key={index}>
        {part}
        <br />
      </React.Fragment>
    ));
  };

  return (
    <div className={`chat-message ${message.sender}`}>
      <p className="message">{formatText(message.text)}</p>
    </div>
  );
};

export default ChatMessage;
