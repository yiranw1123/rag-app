import {call, put, takeEvery } from "redux-saga/effects";
import { 
    getActiveChatSuccess,
    getActiveChatFailure,
    addMessage,
    getHistorySuccess,
    getHistoryFailure,
} from "../features/chatState";
import {fetchChatById, fetchChathistoryById} from '../api';

function* workGetActiveChat(action){
    try{
        const chatData = yield call(fetchChatById, action.payload);
        yield put(getActiveChatSuccess(chatData));
    } catch(error){
        console.error("Failed to fetch chat data: ", error);
        yield put(getActiveChatFailure(error.message));
    }
}

function* handleAddMsgToHistory(action){

}

function* handleFetchChatHistory(action){
    try{
        const {activeChatId} = action.payload;
        const msgHistory = yield call(fetchChathistoryById, activeChatId);
        yield put(getHistorySuccess(msgHistory));
    } catch(error){
        console.error("Failed to fetch chat data: ", error);
        yield put(getHistoryFailure(error.message));
    }
}

function* chatSaga(){
    yield takeEvery('chat/fetchActiveChat', workGetActiveChat);
    yield takeEvery('chat/fetchChatHistory', handleFetchChatHistory);
    yield takeEvery('chat/addMessage', handleAddMsgToHistory);
}

export default chatSaga;