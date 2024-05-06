import {takeEvery, call, put, } from 'redux-saga/effects';
import {
  addChatSessionSuccess, addChatSessionFailure,
  deleteChatSessionSuccess, deleteChatSessionFailure
} from '../features/clientDBState.js';
import {
  addChatSessionToDB, deleteChatSessionFromDB,
  addChatHistoryToDB, deleteChatHistoryFromDB
} from '../chatApi.js';


function* handleAddChatSession(action) {
  try {
    const params = action.payload;
    const baseData = {
      createTime: Date.now(),
      updateTime: Date.now(),
      knowledgeBaseId: params?.knowledgeBaseId || 0,
    };
    const newSession = yield call(addChatSessionToDB, baseData);
    yield put(addChatSessionSuccess(newSession));
  } catch(error) {
    yield put(addChatSessionFailure(error.toString()));
  }
}

function* handleDeleteChatSession(action) {
  try {
    yield call(deleteChatSessionFromDB, action.payload);
    yield put(deleteChatSessionSuccess(action.payload));
  } catch(error) {
    yield put(deleteChatSessionFailure(error.toString()));
  }
}

function* handleAddChatHistory(action) {
  try {
    const newHistory = yield call(addChatHistoryToDB, action.payload);
    yield put(addChatHistorySuccess(newHistory));
  } catch(error) {
    yield put(addChatHistoryFailure(error.toString()));
  }
}

function* handleDeleteChatHistory(action) {
  try {
    yield call(deleteChatHistoryFromDB, action.payload);
    yield put(deleteChatHistorySuccess(action.payload));
  } catch(error) {
    yield put(deleteChatHistoryFailure(error.toString()));
  }
}

function* clientDbSaga(){
  yield takeEvery('clientDB/addChatSession', handleAddChatSession);
  yield takeEvery('clientDB/deleteChatSession', handleDeleteChatSession);
  yield takeEvery('clientDB/addChatHistory', handleAddChatHistory);
  yield takeEvery('clientDB/deleteChatHistory', handleDeleteChatHistory);
}

export default clientDbSaga;