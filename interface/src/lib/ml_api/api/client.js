
import { baseGet } from "../../api_client.js"
const BaseURL = import.meta.env.VITE_ML_SERVER_URL
/**
 * @param {string} endpoint
 * @param {{string:any[] | number | string} | undefined} params 
 */
export async function get(endpoint, params = undefined) {
    return baseGet(BaseURL, endpoint, params);
}
