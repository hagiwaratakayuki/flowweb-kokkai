/* eslint-disable */
/**
 * This file was automatically generated by json-schema-to-typescript.
 * DO NOT MODIFY IT BY HAND. Instead, modify the source JSONSchema file,
 * and run json-schema-to-typescript to regenerate this file.
 */

export type Keyword = string;
export type Published = string;
export type TextId = string;
export type LinkedCount = number;
export type Weight = number;
export type PublishedList = string[];

export interface NodeKeyword {
  keyword: Keyword;
  published: Published;
  text_id: TextId;
  linked_count: LinkedCount;
  weight: Weight;
  published_list: PublishedList;
  [k: string]: unknown;
}