import {call, put, takeEvery } from "redux-saga/effects";
import { 
    getActiveChatSuccess,
    getActiveChatFailure,
    getHistorySuccess,
    getHistoryFailure,
} from "../features/chatState";

function* workGetActiveChat(action){
}

function* handleFetchChatHistory(action){
}

function* chatSaga(){
    yield takeEvery('chat/fetchActiveChat', workGetActiveChat);
    yield takeEvery('chat/fetchChatHistory', handleFetchChatHistory);
}

export default chatSaga;