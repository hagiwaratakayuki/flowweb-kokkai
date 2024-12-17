import { FlowEntry } from "$lib/relay_types/flow"

export type IntaractiveData = {
    nodes: FlowEntry[],
    isOverwraped: boolean

    x: number,
    y: number,
    maxWeight: number
}

export type FlowNodeEventMessage = {
    interactiveData: IntaractiveData,
    mouseEvent: MouseEvent
    x: number
    y: number

}


export type FlowNodeEvent = CustomEvent<FlowNodeEventMessage>
