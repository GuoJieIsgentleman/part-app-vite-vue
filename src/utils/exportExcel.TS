//导出文件工具类
import FileSaver from "file-saver";
import XLSX from "xlsx";

import service from './request'



/**
 * 
 * @param {String} id 表格id,类名为.class id为#id
 * @param {String} title  要导出的excel表格名称
 */
export const exportTable = (id, title) => {
  //  .table要导出的是哪一个表格
  let table = document.querySelector(id).cloneNode(true);


  // 因为element-ui的表格的fixed属性导致多出一个table，会下载重复内容，这里删除掉
  // table.removeChild(table.querySelector(".el-table__fixed-right"));
  table.removeChild(table.querySelector(".el-table__fixed"));

  let wb = XLSX.utils.table_to_book(table, { raw: true }); //mytable为表格的id名
  /* get binary string as output */


  var wbout = XLSX.write(wb, {
    bookType: "xlsx",
    bookSST: true,
    type: "array",
  });

  let blob = new Blob([wbout], { type: "application/octet-stream" })
  let objectUrl = URL.createObjectURL(blob);
  // let a = document.createElement('a');
  // a.setAttribute('style', 'display:none');
  // a.setAttribute('href', objectUrl);
  // a.setAttribute('download', `${title}.xlsx`);
  // document.body.appendChild(a);
  // console.log('a')
  // console.log(a)
  // a.click();
  // URL.revokeObjectURL(objectUrl);
  // document.body.removeChild(a);


  //
  service.get('/savefile', {
    params: {
      objectUrl: objectUrl,
      filename: title,
      type: 'xlsx'
    }
  })






  try {
    FileSaver.saveAs(
      blob,
      title + ".xlsx"
    );
  } catch (e) {
    if (typeof console !== "undefined") console.log(e, wbout);
  }
  return wbout;
}
