import { all, fork } from 'redux-saga/effects';
import chatSaga from './chatSaga';
import webSocketSaga from './webSocketSaga';
import clientDbSaga from './clientDbSaga';

function * rootSaga(){
    yield all([
        fork(chatSaga),
        fork(webSocketSaga),
        fork(clientDbSaga)
    ]);
}
export default rootSaga;