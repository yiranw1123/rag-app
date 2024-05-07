import {call, put, takeEvery } from "redux-saga/effects";
import { 
  fetchFilesListFailure, fetchFilesListSuccess
} from "../features/chatState";
import {fetchKBFiles} from '../api';

function* workGetActiveChat(action){
}

function* handleFetchFilesList(action){
    try{
        const kbId = action.payload;
        const filesList = yield call(fetchKBFiles, kbId);
        yield put(fetchFilesListSuccess(filesList));
    } catch(error){
        yield put(fetchFilesListFailure(error.toString()));
    }
}

function* chatSaga(){
    yield takeEvery('chat/fetchActiveChat', workGetActiveChat);
    yield takeEvery('chat/fetchFilesList', handleFetchFilesList);
}

export default chatSaga;