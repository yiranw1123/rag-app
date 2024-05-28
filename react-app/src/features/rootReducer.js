import { combineReducers } from "@reduxjs/toolkit";
import chatReducer from '../features/chatState';
import websocketReducer from '../features/webSocketState';
import questionReducer from './questionState';
import tagReducer from './tagState';

const rootReducer = combineReducers({
    chat: chatReducer,
    websocket: websocketReducer,
    questionStore:questionReducer,
    tagStore: tagReducer
});

export default rootReducer;