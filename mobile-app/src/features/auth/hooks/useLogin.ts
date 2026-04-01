import { useMutation } from "@tanstack/react-query";
import { useShallow } from "zustand/react/shallow";

import { api } from "features/core";
import { useAuthStore } from "./useAuthStore";

export type LoginResponse = {
  access_token: string;
  token_type: string;
};

export type LoginRequest = {
  username: string;
  password: string;
};

export const useLogin = () => {
  const { setAccessToken, setTokenType } = useAuthStore(
    useShallow((state) => ({
      setAccessToken: state.setAccessToken,
      setTokenType: state.setTokenType,
    })),
  );

  return useMutation({
    mutationKey: ["login"],
    mutationFn: ({ username, password }: LoginRequest) =>
      api
        .post<LoginResponse>("/token", {
          username,
          password,
        })
        .then((res) => res.data),
    onSuccess: (data) => {
      setAccessToken(data.access_token);
      setTokenType(data.token_type);
    },
  });
};
