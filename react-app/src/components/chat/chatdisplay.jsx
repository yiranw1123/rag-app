import { useDispatch, useSelector } from "react-redux";
import { fetchQuestions, selectedQuestion } from "../../features/questionState";
import styles from "./ChatDisplay.module.css";
import { useState, useEffect } from "react";
import { selectChatId } from "../../features/chatState";

const ChatDisplay = () => {
  const dispatch = useDispatch();
  const selectedQuestionState = useSelector(selectedQuestion);
  const chatId = useSelector(selectChatId);
  const[sources, setSources] = useState([]);
  const [expandedSources, setExpandedSources] = useState({});

  const toggleSource = (srcIdx) => {
    const key = `${srcIdx}`;
    setExpandedSources(prev => ({
      ...prev,
      [key]: !prev[key]
    }));
  };

  useEffect(() => {
    dispatch(fetchQuestions({chatId}));
  }, [chatId]);

  useEffect(() => {
    if (selectedQuestionState?.payload?.sources) {
      try {
        const {documents} = selectedQuestionState.payload.sources;
        setSources(documents);
      } catch (error) {
        console.error("Failed to parse sources", error);
        setSources([]);
      }
    }
  }, [selectedQuestionState?.payload?.sources]);

  if(!selectedQuestionState){
    return <div></div>;
  }
  
  const questionToDisplay = selectedQuestionState.payload;

  if(!questionToDisplay || ! questionToDisplay.question){
    return <div></div>;
  }

  return(
    <div className={styles.messageBlock}>
      <div className={`${styles.messageContent} ${styles.question}`}>
          {questionToDisplay?.question}
      </div>
      {questionToDisplay?.answer?.trim() && (
        <div className={`${styles.messageContent} ${styles.answer}`}>
          {questionToDisplay.answer}
        </div>
      )
}



      {sources && (
        <div className={styles.sourcesGrid}>
          {sources.map((source, srcIdx) => (
            <div key={srcIdx} className={`${styles.sourceItem} ${expandedSources[`${srcIdx}`] ? styles.expanded : styles.collapsed}`}
              onClick={() => toggleSource(srcIdx)}>
              {source.page_content}
            </div>
          ))}
        </div>
        )
      }
    </div>
  );
};
export default ChatDisplay;