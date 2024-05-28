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

import {addQuestion, updateQuestionWithResponse} from "../features/questionState";

function createWebSocketChannel(socket){
    return eventChannel(emit => {
        socket.onopen = () =>{
            emit(websocketOpened());
            console.log("connected to websocket");
        };
        socket.onmessage = (event) => {
            const response = JSON.parse(event.data);
            emit(websocketMessageReceived(response));
            emit(updateQuestionWithResponse(response));
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
    yield put(websocketOpened(chatId));
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
    const messageQueue = [];
    while(true){
        const {payload} = yield take(sendMessage);
        messageQueue.push(payload);
        while(messageQueue.length > 0 && socket.readyState === WebSocket.OPEN){
            const messageToSend = messageQueue.shift();
            try{
                socket.send(JSON.stringify(messageToSend));
                console.log("Dispatching addQuestion:", messageToSend);
                yield put(addQuestion(messageToSend));
            } catch (error) {
                messageQueue.unshift(messageToSend)
                yield put(websocketError("Failed to send message"));
                break;
            }
        }
    }
}

function* webSocketSaga(){
    while (true){
        const {payload} = yield take('websocket/websocketConnecting');
        const {chatId} = payload;
        if(chatId){
            const socket = yield call(initializeWebSocket, chatId);
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