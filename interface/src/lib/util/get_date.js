/**
   * 
   * @param {string} datetime
   */
export function getDate(datetime) {
    return Array.from(datetime.matchAll(/\d+/g)).slice(0, 3).join('/');
}