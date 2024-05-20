import React, { useRef, useState} from 'react';
import {CreateKBandUploadFile} from '../api';

const CreateKBForm = ({onFormSubmit})=> {
  const initialForm = {
    knowledgebase_name:"",
    description:""
  };
  const [form, setForm] = useState(initialForm);
  const [files, setFiles] = useState([]);
  const [isCreating, setIsCreating] = useState(false);
  const fileInputRef = useRef();

  const handleInputChange = (event) => {
    const value = event.target.value;
    
    setForm({
      ...form,
      [event.target.name] : value,
    });
  };

  const handleFilesChange = (event)=> {
    setFiles([...event.target.files]);
  }

  const handleSubmit = async (event) =>{
    event.preventDefault();

    if(files.length === 0){
      alert("No file is selected, please add files.");
      return;
    }

    setIsCreating(true);

    const createKBData = new FormData();
    
    Object.entries(form).forEach(([key, value]) => {
      console.log(`Appending form field: ${key}: ${value}`); 
      createKBData.append(key, value);
    });

    files.forEach((file, index) => {
      createKBData.append('files', file);
    });

    // Log formData entries
    for (let pair of createKBData.entries()) {
      console.log(`${pair[0]}: ${pair[1]}`);
    }
    
    
    try{
      await CreateKBandUploadFile(createKBData);
    } catch (error) {
      console.error("Error uploading files: ", error);
      throw error;
    } finally{
      // reset the form to empty for next req
      setForm(initialForm);
      if(fileInputRef.current){
        fileInputRef.current.value = '';
      }
      setIsCreating(false);
      onFormSubmit();
    };
  }

  return (
    <div className={'create-kb-form'}>
      <form onSubmit={handleSubmit}>
        <h2>Create Knowledgebase</h2>
        <div className='mb-3'>
          <label htmlFor='knowledgebase_name' className='form-label'>
            KnowledgeBase Name
          </label>
          <input type='text' className='form-control' id='knowledgebase_name' name='knowledgebase_name' onChange={handleInputChange} value={form.knowledgebase_name} autoComplete='off'></input>
        </div>

        <div className='mb-3'>
          <label htmlFor='description' className='form-label'>
            Description
          </label>
          <input type='text' className='form-control' id='description' name='description' onChange={handleInputChange} value={form.description}></input>
        </div>

        <div className='mb-3'>
          <label htmlFor='fupload' className='form-label'>
            Upload Files
          </label>
          <input type='file' className='form-control' id='fupload' name='fupload' onChange={handleFilesChange} multiple ref={fileInputRef}></input>
        </div>
        <button type="submit" className='btn btn-primary'>Create</button>
      </form>
      {isCreating && <span>Creating KnowledgeBase...</span>}
    </div>
  );
}

export default CreateKBForm;