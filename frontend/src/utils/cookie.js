/*
 * @Description: Copyright © 1999 - 2021 Winter. All Rights Reserved. 
 * @Author: Winter
 * @Email: 837950571@qq.com
 * @Date: 2021-04-14 20:01:44
 * @LastEditTime: 2021-04-14 20:01:45
 */
export function setCookie(key, value, t) {
    var oDate = new Date();
    oDate.setDate(oDate.getDate() + t);
    document.cookie = key + "=" + value + "; expires=" + oDate.toDateString();
}

export function getCookie(key) {
    var arr1 = document.cookie.split("; ");//由于cookie是通过一个分号+空格的形式串联起来的，所以这里需要先按分号空格截断,变成[name=Jack,pwd=123456,age=22]数组类型；
    for (var i = 0; i < arr1.length; i++) {
        var arr2 = arr1[i].split("=");//通过=截断，把name=Jack截断成[name,Jack]数组；
        if (arr2[0] == key) {
            return decodeURI(arr2[1]);
        }
    }
}

export function removeCookie(key) {
    setCookie(key, "", -1); // 把cookie设置为过期
}