import { combineReducers } from "@reduxjs/toolkit";
import chatHistoryReducer from './chatHistoryReducer';
import activeChatReducer from '../features/activeChatState';

const rootReducer = combineReducers({
    activeChat: activeChatReducer,
    chatHistories: chatHistoryReducer,
});

export default rootReducer;