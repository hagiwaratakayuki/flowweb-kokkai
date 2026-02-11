import { get } from "../client"
/**
 * @returns {Promise<import("$lib/ml_api/api_types/TextOverViews").TextOverviews>}
 */
export function all_summary() {
    return get('node/all_summary')

}
