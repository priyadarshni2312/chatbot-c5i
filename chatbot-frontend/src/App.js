import React, { useState, useEffect, useRef } from "react";
import "./App.css";
import Header from "./components/Header";
import ChatWindow from "./components/ChatWindow";
import ChatForm from "./components/ChatForm";
import API_BASE_URL from "./config";
import axios from "axios";

function App() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const chatWindowRef = useRef(null);

  const addMessage = (
    text,
    sender = "user",
    timestamp = new Date().toISOString()
  ) => {
    setMessages((prevMessages) => [
      ...prevMessages,
      { text, sender, timestamp },
    ]);
  };

  const handleSendMessage = async (input) => {
    addMessage(input, "user");
    setIsLoading(true);

    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/query/`,
        { question: input },
        { headers: { "Content-Type": "application/json" } }
      );

      setIsLoading(false);

      const botResponse = response.data.response;
      addMessage(botResponse, "bot");
    } catch (error) {
      console.error("Error sending message:", error);
      setIsLoading(false);
    }
  };

  useEffect(() => {
    const fetchChatHistory = async () => {
      try {
        const response = await axios.get(
          `${API_BASE_URL}/api/chat-history/1`
        );
        const chatHistory = response.data.chat_history.flatMap((entry) => [
          {
            text: entry.question,
            sender: "user",
          },
          {
            text: entry.response,
            sender: "bot",
          },
        ]);
        setMessages(chatHistory);
      } catch (error) {
        console.error("Error fetching chat history:", error);
      }
    };

    fetchChatHistory();
  }, []);

  useEffect(() => {
    // Scroll to bottom whenever messages or isLoading changes
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  return (
    <div className="App">
      <Header />
      <ChatWindow
        messages={messages}
        isLoading={isLoading}
        chatWindowRef={chatWindowRef}
      />
      <ChatForm onSendMessage={handleSendMessage} />
    </div>
  );
}

export default App;
