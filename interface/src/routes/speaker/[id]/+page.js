
// eslint-disable-next-line no-unused-vars
import { error } from '@sveltejs/kit';
import { data } from "$lib/ml_api/api/speaker/data";
/** @type {import('./$types').PageLoad} */
export async function load({ params }) {


    return await data(params.id)


}