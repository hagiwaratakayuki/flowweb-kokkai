/**
 * @typedef {import("$lib/ml_api/api_types/TextOverView").TextOverview} TextOverview
 * 
*/
/**
 * 
 * @param {Array<TextOverview>} overViews 
 * @returns 
 */
export function overviews_to_flow(overViews) {
    let maxConnected = -Infinity;


    /**
     * @type {import("$lib/relay_types/flow").Edges}
     */
    const edges = [];

    for (const overview of overViews) {

        maxConnected = Math.max(maxConnected, overview.linked_count);

        for (const to of overview.link_to || []) {
            edges.push({
                from: overview.id,
                to,
            });
        }
    }

    const maxWeight = Math.log(maxConnected) || 1;

    const nodes = overViews.map(function (row) {
        row.weight = Math.max(Math.log(row.linked_count || 1) / maxWeight, 0.1);

        row.y = row.position;
        return row;
    });
    return {
        nodes,
        edges,

    };

}