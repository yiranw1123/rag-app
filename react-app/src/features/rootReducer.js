import { combineReducers } from "@reduxjs/toolkit";
import chatReducer from '../features/chatState';
import websocketReducer from '../features/webSocketState';
import clientDBReducer from '../features/clientDBState';

const rootReducer = combineReducers({
    chat: chatReducer,
    websocket: websocketReducer,
    clientDb: clientDBReducer

});

export default rootReducer;