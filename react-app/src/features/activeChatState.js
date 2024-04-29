import { createSlice } from '@reduxjs/toolkit';

export const activeChatSlice = createSlice({
    name: 'activeChat',
    initialState:{
        activeChat: null,
        isLoading: false
    },
    reducers:{
        fetchActiveChat: (state, action) => {
            state.isLoading = true;
        },
        getActiveChatSuccess: (state, action) => {
            state.activeChat = action.payload;
            state.isLoading = false;
        },
        getActiveChatFailure: (state) => {
            state.isLoading = false;
        }
    }
});

export const {fetchActiveChat, getActiveChatFailure, getActiveChatSuccess} = activeChatSlice.actions;
export default activeChatSlice.reducer;