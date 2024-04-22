import { useEffect, useState } from 'react';
import api from '../api';

const ChatList = () => {
  const [chats, setChats] = useState([]);

  const fetchChats = async() => {
    const response = await api.get('/chat/');
    setChats(response.data);
  };

  useEffect(() =>{
    fetchChats();
  });

  return (
    <div className='chatList'>
      {chats.map(chat =>(
        <div className="chatItem" key = {chat.id} onClick={() => onSelectChat(chat.id)}>
          {chat.name}
        </div>
      ))}
    </div>
  );

};
export default ChatList;