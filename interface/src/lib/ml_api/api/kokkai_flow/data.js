import { get } from "../client"
/**
 * @param {number} id 
 * @returns {Promise<import("$lib/ml_api/api_types/KokkaiClusterData").KokkaiClusterData>}
 */
export function kokkai_flow_data(id) {
    // @ts-ignore
    return get('kokkai_cluster/data', { id })

}
