import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';
import { RootState } from './store';

export interface Item {
  id: str;
  name: str;
  description?: str;
  price: number;
}

interface ItemState {
  items: Item[];
  status: 'idle' | 'loading' | 'succeeded' | 'failed';
  error: str | null;
}

const initialState: ItemState = {
  items: [],
  status: 'idle',
  error: null,
};

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8002';

export const fetchItems = createAsyncThunk('items/fetchItems', async (_, { getState }) => {
  const state = getState() as RootState;
  const response = await axios.get(`${API_URL}/items`, {
    headers: { Authorization: `Bearer ${state.auth.token}` }
  });
  return response.data;
});

export const createItem = createAsyncThunk('items/createItem', async (item: Omit<Item, 'id'>, { getState }) => {
  const state = getState() as RootState;
  const response = await axios.post(`${API_URL}/items`, item, {
    headers: { Authorization: `Bearer ${state.auth.token}` }
  });
  return response.data;
});

export const updateItem = createAsyncThunk('items/updateItem', async (item: Item, { getState }) => {
  const state = getState() as RootState;
  const response = await axios.put(`${API_URL}/items/${item.id}`, item, {
    headers: { Authorization: `Bearer ${state.auth.token}` }
  });
  return response.data;
});

export const deleteItem = createAsyncThunk('items/deleteItem', async (id: str, { getState }) => {
  const state = getState() as RootState;
  await axios.delete(`${API_URL}/items/${id}`, {
    headers: { Authorization: `Bearer ${state.auth.token}` }
  });
  return id;
});

const itemSlice = createSlice({
  name: 'items',
  initialState,
  reducers: {},
  extraReducers(builder) {
    builder
      .addCase(fetchItems.pending, (state) => { state.status = 'loading'; })
      .addCase(fetchItems.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.items = action.payload;
      })
      .addCase(fetchItems.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message || null;
      })
      .addCase(createItem.fulfilled, (state, action) => { state.items.push(action.payload); })
      .addCase(updateItem.fulfilled, (state, action) => {
        const index = state.items.findIndex(i => i.id === action.payload.id);
        if (index !== -1) state.items[index] = action.payload;
      })
      .addCase(deleteItem.fulfilled, (state, action) => {
        state.items = state.items.filter(i => i.id !== action.payload);
      });
  },
});

export default itemSlice.reducer;
