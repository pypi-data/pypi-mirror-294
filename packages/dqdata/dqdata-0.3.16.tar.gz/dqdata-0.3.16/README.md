# dqdata

Data sdk for Ducheng Quant Database.


## !!!   0.3.13版本BreakChange  !!!

此版本调整了WindUtil的引入方式，不再支持从dqdata直接导出

`from dqdata import windUtils`
改成
`from dqdata.wind_utils import WindUtil`

## 1、安装：

```
pip install dqdata

或指定版本

pip install dqdata==0.3.7
```

```buildoutcfg
依赖包：numpy, pandas, urllib3, request, logbook, schedule, watchdog
```

## 2、ApiClient

#### (1)、实例创建

```buildoutcfg
ApiClient(token='', host='api.shducheng.net', port=80, log_level='INFO', api_urls=None)

token: token字符串
host: 接口服务地址，默认：api.shducheng.net
port: 接口服务端口，默认：80
log_level: 日志级别，默认：INFO
api_urls: 接口地址服务路径
```

##### 示例：

```
api = ApiClient(token='xxxx-xxxx-xxxx')
```

#### (2)、查询指标信息

##### 方法说明：

```buildoutcfg
get_idx_dict(idx)

idx: 指标id
```

##### 示例：通过id查询指标信息

```
info = api.get_idx_dict(109646)
print(info)
```

##### 执行结果

```
{'id': 109646, 'code': 'RB_DC', 'name': '河钢承钢：天津市场价格：螺纹钢：HRB400E：Ф18-25mm（日）', 'unit': '元/吨', 'frequency': '日', 'description': None, 'tableName': 'T_STEEL', 'sourceType': 'mysteel', 'sourceCode': 'ST_0001246521', 'sourceDescription': None, 'industry': '黑色', 'type': '现货价格', 'commodity': 'RB', 'sjbId': None, 'userId': None, 'rowsCount': 1191, 'dateFirst': '2016-07-21T00:00:00', 'dateLast': '2021-04-28T00:00:00', 'timeLastUpdate': '2021-04-28T19:56:44.783', 'timeLastRequest': None, 'priority': None, 'status': None, 'shortName': None, 'updateDescription': None, 'indexPropertiesList': None, 'categoryId': None, 'indexName': None}
```

#### (3)、通过类型查询指标列表

##### 方法说明：

```buildoutcfg
get_dict_list(source_type):

source_type: 指标来源类型
```

##### 示例：通过类型查询指标列表

```
df = api.get_dict_list('wind')
print(df)
```

##### 执行结果

```
          id    code       name  ... categoryIdList commodityName sorting
0     102786  EXC_JY      美元中间价  ...           None          None    None
1     102804  PTA_JY  FOB鹿特丹 MX  ...           None          None    None
2     102805  PTA_JY    国产MX：华东  ...           None          None    None
3     102818  PTA_JY  国产PX：镇海炼化  ...           None          None    None
4     102835   PF_JY  TA01M.CZC  ...           None          None    None
...      ...     ...        ...  ...            ...           ...     ...
```

#### (4)、查询指标数据

##### 方法说明：

```buildoutcfg
get_series(ids, start_dt='2015-01-01', end_dt=None, column='id')

ids: 指标id或id列表
start_dt: 开始日期，默认：2015年1月1日
end_dt: 截至日期，默认：当日日期
column: 列名字段：id/name
```

##### 示例：通过id列表查询指标数据

```
df = api.get_series([109645, 109646], start_dt='2021-05-15')
print(df)
```

##### 执行结果

```
            109645  109646
date                      
2021-05-17  5910.0  5920.0
2021-05-18  5880.0  5910.0
2021-05-19  5610.0  5640.0
2021-05-20  5500.0  5530.0
2021-05-21  5450.0  5500.0
2021-05-24  5260.0  5310.0
2021-05-25  5210.0  5260.0
2021-05-26  5080.0  5130.0
2021-05-27  4980.0  5030.0
2021-05-28  5070.0  5120.0
```

##### 示例：使用指标名称作为列名

