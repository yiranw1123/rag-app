import React, {useState, useEffect} from 'react'
import './../node_modules/bootstrap/dist/css/bootstrap.min.css'
import api from './api'
import FileUploader from './FileUploader'

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
    <div>
      <nav className='navbar navbar-dark bg-primary'>
        <div className='container-fluid'>
          <a className='navbar-brand' href='#'>
            KnowledgeBase
          </a>
        </div>
      </nav>
      <div className='container'><FileUploader onFormSubmit={fetchKnowledgebase}/></div>
      <table className='table table-striped table-bordered table-hover' id='tableContainer'>
        <thead>
          <tr>
            <th>name</th>
            <th>id</th>
            <th>embedding</th>
            <th>created</th>
            <th>updated</th>
          </tr>
        </thead>
        <tbody>
          {knowledgebase.map((knowledgebase) => (
            <tr key={knowledgebase.id}>
              <td>{knowledgebase.name}</td>
              <td>{knowledgebase.embedding}</td>
              <td>{knowledgebase.created}</td>
              <td>{knowledgebase.updated}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
};

export default App;
