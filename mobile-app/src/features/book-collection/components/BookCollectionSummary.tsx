import { Text, View } from "tamagui";
import { useMyBookCollectionSummary } from "../hooks";

export const BookCollectionSummaryComponent = () => {
  const { data, isLoading, isError } = useMyBookCollectionSummary();
  return (
    <View>
      <Text>{data?.total} Books</Text>
    </View>
  );
};
