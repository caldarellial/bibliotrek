export type CollectedBook = {
  id: string;
  title: string;
  subtitle: string;
  isbn_10: string;
  isbn_13: string;
  thumbnail_url: string;
  authors: Author[];
};

export type Author = {
  created_at: string;
  updated_at: string | null;
  name: string;
  id: string;
};

export type BookCollectionSummary = {
  total: number;
};
