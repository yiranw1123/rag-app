import ChatList from '../components/chatlist';
import ChatWindow from '../components/chatwindow';
import styles from "./Chat.module.css";
import React, { useState } from 'react';


const Chat = () =>{
  //chat session id
  const [activeChat, setActiveChat] = useState('');

  return(
    <div className={styles.chatContainer}>
      <ChatList setActiveChat={setActiveChat}></ChatList>
      <ChatWindow activeChat={activeChat}></ChatWindow>
    </div>
  );

};

export default Chat;