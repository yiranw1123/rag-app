import { createSelector, createSlice } from '@reduxjs/toolkit';

export const chatSlice = createSlice({
    name: 'chat',
    initialState:{
        activeChat: null,
        isLoading: false,
        chatHistories:{},  //session_id: [msgs...]
        error: null
    },
    reducers:{
        fetchActiveChat: (state) => {
            state.isLoading = true;
        },
        getActiveChatSuccess: (state, action) => {
            state.activeChat = action.payload;
            state.isLoading = false;
        },
        getActiveChatFailure: (state) => {
            state.isLoading = false;
        },
        fetchChatHistory: (state) => {
            state.isLoading = true;
        },
        getHistorySuccess: (state, action) => {
            state.chatHistories[state.activeChat.id] = action.payload;
            state.isLoading = false;
        },
        getHistoryFailure: (state, action) => {
            state.isLoading = false;
            state.error = action.payload;
        },
        addMessage: (state, action) => {
            const {message} = action.payload;
            const chatId = state.activeChat.id;
            if(!state.chatHistories[chatId]){
                state.chatHistories[chatId] = [];
            }
            state.chatHistories[chatId].push(message);
        }
    }
});

export const {
    fetchActiveChat, 
    getActiveChatFailure, 
    getActiveChatSuccess,
    fetchChatHistory,
    getHistoryFailure,
    getHistorySuccess,
    addMessage
} = chatSlice.actions;
export default chatSlice.reducer;

const getChatHistories = state => state.chat.chatHistories;

export const selectChatHistoryById = createSelector(
    [getChatHistories, (state, chatId) =>  chatId],
    (chatHistories, chatId) => chatHistories[chatId] || []
);

export const selectActiveChatId = state => state.chat.activeChat?.id;