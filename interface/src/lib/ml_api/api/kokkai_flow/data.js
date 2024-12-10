import { get } from "../client"
/**
 * @param {number} id 
 * @returns {Promise<import("$lib/ml_api/api_types/KokkaiClusterData").KokkaiClusterData>}
 */
export function entity_all(id) {
    // @ts-ignore
    return get('cluster/data', { id })

}
