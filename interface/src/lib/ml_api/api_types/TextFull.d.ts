/* eslint-disable */
/**
 * This file was automatically generated by json-schema-to-typescript.
 * DO NOT MODIFY IT BY HAND. Instead, modify the source JSONSchema file,
 * and run json-schema-to-typescript to regenerate this file.
 */

export type Title = string;
export type Body = string;
export type Published = string;
export type Auther = string;
export type AutherId = string;
export type Keywords = string[];
export type Clustres = ClusterOverview[] | null;
export type Id = string | number;
export type Title1 = string;
export type MemberCount = number;
export type ShortKeywords = string[];
export type ClustresNext = string | null;
export type LinkeTo = unknown[] | null;
export type LinkedFrom = TextOverview[] | null;
export type Id1 = string | number;
export type Title2 = string;
export type Published1 = string;
export type Body1 = string;
export type Author = string;
export type AuthorId = string;
export type LinkedCount = number;
export type LinkTo = string[] | null;
export type Position = number | null;
export type LinkedFromNext = string | null;

export interface TextFull {
  title?: Title;
  body?: Body;
  published?: Published;
  auther?: Auther;
  auther_id?: AutherId;
  keywords?: Keywords;
  clustres?: Clustres;
  clustres_next?: ClustresNext;
  linke_to?: LinkeTo;
  linked_from?: LinkedFrom;
  linked_from_next?: LinkedFromNext;
  [k: string]: unknown;
}
export interface ClusterOverview {
  id: Id;
  title?: Title1;
  member_count: MemberCount;
  short_keywords: ShortKeywords;
  [k: string]: unknown;
}
export interface TextOverview {
  id: Id1;
  title: Title2;
  published: Published1;
  body: Body1;
  author: Author;
  author_id: AuthorId;
  linked_count: LinkedCount;
  link_to?: LinkTo;
  position: Position;
  [k: string]: unknown;
}
