import { createSlice } from '@reduxjs/toolkit';

export const tagSlice = createSlice({
  name:"tagStore",
  initialState:{
    //Dictionary of list where key is chatId
    tags:[],
    selectedTags: [],
    isLoading:false
  },
  reducers:{
    fetchTags: (state) => {
      state.isLoading = true;
    },
    setTags:(state, action) => {
      const {payload} = action;
      state.tags = payload;
    },
    toggleTag: (state, action) => {

    },
    setSelectedTags:(state, action) => {
      const {payload} = action;
      state.selectedTags = payload;

    }
  }
});

export const {
  setTags,
  fetchTags,
  toggleTag,
  setSelectedTags
} = tagSlice.actions;
export default tagSlice.reducer;

export const selectTags = state => state.tagStore.tags;
export const getSelectedTags = state => state.tagStore.selectedTags