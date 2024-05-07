import { createSlice } from '@reduxjs/toolkit';


const initialState= {
  isLoading: false,
  error: null,
  chatId: null
}

export const clientDBSlice = createSlice({
  name: 'clientDB',
  initialState,
  reducers:{
    addChatSession: (state) => {
      state.isLoading = true;
    },
    addChatSessionSuccess: (state, action) => {
      state.chatId = action.payload;
      state.isLoading = false;
    },
    addChatSessionFailure: (state, action) => {
      state.isLoading = false;
      state.error = action.payload;
    },
    deleteChatSession: (state) => {
      state.isLoading = true;
    },
    deleteChatSessionSuccess: (state) => {
      state.isLoading = false;
    },
    deleteChatSessionFailure: (state, action) => {
      state.isLoading = false;
      state.error = action.payload;
    },
    addChatHistory: (state) => {
      state.isLoading = true;
    },
    addChatHistorySuccess: (state) => {
      state.isLoading = false;
    },
    addChatHistoryFailure: (state, action) => {
      state.isLoading = false;
      state.error = action.payload;
    },
    deleteChatHistory: (state) => {
      state.isLoading = true;
    },
    deleteChatHistorySuccess: (state) => {
      state.isLoading = false;
    },
    deleteChatHistoryFailure: (state, action) => {
      state.isLoading = false;
      state.error = action.payload;
    },
    getChatHistoryWithSessionId: (state) => {
      state.isLoading = true;
    },
    getChatHistoryWithSessionIdSuccess: (state) => {
      state.isLoading = false;
    },
    getChatHistoryWithSessionIdFaillure: (state, action) => {
      state.isLoading = false;
      state.error = action.payload;
    }
  }
});

export const {
  addChatHistory, addChatHistorySuccess, addChatHistoryFailure,
  deleteChatHistory, deleteChatHistoryFailure, deleteChatHistorySuccess,
  addChatSession, addChatSessionFailure, addChatSessionSuccess,
  deleteChatSession, deleteChatSessionFailure, deleteChatSessionSuccess
} = clientDBSlice.actions;

export default clientDBSlice.reducer;