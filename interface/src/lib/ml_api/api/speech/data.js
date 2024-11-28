import { get } from "../client"
/**
 * @param {number} id 
 * @returns {Promise<import("$lib/ml_api/api_types/SpeechData").SpeechData>}
 */
export function data(id) {
    // @ts-ignore
    return get('speech/data', { id })

}