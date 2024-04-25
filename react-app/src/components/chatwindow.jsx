import { useState } from "react";
import styles from "./ChatWindow.module.css";
import useWebSocket from 'react-use-websocket';


const ChatWindow = ({activeChat}) => {
  const {id, chat_name} = activeChat;
  const socketUrl = `ws://127.0.0.1:8000/chat/${id}/ws`;
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);

  const {sendMessage, lastMessage, readyState} = useWebSocket(socketUrl,
    {
      onOpen: () => console.log("Connected to WebSocket"),
      onClose: () => console.log("Disconnected from WebSocket"),
      shouldReconnect: (closeEvent) => true,
      onMessage: (event) => {
        if(event.data){
          console.log("Received msg: ", event.data);
          setMessages(prevMessages => [...prevMessages, {sender: "assistant", text:event.data}]);
        }
      },
    }
  );

  const handleSendMessage =  async () => {
    sendMessage(message);
    setMessages(prevMessages => [...prevMessages, {sender: "me", text: message}]);
    console.log("Sent msg: ", message);
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
      <h3>{chat_name}</h3>
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