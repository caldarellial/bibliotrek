import { useRouter, Stack } from "expo-router";
import { Card, View, Text } from "tamagui";
import { AuthFormProvider, useAuthStore } from "features/auth";
import { useEffect } from "react";

export default function AuthLayout() {
  const { accessToken } = useAuthStore();
  const router = useRouter();

  useEffect(() => {
    if (accessToken) {
      router.replace("/main");
    }
  }, [accessToken]);

  return (
    <AuthFormProvider>
      <View
        width="100%"
        height="100%"
        backgroundColor="#22415E"
        display="flex"
        justifyContent="center"
        alignItems="center"
      >
        <Card
          width="92%"
          maxWidth={480}
          minHeight={520}
          backgroundColor="white"
          padding="$4"
          borderRadius="$6"
        >
          <View
            marginBottom="$4"
            display="flex"
            justifyContent="center"
            alignItems="center"
          >
            <Text>Get started with Bibliotrek</Text>
          </View>
          <Stack
            screenOptions={{
              headerShown: false,
              contentStyle: { backgroundColor: "white" },
            }}
          />
        </Card>
      </View>
    </AuthFormProvider>
  );
}
