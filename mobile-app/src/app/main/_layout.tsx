import { Slot } from "expo-router";
import { View } from "tamagui";

export default function MainLayout() {
  return (
    <View width="100%" height="100%">
      <Slot />
    </View>
  );
}
