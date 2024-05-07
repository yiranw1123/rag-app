import { createSlice } from '@reduxjs/toolkit';

export const webSocketSlice = createSlice({
    name:"websocket",
    initialState:{
        isConnected: false,
        error: null
    },
    reducers:{
        websocketConnecting: () =>{},
        websocketOpened: (state) => {
            state.isConnected = true;
        },
        websocketClosed: (state) => {
            state.isConnected = false;
            state.chatId = null;
        },
        websocketMessageReceived: (action) => {
            console.log("received message: ", action.payload);
        },
        websocketError: (state, action) => {
            state.error = action.payload;
        },
        sendMessage: () => {},
        websocketDisconnect:() => {}
    }
});

export const{
    websocketConnecting,
    websocketOpened,
    websocketClosed,
    websocketMessageReceived,
    websocketError,
    websocketDisconnect,
    sendMessage
} = webSocketSlice.actions;

export default webSocketSlice.reducer;