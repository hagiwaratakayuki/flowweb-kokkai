

import { error } from '@sveltejs/kit';
import { all_summary } from "$lib/ml_api/api/node/all_summary";
/** @type {import('./$types').PageLoad} */
export async function load({params}) {

    try {

        // @ts-ignore
        const summary = await all_summary();
        return { summary }
    } catch (e) {
        error(400, "bad request");
    }

}