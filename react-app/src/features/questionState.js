import { createSlice } from '@reduxjs/toolkit';

export const questionSlice = createSlice({
  name:"question",
  initialState:{
    //Dictionary of list where key is chatId
    questions:[],
    filteredQuestions:[],
    selectedQuestion: null,
    isLoading:false
  },
  reducers:{
    addQuestion:() => {

    },
    updateQuestionWithResponse:() =>{
      
    },
    fetchQuestions: (state) => {
      state.isLoading = true;
    },
    setQuestions:(state, payload) => {
      state.questions = payload;
    },
    setSelectedQuestion: (state) => {
    },
    setFilteredQuestion:(state) => {

    },
  }
});

export const {
  addQuestion,
  updateQuestionWithResponse,
  fetchQuestions,
  setQuestions
} = questionSlice.actions;
export default questionSlice.reducer;