
// eslint-disable-next-line no-unused-vars
import { error } from '@sveltejs/kit';
import { entity_all } from "$lib/ml_api/api/text/entity_all";
/** @type {import('./$types').PageLoad} */
export async function load({ params }) {

    try {
        // @ts-ignore
        return await entity_all(params.id)
    } catch (e) {
        error(400, "bad request");
    }

}