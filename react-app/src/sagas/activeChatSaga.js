import {call, put, takeEvery } from "redux-saga/effects";
import { getActiveChatSuccess, getActiveChatFailure } from "../features/activeChatState";
import {fetchChatById} from '../api';

function* workGetActiveChat(action){
    try{
        const chatData = yield call(fetchChatById, action.payload);
        yield put(getActiveChatSuccess(chatData));
    } catch(error){
        console.error("Failed to fetch chat data: ", error);
        yield put(getActiveChatFailure(error.message));
    }
}

function* activeChatSaga(){
    yield takeEvery('activeChat/fetchActiveChat', workGetActiveChat);
}

export default activeChatSaga;