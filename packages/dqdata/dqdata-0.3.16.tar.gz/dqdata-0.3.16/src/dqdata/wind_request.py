import requests
import pandas as pd
import json
import datetime

from urllib.parse import urlencode
from WindPy import w
import logging



class WDAdaptorClient:
    """
    包装注册中心API以匹配WindPy原本接口
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    @classmethod
    def wsd(cls, res_url, codes, fields, start_date=None, end_date=None, options=None, *arga, **argb):
        result = w.WindData()
        params = {
            'codes': codes if codes is not None else '',
            'fields': fields if fields is not None else '',
            'startTime': start_date if start_date is not None else '',
            'endTime': end_date if end_date is not None else '',
            'options': options if options is not None else '',
        }
        params = urlencode(params, safe=','';''=')
        url = res_url + '/wind/wsd?' + params
        res = requests.get(url)

        try:
            wd = json.loads(res.content.decode("utf-8"), object_hook=custom_json_decoder)
        except Exception as e:
            logging.error(f"解析JSON时发生错误: {e}")
        result.ErrorCode = wd['errorCode']
        result.Codes = wd['codeList']
        result.Fields = wd['fieldList']
        result.asDate = True
        converted_dates = [datetime.datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S').date() for time_str in
                           wd['timeList']]
        result.Times = converted_dates

        ec = wd['errorCode']
        data_list = []
        if wd is not None and ec == 0 and len(wd['timeList']) > 0 and len(wd['data']) > 0:
            fields_length = len(wd['fieldList'])
            codes_length = len(wd['codeList'])
            if fields_length > codes_length:
                data_length = fields_length
            else:
                data_length = codes_length
            if data_length <= 1:
                data_list = [wd['data']]
            data_list = [[] for _ in range(data_length)]
            for i, element in enumerate(wd['data']):
                target_list_index = i % data_length
                data_list[target_list_index].append(element)
            if start_date is None and end_date is None:
                new_data_list = []
                for sub_list in data_list:
                    if sub_list:
                        new_data_list.append([sub_list[-1]])
                data_list = new_data_list
        result.Data = data_list

        if 'usedfdt' in argb.keys():
            usedfdt = argb['usedfdt']
            if usedfdt:
                if not isinstance(usedfdt, bool):
                    print('the parameter usedfdt which should be the Boolean type!')
                else:
                    return cls.wpy_wdata2fdf(result)
        if 'usedf' in argb.keys():
            usedf = argb['usedf']
            if usedf:
                if not isinstance(usedf, bool):
                    print('the parameter usedf which should be the Boolean type!')
                else:
                    return cls.wpy_wdata2df(result)
        return result

    @classmethod
    def wss(cls, res_url, codes, fields, options=None):
        result = w.WindData()
        params = {
            'codes': codes if codes is not None else '',
            'fields': fields if fields is not None else '',
            'options': options if options is not None else '',
        }
        params = urlencode(params, safe=','';''=')
        url = res_url + '/wind/wss?' + params
        res = requests.get(url)

        wd = json.loads(res.content.decode("gbk"))
        result.ErrorCode = wd['errorCode']
        result.Codes = wd['codeList']
        result.Fields = wd['fieldList']
        result.asDate = True
        converted_dates = [datetime.datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S').date() for time_str in
                           wd['timeList']]
        result.Times = converted_dates

        ec = wd['errorCode']
        data_list = []
        if wd is not None and ec == 0 and len(wd['timeList']) > 0 and len(wd['data']) > 0:
            data = {'date': wd['timeList']}
            fields_length = len(wd['fieldList'])
            codes_length = len(wd['codeList'])
            if fields_length > codes_length:
                data_length = fields_length
            else:
                data_length = codes_length
            data_list = [wd['data'][i:i + data_length] for i in range(0, len(wd['data']), data_length)]
        result.Data = data_list
        return result

    @classmethod
    def edb(cls, res_url, codes, start_date, end_date, options=None, *arga, **argb):
        result = w.WindData()
        params = {
            'codes': codes if codes is not None else '',
            'startTime': start_date if start_date is not None else '',
            'endTime': end_date if end_date is not None else '',
            'options': options if options is not None else '',
        }
        params = urlencode(params, safe=','';''=')
        url = res_url + '/wind/edb?' + params
        res = requests.get(url)

        try:
            wd = json.loads(res.content.decode("utf-8"), object_hook=custom_json_decoder)
        except Exception as e:
            logging.error(f"解析JSON时发生错误: {e}")
        result.ErrorCode = wd['errorCode']
        result.Codes = wd['codeList']
        result.Fields = wd['fieldList']
        result.asDate = True
        converted_dates = [datetime.datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S').date() for time_str in
                           wd['timeList']]
        result.Times = converted_dates

        ec = wd['errorCode']
        data_list = []
        if wd is not None and ec == 0 and len(wd['timeList']) > 0 and len(wd['data']) > 0:
            codes_length = len(wd['codeList'])
            if codes_length <= 1:
                data_list = [wd['data']]
            data_list = [[] for _ in range(codes_length)]
            for i, element in enumerate(wd['data']):
                target_list_index = i % codes_length
                data_list[target_list_index].append(element)
        result.Data = data_list

        if 'usedfdt' in argb.keys():
            usedfdt = argb['usedfdt']
            if usedfdt:
                if not isinstance(usedfdt, bool):
                    print('the parameter usedfdt which should be the Boolean type!')
                else:
                    return cls.wpy_wdata2fdf(result)
        if 'usedf' in argb.keys():
            usedf = argb['usedf']
            if usedf:
                if not isinstance(usedf, bool):
                    print('the parameter usedf which should be the Boolean type!')
                else:
                    return cls.wpy_wdata2df(result)
        return result

    @classmethod
    def wset(cls, res_url, reportName, options, *arga, **argb):
        result = w.WindData()
        options = cls.wpy_t2options(options, arga, argb)
        params = {
            'reportName': reportName if reportName is not None else '',
            'options': options if options is not None else '',
        }
        params = urlencode(params, safe=','';''=')
        url = res_url + '/wind/wset?' + params
        res = requests.get(url)

        try:
            wd = json.loads(res.content.decode("utf-8"), object_hook=custom_json_decoder)
        except Exception as e:
            logging.error(f"解析JSON时发生错误: {e}")
        result.ErrorCode = wd['errorCode']
        result.Codes = wd['codeList']
        result.Fields = wd['fieldList']
        result.asDate = True
        converted_dates = [datetime.datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S').date() for time_str in
                           wd['timeList']]
        result.Times = converted_dates

        data_list = []
        ec = wd['errorCode']
        if wd is not None and ec == 0 and len(wd['timeList']) > 0 and len(wd['data']) > 0:
            fields_length = len(wd['fieldList'])
            if fields_length <= 1:
                data_list = [wd['data']]
            data_list = [[] for _ in range(fields_length)]
            for i, element in enumerate(wd['data']):
                target_list_index = i % fields_length
                data_list[target_list_index].append(element)
        result.Data = data_list

        if 'usedfdt' in argb.keys():
            usedfdt = argb['usedfdt']
            if usedfdt:
                if not isinstance(usedfdt, bool):
                    print('the parameter usedfdt which should be the Boolean type!')
                else:
                    return cls.wpy_wdata2fdf(result)
        if 'usedf' in argb.keys():
            usedf = argb['usedf']
            if usedf:
                if not isinstance(usedf, bool):
                    print('the parameter usedf which should be the Boolean type!')
                else:
                    return cls.wpy_wdata2df(result)
        return result

    @classmethod
    def wpy_t2options(cls, options, arga, argb):
        method_name = '_w__t2options'
        if hasattr(w, method_name):
            method = getattr(w, method_name)

        if 'method' in locals():
            return method(options, arga, argb)
        else:
            print("Method not found")

    @classmethod
    def wpy_wdata2df(cls, out, isTDays=False):
        if out.ErrorCode != 0:
            df = pd.DataFrame(out.Data, index=out.Fields)
            df.columns = [x for x in range(df.columns.size)]
            return out.ErrorCode, df.T
        col = out.Times
        if len(out.Codes) == len(out.Fields) == 1:
            idx = out.Fields
            if len(out.Times) == 1 and isTDays == False:
                col = out.Codes
        elif len(out.Codes) > 1 and len(out.Fields) == 1:
            idx = out.Codes
            if len(out.Times) == 1:
                col = out.Codes
                idx = out.Fields
        elif len(out.Codes) == 1 and len(out.Fields) > 1:
            idx = out.Fields
            if len(out.Times) == 1:
                col = out.Codes
                idx = out.Fields
        else:
            idx = None
            df = pd.DataFrame(out.Data)
            dft = df.T
            dft.columns = out.Fields
            dft.index = out.Codes
        if idx:
            df = pd.DataFrame(out.Data, columns=col)
            dft = df.T
            dft.columns = idx
            # dft.index = idx
        return out.ErrorCode, dft.infer_objects()

    @classmethod
    def wpy_wdata2fdf(cls, out, isTDays=False):
        if out.ErrorCode != 0:
            df = pd.DataFrame(out.Data, index=out.Fields)
            df.columns = [x for x in range(df.columns.size)]
            return out.ErrorCode, df.T
        col = out.Times
        if len(out.Codes) == len(out.Fields) == 1:
            idx = out.Fields
            if len(out.Times) == 1 and isTDays == False:
                col = out.Codes
        elif len(out.Codes) > 1 and len(out.Fields) == 1:
            idx = out.Codes
            if len(out.Times) == 1:
                col = out.Codes
                idx = out.Fields
        elif len(out.Codes) == 1 and len(out.Fields) > 1:
            idx = out.Fields
            if len(out.Times) == 1:
                col = out.Codes
                idx = out.Fields
        else:
            idx = None
            df = pd.DataFrame(out.Data)
            dfdt = df.applymap(w.transformNulldate2NaT)
            dft = dfdt.T
            dft.columns = out.Fields
            dft.index = out.Codes
        if idx:
            df = pd.DataFrame(out.Data, columns=col)
            dfdt = df.applymap(w.transformNulldate2NaT)
            dft = dfdt.T
            dft.columns = idx
            # dft.index = idx
        return out.ErrorCode, dft.infer_objects()


def custom_json_decoder(dct):
    if 'data' not in dct:
        return dct
    rlist = []
    value_type = None
    for value in dct['data']:
        if value != 'NaN':
            value_type = type(value)
    for value in dct['data']:
        if value == 'NaN':
            if value_type == int:
                rlist.append(int('nan'))
            elif value_type == float:
                rlist.append(float('nan'))
            else:
                rlist.append(None)
        elif isinstance(value, str) and '-' in value and 'T' in value:
            try:
                rlist.append(datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S'))
            except ValueError:
                rlist.append(value)
        elif isinstance(value, dict) and len(value) == 0:
            rlist.append(None)
        else:
            rlist.append(value)
    dct['data'] = rlist
    return dct
