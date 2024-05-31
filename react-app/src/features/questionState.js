import { createSlice } from '@reduxjs/toolkit';

export const questionSlice = createSlice({
  name:"questionStore",
  initialState:{
    //Dictionary of list where key is chatId
    questions:[],
    filteredQuestions:[],
    selectedQuestion: null,
    isLoading:false,
    lastAdded:null,
    lastUpdated: null
  },
  reducers:{
    addQuestion:() => {},
    updateQuestionWithResponse:() =>{},
    addQuestionSuccess:(state) => {
      state.lastAdded = new Date().getTime();
    },
    updateQuestionSuccess:(state) => {
      state.lastUpdated = new Date().getTime();
    },
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
    clearQuestions:(state) => {
      state.questions = [];
    },
    storeQuestions:() =>{},
    setSelectedQuestion: (state, payload) => {
      state.selectedQuestion = payload;
    },
    setFilteredQuestions:(state, action) => {
      state.filteredQuestions = action.payload;
    },
  }
});

export const {
  addQuestion, addQuestionSuccess,
  updateQuestionWithResponse,updateQuestionSuccess,
  fetchQuestions, storeQuestions, setQuestions, clearQuestions,
  setSelectedQuestion,
  updateSelectedQuestion,
  setFilteredQuestions
} = questionSlice.actions;
export default questionSlice.reducer;

export const selectedQuestion= state => state.questionStore.selectedQuestion;
export const selectQuestions = state => {
  const { filteredQuestions, questions } = state.questionStore;
  // Check if filteredQuestions is not empty, if so, return it; otherwise, return all questions.
  return filteredQuestions.length > 0 ? filteredQuestions : questions;
};

export const getLastUpdated = state => state.questionStore.lastUpdated;
export const getLastAdded = state => state.questionStore.lastAdded;
