// src/components/ChatRoom.js
import React, { useState, useEffect, useRef } from "react";
import io from "socket.io-client";
import { useLocation } from "react-router-dom";

const ChatRoom = () => {
  const location = useLocation();
  const { chatRoomId, adminId } = location.state;
  const [messages, setMessages] = useState([]);
  const [messageInput, setMessageInput] = useState("");
  const socketRef = useRef(null);

  useEffect(() => {
    // Initialize the socket inside useEffect
    socketRef.current = io("http://localhost:5555", {
      transports: ["websocket"], // Force WebSocket transport
    });

    // Function to set up socket event listeners
    const setupSocketListeners = () => {
      socketRef.current.on("new_message", (newMessageData) => {
        const newMessage = newMessageData.message
          ? { content: newMessageData.message }
          : newMessageData;
        setMessages((prevMessages) => [...prevMessages, newMessage]);
      });
    };

    if (chatRoomId) {
      // Emit event to join the room
      socketRef.current.emit("join_room", { chat_room_id: chatRoomId });

      setupSocketListeners();

      const fetchMessages = async () => {
        try {
          const response = await fetch(
            `http://localhost:5555/chat_room/${chatRoomId}/messages`,
            {
              method: "GET",
              headers: {
                "Content-Type": "application/json",
              },
            }
          );
          if (!response.ok) {
            throw new Error("Network response was not okay!");
          }
          const messages = await response.json();
          setMessages(messages);
        } catch (error) {
          console.error(`Error fetching messages: ${error}`);
        }
      };

      fetchMessages();
    }

    return () => {
      socketRef.current.off("new_message");
      socketRef.current.emit("leave_room", { chat_room_id: chatRoomId });
      socketRef.current.disconnect();
    };
  }, [chatRoomId]);

  const sendMessage = () => {
    if (messageInput.trim()) {
      // Emitting the message event with necessary data
      socketRef.current.emit("send_message", {
        chat_room_id: chatRoomId,
        message: messageInput,
        admin_id: adminId,
        sender_type: "user",
      });
      setMessageInput("");
    }
  };

  const renderMessage = (msg) => {
    const isSentByCurrentUser = msg.sender_type === "user";
    const messageClass = isSentByCurrentUser ? "sent" : "received";

    return (
      <div key={msg.id} className={`message ${messageClass}`}>
        <p>{msg.content}</p>
      </div>
    );
  };

  return (
    <div>
      <div id="messagesList">{messages.map(renderMessage)}</div>
      <input
        type="text"
        value={messageInput}
        onChange={(e) => setMessageInput(e.target.value)}
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
};

export default ChatRoom;
