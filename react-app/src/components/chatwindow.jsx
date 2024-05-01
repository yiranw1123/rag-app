import { useState, useEffect, useContext } from "react";
import styles from "./ChatWindow.module.css";
import { useSelector, useDispatch } from 'react-redux';
import { 
  selectActiveChatId,
  selectChatHistoryById,
  fetchChatHistory,
  addMessage
} from "../features/chatState";
import { 
  sendMessage, 
  websocketConnecting, 
  websocketDisconnect 
} from "../features/webSocketState";


const ChatWindow = () => {
  const dispatch = useDispatch();
  const activeChat = useSelector(state => state.chat.activeChat);
  const activeChatId = useSelector(selectActiveChatId);
  const [message, setMessage] = useState('');
  const messages = useSelector(state => selectChatHistoryById(state, activeChatId));

  useEffect(() => {
    // Update the WebSocket URL when activeChat.id changes
    if(activeChatId){
      console.log("Effect run for activeChatId:", activeChatId);
      dispatch(websocketConnecting({activeChatId}));
      dispatch(fetchChatHistory({activeChatId}));
    }

    return () => {
      console.log("Cleaning up for activeChatId:", activeChatId);
      dispatch(websocketDisconnect());
    }
  }, [activeChatId, dispatch]); 

  const handleSendMessage =  async () => {
    dispatch(sendMessage(message));
    console.log("Sent msg: ", message);
    dispatch(addMessage({'sender': 'me', 'text':message}));
    setMessage(''); // Clear input
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  return(
    <div className = {styles.chatWindow}>
      <h3>{activeChat?.chat_name}</h3>
      <div className={styles.chatMessages}>
        {messages.map((msg, index) => (
          <div key={index} className={`${styles.messageBlock} ${msg.sender === 'me' ? styles.me : ''}`}>
            <div className={styles.senderName}>{msg.sender}</div>
            <div className={`${styles.messageContent} ${msg.sender === 'me' ? styles.me : ''}`}>
              {msg.text}
            </div>
          </div>
        ))}
      </div>
      <textarea className="form-control" id="chatInput" rows="4" onChange={(e) => setMessage(e.target.value)} value={message} placeholder="Type your question here..." onKeyDown={handleKeyDown}></textarea>
      <div className={styles.submitButton}>
        <button type="button" className="btn btn-primary" onClick={handleSendMessage}><i className="bi bi-send"></i> (Enter)</button>
      </div>
    </div>
  );
};
export default ChatWindow;