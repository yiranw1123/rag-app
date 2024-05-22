import { createSelector, createSlice } from '@reduxjs/toolkit';

export const chatSlice = createSlice({
  name: 'chat',
  initialState:{
    selectedKB: null,
    chatId: null,
    kbFiles:[],
    isLoading: false,
    tags:[],
    selectedTags:[],
    error: null
  },
  reducers:{
    setSelectedKB: (state, action) => {
      state.selectedKB = action.payload;
    },
    setChatId:(state, action) => {
      state.chatId = action.payload;
    },
    fetchFilesList:(state) => {
      state.isLoading = true;
    },
    fetchFilesListSuccess:(state, action)=>{
      state.kbFiles = action.payload;
      state.isLoading = false;
    },
    fetchFilesListFailure:(state, action)=>{
      state.isLoading = false;
      state.error = action.payload;
    }
  }
});

export const {
  addQuestion,
  setSelectedKB,
  setChatId,
  fetchFilesList, fetchFilesListFailure, fetchFilesListSuccess,
  fetchChatHistory, getHistoryFailure, getHistorySuccess,
} = chatSlice.actions;
export default chatSlice.reducer;

export const selectChatId = state => state.chat.chatId;
