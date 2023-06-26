from modules.core.entity.DictionaryInfo import DictionaryInfo
from modules.core.utils import mysqlUtil


# 删除
def delete(dicKey):
    # 定义要执行的SQL语句
    sql = 'DELETE FROM dictionary_info WHERE dic_key=%s;'

    params = [dicKey]

    result = mysqlUtil.execute(sql, params)
    return result


# 更新
def update(dictionaryInfo):
    # 定义要执行的SQL语句
    sql = 'UPDATE dictionary_info SET  dic_value=%s WHERE dic_key=%s;'

    params = [dictionaryInfo.dic_value,dictionaryInfo.dic_key]

    result = mysqlUtil.execute(sql, params)
    return result


# 查询
def getAll():
    # 定义要执行的SQL语句
    sql = "SELECT * FROM dictionary_info;"
    # 取到查询结果
    result = mysqlUtil.query(sql)
    dicInfoDict = {}
    for dataSet in result:
        dictionaryInfo = {}
        dictionaryInfo['stock_code']=dataSet[0],
        dictionaryInfo['stock_name']=dataSet[1],
        dicInfoDict[dataSet[0]] = dictionaryInfo
    return dicInfoDict


# 查询
def get(dicKey):
    # 定义要执行的SQL语句
    sql = "SELECT * FROM dictionary_info WHERE dic_key='"+ dicKey + "';"
    # 取到查询结果
    result = mysqlUtil.query(sql)
    if result is ():
        return None

    dataSet = result[0]
    dictionaryInfo = DictionaryInfo(
        dic_key = dataSet[0],
        dic_value=dataSet[1],

    )

    return dictionaryInfo

