

import { ElMessage } from "element-plus";
import service from "../utils/request";




export const use_proline_options = async (): Promise<ListItem[]> => {

    let { data } = await service.get('hg_getline')

    //console.log('line_data', data);
    return data.map((el: Array<string | number>) => {
        return {
            value: el[1],
            label: el[1]
        }
    })



}

export const getElectronArea = () => {
    try {
        // 领用区域获取
        return service.get("/hg_getusearea").then(res => {
            console.log('hg_getusearea', res);

            return res.data.map((item: any) => {
                return {
                    value: item[0],
                    label: item[0],
                };
            });

        })
    } catch (error) {
        ElMessage({
            type: 'warning',
            message: '获取数据异常'
        })
    }

}

export const getMachineArea = () => {
    try {
        // 领用区域获取
        return service.get("/hg_getMachineUsearea").then(res => {
            console.log('hg_getMachineUsearea', res);

            return res.data.map((item: any) => {
                return {
                    value: item[0],
                    label: item[0],
                };
            });

        })
    } catch (error) {
        ElMessage({
            type: 'warning',
            message: '获取数据异常'
        })
    }

}





export const options = [
    {
        value: "保养",
        label: "保养",
    },
    {
        value: "外修",
        label: "外修",
    },
    {
        value: "报废",
        label: "报废",
    }
]


export const getElectrontype = async (value?: any) => {


    //通过area 找type
    try {
        let { data: type } = await service.get("/hg_gettype",
            { params: { area: value } });

        console.log('type', type);

        return type.map((item: any) => {
            return {
                value: item[0],
                label: item[0],
            };
        });
    } catch (error) {
        ElMessage({
            type: 'warning',
            message: '获取数据异常'
        })
    }
};


export const getElectronSpesc = (part_name?: any, area?: string, part_type?: string) => {

    //通过area 找type
    try {
        return service.get("/hg_getspesc", {
            params: {
                area: area,
                use_part_name: part_name,
                type: part_type,
            }
        }).then(res => {
            return res.data.map((item: any) => {
                return {
                    value: item[0],
                    label: item[0],
                };
            });
        })
    } catch (error) {
        ElMessage({
            type: 'warning',
            message: '获取数据异常'
        })
    }


};




/* 

    @area 



 */
export const getElectronPartname = async (area?: string, type?: string) => {
    //通过area 找type
    try {
        let { data: partname } = await service.get("/hg_getpartname", {
            params: {
                area: area,
                type: type,

            },
        });



        return partname.map((item: Array<string>) => {
            return {
                value: item[0],
                label: item[0]

            };
        });
    } catch (error) {
        ElMessage({
            type: 'warning',
            message: '获取数据异常'
        })
    }



};

/**
 * 获取电器备件库存
 * @area 区域
 * @type 类型
 * @spec 型号
 * @part_name 名称
 * @returns 获取库存
 */
export const getElectronBalance = async (area: string, type: string, spec: string, part_name: string) => {

    try {

        let { data: balance } = await service.get("/hg_getbalance", {
            params: {
                area: area,
                type: type,
                spec: spec,
                part_name: part_name
            },
        });

        // state.ruleForm.balance = balance[0][0];
        // state.ruleForm.original = balance[0][1];

        return balance
    } catch (error) {
        ElMessage({
            type: 'warning',
            message: '获取数据异常'
        })
    }

};


/* =获取使用部位 */

export const getElectronSiteUse = async (area: string, type: string, spec: string, part_name: string): Promise<string> => {
    let { data } = await service.get('hg_get_site_use', {
        params: {
            area: area,
            type: type,
            spec: spec,
            part_name: part_name
        }
    })
    return data[0]

}



export interface ListItem {
    label: string
    value: string
}





export const typeOption = [
    {
        value: "回库",
        label: "回库",
    }
]



// export const scrapOption = [
//     {
//         value: "报废",
//         label: "报废",
//     },
//     {
//         value: "不报废",
//         label: "不报废",
//     },
//     {
//         value: "外修",
//         label: "外修",
//     },
//     {
//         value: "成套",
//         label: "成套",
//     },
// ]





/**
 * 获取电器备件库存
 * @area 区域
 * @type 类型
 * @spec 型号
 * @part_name 名称
 * @returns 获取库存
 */
export const getMachineBalance = async (area: string, type: string, spec: string, part_name: string) => {

    try {

        let { data: balance } = await service.get("/hg_getMachineBalance", {
            params: {
                area: area,
                type: type,
                spec: spec,
                part_name: part_name
            },
        });



        return balance
    } catch (error) {
        ElMessage({
            type: 'warning',
            message: '获取数据异常'
        })
    }

};




export const getMachinetype = async (value?: any) => {


    //通过area 找type
    try {
        let { data: type } = await service.get("/hg_getMachineType",
            { params: { area: value } });

        console.log('type', type);

        return type.map((item: any) => {
            return {
                value: item[0],
                label: item[0],
            };
        });
    } catch (error) {
        ElMessage({
            type: 'warning',
            message: '获取数据异常'
        })
    }
};


export const getMachineSpesc = (part_name?: any, area?: string, part_type?: string) => {

    //通过area 找type
    try {
        return service.get("/hg_getMachineSpesc", {
            params: {
                area: area,
                use_part_name: part_name,
                type: part_type,
            }
        }).then(res => {
            return res.data.map((item: any) => {
                return {
                    value: item[0],
                    label: item[0],
                };
            });
        })
    } catch (error) {
        ElMessage({
            type: 'warning',
            message: '获取数据异常'
        })
    }


};




/* 

    @area 



 */
export const getMachinePartName = async (area?: string, type?: string) => {
    //通过area 找type
    try {
        let { data: partname } = await service.get("/hg_getMachinePartName", {
            params: {
                area: area,
                type: type,

            },
        });



        return partname.map((item: Array<string>) => {
            return {
                value: item[0],
                label: item[0]

            };
        });
    } catch (error) {
        ElMessage({
            type: 'warning',
            message: '获取数据异常'
        })
    }



};




/* =获取使用部位 */

export const getMachineSiteUse = async (area: string, type: string, spec: string, part_name: string): Promise<string> => {
    let { data } = await service.get('hg_get_Machine_site_use', {
        params: {
            area: area,
            type: type,
            spec: spec,
            part_name: part_name
        }
    })
    return data[0]

}
