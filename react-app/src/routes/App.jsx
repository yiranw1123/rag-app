import React, {useState, useEffect} from 'react'
import api from '../api'
import CreateKBForm from '../components/createkbform'
import styles from "./App.module.css";
import KBTable from '../components/kbtable'
import UploadFileForm from '../components/uploadfileform';
import DetailsTable from '../components/detailstable';

const App = () => {
  const [knowledgebase, setKnowledgebase] = useState([]);
  const [showDetails, setShowDetails] = useState(false);
  const [selectedKB, setSelectedKB] = useState('');
  const [files, setFiles] = useState([]);

  const fetchFiles = async(kbId) =>{
    const response = await api.get(`/knowledgebase/${kbId}/files/`);
    console.log("successuflly fetched files");
    setFiles(response.data);
  };

  const fetchKnowledgebase = async() =>{
    const response = await api.get('/knowledgebase/');
    setKnowledgebase(response.data);
  };

  useEffect(() => {
    fetchKnowledgebase();
  }, []);

  const handleView = (kbId) => {
    setSelectedKB(kbId);
    fetchFiles(kbId);
    setShowDetails(true);
  };

  const handleDelete = async(kbId) => {
    try{
      await api.delete(`/knowledgebase/${kbId}`);
    }catch (error) {
      console.error("Error deleting KB:", error);
    }
    try{
      await fetchKnowledgebase();
    }catch (error) {
      console.error("Error fetching kB data:", error);
    }
  };

  const handleFileDelete = async(fileId, kbId) => {
    try{
      console.log(fileId);
      await api.delete(`/knowledgebasefile/${fileId}`);
    }catch (error) {
      console.error("Error deleting file:", error);
    }
    try{
      await fetchFiles(kbId);
    }catch (error) {
      console.error("Error fetching files:", error);
    }
  };

  return (
    <div className={styles.gridContainer}>
      <header className={styles.header}>
        <h1> KnowledgeBase</h1>
      </header>
      <main className={styles.main}>
        <div className={styles.upperMain}>
          <div className={styles.mainCreateForm}><CreateKBForm onFormSubmit={fetchKnowledgebase}/></div>
          <div className={styles.mainUploadForm}><UploadFileForm data={knowledgebase} onFormSubmit={fetchFiles} jumpToDetails={handleView}/></div>
        </div>
        <div className={styles.tableDisplay}>
          {!showDetails ? (
            <KBTable data={knowledgebase} rowsPerPage={10} onView={handleView} onDelete={handleDelete}></KBTable>
          ) : (
            <DetailsTable data={files} rowsPerPage={10} kbId={selectedKB}  onDelete={handleFileDelete} onBack={() => setShowDetails(false)}></DetailsTable>
          )}
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
