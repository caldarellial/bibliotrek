import { useMutation } from "@tanstack/react-query";
import { useShallow } from "zustand/react/shallow";

import { api } from "features/core";
import { useAuthStore } from "./useAuthStore";

export type RefreshAuthResponse = {
  access_token: string;
  token_type: string;
  refresh_token: string;
};

export type RefreshAuthRequest = {
  refresh_token: string;
};

export const useRefreshAuth = () => {
  const { setAccessToken, setTokenType, setRefreshToken } = useAuthStore(
    useShallow((state) => ({
      setAccessToken: state.setAccessToken,
      setTokenType: state.setTokenType,
      setRefreshToken: state.setRefreshToken,
    })),
  );

  return useMutation({
    mutationKey: ["login"],
    mutationFn: ({ refresh_token }: RefreshAuthRequest) =>
      api
        .post<RefreshAuthResponse>("/refresh-token", {
          refresh_token,
        })
        .then((res) => res.data),
    onSuccess: (data) => {
      setAccessToken(data.access_token);
      setTokenType(data.token_type);
      setRefreshToken(data.refresh_token);
    },
  });
};
