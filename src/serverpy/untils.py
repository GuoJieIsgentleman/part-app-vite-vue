

import pinyin
import connect

# 增加记录


def addoperatelog():
    db = connect.getConn()
    cursor = db.cursor()


# 生成machine name


def FunctionName():
    # 查询出所有结果 然后生成
    db = connect.getConn()
    cursor = db.cursor()
    cursor.execute('''
              select * from machine_parts_detail     
                   
                   ''')

    rs = cursor.fetchall()

    for i in rs:

        part_name = i[1]
        spesc = i[2]
        area = i[3]
        machine_part_name = i[11]
        machin_part_id = f'{machine_part_name}_{area}'

        updatesql = f'''
        update machine_parts_detail set machine_part_id='{machin_part_id}'
        where part_name='{part_name}' and area='{area}' and part_spec='{spesc}'
        and machine_part_name='{machine_part_name}'
    '''
        cursor.execute(updatesql)

    db.commit()
    print('success')


FunctionName()
