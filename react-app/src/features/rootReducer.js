import { combineReducers } from "@reduxjs/toolkit";
import chatReducer from '../features/chatState';
import websocketReducer from '../features/webSocketState';
import questionReducer from './questionState'

const rootReducer = combineReducers({
    chat: chatReducer,
    websocket: websocketReducer,
    question:questionReducer
});

export default rootReducer;