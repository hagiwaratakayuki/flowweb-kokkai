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
    const instance = new GetUrl(base)
    return instance.call.bind(instance)
}