```
df = api.get_series([109645, 109646], column='name', start_dt='2021-05-15')
print(df)
```

##### 执行结果

```
            鑫达：天津市场价格：螺纹钢：HRB400E：Ф18-25mm（日）  河钢承钢：天津市场价格：螺纹钢：HRB400E：Ф18-25mm（日）
date                                                                              
2021-05-17                             5910.0                               5920.0
2021-05-18                             5880.0                               5910.0
2021-05-19                             5610.0                               5640.0
2021-05-20                             5500.0                               5530.0
2021-05-21                             5450.0                               5500.0
2021-05-24                             5260.0                               5310.0
2021-05-25                             5210.0                               5260.0
2021-05-26                             5080.0                               5130.0
2021-05-27                             4980.0                               5030.0
2021-05-28                             5070.0                               5120.0
```

#### (5)、获取公式数据

##### 方法说明：

```buildoutcfg
formula_series(formulas, start_dt='2015-01-01', end_dt=None, column='id')

formulas: 公式或公式列表
start_dt: 开始日期，默认：2015年1月1日
end_dt: 截至日期，默认：当日日期
```

##### 示例：获取公式数据

```
df = api.formula_series(['diff(idx(171794))', 'idx(171794)-lag(idx(171794),1)'], start_dt='2021-05-15')
print(df)
```

##### 执行结果

```
            diff(idx(171794))  idx(171794)-lag(idx(171794),1)
date                                                         
2021-05-17                NaN                          0.0204
2021-05-18            -0.0119                         -0.0119
2021-05-19             0.0341                          0.0341
2021-05-20            -0.0460                         -0.0460
2021-05-21            -0.0034                         -0.0034
...                       ...                             ...
2022-07-15            -0.0443                         -0.0443
2022-07-18             0.0703                          0.0703
2022-07-19             0.0354                          0.0354
2022-07-20             0.0056                          0.0056
2022-07-21            -0.1518                         -0.1518
```

#### (6)、插入指标数据

##### 方法说明：

```buildoutcfg
save_series(items, overwrite=False):

items: 指标数据列表，格式：[{'idx': 100001, 'date': datetime.datetime.today(), 'value': 100.05 }]
overwrite: 是否覆盖已有相同日期值，默认False
```

##### 示例：插入数据

```
items = []

for i in range(11):
    items.append({'idx': 114278, 'date': dt.datetime.today() - dt.timedelta(days=i + 10), 'value': i * 100})
    items.append({'idx': 109646, 'date': dt.datetime.today() - dt.timedelta(days=i + 10), 'value': i * 1000})

api.save_series(items, overwrite=False)
```

##### 执行结果

```
2021-06-01 17:12:05,983 - api_client.py[line:116]- INFO: T_STEEL 更新或新增了22条记录
```

##### 查询数据

```
df = api.get_series([109645, 109646], column='id', start_dt='2021-05-15')
print(df)
```

##### 执行结果

```
            109645  109646
date                      
2021-05-15   700.0  7000.0
2021-05-16   600.0  6000.0
2021-05-17   500.0  5000.0
2021-05-18   400.0  4000.0
2021-05-19   300.0  3000.0
2021-05-20   200.0  2000.0
2021-05-21   100.0  1000.0
2021-05-22     0.0     0.0
```

#### (7)、删除指标数据

##### 方法说明：

```buildoutcfg
del_series(ids, start_dt='1900-01-01', end_dt='2999-01-01')

ids: 指标id或id列表
start_dt: 开始日期，默认：1900-01-01
end_dt: 截至日期，默认：2999-01-01
```

##### 示例：清空数据

```
api.del_series([109645, 109646])
```

##### 执行结果

```
2021-06-01 14:55:42,583 - api_client.py[line:131]- INFO: 删除了728条数据。
2021-06-01 14:55:42,810 - api_client.py[line:131]- INFO: 删除了1191条数据。
```

##### 示例：删除指定起始日期数据

```
api.del_series([109645, 109646], start_dt='2021-04-15')
```

##### 执行结果

