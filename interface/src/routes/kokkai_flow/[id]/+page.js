

import { error } from '@sveltejs/kit';
import { kokkai_flow_data } from "$lib/ml_api/api/kokkai_flow/data";
/** @type {import('./$types').PageLoad} */
export async function load({ params }) {
    if (params.id == 'installHook.js.map') {
        error(400, "bad request");
    }
    try {

        // @ts-ignore
        const flow = await kokkai_flow_data(params.id);
        return { flow }
    } catch (e) {
        error(400, "bad request");
    }

}