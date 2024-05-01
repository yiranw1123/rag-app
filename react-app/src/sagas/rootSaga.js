import { all, fork } from 'redux-saga/effects';
import chatSaga from './chatSaga';
import webSocketSaga from './webSocketSaga';

function * rootSaga(){
    yield all([
        chatSaga(),
        fork(webSocketSaga)
    ]);
}
export default rootSaga;