```
2021-06-01 14:59:28,538 - api_client.py[line:131]- INFO: 删除了15条数据。
2021-06-01 14:59:28,585 - api_client.py[line:131]- INFO: 删除了15条数据。
```

#### (8)、消息工具

##### 方法说明(短信)：

```buildoutcfg
send_sms(number, text, name='')

number: 手机号码
text: 消息文本
name: 通知名称
```

##### 示例：发送短消息

```
api.send_sms('139********', 'TableXXX数据更新完成', name='数据表更新')
```

##### 方法说明(微信)：

```buildoutcfg
send_wx(email, text)

email: 邮箱账号
text: 消息文本
```

##### 示例：发送微信消息

```
api.send_wx('zhangx@shxxxx.com.cn', 'TableXXX 数据更新完成')
```

## 3、 Wind API工具类

#### (1)、工具类引入

```buildoutcfg
from dqdata.windUtil import WindUtil
```

#### (2)、获取交易日

##### 方法说明：

```buildoutcfg
tdays(start_date, end_date=None)

start_dt: 开始日期，格式：'2015-01-01'
end_dt: 截至日期，默认：当前日期
```

##### 示例：指定起止时间查询交易日列表

```
l = WindUtil.tdays('2020-03-15', end_date='2020-03-30')
print(l)
```

##### 执行结果

```
[datetime.datetime(2022, 3, 15, 0, 0), datetime.datetime(2022, 3, 16, 0, 0), datetime.datetime(2022, 3, 17, 0, 0), datetime.datetime(2022, 3, 18, 0, 0), datetime.datetime(2022, 3, 21, 0, 0), datetime.datetime(2022, 3, 22, 0, 0), datetime.datetime(2022, 3, 23, 0, 0), datetime.datetime(2022, 3, 24, 0, 0), datetime.datetime(2022, 3, 25, 0, 0), datetime.datetime(2022, 3, 28, 0, 0), datetime.datetime(2022, 3, 29, 0, 0), datetime.datetime(2022, 3, 30, 0, 0)]
```

#### (3)、获取时间序列数据(多品种单指标或单品种多指标)

##### 方法说明：

```buildoutcfg
wsd(codes, fields, start_date=None, end_date=None, options=None)

codes: Wind代码
fields: 数据栏位
start_date: 开始日期，默认：当前日期
end_date: 截止日期，默认：当前日期
options: wsd选项
```

##### 示例：查询恒生电子日行情数据

```
df = WindUtil.wsd('600570.SH', 'open,close,high,low', start_date='2021-04-01', end_date='2021-04-05')
print(df)
```

##### 执行结果

```
         date   OPEN  CLOSE   HIGH    LOW
0  2021-04-01  83.70  84.60  84.77  83.47
1  2021-04-02  84.80  84.78  85.43  84.21
2  2021-04-06  84.80  86.00  86.22  83.80
3  2021-04-07  85.46  84.35  85.60  82.81
4  2021-04-08  83.96  84.20  85.23  83.31
5  2021-04-09  85.00  82.84  85.00  81.83
6  2021-04-12  81.88  81.78  83.20  80.14
7  2021-04-13  81.30  81.08  82.14  80.55
8  2021-04-14  81.10  82.20  82.59  80.41
9  2021-04-15  82.18  82.68  82.90  81.60
```

#### (4)、获取宏观经济指标数据

##### 方法说明：

```buildoutcfg
edb(codes, start_date=None, end_date=None, options=None)

codes: Wind代码
start_date: 开始日期，默认：当前日期
end_date: 截止日期，默认：当前日期
options: wsd选项
```

##### 示例：查询住宅房屋新开工面积数据

```
df = WindUtil.edb('S0049582', start_date='2020-01-01', end_date='2021-04-01', options='')
print(df)
```

##### 执行结果

