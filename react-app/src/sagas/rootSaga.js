import { all } from 'redux-saga/effects';
import activeChatSaga from './activeChatSaga';

function * rootSaga(){
    yield all([
        activeChatSaga(),
    ]);
}
export default rootSaga;