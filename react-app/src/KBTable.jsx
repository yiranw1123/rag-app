import api from './api'
import React, {useState, useEffect} from 'react'

const KBTable = () =>{
  const [knowledgebase, setKnowledgebase] = useState([]);

  const fetchKnowledgebase = async() =>{
    const response = await api.get('/knowledgebase/');
    setKnowledgebase(response.data)
  };

  useEffect(() => {
    fetchKnowledgebase();
  }, []);

  return(
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
  )

};

export default KBTable;