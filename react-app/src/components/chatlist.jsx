import { useEffect, useState } from 'react';
import {fetchAllKB, fetchChats, createChat} from '../api';
import styles from "./ChatList.module.css";
import { useNavigate } from "react-router-dom";

const ChatList = ({setActiveChat}) => {
  const [selectedKB, setSelectedKB] = useState("");
  const navigate = useNavigate();
  const [chats, setChats] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [knowledgebase, setKnowledgebase] = useState([]);

  const resetSelection = () => {
    setSelectedKB("");
  }

  const goToChat = async () =>{
    try{
      const data = await createChat(selectedKB);
      navigate(`/chat/${data.id}`);
    } catch (error) {
      console.error("Error fetching chat:", error);
    }finally{
      resetSelection();
      setShowForm(false);
      const data = await fetchChats();
      console.log(data);
      setChats(data);
    }
  };

  const handleCreateChat = async () => {
    const kbs = await fetchAllKB();
    setKnowledgebase(kbs);
    setShowForm(!showForm);  // Toggle the visibility of the form
  };

  const onSelectChat = (chat) => {
    navigate(`/chat/${chat.id}`)
    setActiveChat(chat);
  };

  useEffect(() =>{
    const fetchAndSetChats = async () => {
      try{
        const data = await fetchChats();
        console.log(data);
        setChats(data);
      } catch(error){
        console.error('Failed to fetch chats:', error);
      }
    };
    fetchAndSetChats();
  }, []);

  return (
    <div className={styles.chatListContainer}>
      <div className={styles.listHeader}>
        <h3>All Chats  ({chats.length})</h3>
        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" className="bi bi-plus-lg" viewBox="0 0 16 16" onClick={handleCreateChat}>
          <path fillRule="evenodd" d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2"/>
        </svg>
      </div>

      <div>
        {showForm &&
          <div className="form-container">
            <select className="form-select" value={selectedKB} onChange={e => setSelectedKB(e.target.value)} id="kb-dropdown">
              <option value="">Select a KnowledgeBase</option>
              {knowledgebase.map((kb) => (
                <option key={kb.id} value={kb.id}>{`${kb.id}: ${kb.name}`}</option>
              ))}
            </select>
            <div className={styles.submitButton}>
              <button type="button" className="btn btn-primary" onClick={goToChat}>Submit</button>
            </div>
          </div>
        }
      </div>

      {chats.map(chat =>(
        <div key = {chat.id} className={styles.chatItem} onClick={() => onSelectChat(chat)}>
          {chat.chat_name}
        </div>
      ))}
    </div>
  );

};
export default ChatList;