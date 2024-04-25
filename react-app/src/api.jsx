import axios from 'axios';

const api = axios.create({
    baseURL:"http://127.0.0.1:8000",
});
export default api;

// KB CRUD
export const createKB = async(form) =>{
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
};

export const fetchAllKB = async () => {
    try{
        const response = await api.get('/knowledgebase/');
        return response.data;
    } catch (error){
        console.error("Failed to fetch all KB: ", error);
        throw error;
    }
};

export const deleteKB = async(kbId) =>{
    try{
        await api.delete(`/knowledgebase/${kbId}`);
      }catch (error) {
        console.error("Error deleting KB:", error);
      }
};

// KB Files CRUD
export const fetchKBFiles = async (kbId) => {
    try{
        const response = await api.get(`/knowledgebase/${kbId}/files/`);
        console.log("successuflly fetched files");
        return response.data;
    } catch (error){
        console.error("Failed to fetch KB files: ", error);
        throw error;
    }
};

export const deleteKBFile = async(fileId, kbId) => {
    try{
        await api.delete(`/knowledgebasefile/${fileId}`);
      }catch (error) {
        console.error("Error deleting file:", error);
      }
};

export const uploadFile = async (kbId, filesData) =>{
    try{
        const config = {
            headers: {
              'content-type': 'multipart/form-data',
            }
        };
        const response =  await api.post(`/knowledgebase/${kbId}/upload/`, filesData, config);
        if(response.status === 201){
          console.log('Successfully uploaded files to server');
        } else {
          throw new Error(`Unexpected status code: ${response.status} `);
        }
      } catch (error) {
        console.error("Error uploading files: ", error);
        throw error;
      } 
};

//Chat CRUD
export const fetchChatById = async (id) => {
    const response = await api.get(`/chat/${id}`);
    return response.data;
};

export const createChat = async (kbId) => {
    try{
        response = await api.get(`/chat/kb_id/${kbId}`);
        if(response.status !== 200){
            throw new Error("Network response was not ok " + response.statusText);
        }
        return response.data;
    } catch (error) {
        console.error("Error fetching chat:", error);
    }
};

export const fetchChats = async() => {
    const response = await api.get('/chat/');
    return response.data;
  };