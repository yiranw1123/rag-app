import React, {useRef, useState} from 'react';
import { uploadFile } from '../api';

const UploadFileForm = ({data, onFormSubmit, jumpToDetails}) => {
  const [selectedKB, setSelectedKB] = useState("");
  const [files, setFiles] = useState([]);
  const [isUploading, setIsUploading] = useState(false);
  const fileInputRef = useRef();

  const handleMultipleChange = (event)=> {
    setFiles([...event.target.files]);
  }

  const resetSelection = () => {
    setSelectedKB("");
  }

  const handleMultipleSubmit = async (event) =>{
    event.preventDefault();

    if(files.length === 0){
      alert("No file is selected");
      return;
    }

    const filesData = new FormData();

    files.forEach((file, index) => {
      filesData.append('files', file);
    });

    const kbId = document.getElementById("kb-dropdown").value; 

    //reset input files for next upload
    resetSelection();
    if(fileInputRef.current){
      fileInputRef.current.value = '';
    }
    setIsUploading(true);

    try{
      await uploadFile(kbId, filesData);
    } catch (error) {
      console.error("Error uploading files: ", error);
      throw error;
    } finally{
      setIsUploading(false);
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
      {isUploading && <span>Uploading Files to DB...</span>}
    </div>
  );
};

export default UploadFileForm;