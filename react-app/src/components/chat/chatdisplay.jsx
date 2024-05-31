import { useSelector } from "react-redux";
import { selectedQuestion } from "../../features/questionState";
import styles from "./ChatDisplay.module.css";
import { useState, useEffect } from "react";

const ChatDisplay = () => {
  const selectedQuestionState = useSelector(selectedQuestion);
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
    if (selectedQuestionState?.payload?.sources) {
      try {
        const parsedSources = JSON.parse(selectedQuestionState.payload.sources);
        setSources(parsedSources.documents);
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
      <div className={`${styles.messageContent} ${styles.answer}`}>
          {questionToDisplay?.answer}
      </div>

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