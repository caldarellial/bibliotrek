import { useInfiniteQuery } from "@tanstack/react-query";

import { api } from "features/core";
import { CollectedBook } from "../models";
import { AxiosResponse } from "axios";

export const useMyBookCollection = () => {
  return useInfiniteQuery<
    AxiosResponse<{ books: CollectedBook[] }>,
    Error,
    CollectedBook[],
    string[],
    number
  >({
    queryKey: ["my-book-collection"],
    queryFn: ({ pageParam = 0 }) =>
      api.get("/users/me/collected-books", { params: { page: pageParam } }),
    getNextPageParam: (_lastPage, _allPages, lastPageParam) =>
      lastPageParam + 1,
    initialPageParam: 0,
    select: (data) => data.pages.flatMap((page) => page.data.books),
  });
};