```
          date        CLOSE
0   2020-02-29    7559.4648
1   2020-03-31   20799.4490
2   2020-04-30   35248.3115
3   2020-05-31   50887.6337
4   2020-06-30   71582.8599
5   2020-07-31   88089.0966
6   2020-08-31  102485.8912
7   2020-09-30  117193.0523
8   2020-10-31  132481.0900
9   2020-11-30  147343.6000
10  2020-12-31  164328.5300
11  2021-02-28   12735.8000
12  2021-03-31   27056.8100
13  2021-04-30   40334.5984
```

#### (5)、获取最新行情数据

##### 方法说明：

```buildoutcfg
wsq(codes, fields)

codes: Wind代码
fields: 数据栏位
```

##### 示例：查询CU2207.SHF,RB2208.SHF最新价和成交量

```
df = WindUtil.wsq('CU2207.SHF,RB2208.SHF', 'rt_latest,rt_last_vol')
print(df)
```

##### 执行结果

```
         code  RT_LATEST  RT_LAST_VOL
0  CU2207.SHF    61480.0          5.0
1  RB2208.SHF     4211.0          2.0
```

#### (6)、获取板块成分(通过Wind板块ID)

##### 方法说明：

```buildoutcfg
sectors(sectorid, date=None)

sectorid: Wind板块ID
date: 指定日期，默认：当前日期
```

##### 示例：查询指定日期国内商品交易品种

```
df = WindUtil.sectors('1000010084000000', date='2020-08-28')
print(df)
```

##### 执行结果

```
         date wind_code  sec_name
1  2020-08-28     A.DCE     DCE豆一
2  2020-08-28    AG.SHF    SHFE白银
3  2020-08-28    AL.SHF     SHFE铝
4  2020-08-28    AP.CZC    CZCE苹果
5  2020-08-28    AU.SHF    SHFE黄金
..         ...        ...      ...
56 2020-08-28    WH.CZC    CZCE强麦
57 2020-08-28    WR.SHF    SHFE线材
58 2020-08-28     Y.DCE     DCE豆油
59 2020-08-28    ZC.CZC   CZCE动力煤
60 2020-08-28    ZN.SHF     SHFE锌
```

#### (7)、获取指数成分(通过Wind代码)

##### 方法说明：

```buildoutcfg
sectors_by_code(wind_code, date=None)

wind_code: Wind代码
date: 指定日期，默认：当前日期
```

##### 示例：查询沪深300成分股

```
df = WindUtil.sectors_by_code('000300.SH')
print(df)
```

##### 执行结果

```
          date  wind_code sec_name
1   2022-07-04  000001.SZ     平安银行
2   2022-07-04  000002.SZ      万科A
3   2022-07-04  000063.SZ     中兴通讯
4   2022-07-04  000066.SZ     中国长城
5   2022-07-04  000069.SZ     华侨城A
..         ...        ...      ...
296 2022-07-04  688363.SH     华熙生物
297 2022-07-04  688396.SH      华润微
298 2022-07-04  688561.SH    奇安信-U
299 2022-07-04  688599.SH     天合光能
300 2022-07-04  688981.SH     中芯国际
```

#### (8)、获取指定品种期货合约

##### 方法说明：

```buildoutcfg
fu_contracts(wind_code, start_date=None, end_date=None)

wind_code: Wind品种代码
start_date: 开始日期，默认：当前日期
end_date: 截至日期，默认：当前日期
```

##### 示例：查询黄大豆1号期货合约

```
df = WindUtil.fu_contracts('A.DCE')
print(df)
```

##### 执行结果

```
      sec_name   code  wind_code delivery_month  change_limit  target_margin contract_issue_date last_trade_date last_delivery_month
1  黄大豆1号2207合约  A2207  A2207.DCE         202207           8.0           20.0          2021-07-15      2022-07-14          2022-07-19
2  黄大豆1号2209合约  A2209  A2209.DCE         202209           8.0           12.0          2021-09-15      2022-09-15          2022-09-20
3  黄大豆1号2211合约  A2211  A2211.DCE         202211           8.0           12.0          2021-11-15      2022-11-14          2022-11-17
4  黄大豆1号2301合约  A2301  A2301.DCE         202301           8.0           12.0          2022-01-18      2023-01-17          2023-01-20
5  黄大豆1号2303合约  A2303  A2303.DCE         202303           8.0           12.0          2022-03-15      2023-03-14          2023-03-17
6  黄大豆1号2305合约  A2305  A2305.DCE         202305           8.0           12.0          2022-05-19      2023-05-18          2023-05-23
```

