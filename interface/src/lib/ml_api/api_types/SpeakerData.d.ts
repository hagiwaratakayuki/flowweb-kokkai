/* eslint-disable */
/**
 * This file was automatically generated by json-schema-to-typescript.
 * DO NOT MODIFY IT BY HAND. Instead, modify the source JSONSchema file,
 * and run json-schema-to-typescript to regenerate this file.
 */

export type Name = string;
export type Group = string;
export type Position = string;
export type Session = number;
export type Role = string;
export type House = string;
export type Comittie = string;
export type SameNames = [unknown, unknown][];
export type Title = string;
export type MeetingId = string;
export type Meeting = string;
export type Speaker = string;
export type SpeakerId = string;
export type Speehes = SpeechOverview[];

export interface SpeakerData {
  speaker: SpeakerSingle;
  same_names: SameNames;
  speehes: Speehes;
  [k: string]: unknown;
}
export interface SpeakerSingle {
  id: Id;
  name: Name;
  group: Group;
  position: Position;
  session: Session;
  role: Role;
  house: House;
  comittie: Comittie;
  [k: string]: unknown;
}
export interface Id {
  [k: string]: unknown;
}
export interface SpeechOverview {
  id: Id1;
  title: Title;
  meeting_id: MeetingId;
  meeting: Meeting;
  speaker: Speaker;
  speaker_id: SpeakerId;
  [k: string]: unknown;
}
export interface Id1 {
  [k: string]: unknown;
}
