from __future__ import annotations

from typing import TYPE_CHECKING, Annotated, Optional

from fastapi import Depends
from googleapiclient.discovery import Resource, build
from pydantic import BaseModel, ConfigDict

from app.config import get_settings

if TYPE_CHECKING:
  from googleapiclient._apis.books.v1 import BooksResource  # pyright: ignore[reportMissingModuleSource]
else:
  BooksResource = Resource

_settings = get_settings()


def get_google_books_service() -> BooksResource:
  return build("books", "v1", developerKey=_settings.google_discovery_api_key)


GoogleBooksServiceDep = Annotated[BooksResource, Depends(get_google_books_service)]  # pyright: ignore[reportGeneralTypeIssues]


class VolumeImageLinks(BaseModel):
  model_config = ConfigDict(extra="ignore")

  smallThumbnail: Optional[str] = None
  thumbnail: Optional[str] = None
  small: Optional[str] = None
  medium: Optional[str] = None
  large: Optional[str] = None
  extraLarge: Optional[str] = None


class IndustryIdentifier(BaseModel):
  model_config = ConfigDict(extra="ignore")

  type: str
  identifier: str


class VolumeDimensions(BaseModel):
  model_config = ConfigDict(extra="ignore")

  height: Optional[str] = None
  width: Optional[str] = None
  thickness: Optional[str] = None


class VolumeInfo(BaseModel):
  model_config = ConfigDict(extra="ignore")

  title: Optional[str] = None
  subtitle: Optional[str] = None
  authors: Optional[list[str]] = None
  publisher: Optional[str] = None
  publishedDate: Optional[str] = None
  description: Optional[str] = None
  industryIdentifiers: Optional[list[IndustryIdentifier]] = None
  pageCount: Optional[int] = None
  dimensions: Optional[VolumeDimensions] = None
  printType: Optional[str] = None
  mainCategory: Optional[str] = None
  categories: Optional[list[str]] = None
  averageRating: Optional[float] = None
  ratingsCount: Optional[int] = None
  maturityRating: Optional[str] = None
  contentVersion: Optional[str] = None
  imageLinks: Optional[VolumeImageLinks] = None
  language: Optional[str] = None
  previewLink: Optional[str] = None
  infoLink: Optional[str] = None
  canonicalVolumeLink: Optional[str] = None


class ListPrice(BaseModel):
  model_config = ConfigDict(extra="ignore")

  amount: Optional[float] = None
  currencyCode: Optional[str] = None


class SaleInfo(BaseModel):
  model_config = ConfigDict(extra="ignore")

  country: Optional[str] = None
  saleability: Optional[str] = None
  isEbook: Optional[bool] = None
  listPrice: Optional[ListPrice] = None
  retailPrice: Optional[ListPrice] = None
  buyLink: Optional[str] = None


class EpubAccess(BaseModel):
  model_config = ConfigDict(extra="ignore")

  isAvailable: Optional[bool] = None
  acsTokenLink: Optional[str] = None


class PdfAccess(BaseModel):
  model_config = ConfigDict(extra="ignore")

  isAvailable: Optional[bool] = None
  acsTokenLink: Optional[str] = None


class AccessInfo(BaseModel):
  model_config = ConfigDict(extra="ignore")

  country: Optional[str] = None
  viewability: Optional[str] = None
  embeddable: Optional[bool] = None
  publicDomain: Optional[bool] = None
  textToSpeechPermission: Optional[str] = None
  epub: Optional[EpubAccess] = None
  pdf: Optional[PdfAccess] = None
  accessViewStatus: Optional[str] = None


class GoogleBooksVolume(BaseModel):
  model_config = ConfigDict(extra="ignore")

  kind: Optional[str] = None
  id: str
  etag: Optional[str] = None
  selfLink: Optional[str] = None
  volumeInfo: VolumeInfo
  saleInfo: Optional[SaleInfo] = None
  accessInfo: Optional[AccessInfo] = None

  def isbn_10(self) -> Optional[str]:
    if not self.volumeInfo.industryIdentifiers:
      return None
    return getattr(next((i for i in self.volumeInfo.industryIdentifiers if i.type == "ISBN_10"), None), "identifier", None)

  def isbn_13(self) -> Optional[str]:
    if not self.volumeInfo.industryIdentifiers:
      return None
    return getattr(next((i for i in self.volumeInfo.industryIdentifiers if i.type == "ISBN_13"), None), "identifier", None)


class GoogleBooksVolumesSearchResponse(BaseModel):
  model_config = ConfigDict(extra="ignore")

  kind: Optional[str] = None
  items: Optional[list[GoogleBooksVolume]] = None
  totalItems: int = 0


def search_books(query: str, service: GoogleBooksServiceDep) -> GoogleBooksVolumesSearchResponse:
  request = service.volumes().list(q=query)
  raw = request.execute()
  return GoogleBooksVolumesSearchResponse.model_validate(raw)