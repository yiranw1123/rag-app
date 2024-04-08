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
      <header className={styles.header}>
        <h1> KnowledgeBase</h1>
      </header>
      <main className={styles.main}>
        <div className={styles.upperMain}>
          <div className={styles.mainCreateForm}><CreateKBForm onFormSubmit={fetchKnowledgebase}/></div>
          <div className={styles.mainUploadForm}><UploadFileForm data={knowledgebase} onFormSubmit={fetchKnowledgebase}/></div>
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
