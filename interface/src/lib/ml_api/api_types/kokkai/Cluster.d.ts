/* eslint-disable */
/**
 * This file was automatically generated by json-schema-to-typescript.
 * DO NOT MODIFY IT BY HAND. Instead, modify the source JSONSchema file,
 * and run json-schema-to-typescript to regenerate this file.
 */

export type Title = string;
export type MemberCount = number;
export type ShortKeywords = string[];

export interface Cluster {
  title?: Title;
  member_count: MemberCount;
  short_keywords: ShortKeywords;
  [k: string]: unknown;
}