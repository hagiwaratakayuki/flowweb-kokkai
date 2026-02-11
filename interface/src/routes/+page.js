// eslint-disable-next-line no-unused-vars
import { error } from '@sveltejs/kit';
import { all_summary } from "$lib/ml_api/api/node/all_summary";

export async function load() {

    try {

        // @ts-ignore
        const summary = await all_summary();
        return { summary }
    } catch (e) {
        error(400, "bad request");
    }

}