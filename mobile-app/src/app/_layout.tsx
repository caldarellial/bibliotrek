import { Slot } from "expo-router";
import { StatusBar } from "expo-status-bar";
import { TamaguiProvider, View, Text } from "tamagui";

import { config } from "../../tamagui.config";

export default function RootLayout() {
  return (
    <TamaguiProvider config={config} defaultTheme="light">
      <View width="100%" height="100%" backgroundColor="#22415E">
        <StatusBar style="auto" />
        <Slot />
      </View>
    </TamaguiProvider>
  );
}
