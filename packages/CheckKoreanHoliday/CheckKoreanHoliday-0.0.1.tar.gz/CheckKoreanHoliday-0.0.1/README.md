## CheckKoreanHoliday

Check the day is holiday or not

You need api key from "data.go.kr"

check below url for api key 

[한국천문연구원_특일 정보 API](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15012690)


> pip install CheckKoreanHoliday
>
> from CheckKoreanHoliday import CheckKoreanHoliday
>
> foo = CheckKoreanHoliday.CheckKoreanHoliday()
>
> print(foo.checkHoliday()) #for today
>
> from datetime import datetime
> someday = datetime.strptime('20240903','%Y%m%d')
> print(foo.checkHoliday(someday)) #for someday

