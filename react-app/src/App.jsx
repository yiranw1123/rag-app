import React, {useState, useEffect} from 'react'
import api from './api'
import CreateKBForm from './CreateKBForm'
import styles from "./App.module.css";
import Table from './components/table'
import UploadFileForm from './UploadFileForm';

const App = () => {
  const [knowledgebase, setKnowledgebase] = useState([]);

  const fetchKnowledgebase = async() =>{
    const response = await api.get('/knowledgebase/');
    setKnowledgebase(response.data)
  };

  useEffect(() => {
    fetchKnowledgebase();
  }, []);

  return (
    <div className={styles.gridContainer}>
      <header>
        <h1> KnowledgeBase</h1>
      </header>

      <aside className={styles.aside}>
        <div className={styles.asideCloseIcon}>
          <strong>&times;</strong>
        </div>
        <ul className={styles.asideList}>
          <li className={styles.asideListItem}>KnowledgeBase</li>
          <li className={styles.asideListItem}>Chat</li>
        </ul>
      </aside>

      <main className={styles.main}>
        <div className={styles.upperMain}>
          <div className={styles.mainCreateForm}><CreateKBForm/></div>
          <div className={styles.mainUploadForm}><UploadFileForm data={knowledgebase}/></div>
        </div>
        <div className={styles.mainKbtable}>
          <Table data={knowledgebase} rowsPerPage={5}></Table>
        </div>
      </main>
      <footer className={styles.footer}>
        <div className="footer_copyright">&copy;2024</div>
        <div className="footer_byline">Made with &hearts;</div>
      </footer>
    </div>
  )
};

export default App;
