import type { AppFieldExtendedReactFormApi } from "@tanstack/react-form";
import { createFormHook } from "@tanstack/react-form";
import type { ComponentProps } from "react";
import { Button, Input } from "tamagui";

import { FormReadyInput, SubmitButton } from "../components";

import { fieldContext, formContext } from "./formHookContexts";

const fieldComponents = {
  TextField: FormReadyInput,
  EmailField: (props: ComponentProps<typeof FormReadyInput>) => (
    <FormReadyInput type="email" autoCapitalize="none" {...props} />
  ),
  PasswordField: (props: ComponentProps<typeof FormReadyInput>) => (
    <FormReadyInput type="password" {...props} />
  ),
};

const formComponents = {
  SubmitButton,
};

/**
 * Form-level validator generics are `any` so this type accepts function validators,
 * standard schemas (e.g. Zod), and the matching `FormState` / error-map inference.
 * `TFormData` and field/form components stay precise.
 */
export type AppFormApi<TFormData> = AppFieldExtendedReactFormApi<
  TFormData,
  any,
  any,
  any,
  any,
  any,
  any,
  any,
  any,
  any,
  any,
  unknown,
  typeof fieldComponents,
  typeof formComponents
>;

export const { useAppForm, useTypedAppFormContext } = createFormHook({
  fieldComponents,
  fieldContext,
  formContext,
  formComponents,
});
