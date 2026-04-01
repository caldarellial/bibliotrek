import * as SecureStore from "expo-secure-store";
import { useCallback } from "react";
import { useAuthStore } from "./useAuthStore";
import { useShallow } from "zustand/react/shallow";

export const useExistingAuth = () => {
  const { setAccessToken, setTokenType } = useAuthStore(
    useShallow((state) => ({
      setAccessToken: state.setAccessToken,
      setTokenType: state.setTokenType,
      accessToken: state.accessToken,
      tokenType: state.tokenType,
    })),
  );

  return useCallback(
    (onSuccess: () => void, onFail: () => void) => {
      const existingAccessToken = SecureStore.getItem("access_token");
      const existingTokenType = SecureStore.getItem("token_type");
      if (existingAccessToken && existingTokenType) {
        setAccessToken(existingAccessToken);
        setTokenType(existingTokenType);
        onSuccess();
      } else {
        onFail();
      }
    },
    [setAccessToken, setTokenType],
  );
};
