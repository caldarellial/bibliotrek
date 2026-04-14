import { create } from "zustand";
import * as SecureStore from "expo-secure-store";

export type AuthStore = {
  accessToken: string | null;
  setAccessToken: (accessToken: string) => void;
  clearAccessToken: () => void;
  tokenType: string | null;
  setTokenType: (tokenType: string) => void;
  refreshToken: string | null;
  setRefreshToken: (refreshToken: string) => void;
};

export const useAuthStore = create<AuthStore>((set) => ({
  accessToken: null,
  setAccessToken: (accessToken: string) => {
    SecureStore.setItem("access_token", accessToken);
    set({ accessToken });
  },
  clearAccessToken: () => {
    SecureStore.deleteItemAsync("access_token");
    set({ accessToken: null });
  },
  tokenType: null,
  setTokenType: (tokenType: string) => {
    SecureStore.setItem("token_type", tokenType);
    set({ tokenType });
  },
  refreshToken: null,
  setRefreshToken: (refreshToken: string) => {
    SecureStore.setItem("refresh_token", refreshToken);
    set({ refreshToken });
  },
}));
