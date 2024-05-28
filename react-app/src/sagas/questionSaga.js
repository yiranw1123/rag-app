import { takeEvery, select, put, call } from "redux-saga/effects";
import { fetchChatHistoryById } from "../api";
import { selectedQuestion, setQuestions, setSelectedQuestion, storeQuestions, updateSelectedQuestion } from "../features/questionState";
import {clientDb} from '../db/clientDb';
import { selectChatId } from "../features/chatState";
import Dexie from "dexie";

function* handleAddQuestion(action) {
  const {id, question} = action.payload;
  const chatId = yield select(selectChatId);
  const newQuestionData = {
    chatId: chatId,
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
    yield put(setQuestions(questions));
    yield put(storeQuestions(questions));

  } catch (error){
    console.log("Error fetching questions..", error);
  }
}

function prepareRecord(jsonObject) {
  const tagNames = jsonObject.tags.map(tag => tag.text);

  return {
    chatId: jsonObject.chat_id,
    questionId: jsonObject.id,
    question: jsonObject.question,
    answer: jsonObject.answer,
    sources: JSON.stringify(jsonObject.sources),  // Serialize complex nested objects
    tags: tagNames
  };
}

function* storeQuestionsToIndexDB(action){
  const questions = action.payload;
  const records = questions.map(prepareRecord);
  try {
    const existingQuestions = yield clientDb.questionHistory
                              .where('questionId')
                              .anyOf(records.map(r => r.questionId))
                              .toArray();
    
    // Create a Set of existing question IDs for quick lookup
    const existingQuestionIds = new Set(existingQuestions.map(q => q.questionId));

    // Filter out records that are already in the database
    const newRecords = records.filter(record => !existingQuestionIds.has(record.questionId));

    if(newRecords.length){
      // Use call effect for better testability and control over async operations
      yield call(() =>
        clientDb.transaction('rw', clientDb.questionHistory, async () => {
          await clientDb.questionHistory.bulkAdd(newRecords);
        }));
        console.log("Records added successfully!");
    }
  } catch (e) {
    if (e instanceof Dexie.BulkError) {
      console.error("Some records failed to add:", e.failures);
    } else {
      console.error("Failed to store data in IndexedDB:", e);
    }
  }
}

function* questionSaga(){
  yield takeEvery('questionStore/addQuestion', handleAddQuestion);
  yield takeEvery('questionStore/updateQuestionWithResponse', handleUpdateQuestionResponse);
  yield takeEvery('questionStore/fetchQuestions', handleFetchQuestion);
  yield takeEvery('questionStore/storeQuestions', storeQuestionsToIndexDB);
}
  
export default questionSaga;