#### (9)、获取期货主力合约代码

##### 方法说明：

```buildoutcfg
fu_hiscode(wind_code, trade_date=None)

wind_code: Wind品种代码
trade_date: 指定日期，默认：当前日期
```

##### 示例：查询黄大豆1号期货主力合约代码

```
s = WindUtil.fu_hiscode('A.DCE')
print(s)
```

##### 执行结果

```
A2209.DCE
```

## 4、SimTrader

#### (1)、实例创建

```buildoutcfg
SimTrader(token: str, account_id: int, host='http://sim.shducheng.net', port=8087, log_level='INFO', api_urls=None)

token: token字符串
host: 接口服务地址，默认：http://sim.shducheng.net
port: 接口服务端口，默认：8087
log_level: 日志级别，默认：INFO
api_urls: 接口地址服务地址字典
```

##### 示例：

```
from dqdata import Order, SimTrader

sim = SimTrader(token='xxxx-xxxx-xxxx', account_id=1)
```

#### (2)、账户资金查询

##### 方法说明：

```buildoutcfg
query_cash()
```

##### 示例：

```
info = sim.query_cash()
print(info)
```

##### 执行结果

```
{   
    'available': 636057.4203548828,
    'cum_commission': 365.5750217040304,
    'cum_inout': 1000000.0,
    'cum_pnl': 500.0,
    'cum_trade': 364077.0046234131,
    'fpnl': -20636.988449096698,
    'frozen': 364077.0046234131,
    'nav': 979497.4365291992,
    'pnl': -20502.563470800756
}
  ```

#### (3)、账户持仓查询

##### 方法说明：

```buildoutcfg
query_positions()
```

##### 示例：

```
info = sim.query_positions()
print(info)
```

##### 执行结果

```
[   
    {   'amount': 56570.0,
        'available': 15,
        'available_today': 0,
        'cost': 0.0,
        'created_at': '2022-08-31 14:04:11',
        'fpnl': -1250.0000000000227,
        'order_frozen': 0,
        'order_frozen_today': 0,
        'price': 3763.0,
        'side': 1,
        'symbol': 'SHFE.rb2301',
        'updated_at': '2022-09-23 20:51:51',
        'volume': 15,
        'volume_today': 0,
        'vwap': 3771.3333333333335
    },
    {   'amount': 592900.0,
        'available': 10,
        'available_today': 10,
        'cost': 0.0,
        'created_at': '2022-09-26 14:01:59',
        'fpnl': 0.0,
        'order_frozen': 0,
        'order_frozen_today': 0,
        'price': 59290.0,
        'side': 1,
        'symbol': 'SHFE.cu2212',
        'updated_at': '2022-09-26 14:02:06',
        'volume': 10,
        'volume_today': 10,
        'vwap': 59290.0
    }
]
```

#### (4)、当日订单查询

##### 方法说明：

```buildoutcfg
query_orders()
```

##### 示例：

```
info = sim.query_orders()
print(info)
```

##### 执行结果

```
[   
    {   'cl_ord_id': '29107026-3d64-11ed-9bfc-00163e18a8b3',
        'created_at': '2022-09-26 14:26:31',
        'filled_amount': 0.0,
        'filled_commission': 0.0,
        'filled_volume': 0,
        'filled_vwap': 0.0,
        'ord_rej_reason': 0,
        'ord_rej_reason_detail': '',
        'order_style': 1,
        'order_type': 1,
        'position_effect': 1,
        'position_side': 1,
        'price': 59000.0,
        'side': 1,
        'status': 12,
        'symbol': 'SHFE.cu2212',
        'updated_at': '2022-09-26 15:00:00',
        'volume': 10
    },
    {   'cl_ord_id': 'bbe36dbb-3d60-11ed-9bfc-00163e18a8b3',
        'created_at': '2022-09-26 14:01:59',
        'filled_amount': 592900.0,
        'filled_commission': 0.0,
        'filled_volume': 10,
        'filled_vwap': 59290.0,
        'ord_rej_reason': 0,
        'ord_rej_reason_detail': '',
        'order_style': 1,
        'order_type': 1,
        'position_effect': 1,
        'position_side': 1,
        'price': 59300.0,
        'side': 1,
        'status': 3,
        'symbol': 'SHFE.cu2212',
        'updated_at': '2022-09-26 14:02:06',
        'volume': 10
    }
]
```

