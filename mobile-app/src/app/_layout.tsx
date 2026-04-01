import "../i18n";

import { Slot } from "expo-router";
import { StatusBar } from "expo-status-bar";
import { TamaguiProvider, View } from "tamagui";

import { config } from "../../tamagui.config";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient();

export default function RootLayout() {
  return (
    <TamaguiProvider config={config} defaultTheme="light">
      <QueryClientProvider client={queryClient}>
        <View width="100%" height="100%">
          <StatusBar style="auto" />
          <Slot />
        </View>
      </QueryClientProvider>
    </TamaguiProvider>
  );
}
