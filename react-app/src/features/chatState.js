import { createSelector, createSlice } from '@reduxjs/toolkit';

export const chatSlice = createSlice({
  name: 'chat',
  initialState:{
    selectedKB: null,
    chatId: null,
    kbFiles:[],
    isLoading: false,
    //Dictionary of list where key is chatId
    chatHistories:{},
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
    },
    fetchChatHistory: (state) => {
      state.isLoading = true;
    },
    getHistorySuccess: (state, action) => {
      state.chatHistories[state.chat.chatId] = action.payload;
      state.isLoading = false;
    },
    getHistoryFailure: (state, action) => {
      state.isLoading = false;
      state.error = action.payload;
    },
    addMessage: (state, action) => {
      const chatId = state.chatId.id;
      if(!state.chatHistories[chatId]){
          state.chatHistories[chatId] = [];
      }
      state.chatHistories[chatId].push(action.payload);
    }
  }
});

export const {
  addMessage,
  setSelectedKB,
  setChatId,
  fetchFilesList, fetchFilesListFailure, fetchFilesListSuccess,
  fetchChatHistory, getHistoryFailure, getHistorySuccess,
} = chatSlice.actions;
export default chatSlice.reducer;

const getChatHistories = state => state.chat.chatHistories;

export const selectChatHistoryById = createSelector(
    [getChatHistories, (chatId) => chatId],
    (chatHistories, chatId) => chatHistories[chatId] || []
);