#### (5)、未完成订单查询

##### 方法说明：

```buildoutcfg
query_unfinished_orders()
```

##### 示例：

```
info = sim.query_unfinished_orders()
print(info)
```

##### 执行结果

```
[   
    {   'cl_ord_id': '29107026-3d64-11ed-9bfc-00163e18a8b3',
        'created_at': '2022-09-26 14:26:31',
        'filled_amount': 0.0,
        'filled_commission': 0.0,
        'filled_volume': 0,
        'filled_vwap': 0.0,
        'ord_rej_reason': 0,
        'ord_rej_reason_detail': '',
        'order_style': 1,
        'order_type': 1,
        'position_effect': 1,
        'position_side': 1,
        'price': 59000.0,
        'side': 1,
        'status': 12,
        'symbol': 'SHFE.cu2212',
        'updated_at': '2022-09-26 15:00:00',
        'volume': 10
    },
]
```

#### (6)、账户历史订单查询

##### 方法说明：

```buildoutcfg
query_history_orders()
```

##### 示例：

```
info = sim.query_history_orders()
print(info)
```

##### 执行结果

```
[   
    {   'client_id': 'fd173e3c-34c9-11ed-b138-00163e18a8b3',
        'created_at': '2022-09-15 15:42:46',
        'date': '2022-09-15',
        'filled_amount': 0.0,
        'filled_commission': 0.0,
        'filled_price': 0.0,
        'filled_volume': 0,
        'id': 18,
        'order_type': '1',
        'position_effect': '1',
        'position_side': '1',
        'price': 3722.0,
        'reject_reason': None,
        'reject_reason_detail': None,
        'side': '1',
        'status': '5',
        'symbol': 'SHFE.rb2301',
        'updated_at': '2022-09-15 16:09:22',
        'user_id': 41062089,
        'volume': 4
    },
    {   'client_id': '4cb76ccf-34d1-11ed-b138-00163e18a8b3',
        'created_at': '2022-09-15 16:35:06',
        'date': '2022-09-15',
        'filled_amount': 0.0,
        'filled_commission': 0.0,
        'filled_price': 0.0,
        'filled_volume': 0,
        'id': 17,
        'order_type': '1',
        'position_effect': '2',
        'position_side': '1',
        'price': 3722.0,
        'reject_reason': None,
        'reject_reason_detail': None,
        'side': '2',
        'status': '1',
        'symbol': 'SHFE.rb2301',
        'updated_at': '2022-09-15 16:35:06',
        'user_id': 41062089,
        'volume': 6
    },

    ...
    
]
```

#### (7)、账户业绩查询

##### 方法说明：

```buildoutcfg
query_performance(with_detail = False):

with_detail: 详情标识，值为True时，返回每日资金、持仓及订单信息
```

##### 示例：

```
info = sim.query_performance()
print(info)
```

##### 执行结果

```
{   'indicators': {   'annual_return': 0.06362,
                      'annual_volatility': 0.02866,
                      'calmar_ratio': 27.352,
                      'cumulative_return': 0.0019599999999999618,
                      'end_date': '2022-09-26',
                      'max_drawdown': -0.00233,
                      'omega_ratio': 1.545,
                      'sharpe_ratio': 2.165,
                      'sortino_ratio': 4.478,
                      'start_date': '2022-09-15'
                   },
    'returns': [   {'date': '2022-09-15', 'net_value': 1.00042},
                   {'date': '2022-09-16', 'net_value': 0.998973},
                   {'date': '2022-09-19', 'net_value': 0.999373},
                   {'date': '2022-09-20', 'net_value': 1.00009},
                   {'date': '2022-09-21', 'net_value': 0.998093},
                   {'date': '2022-09-22', 'net_value': 1.00213},
                   {'date': '2022-09-23', 'net_value': 1.00202},
                   {'date': '2022-09-26', 'net_value': 1.00196}
                ]
}
```

