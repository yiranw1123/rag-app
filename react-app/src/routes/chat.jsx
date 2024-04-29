import ChatList from '../components/chatlist';
import ChatWindow from '../components/chatwindow';
import styles from "./Chat.module.css";
import { useSelector, useDispatch } from 'react-redux';
import React, { useEffect } from 'react';
import {useParams} from 'react-router-dom';
import { fetchActiveChat } from "../features/activeChatState";

const Chat = () =>{
  const dispatch = useDispatch();
  const {id} = useParams();
  const activeChat = useSelector(state =>state.activeChat.activeChat);
  console.log(activeChat);
  const isLoading = useSelector(state => state.activeChat.isLoading);

  useEffect(() => {
    const loadChat = async () =>{
      if(id) {
        dispatch(fetchActiveChat(id));
      }
    };
    loadChat();
  }, [id, dispatch]);

  return(
    <div className={styles.chatContainer}>
      <ChatList/>
      <ChatWindow/>
    </div>
  );
};

export default Chat;