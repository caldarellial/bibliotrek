import { Link } from "expo-router";
import { useAuthFormStore } from "features/auth";
import { useTranslation } from "react-i18next";
import { Button, Input, Separator, Spacer, YStack } from "tamagui";

export default function Login() {
  const { t } = useTranslation("auth");
  const loginForm = useAuthFormStore((state) => state.loginForm);
  return (
    <YStack alignItems="center">
      <YStack gap="$4" backgroundColor="white" width="100%">
        <loginForm.AppField name="username">
          {(field) => <field.EmailField placeholder="Email" field={field} />}
        </loginForm.AppField>
        <loginForm.AppField name="password">
          {(field) => (
            <field.PasswordField placeholder="Password" field={field} />
          )}
        </loginForm.AppField>
        <loginForm.AppForm>
          <loginForm.SubmitButton>{t("loginIn")}</loginForm.SubmitButton>
        </loginForm.AppForm>
      </YStack>
      <Spacer />
      <Separator width="50%" />
      <Spacer />
      <Link href="/auth">{t("dontHaveAnAccount")}</Link>
    </YStack>
  );
}
