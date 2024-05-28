import { createSlice } from '@reduxjs/toolkit';

export const questionSlice = createSlice({
  name:"questionStore",
  initialState:{
    //Dictionary of list where key is chatId
    questions:[],
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
    setQuestions:(state, action) => {
      const {payload} = action;
      state.questions = payload;
    },
    storeQuestions:() =>{

    },
    setSelectedQuestion: (state, payload) => {
      state.selectedQuestion = payload;
    },
    updateSelectedQuestion:() => {

    },
    setFilteredQuestion:(state, action) => {
      state.filteredQuestions = action.payload;
    },
  }
});

export const {
  addQuestion,
  updateQuestionWithResponse,
  fetchQuestions, storeQuestions, setQuestions,
  setSelectedQuestion,
  updateSelectedQuestion,
  setFilteredQuestion
} = questionSlice.actions;
export default questionSlice.reducer;

export const selectedQuestion= state => state.questionStore.selectedQuestion;
export const selectQuestions= state => state.questionStore.questions;