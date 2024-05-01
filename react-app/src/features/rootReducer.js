import { combineReducers } from "@reduxjs/toolkit";
import chatReducer from '../features/chatState';
import websocketReducer from '../features/webSocketState';

const rootReducer = combineReducers({
    chat: chatReducer,
    websocket: websocketReducer
});

export default rootReducer;