import {call, put, takeEvery } from "redux-saga/effects";
import { 
  fetchFilesListFailure, fetchFilesListSuccess,
  getHistoryFailure,
  getHistorySuccess
} from "../features/chatState";
import {fetchKBFiles, fetchChatHistoryById} from '../api';

function* handleFetchFilesList(action){
  try{
    const kbId = action.payload;
    const filesList = yield call(fetchKBFiles, kbId);
    yield put(fetchFilesListSuccess(filesList));
  } catch(error){
    yield put(fetchFilesListFailure(error.toString()));
  }
}

function* handleFetchChatHistory(action){
  try{
    const chatId = action.payload;
    const chatHistory = yield call(fetchChatHistoryById, chatId);
    yield put(getHistorySuccess(chatHistory));
  } catch(error){
    yield put(getHistoryFailure(error.toString()));
  }
}

function* chatSaga(){
  yield takeEvery('chat/fetchFilesList', handleFetchFilesList);
  yield takeEvery('chat/fetchChatHistory', handleFetchChatHistory);
}

export default chatSaga;