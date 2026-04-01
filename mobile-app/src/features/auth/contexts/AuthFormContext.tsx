import type { AppFormApi } from "features/form";
import { useAppForm } from "features/form";
import {
  createContext,
  useContext,
  useLayoutEffect,
  useRef,
  type ReactNode,
} from "react";
import { useStore } from "zustand";
import { createStore, type StoreApi } from "zustand/vanilla";
import { z } from "zod";
import { useLogin, useRegister } from "../hooks";

export type AuthFormValues = {
  username: string;
  password: string;
};

export type AuthFormContextType = {
  loginForm: AppFormApi<AuthFormValues>;
  registerForm: AppFormApi<AuthFormValues>;
};

function createAuthFormStore(defaults: AuthFormContextType) {
  return createStore<AuthFormContextType>(() => ({
    loginForm: defaults.loginForm,
    registerForm: defaults.registerForm,
  }));
}

export const AuthFormStoreContext =
  createContext<StoreApi<AuthFormContextType> | null>(null);

export const AuthFormProvider = ({ children }: { children: ReactNode }) => {
  const { mutateAsync: login } = useLogin();
  const { mutateAsync: register } = useRegister();

  const storeRef = useRef<ReturnType<typeof createAuthFormStore> | null>(null);

  const loginForm = useAppForm({
    defaultValues: {
      username: "",
      password: "",
    },
    validators: {
      onChange: z.object({
        username: z.string().email(),
        password: z.string().min(4),
      }),
    },
    onSubmit: async (values) => {
      await login({
        username: values.value.username,
        password: values.value.password,
      });
    },
  });
  const registerForm = useAppForm({
    defaultValues: {
      username: "",
      password: "",
    },
    validators: {
      onChange: z.object({
        username: z.string().email(),
        password: z.string().min(8),
      }),
    },
    onSubmit: async (values) => {
      await register({
        username: values.value.username,
        password: values.value.password,
      });
    },
  });

  if (!storeRef.current) {
    storeRef.current = createAuthFormStore({ loginForm, registerForm });
  }
  const store = storeRef.current;

  useLayoutEffect(() => {
    store.setState({ loginForm, registerForm });
  }, [loginForm, registerForm, store]);

  return (
    <AuthFormStoreContext.Provider value={store}>
      {children}
    </AuthFormStoreContext.Provider>
  );
};

export function useAuthFormStore<T>(
  selector: (state: AuthFormContextType) => T,
): T {
  const store = useContext(AuthFormStoreContext);
  if (!store) {
    throw new Error("useAuthFormStore must be used within AuthFormProvider");
  }
  const selected = useStore(store, selector);

  return selected;
}
