import React, {useEffect, useRef, useState} from 'react';
import api from '../api';

const UploadFileForm = ({data, onFormSubmit, jumpToDetails}) => {
  const [selectedKB, setSelectedKB] = useState("");
  const [files, setFiles] = useState([]);
  const fileInputRef = useRef();

  const handleMultipleChange = (event)=> {
    setFiles([...event.target.files]);
  }

  const resetSelection = () => {
    setSelectedKB("");
  }

  const handleMultipleSubmit = async (event) =>{
    event.preventDefault();

    const filesData = new FormData();

    files.forEach((file, index) => {
      filesData.append('files', file);
    });

    const config = {
      headers: {
        'content-type': 'multipart/form-data',
      },
    };

    const kbId = document.getElementById("kb-dropdown").value; 
    console.log(kbId);

    try{
      const response =  await api.post(`/knowledgebase/${kbId}/upload/`, filesData, config);
      if(response.status === 201){
        console.log('Successfully uploaded files to server');
      } else {
        throw new Error(`Unexpected status code: ${response.status} `);
      }
    } catch (error) {
      console.error("Error uploading files: ", error);
      throw error;
    } finally{
      // reset file pointer
      if(fileInputRef.current){
        fileInputRef.current.value = '';
      }
      resetSelection();
      await onFormSubmit(kbId);
    };
  }
  return(
    <div className={'upload-form'}>
      <form onSubmit={handleMultipleSubmit}>
        <h2>File Upload</h2>
        <label htmlFor="kb-dropdown">KnowledgeBase</label>
        <select className='form-select' value={selectedKB} onChange={e => setSelectedKB(e.target.value)} id='kb-dropdown'>
          <option value="">Select a KnowledgeBase</option>
          {data.map((kb) => (
            <option key={kb.id} value={kb.id}>{`${kb.id}:  ${kb.name}`}</option>
          ))}
        </select>
        <div className='mb-3'>
          <label htmlFor='fupload' className='form-label'>
            Upload Files
          </label>
          <input type='file' className='form-control' id='fupload' name='fupload' onChange={handleMultipleChange} multiple ref={fileInputRef}></input>
        </div>
        <button type="submit" className='btn btn-primary' onClick={() => jumpToDetails(document.getElementById("kb-dropdown").value)}>Upload</button>

      </form>
    </div>
  );
};

export default UploadFileForm;