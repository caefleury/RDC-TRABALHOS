import React from "react";
import { useNavigate } from "react-router-dom";

const CreateChatRoom = ({ adminId }) => {
  const navigate = useNavigate();

  const onCreateChatRoom = async (adminId) => {
    try {
      const response = await fetch("http://localhost:5000/create_group", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          participant_id: adminId,
          name: "Novo grupo",
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const chatRoom = await response.json();
      navigate(`/group/${chatRoom.chat_room_id}`, {
        state: { adminId: adminId },
      });
    } catch (error) {
      console.error(`Failed to create chat room: ${error}`);
    }
  };

  return (
    <div>
      <button onClick={() => onCreateChatRoom(adminId)}>Message</button>
    </div>
  );
};

export default CreateChatRoom;
