import { get } from "../client"
/**
 * @param {number} id 
 * @returns {Promise<import("$lib/ml_api/api_types/TextFull").TextFull>}
 */
export function entity_all(id) {
    // @ts-ignore
    return get('text/entity_all', { id })

}
