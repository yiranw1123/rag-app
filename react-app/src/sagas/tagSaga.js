import { takeEvery, select, put, call } from "redux-saga/effects";
import { clientDb } from "../db/clientDb";
import { setTags, getSelectedTags, setSelectedTags } from "../features/tagState";
import { selectQuestions } from "../features/questionState";

function* fetchTags(action){
  const {chatId} = action.payload;
  try {
    const allQuestions = yield clientDb.questionHistory
                                       .where('chatId')
                                       .equals(chatId)
                                       .toArray();

    const allTags = new Set(allQuestions.flatMap(q => q.tags));

    yield put(setTags(Array.from(allTags)));
  } catch (error) {
    console.error('Failed to fetch unique tags:', error);
  }
}

function* handleToggleTag(action){
  const currentSelectedTags = yield select(getSelectedTags);
  const tag = action.payload;
  // Determine if the tag is currently selected
  const isSelected = currentSelectedTags.includes(tag);

  // Create a new array with the tag toggled
  const newSelectedTags = isSelected 
  ? currentSelectedTags.filter(t => t !== tag)  // Remove the tag
  : [...currentSelectedTags, tag];              // Add the tag

  yield put(setSelectedTags(newSelectedTags));

  // Filter questions based on new selected tags
  if (newSelectedTags.length > 0) {
    const questions = yield select(selectQuestions);
    const filtered = questions.filter(question =>
      newSelectedTags.every(tag => question.tags && question.tags.includes(tag))
    );
    yield put(setFilteredQuestions(filtered));
  } else {
    // If no tags are selected, clear the filtered questions
    yield put(setFilteredQuestions([]));
  }
}

function* tagSaga(){
    yield takeEvery('tagStore/fetchTags', fetchTags);
    yield takeEvery('tagStore/toggleTag', handleToggleTag);
}
    
export default tagSaga;