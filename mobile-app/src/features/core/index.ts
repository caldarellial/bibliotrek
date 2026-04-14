import axios from "axios";
import * as SecureStore from "expo-secure-store";

export const api = axios.create({
  baseURL: process.env.EXPO_PUBLIC_API_URL,
  headers: {
    Authorization: `Bearer ${SecureStore.getItem("access_token")}`,
    "Content-Type": "application/json",
  },
});
