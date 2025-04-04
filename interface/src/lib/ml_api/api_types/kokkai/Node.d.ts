/* eslint-disable */
/**
 * This file was automatically generated by json-schema-to-typescript.
 * DO NOT MODIFY IT BY HAND. Instead, modify the source JSONSchema file,
 * and run json-schema-to-typescript to regenerate this file.
 */

export type Data = string;
export type Author = string;
export type AuthorId = string;
export type LinkTo = string[] | null;
export type LinkedCount = number;
export type Published = string;
export type Weight = number;
export type Title = string;
export type PublishedList = string[];
export type Hash = string;

export interface Node {
  data: Data;
  author?: Author;
  author_id?: AuthorId;
  link_to: LinkTo;
  linked_count: LinkedCount;
  published: Published;
  weight: Weight;
  title: Title;
  published_list: PublishedList;
  hash: Hash;
  [k: string]: unknown;
}
