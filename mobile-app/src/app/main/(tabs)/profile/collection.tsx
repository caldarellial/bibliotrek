import { BookCollection } from "features/book-collection/";
import { View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

export default function Collection() {
  return (
    <SafeAreaView>
      <View>
        <BookCollection />
      </View>
    </SafeAreaView>
  );
}
