import type { AnyFieldApi } from "@tanstack/react-form";
import { Input, InputProps, View } from "tamagui";

export const FormReadyInput = ({
  field,
  ...props
}: {
  field: AnyFieldApi;
} & InputProps) => {
  return (
    <View>
      <Input
        value={String(field.state.value ?? "")}
        onChangeText={(value) => field.handleChange(value)}
        onBlur={() => field.handleBlur()}
        {...props}
      />
    </View>
  );
};
