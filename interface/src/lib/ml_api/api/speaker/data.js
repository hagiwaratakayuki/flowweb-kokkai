import { get } from "../client"
/**
 * @param {any} id 
 * @returns {Promise<import("$lib/ml_api/api_types/SpeakerData").SpeakerData>}
 */
export function data(id) {
    // @ts-ignore
    return get('speaker/data', { id })

}