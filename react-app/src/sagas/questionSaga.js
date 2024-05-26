import { takeEvery, select, put, call } from "redux-saga/effects";
import { fetchChatHistoryById } from "../api";
import { selectedQuestion, setQuestions, setSelectedQuestion, updateSelectedQuestion } from "../features/questionState";
import {clientDb} from '../db/clientDb';
import { selectChatId } from "../features/chatState";

function* handleAddQuestion(action) {
  const {id, question} = action.payload;
  const chatId = yield select(selectChatId);
  const newQuestionData = {
    chatId: chatId.id,
    questionId: id,
    question: question,
    answer:'',
    sources:'',
    tags:[]
  }
  try {
    const id = yield clientDb.questionHistory.add(newQuestionData);
    console.log('Added question with ID:', id);
  } catch (error) {
    console.error('Error adding question to IndexedDB:', error);
  }
}

function* handleUpdateQuestionResponse(action){
  const {id, chat_id, answer, sources, tags, timestamp} = action.payload;
  //const chatId = yield select(selectChatId);
  const key = [chat_id, id];
  const currMessage = yield clientDb.questionHistory
    .where('[chatId+questionId]')
    .equals(key)
    .first();

  if (currMessage) {
    currMessage.answer = answer;
    currMessage.sources = sources;
    currMessage.tags = tags;
  } else {
    console.log('No existing question found to update');
  }

  const currSelectedQuestion = yield select(selectedQuestion);
  if (currSelectedQuestion.payload.id == currMessage.questionId){
    yield put(setSelectedQuestion(currMessage));
  }

  try{
    // Using 'put' to update the record as 'add' will not update an existing record but insert a new one
    const id = yield clientDb.questionHistory.put(currMessage);
    console.log('Updated question with ID:', id);
  } catch (error) {
    console.error('Error updating question in IndexedDB:', error);
  }
}

function* handleFetchQuestion(action){
  const {chatId} = action.payload;
  try{
    const questions = yield call(fetchChatHistoryById, chatId);
    // Write fetched questions to IndexedDB
    //yield call([clientDb.questionHistory, 'bulkPut'], questions); 
    yield put(setQuestions(questions));
  } catch (error){
    console.log("Error fetching questions..", error);
  }
}

function* questionSaga(){
  yield takeEvery('question/addQuestion', handleAddQuestion);
  yield takeEvery('question/updateQuestionWithResponse', handleUpdateQuestionResponse);
  yield takeEvery('question/fetchQuestions', handleFetchQuestion);
}
  
export default questionSaga;