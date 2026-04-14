import { useQuery } from "@tanstack/react-query";
import { AxiosResponse } from "axios";
import { api } from "features/core";

import { BookCollectionSummary } from "../models";

export const useMyBookCollectionSummary = () => {
  return useQuery<
    AxiosResponse<BookCollectionSummary>,
    unknown,
    BookCollectionSummary
  >({
    queryKey: ["my-book-collection-summary"],
    queryFn: () =>
      api.get("/users/me/collected-books", {
        params: { page: 0, page_size: 0 },
      }),
    select: (data) => data.data,
  });
};
