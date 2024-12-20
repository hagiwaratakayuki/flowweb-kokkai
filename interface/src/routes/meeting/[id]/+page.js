
// eslint-disable-next-line no-unused-vars
import { error } from '@sveltejs/kit';
import { data } from "$lib/ml_api/api/meeting/data";
/** @type {import('./$types').PageLoad} */
export async function load({ params }) {

    try {
        // @ts-ignore
        return await data(params.id)
    } catch (e) {
        error(400, "bad request");
    }

}