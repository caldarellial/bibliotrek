import { ListItem, ScrollView } from "tamagui";

import { useMyBookCollection } from "../hooks";
import { BookListing } from "../components";

export const BookCollection = () => {
  const { data, isLoading, isError, fetchNextPage, hasNextPage } =
    useMyBookCollection();
  return (
    <ScrollView>
      <ListItem>
        {data?.map((book) => (
          <BookListing key={book.id} book={book} />
        ))}
      </ListItem>
    </ScrollView>
  );
};
