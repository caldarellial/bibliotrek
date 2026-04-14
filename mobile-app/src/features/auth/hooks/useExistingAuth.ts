import * as SecureStore from "expo-secure-store";
import { useCallback } from "react";
import { useRefreshAuth } from "./useRefreshAuth";

export const useExistingAuth = () => {
  const { mutateAsync: refreshAuth } = useRefreshAuth();

  return useCallback((onSuccess: () => void, onFail: () => void) => {
    const existingRefreshToken = SecureStore.getItem("refresh_token");
    if (existingRefreshToken) {
      refreshAuth({ refresh_token: existingRefreshToken })
        .then(onSuccess)
        .catch(onFail);
    } else {
      onFail();
    }
  }, []);
};
