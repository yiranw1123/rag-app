import React, { useRef, useState} from 'react';
import api from '../api';

const CreateKBForm = ({onFormSubmit})=> {
  const initialForm = {
    knowledgebase_name:"",
    description:""
  };
  const [form, setForm] = useState(initialForm);
  const [files, setFiles] = useState([]);
  const fileInputRef = useRef();

  const handleInputChange = (event) => {
    const value = event.target.value;
    
    setForm({
      ...form,
      [event.target.name] : value,
    });
  };

  const handleMultipleChange = (event)=> {
    setFiles([...event.target.files]);
  }

  const createKnowledgeBase = async (event) => {
    try {
      const response = await api.post('/knowledgebase/', form);
      if(response.status === 201){
        const kbId = response.data.kb_id;
        console.log(`Successfully created knowledgebase with id ${kbId}`);
        return kbId;
      } else{
        throw new Error(`Unexpected status code: ${response.status} `);
      }
    } catch (error) {
      console.error("Error creating knowledgebase: ", error);
      throw error; // Rethrow to handle in the caller function
    }
  }

  const handleMultipleSubmit = async (event) =>{
    event.preventDefault();

    const kbId = await createKnowledgeBase(form);
    const filesData = new FormData();

    files.forEach((file, index) => {
      filesData.append('files', file);
    });

    const config = {
      headers: {
        'content-type': 'multipart/form-data',
      },
    };
    
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
      // reset the form to empty for next req
      setForm(initialForm);
      if(fileInputRef.current){
        fileInputRef.current.value = '';
      }
      onFormSubmit(kbId);
    };
  }

  return (
    <div className={'create-kb-form'}>
      <form onSubmit={handleMultipleSubmit}>
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
          <input type='file' className='form-control' id='fupload' name='fupload' onChange={handleMultipleChange} multiple ref={fileInputRef}></input>
        </div>

        <button type="submit" className='btn btn-primary'>Create</button>
      </form>
    </div>
  );
}

export default CreateKBForm;