##### 示例：返回每日资金、持仓及订单信息：

```
info = sim.query_performance(with_detail=True)
print(info)
```

##### 执行结果

```
{   'indicators': {   'annual_return': 0.06362,
                      'annual_volatility': 0.02866,
                      'calmar_ratio': 27.352,
                      'cumulative_return': 0.0019599999999999618,
                      'end_date': '2022-09-26',
                      'max_drawdown': -0.00233,
                      'omega_ratio': 1.545,
                      'sharpe_ratio': 2.165,
                      'sortino_ratio': 4.478,
                      'start_date': '2022-09-15'
                  },
    'orders': [   {   'client_id': 'fd173e3c-34c9-11ed-b138-00163e18a8b3',
                      'created_at': '2022-09-15 15:42:46',
                      'date': '2022-09-15',
                      'filled_amount': 0.0,
                      'filled_commission': 0.0,
                      'filled_price': 0.0,
                      'filled_volume': 0,
                      'id': 18,
                      'order_type': '1',
                      'position_effect': '1',
                      'position_side': '1',
                      'price': 3722.0,
                      'reject_reason': None,
                      'reject_reason_detail': None,
                      'side': '1',
                      'status': '5',
                      'symbol': 'SHFE.rb2301',
                      'updated_at': '2022-09-15 16:09:22',
                      'user_id': 41062089,
                      'volume': 4
                  },
                  ...
              ],
    'positions': [   {   'amount': 185147.0,
                         'available': 50,
                         'available_today': 0,
                         'cost': 3702.95,
                         'created_at': '2022-08-31 14:04:11',
                         'date': '2022-09-15',
                         'fpnl': 9026.79,
                         'frozen': 0.0,
                         'id': 25,
                         'side': '1',
                         'symbol': 'SHFE.rb2301',
                         'updated_at': '2022-09-15 21:00:21',
                         'user_id': 41062089,
                         'volume': 50,
                         'volume_today': 0
                     },
                     ...
                ],
    'returns': [   {   'cash': 9658010.0,
                       'cum_pnl': -1773.45,
                       'date': '2022-09-15',
                       'frozen': 337128.0,
                       'nav': 10004200.0,
                       'net_value': 1.00042,
                       'pnl': 4166.56,
                       'returns': 0.00042
                   },
                   {   'cash': 9698510.0,
                       'cum_pnl': -3365.12,
                       'date': '2022-09-16',
                       'frozen': 288910.0,
                       'nav': 9989730.0,
                       'net_value': 0.998973,
                       'pnl': -10270.7,
                       'returns': -0.0014463925
                   },
                   ...
               ]
    }

```

#### (8)、账户业绩查询

##### 方法说明：

```buildoutcfg
query_performance(with_detail = False):

with_detail: 详情标识，值为True时，返回每日资金、持仓及订单信息
```

##### 示例：

```
info = sim.query_performance()
print(info)
```

##### 执行结果

```
{   'indicators': {   'annual_return': 0.06362,
                      'annual_volatility': 0.02866,
                      'calmar_ratio': 27.352,
                      'cumulative_return': 0.0019599999999999618,
                      'end_date': '2022-09-26',
                      'max_drawdown': -0.00233,
                      'omega_ratio': 1.545,
                      'sharpe_ratio': 2.165,
                      'sortino_ratio': 4.478,
                      'start_date': '2022-09-15'
                   },
    'returns': [   {'date': '2022-09-15', 'net_value': 1.00042},
                   {'date': '2022-09-16', 'net_value': 0.998973},
                   {'date': '2022-09-19', 'net_value': 0.999373},
                   {'date': '2022-09-20', 'net_value': 1.00009},
                   {'date': '2022-09-21', 'net_value': 0.998093},
                   {'date': '2022-09-22', 'net_value': 1.00213},
                   {'date': '2022-09-23', 'net_value': 1.00202},
                   {'date': '2022-09-26', 'net_value': 1.00196}
                ]
}
```

