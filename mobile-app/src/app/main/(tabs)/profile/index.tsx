import { useRouter } from "expo-router";
import { BookCollectionSummaryComponent } from "features/book-collection";
import { TouchableOpacity } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { View } from "tamagui";

export default function ProfileTab() {
  const router = useRouter();
  return (
    <SafeAreaView>
      <View>
        <TouchableOpacity
          onPress={() => router.push("/main/profile/collection")}
        >
          <BookCollectionSummaryComponent />
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}
