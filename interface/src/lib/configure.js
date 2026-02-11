/**
 * 
 * @param {'server' | 'client'} server_or_client 
 * @param {string} name
 */
export async function loadConfigure(server_or_client, name) {

    /*if (server_or_client === 'server') {
        if (import.meta) {

        }

    }*/
    const filepath = '.' + [server_or_client, '/configure/', import.meta.env.MODE, name] + '.js'
    await import.meta.glob(filepath)
}