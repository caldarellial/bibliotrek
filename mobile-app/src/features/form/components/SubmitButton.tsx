import { useStore } from "@tanstack/react-form";
import { Button, Spinner } from "tamagui";
import { useState } from "react";

import { useAppFormContext } from "../hooks/formHookContexts";

export const SubmitButton = ({ children }: { children: React.ReactNode }) => {
  const form = useAppFormContext();
  const [submitting, setSubmitting] = useState(false);
  const isValid = useStore(form.store, (state) => state.isValid);
  console.log(isValid);
  return (
    <Button
      onPress={() => {
        setSubmitting(true);
        form.handleSubmit().finally(() => {
          setSubmitting(false);
        });
      }}
      theme="accent"
      disabled={submitting || !isValid}
      opacity={!isValid ? 0.5 : 1}
    >
      {submitting ? <Spinner /> : children}
    </Button>
  );
};
