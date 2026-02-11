/**
  *
  * @param {string[]}keywords
  */
export function keywordPretter(keywords) {
    /**
     * @type {string[]}
     */
    const ret = [];
    for (const keyword of keywords) {
        let index = 0;
        let isPush = true;
        while (index < ret.length) {
            const target = ret[index];
            if (keyword.indexOf(target) !== -1) {
                isPush = false;
                ret[index] = keyword;
                break;
            }
            if (target.indexOf(keyword) !== -1) {
                isPush = false;

                break;
            }
            index++;
        }
        if (isPush == true) {
            ret.push(keyword);
        }
    }
    return ret;
}