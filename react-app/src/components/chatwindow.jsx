import { useState } from "react";
import styles from "./ChatWindow.module.css";
import api from '../api';

const ChatWindow = (activeChat) => {
  const [message, setMessage] = useState('');

  const sendMessage =  async () => {
    console.log("Setting message:", message);
    setMessage('');  // Clear input after sending
  };

  const onSend = async () => {
    await sendMessage();
    resposne = await api.post(`/chat/${activeChat}`)

    
  };

  return(
    <div className = {styles.chatWindow}>
      <div className={styles.chatMessages}>
        <p>This is a paragraph...</p>
      </div>

      <div className="mb-3">
        <label htmlFor="chatInput" className={styles.chatInput}>Input</label>
        <textarea className="form-control" id="chatInput" rows="3"></textarea>
        <button type="button" className="btn btn-primary" onClick={onSend}><i className="bi bi-send"></i> (Send)</button>
      </div>
    </div>
  );
};
export default ChatWindow;