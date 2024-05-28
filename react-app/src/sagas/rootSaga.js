import { all, fork } from 'redux-saga/effects';
import chatSaga from './chatSaga';
import webSocketSaga from './webSocketSaga';
import questionSaga from './questionSaga';
import tagSaga from './tagSaga';

function* rootSaga(){
  yield all([
    fork(chatSaga),
    fork(webSocketSaga),
    fork(questionSaga),
    fork(tagSaga)
  ]);
}

export default rootSaga;