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
export type Title = string;
export type MemberCount = number;
export type Keywords = string[];
export type Weight = number;
export type TotalWeight = number;
export type Session1 = number;
export type Clusters = ClusterOverview[];
export type Cursor = string | null;
export type Discussion = SpeechOverview[] | null;
export type Title1 = string;
export type MeetingId1 = string;
export type Meeting1 = string;
export type Speaker1 = string;
export type SpeakerId1 = string;

export interface SpeechData {
  speech: SpeechSingle;
  clusters: ClusterOverviews;
  discussion?: Discussion;
  [k: string]: unknown;
}
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
export interface ClusterOverviews {
  clusters: Clusters;
  cursor: Cursor;
  [k: string]: unknown;
}
export interface ClusterOverview {
  id: Id1;
  title: Title;
  member_count: MemberCount;
  keywords: Keywords;
  weight: Weight;
  total_weight: TotalWeight;
  session: Session1;
  [k: string]: unknown;
}
export interface Id1 {
  [k: string]: unknown;
}
export interface SpeechOverview {
  id: Id2;
  title: Title1;
  meeting_id: MeetingId1;
  meeting: Meeting1;
  speaker: Speaker1;
  speaker_id: SpeakerId1;
  [k: string]: unknown;
}
export interface Id2 {
  [k: string]: unknown;
}