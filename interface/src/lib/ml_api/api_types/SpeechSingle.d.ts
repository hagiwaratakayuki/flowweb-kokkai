/* eslint-disable */
/**
 * This file was automatically generated by json-schema-to-typescript.
 * DO NOT MODIFY IT BY HAND. Instead, modify the source JSONSchema file,
 * and run json-schema-to-typescript to regenerate this file.
 */

export type MeetingId = string;
export type Meeting = string;
export type Speaker = string;
export type SpeakerId = string;
export type ResponseTo = string | null;
export type ResponseFrom = string | null;
export type DiscussionId = string | null;
export type Url = string;
export type Order = number;
export type Session = number;
export type Issue = string;
export type House = string;
export type Body = string;

export interface SpeechSingle {
  id: Id;
  meeting_id: MeetingId;
  meeting: Meeting;
  speaker: Speaker;
  speaker_id: SpeakerId;
  response_to?: ResponseTo;
  response_from?: ResponseFrom;
  discussion_id?: DiscussionId;
  url: Url;
  order: Order;
  session: Session;
  issue: Issue;
  house: House;
  body: Body;
  [k: string]: unknown;
}
export interface Id {
  [k: string]: unknown;
}