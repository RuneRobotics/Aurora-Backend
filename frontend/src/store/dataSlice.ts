import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { Data } from '../types';

interface DataState {
  data: Data | null;
}

const initialState: DataState = {
  data: null
};

const dataSlice = createSlice({
  name: 'data',
  initialState,
  reducers: {
    setData: (state, action: PayloadAction<Data>) => {
      state.data = action.payload;
    }
  }
});

export const { setData } = dataSlice.actions;
export default dataSlice.reducer;