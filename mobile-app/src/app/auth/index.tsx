import { Link } from "expo-router";
import { useAuthFormStore } from "features/auth";
import { useTranslation } from "react-i18next";
import { Separator, Spacer, YStack } from "tamagui";

export default function Signup() {
  const { t } = useTranslation("auth");
  const registerForm = useAuthFormStore((state) => state.registerForm);

  return (
    <YStack alignItems="center">
      <YStack gap="$4" backgroundColor="white" width="100%">
        <registerForm.AppField name="username">
          {(field) => <field.EmailField placeholder="Email" field={field} />}
        </registerForm.AppField>
        <registerForm.AppField name="password">
          {(field) => (
            <field.PasswordField placeholder="Password" field={field} />
          )}
        </registerForm.AppField>
        <registerForm.AppForm>
          <registerForm.SubmitButton>{t("signUp")}</registerForm.SubmitButton>
        </registerForm.AppForm>
      </YStack>
      <Spacer />
      <Separator width="50%" />
      <Spacer />
      <Link href="/auth/login">{t("alreadyHaveAnAccount")}</Link>
    </YStack>
  );
}
