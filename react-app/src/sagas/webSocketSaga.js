import { fork, call, put, take, cancelled, cancel} from "redux-saga/effects";
import { eventChannel } from 'redux-saga';
import { 
    websocketConnecting,
    websocketClosed, 
    websocketMessageReceived,
    websocketOpened,
    websocketError,
    websocketDisconnect,
    sendMessage
} from "../features/webSocketState";

import {addMessage} from "../features/chatState";

function createWebSocketChannel(socket){
    return eventChannel(emit => {
        socket.onopen = () =>{
            emit(websocketOpened());
            console.log("connected to websocket");
        };
        socket.onmessage = (event) => {
            const message = event.data;
            emit(websocketMessageReceived(message));
            emit(addMessage(message));
        };
        socket.onclose = () => {
            emit(websocketClosed());
            console.log("disconnected from websocket");
        };
        socket.onerror = (error) => {
            emit(websocketError(error.message));
        };
        return () => {
            socket.close();
        };
    });
}

function* initializeWebSocket(chatId) {
    const socketUrl = `ws://127.0.0.1:8000/chat/${chatId}/ws`;
    const socket = new WebSocket(socketUrl);
    yield put(websocketConnecting(chatId));
    return socket;
}

function* createConnection(socket){
    const channel = yield call(createWebSocketChannel, socket);

    try{
        while(true) {
            const action = yield take(channel);
            yield put(action);
        } 
    } catch (error) {
        yield put(websocketError(error));
    }  finally {
        if(yield cancelled()){
            channel.close();
            socket.close();
            yield put(websocketClosed());
        }
    }
}

function* watchSendMessage(socket){
    while(true){
        const {payload} = yield take(sendMessage);
        try{
            if(socket.readyState === WebSocket.OPEN){
                socket.send(JSON.stringify(payload));
                emit(addMessage(payload));
            } else{
                yield put(websocketError('Socket is closed'));
            }
        } catch (error) {
        yield put(websocketError(error.toString()));
        }
    }
}

function* webSocketSaga(){
    while (true){
        const {payload} = yield take('websocket/websocketConnecting');
        if(payload.activeChatId){
            const socket = yield call(initializeWebSocket, payload.activeChatId);
            const task = yield fork(createConnection, socket);
            const sendMessageTask = yield fork(watchSendMessage, socket);
            yield take(websocketDisconnect);
            yield cancel(task);
            yield cancel(sendMessageTask);
            socket.close();

        }
    }
}

export default webSocketSaga;