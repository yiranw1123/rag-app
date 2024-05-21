import { createSelector, createSlice } from '@reduxjs/toolkit';

export const chatSlice = createSlice({
  name: 'chat',
  initialState:{
    selectedKB: null,
    chatId: null,
    kbFiles:[],
    isLoading: false,
    //Dictionary of list where key is chatId
    questions:[],
    filteredQuestions:[],
    selectedQuestion: null,
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
    },
    fetchQuestions: (state) => {
      state.isLoading = true;
    },
    setQuestions: (state) => {
      state.isLoading = true;
    },
    selectQuestion:(state) => {

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