#### (9)、委托下单

##### 方法说明：

```buildoutcfg
send_order(symbol, volume, price=0, buy_sell=Order.Buy, open_lose=Order.Open, order_type=Order.PriceLimit)

symbol: 合约代码
volume: 委托数量
price: 委托价格，市价单可不填，默认0
buy_sell: 买卖方向: Order.Buy | Order.Sell，默认Order.Buy
open_lose: 开平方向: Order.Open | Order.Close | Order.CloseToday | Order.CloseYesterday，默认Order.Open
order_type: 价格类型: Order.PriceLimit | Order.PriceMarket，默认Order.PriceLimit
```

##### 示例：

```
info = sim.send_order('SHFE.rb2301', 5, 3750, buy_sell=Order.Buy, open_lose=Order.Open)
print(info)
```

##### 执行结果

```
{'cl_ord_id': '0cf54113-3d79-11ed-9bfc-00163e18a8b3'}
```

#### (10)、批量下单

##### 方法说明：

```buildoutcfg
batch_order(orders: list):

orders: 订单列表
```

##### 示例：

```
orders = [
        {
            'symbol': 'SHFE.rb2301',
            'order_type': Order.PriceMarket,
            'order_style': Order.ByTargetVolume,
            'position_side': Order.PositionLong,
            'target_volume': 2
        },
        {
            'symbol': 'SHFE.rb2305',
            'order_type': Order.PriceMarket,
            'order_style': Order.ByTargetVolume,
            'position_side': Order.PositionShort,
            'target_volume': 2
        }
    ]

info = sim.batch_order(orders)
print(info)
```

##### 执行结果

```
[
    {'cl_ord_id': '0fb74e6d-542b-11ed-87d0-00163e18a8b3'}, 
    {'cl_ord_id': '0fb74e84-542b-11ed-87d0-00163e18a8b3'}
]
```

#### (11)、撤单委托

##### 方法说明：

```buildoutcfg
cancal_order(ids: list)

ids: 订单号列表
```

##### 示例：

```
sim.cancal_order(['0cf54113-3d79-11ed-9bfc-00163e18a8b3'])
```

#### (12)、全部撤单

##### 方法说明：

```buildoutcfg
cancel_all()
```

##### 示例：

```
sim.cancel_all()
```

#### (13)、全部平仓

##### 方法说明：

```buildoutcfg
close_all()
```

##### 示例：

```
sim.close_all()
```

#### (14)、账户数据同步

##### 方法说明：

```buildoutcfg
account_sync()
```

##### 示例：

```
sim.account_sync()
```

#### (15)、文件单工具

##### 实例创建：

```buildoutcfg
fo = FileOrder(trade_api: SimTrader, file_path: str, file_ext: str = '.csv', timers: list = None, init_run: bool = True)

trade_api: 交易/仿真交易API
file_path: 文件目录
file_ext: 文件后缀，默认：.csv，仅支持csv和excel文件
timers: 定时运行时间(文件变动外的定时执行)，如：['09:15', '21:15']
init_run: 是否启动时运行一次，默认：True
merge_flag: 监控变化后是否每次合并所有文件，默认：False

##### 订单文件格式示例：

| exchange | code   | target |
| -------- | ------ | ------ |
| DCE      | eb2211 | 3      |
| DCE      | l2301  | -3     |
| CZCE     | MA301  | 0      |
| DCE      | pp2301 | 5      |
| DCE      | v2301  | 5      |

```

##### 运行示例：


```
from dqdata import SimTrader, FileOrder

path = r'C:\Users\tony\Desktop\test'

sim = SimTrader(token='xxxx-xxxx-xxxx', account_id=1)
FileOrder(sim, path, timers=['09:15', '21:15']).start()

```