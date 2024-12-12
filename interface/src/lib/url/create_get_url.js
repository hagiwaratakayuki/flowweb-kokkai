class GetUrl {
    /**
     * 
     * @param {string} base 
     */
    constructor(base) {
        this.base = base
    }
    call(path) {
        return this.base + path
    }
}
/**
 * 
 * @param {string} base 
 */
export function createGetUrl(base) {
    const inatance = new GetUrl(base)
    return inatance.call.bind(inatance)
}