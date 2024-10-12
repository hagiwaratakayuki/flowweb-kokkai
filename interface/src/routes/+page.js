// eslint-disable-next-line no-unused-vars
import { error } from '@sveltejs/kit';
import { all_summary } from "$lib/ml_api/api/text/all_summary";

export async function load() {

    try {
        // @ts-ignore
        return await all_summary();
    } catch (e) {
        error(400, "bad request");
    }

}