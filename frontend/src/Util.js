/**
 * Utility function to format the date as per our requirement
 * @param d
 * @returns {string}
 */
export function getFormattedDate(d){
    return [
      d.getFullYear(),
      ('0' + (d.getMonth() + 1)).slice(-2),
      ('0' + d.getDate()).slice(-2)
    ].join('-');
}

/**
 * Parsing Int data.
 * @param d
 * @returns {number}
 */
export function getIntegerDate(d){
    return parseInt(d.replaceAll("-", ""));
}
