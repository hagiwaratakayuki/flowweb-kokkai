/* eslint-disable */
/**
 * This file was automatically generated by json-schema-to-typescript.
 * DO NOT MODIFY IT BY HAND. Instead, modify the source JSONSchema file,
 * and run json-schema-to-typescript to regenerate this file.
 */

export type LinkedCount = number;
export type Published = string;

export interface Edge {
  linked_from: LinkedFrom;
  link_to: LinkTo;
  linked_count: LinkedCount;
  published: Published;
  [k: string]: unknown;
}
export interface LinkedFrom {
  [k: string]: unknown;
}
export interface LinkTo {
  [k: string]: unknown;
}