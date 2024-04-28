import ChatList from '../components/chatlist';
import ChatWindow from '../components/chatwindow';
import styles from "./Chat.module.css";
import React, { useEffect, useState } from 'react';
import {useParams} from 'react-router-dom';
import {fetchChatById} from '../api';
import { ActiveChatContext } from '../context/ActiveChatContext';

const Chat = () =>{
  const {id} = useParams();
  const [activeChat, setActiveChat] = useState(null);

  useEffect(() => {
    const fetchChat = async (id) => {
      if(id) {
        const chatDetail = await fetchChatById(id);
        setActiveChat(chatDetail);
      }
    };
    fetchChat(id);
  },[id, setActiveChat]);

  return(
    <div className={styles.chatContainer}>
      <ActiveChatContext.Provider value = {{activeChat, setActiveChat}}>
        <ChatList/>
        <ChatWindow/>
      </ActiveChatContext.Provider>
    </div>
  );
};

export default Chat;