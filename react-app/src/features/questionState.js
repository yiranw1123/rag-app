import { createSlice } from '@reduxjs/toolkit';

export const questionSlice = createSlice({
  name:"question",
  initialState:{
    //Dictionary of list where key is chatId
    questions:[],
    tags:[],
    filteredQuestions:[],
    selectedQuestion: null,
    isLoading:false
  },
  reducers:{
    addQuestion:() => {},
    updateQuestionWithResponse:() =>{},
    fetchQuestions: (state) => {
      state.isLoading = true;
    },
    fetchTags: (state) => {
      state.isLoading = true;
    },
    setQuestions:(state, payload) => {
      state.questions = payload;
    },
    setTags:(state, payload) => {
      state.tags = payload;
    },
    setSelectedQuestion: (state, payload) => {
      state.selectedQuestion = payload;
    },
    updateSelectedQuestion:() => {

    },
    setFilteredQuestion:(state) => {

    },
  }
});

export const {
  addQuestion,
  updateQuestionWithResponse,
  fetchQuestions,
  setQuestions,
  setSelectedQuestion,
  updateSelectedQuestion,
  setTags,
  fetchTags
} = questionSlice.actions;
export default questionSlice.reducer;

export const selectedQuestion= state => state.question.selectedQuestion;
export const selectQuestions= state => state.question.questions;
export const selectTags = state => state.question.tags;