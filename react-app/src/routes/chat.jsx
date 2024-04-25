import ChatList from '../components/chatlist';
import ChatWindow from '../components/chatwindow';
import styles from "./Chat.module.css";
import React, { useEffect, useState } from 'react';
import {useParams} from 'react-router-dom';
import api from '../api';


const Chat = () =>{
  const {id} = useParams();
  //chat session id
  const [activeChat, setActiveChat] = useState(null);

  useEffect(() => {
    const fetchChatById = async (id) => {
      if(id) {
        const response = await api.get(`/chat/${id}`);
        setActiveChat(response.data);
      }
    };
    fetchChatById(id);
  },[id]);

  return(
    <div className={styles.chatContainer}>
      {activeChat ? (
        <>
          <ChatList setActiveChat={setActiveChat}/>
          <ChatWindow activeChat={activeChat}/>
        </>
      ):(<p>Loading</p>)}
    </div>
  );
};

export default Chat;