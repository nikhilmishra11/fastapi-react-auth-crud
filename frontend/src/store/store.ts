import { configureStore } from '@reduxjs/toolkit';
import authReducer from './authSlice';
import itemReducer from './itemSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    items: itemReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
