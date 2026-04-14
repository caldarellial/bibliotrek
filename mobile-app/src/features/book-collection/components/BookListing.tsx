import { Image, View, Text } from "tamagui";

import { CollectedBook } from "../models";

export const BookListing = ({ book }: { book: CollectedBook }) => {
  return (
    <View>
      <Image src={book.thumbnail_url} />
      <Text>{book.title}</Text>
      <Text>{book.authors.map((author) => author.name).join(", ")}</Text>
    </View>
  );
};
