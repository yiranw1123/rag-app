import React, {useState, useEffect} from 'react'
import api from './api'
import CreateKBForm from './CreateKBForm'
import styles from "./App.module.css";
import Table from './components/table'

const App = () => {
  const [knowledgebase, setKnowledgebase] = useState([]);
  const [selectedKB, setSelectedKB]= useState("");

  const fetchKnowledgebase = async() =>{
    const response = await api.get('/knowledgebase/');
    setKnowledgebase(response.data)
  };

  useEffect(() => {
    fetchKnowledgebase();
  }, []);

  return (
    <div>
      <nav className='navbar navbar-dark bg-primary custom-navbar'>
        <div className='container-fluid'>
          <a className='navbar-brand' href='#'>
            KnowledgeBase
          </a>
        </div>
      </nav>
      <div className={styles.container}><CreateKBForm onFormSubmit={fetchKnowledgebase}/></div>
      <div className={styles.container}>
        <select onChange={(e) => setSelectedKB(e.target.value)} value={selectedKB} id='kb-dropdown'>
          <option value="">Select a Knowledgebase</option>
          {knowledgebase.map((kb) => (
            <option key={kb.id} value={kb.id}>{kb.name}</option>
          ))}
        </select>
      </div>
      <div className={styles.container}>
        <Table data={knowledgebase} rowsPerPage={5}></Table>
      </div>
    </div>
  )
};

export default App;
