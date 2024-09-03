import requests
import os
import json
from datetime  import datetime 
import calendar
import logging

class CheckKoreanHoliday:
    """Get Korean Holiday List"""
    _API_SpcdeInfoService = "http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService"
    _API_SpcdeInfoService_PATH = "/getRestDeInfo"
    _API_KEY = os.environ['API_KEY']
    _CALENDER_MONTH = 0
    is_holiday_list = []
    is_holiday = False    
    
    def _req(self, host, path, method, headers=None, query=None,  data={}):
        url = host + path
        logging.debug('HTTP Method: %s' % method)
        logging.debug('Request URL: %s' % url)
        logging.debug('Headers: %s' % headers)
        logging.debug('QueryString: ', query)
        if method == 'GET':
            return requests.get(url, headers=headers) if headers != None else requests.get(url, params=query)
        else:
            return requests.post(url, headers=headers, data=data) if headers != None else requests.post(url, data=data)        
        
    def __init__(self):
        self.is_holiday = False        
        self.is_holiday_list = []        
    
    def checkHoliday(self, day = None):
        if day == None:
            day = datetime.now()
        logging.debug('checkHoliday :', day)
                
        if (self.is_holiday_list.__len__ == 0) or (self._CALENDER_MONTH != day.month):
            self._CALENDER_MONTH = day.month
            self.is_holiday_list = []
            NumberOfDays = calendar.monthrange(day.year, day.month)[1]            
            for x in range(NumberOfDays):
                self.is_holiday_list.append(False)

            query = {"solYear" :day.strftime("%Y"), "solMonth" : day.strftime("%m") , "NumOfRows" : 30, "_type" : "json", "ServiceKey" : self._API_KEY}
            logging.debug(query)
            resp = self._req(host=self._API_SpcdeInfoService, path=self._API_SpcdeInfoService_PATH, method='GET', query=query )
            if resp.status_code > 400:
                logging.error(resp.text)
                return False
            
            logging.debug(resp.text)
            retJson = json.loads(resp.text)
            logging.debug(retJson)
            if(retJson["response"]["header"]["resultMsg"] == "NORMAL SERVICE."):
                for y in retJson["response"]["body"]["items"]["item"]:
                    if y["isHoliday"] == "Y":
                        hday = y["locdate"]
                        myDay = datetime.strptime(str(hday), "%Y%m%d")
                        self.is_holiday_list[myDay.day-1] = True

        if( day.weekday() > 5 ):
            self.is_holiday = True
            return True
        
        if( self.is_holiday_list[day.day-1] == True ):
            self.is_holiday = True
            return True
        else:
            self.is_holiday = False
            return False

