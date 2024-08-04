import logo from "./logo.svg";
import "./App.css";
import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import CreateChatRoom from "./components/CreateChat"; // Ensure this path is correct
import ChatRoom from "./components/ChatRoom"; // Ensure this path is correct

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/groups" element={<CreateChatRoom adminId={1} />} />
        <Route path="/chat/:chatRoomId" element={<ChatRoom />} />
      </Routes>
    </Router>
  );
}

export default App;
