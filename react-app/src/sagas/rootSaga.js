import { all, fork } from 'redux-saga/effects';
import chatSaga from './chatSaga';
import webSocketSaga from './webSocketSaga';

function * rootSaga(){
    yield all([
        fork(chatSaga),
        fork(webSocketSaga),
    ]);
}
export default rootSaga;