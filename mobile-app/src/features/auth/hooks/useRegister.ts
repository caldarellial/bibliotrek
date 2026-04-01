import { useMutation } from "@tanstack/react-query";

import { api } from "features/core";
import { useLogin, LoginResponse } from "./useLogin";

export type RegisterResponse = {
  message: string;
  user: string;
};

export type RegisterRequest = {
  username: string;
  password: string;
};

export const useRegister = () => {
  const { mutateAsync: login } = useLogin();

  return useMutation({
    mutationKey: ["register"],
    mutationFn: ({ username, password }: RegisterRequest) =>
      api
        .post<RegisterResponse>("/register", {
          username,
          password,
        })
        .then<LoginResponse>((res) => {
          if (res.status === 200) {
            return login({ username, password });
          } else {
            throw new Error(res.data?.message);
          }
        }),
  });
};
