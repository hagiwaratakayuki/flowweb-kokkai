type AnyData = { [key: string]: any }

export type Edge = {
    from: any,
    to: any,


} & AnyData

export type FlowEntry = {
    id: any,
    y: number,
    weight: number,
    published: string,
    title: string


}

export type Flow = FlowEntry[]


export type Edges = Edge[];

export type DataTransfer = {
    nodes: Flow,
    edges: Edges
}