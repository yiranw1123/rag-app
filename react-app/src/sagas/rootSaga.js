import { all, fork } from 'redux-saga/effects';
import chatSaga from './chatSaga';
import webSocketSaga from './webSocketSaga';
import questionSaga from './questionSaga';

function* rootSaga(){
  yield all([
    fork(chatSaga),
    fork(webSocketSaga),
    fork(questionSaga)
  ]);
}

export default rootSaga;