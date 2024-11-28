let TEXT_BASEPATH = '/text/';

/**
 * @param {string} text_basepath
 */
export function setBaseurl(text_basepath) {
    TEXT_BASEPATH = text_basepath

}

/**
 * @param {string} id
 */
export function getUrl(id) {
    return TEXT_BASEPATH + id
}