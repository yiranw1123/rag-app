import { useEffect, useState } from 'react';
import api from '../api';
import styles from "./ChatList.module.css";
import {useNavigate} from "react-router-dom";

const ChatList = (setActiveChat) => {
  const navigate = useNavigate();
  const [chats, setChats] = useState([]);

  const fetchChats = async() => {
    const response = await api.get('/chat/');
    setChats(response.data);
  };

  const onSelectChat = (chatId) => {
    navigate(`/chat/${chatId}`)
    setActiveChat(chatId);
  };

  useEffect(() =>{
    fetchChats();
  }, []);

  return (
    <div className={styles.chatListContainer}>
      <div className={styles.listHeader}>
        <h3>All Chats</h3>
        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" className="bi bi-plus-lg" viewBox="0 0 16 16">
          <path fillRule="evenodd" d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2"/>
        </svg>
      </div>
      {chats.map(chat =>(
        <div key = {chat.id} className={styles.chatItem} onClick={() => onSelectChat(chat.id)}>
          {chat.chat_name}
        </div>
      ))}
    </div>
  );

};
export default ChatList;