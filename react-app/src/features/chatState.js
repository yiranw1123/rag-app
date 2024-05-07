import { createSelector, createSlice } from '@reduxjs/toolkit';

export const chatSlice = createSlice({
    name: 'chat',
    initialState:{
        selectedKB: null,
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
        setConversationId:(state, action) => {
            state.conversationId = action.payload;
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
            state.chatHistories[state.activeChat.id] = action.payload;
            state.isLoading = false;
        },
        getHistoryFailure: (state, action) => {
            state.isLoading = false;
            state.error = action.payload;
        },
        addMessage: (state, action) => {
            const chatId = state.activeChat.id;
            if(!state.chatHistories[chatId]){
                state.chatHistories[chatId] = [];
            }
            state.chatHistories[chatId].push(action.payload);
        }
    }
});

export const {
    fetchChatHistory, getHistoryFailure, getHistorySuccess,
    addMessage,
    setSelectedKB,
    setConversationId,
    fetchFilesList, fetchFilesListFailure, fetchFilesListSuccess
} = chatSlice.actions;
export default chatSlice.reducer;

const getChatHistories = state => state.chat.chatHistories;

export const selectChatHistoryById = createSelector(
    [getChatHistories, (state, chatId) =>  chatId],
    (chatHistories, chatId) => chatHistories[chatId] || []
);

export const selectActiveChatId = state => state.chat.activeChat?.id;