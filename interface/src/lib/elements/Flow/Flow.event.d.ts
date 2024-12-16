import { IntaractiveData } from './flow';

export type NodeEventMessage = {
    gridInfo: IntaractiveData,
    mouseEvent: MouseEvent

}


export type NodeEvent = CustomEvent<NodeEventMessage>
