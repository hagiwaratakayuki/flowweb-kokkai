import { get } from "../client"
/**
 * @param {number} id 
 * @returns {Promise<import("$lib/ml_api/api_types/MeetingData").MeetingData>}
 */
export function data(id) {
    // @ts-ignore
    return get('meeting/data', { id })

}