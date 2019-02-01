# 모듈에 대한 설명

```python
from PyFGOkr import <모듈 이름>
import PyFGOkr.<모듈 이름>
```

19.01.29 기준 패키지 안에는 네가지 모듈이 있습니다. 사용할 때는 다른 외부 패키지를 이용하실 때처럼 참조할 수 있는 위치에 폴더를 배치한 뒤 import 시켜주세요. discord형 함수들을 이용할 때엔 입력 방식을 꼭 확인해주세요. 

[Discord.py](https://discordpy.readthedocs.io/en/rewrite/index.html)에서 입력한 인자 값은 별다른 옵션 없이 받을 경우 tuple 형태로 파싱되어 넘어오는데, '문자열'을 인자로 하는 함수들은 `' '.join(args)` 같은 함수를 이용하여 문자열로 변환하여 입력시켜야 정상적으로 작동합니다.

| 모듈 이름     |                         기능                          |
| ------------- | :---------------------------------------------------: |
| [calc](#calc) |    FGO의 일반적인 계산 기능을 담당하는 모듈입니다.    |
| [gacha](#gacha)         |       뽑기와 관련된 기능을 담당하는 모듈입니다.       |
| [servstat](#servstat)      | 서번트에 대한 정보를 데이터화 시키기 위한 모듈입니다. |
| [view_pickup](#view_pickup)   |    각종 픽업과 관련된 기능을 담당하는 모듈입니다.     |
| [itemsurfer](#itemsurfer) | 입력한 재료를 효율적으로 파밍할 수 있는 지역을 찾아주는 모듈입니다. |

## [calc](#모듈에-대한-설명)

| 함수 이름                     | 기능                                                         |
| ----------------------------- | :----------------------------------------------------------- |
| fgo_req_exp(...)              | 경험치를 계산하는 함수입니다.                                |
| fgo_np_calc(...)              | 보구 데미지를 계산하는 함수입니다.                           |
| fgo_gain_np_calc(...)         | NP 게이지 수급량을 계산하는 함수입니다.                      |
| fgo_ap_recover_calc(...)      | AP 회복 시간을 계산하는 함수입니다.                          |
| fgo_req_exp_out_discord(...)  | 경험치를 계산하는 함수입니다. 출력 양식이 디스코드에 맞춰졌습니다. |
| fgo_np_calc_discord(...)      | 보구 데미지를 계산하는 함수입니다. 출력 양식이 디스코드에 맞춰졌습니다. |
| fgo_gain_np_calc_discord(...) | NP 게이지 수급량을 계산하는 함수입니다. 출력 양식이 디스코드에 맞춰졌습니다. |

```python
fgo_req_exp(from_int, to_int)
```

현재 레벨에서 목적한 레벨까지 올릴 때 필요한 금색 경험치 카드 개수를 반환합니다. 요소가 2개인 list 자료형으로 반환됩니다. 첫번째 요소는 클래스 보정이 없을 때 필요한 개수를 나타내며 두번째 요소는 클래스 보정을 받을 때 필요한 개수입니다.

- *from_int*
  현재 레벨

- *to_int*
  목표 레벨

```python
fgo_np_calc(atk=14323, card='B', issingle=False, nplevel=1, npupgrade=False, sclass='세이버', rand='', hidden='', atkbuff='0%', colorbuff='0%', npbuff='0%', satk='0%', npsatk='0%', atkconst='0', advantage='', times='')
```

인자값을 적용한 보구 데미지를 계산하여 반환합니다. 각 파라미터에는 default 설정이 되어있어 해당하는 부분만 넣어주면 됩니다.

- *atk*
  서번트의 현재 공격력
- *card*
  보구 카드의 종류. 퀵: 'Q', 아츠:  'A', 버스트:  'B'
- *issingle*
  대인 보구일 경우 True, 대군 보구일 경우 False
- *nplevel*
  보구 레벨 (1~5)
- *npupgrade*
  보구 강화 여부. True면 보구가 강화된 상태
- *sclass*
  클래스 공격력 보정을 위한 서번트의 클래스를 입력
- *rand*
  난수값. '최소'와 '최대' 옵션이 존재합니다.
- *hidden*
  히든 상성. '불리'와 '유리' 옵션이 있습니다.
- *atkbuff*
  공격력 버프 수치
- *colorbuff*
  카드 버프 수치. 버스트 카드 강화(멀린), 아츠 카드 강화(타마모), 퀵 카드 강화 등등.
- *npbuff*
  보구 버프 수치
- *satk*
  특공 버프 수치
- *npsatk*
  보구에 달린 특공 버프 수치(ex: 길가메쉬)
- *atkconst*
  배수가 아닌 상수로 상승하는 공격력 버프(ex: 제갈공명의 3스킬)
- *advantage*
  상성 유불리 여부. '상성'과 '역상성' 옵션이 존재
- *times*
  블라드 3세나 프랑처럼 임의 배율을 가진 캐릭터의 보구 데미지 계산을 위한 임의 배율 설정

```python
fgo_gain_np_calc(efficiency='0.86%', hit=2, card='A', eclass='세이버', firstcard='A', order=1, colorbuff='0%', gainbuff='0%', iscritical=False, isoverkill=False)
```

인자값을 적용한 NP게이지 습득량을 계산하여 반환합니다. 모든 인자에 default 값이 입력되어 있으므로 해당하는 값만 넣어주면 됩니다.

- *efficiency*
  타당 np 수급률
- *hit*
  타수
- *card*
  카드 종류. 퀵: 'Q', 아츠: 'A', 버스트: 'B'
- *eclass*
  보정값 계산을 위한 적 클래스를 입력
- *firstcard*
  첫수 카드 종류. 퀵: 'Q', 아츠: 'A', 버스트: 'B'
- *order*
  계산할 카드의 위치. 1~3. 보구 및 엑스트라 공격은 1로 입력
- *colorbuff*
  카드 버프 수치
- *gainbuff*
  np 수급률 버프
- *iscritical*
  크리티컬이 적용된 경우 True
- *isoverkill*
  오버킬이 적용된 경우 True

```python
fgo_ap_recover_calc(nowap, maxap)
```

현재 AP와, 목표 AP를 입력하여 해당 AP까지 회복되는 시점의 시간을 반환합니다. `dict` 자료형으로 반환됩니다.

```json
{
    "day" : integer, # 0이면 오늘, 1이면 하루 뒤
    "hour" : integer, # 해당 시점의 '시'
    "min" : integer # 해당 시점의 '분'
}
```

가령 { "day" : 1, "hour" : 3, "min" : 45 }는 하루 뒤 3시 45분에 목표 수치까지 AP가 회복된다는 의미입니다.

- *nowap*
  현재 AP
- *maxap*
  목표 AP

```python
fgo_req_exp_out_discord(args)
```

숫자 두 개를 입력받아(list 자료형) 종화 개수에 대한 문자열을 반환합니다.

- *args*
  입력예제 ) ['1', '80']. discord.py에서는 명령어에 관한 인자값을 tuple 형으로 묶어서 주므로 일반적으론 그대로 입력해도 됩니다. 만약 제대로 작동하지 않을 경우 list로 변환하여 넣어주세요.

```python
fgo_np_calc_discord(input_str)
```

문자열을 입력받아 보구 데미지를 반환합니다.

- *input_str*

  ```python
  "공:14323  버스트  대인|대군   보렙:1~5  보퀘  클래스:세이버  난수:최소|입력안함|최대 히든:불리|입력안함|유리  공뻥:30%  색뻥:20%  보뻥:20% 일반특공:10%  보구특공:50%  추가데미지:100  배율:600%  상성|역상성"
  # 입력 예제
  ```

  기본값이 설정되어 있으므로 해당되는 인자만 입력하면 됩니다.

```python
fgo_gain_np_calc_discord(input_str)
```

문자열을 입력받아 NP 게이지 수급량을 반환합니다.

- *input_str*

  ```python
  "수급:0.87% 색뻥:44% 수급뻥:25% 적:라이더 타수:6 카드:아츠 순:3 첫수:아츠 크리티컬 오버킬"
  # 입력 예제
  ```

  기본값이 설정되어 있으므로 해당되는 인자만 입력하면 됩니다.

## [gacha](#모듈에-대한-설명)

> pip install Pillow

| 함수 이름           | 기능                                                         |
| ------------------- | ------------------------------------------------------------ |
| gacha_simulate(...) | 조건을 넣고 해당 조건을 완수할 때의 뽑기 결과를 텍스트로 시뮬레이션합니다. |
| gacha_run(...)      | FGO의 10연차를 시뮬레이션하여 이미지를 생성합니다. 생성된 이미지의 주소가 반환됩니다. |
| gacha_clear()       | 지금까지 만든 10연차 결과 이미지를 모두 삭제합니다.          |

```python
gacha_simulate(args=[], np_lvl=1, star=5, option='string')
```

조건을 입력하고, 조건이 완수될 때의 뽑기 결과를 시뮬레이션하는 함수입니다. 목표 보구 레벨과 레어도(4 or 5)를 입력하면 해당 레어도 서번트의 단일 픽업으로 가정하고, 목표를 달성할 때의 결과를 옵션에 따라 반환합니다. 이 함수를 실행하는 방법은 두 가지가 있습니다.

option의 인자를 'data'로 줄 때와, 주지 않고 'string'으로 실행할 때입니다. 'string'일 때는 결과가 지정된 문자열로 반환되지만 'data' 옵션일 때는 결과가 dict 자료형으로 반환됩니다.

* *args*
  discord 환경에서 이용할 때를 가정하여 설정된 인자입니다. discord.py는 기본적으로 텍스트 입력을 tuple 자료형으로 받아오기 때문에 `gacha_simulate(args)`처럼 큰 가공 없이 그대로 넣어주면 됩니다.

  ```python
  "보<숫자> <4성 또는 5성>"
  "보1 4성"
  "보5 5성"
  # 입력 예제. default 인자 값은 "보1 5성"입니다.
  ```

* *np_lvl*
  보구 레벨. 기본적으로 1이 지정되어 있습니다.

* *star*
  서번트의 레어도. 4 또는 5를 인자로 받습니다. 기본은 5입니다.

* *option*
  반환되는 자료형. 기본은 'string'이며 'data'를 설정값으로 줄 수도 있습니다. 이 때는 dict 자료형으로 반환됩니다.

```python
gacha_run(key='temp')
```

Fate/Grand Order의 10연차를 시뮬레이션하여 이미지를 생성하는 함수입니다. 이미지는 "img/result/" 폴더 내부 디렉터리에 생성됩니다. 반환되는 값은 생성된 이미지의 주소입니다. img 폴더의 <servant_star3~yejang_star5> 폴더 안에 있는 파일들을 리소스로 삼아 이미지를 만들어냅니다. 뽑기를 최신화하고 싶다면 <img/now_pickup.png>와 각 폴더 내부의 파일들을 수정해주면 됩니다.

각 폴더 내의 pickup 폴더 안에 있는 파일은 픽업 대상 요소로, 픽업 확률이 적용됩니다.

* *key*
  웹 애플리케이션 등, 거의 동시에 여러 사용자로부터 요청이 들어왔을 때 이미지가 덮어씌여지는걸 방지하기 위해 설정하는 값입니다. 구현적으로 보면 result 폴더 내부에 생성되는 폴더의 접두어를 뜻합니다. 저는 discord.py를 이용한 채팅 봇을 개발할 때 key 값으로 채팅한 유저의 ID를 이용하였습니다. default 값은 'temp'입니다.

```python
gacha_clear(resultpath='')
```

대상 뽑기 결과 이미지 폴더를 비웁니다. 인자값이 입력되지 않을 경우 해당 폴더를 모두 비웁니다.

* *resultpath*
  뽑기 결과 이미지 폴더 주소를 입력하면 해당 폴더만 삭제할 수 있습니다. `gacha_run()`으로 얻은 주소를 통해 이미지를 출력한 후 `gacha_clear()`의 인자로 넣는 방식으로 활용할 수 있습니다.

## [servstat](#모듈에-대한-설명)

> pip install requests

> pip install bs4

| 함수 이름   | 기능                                                         |
| ----------- | ------------------------------------------------------------ |
| out_dict    | 서번트에 대한 정보를 웹에서 크롤링하여 dict 자료형으로 반환합니다. |
| out_discord | 서번트에 대한 정보를 웹에서 크롤링하여 discord 환경에 맞는 문자열로 반환합니다. |

```python
out_dict(cls, srvn)
```

나무위키 페이지에서 데이터를 파싱하여 dict 자료형으로 반환하는 함수입니다. 대체적으로는 잘 작동하지만 일부 양식이 다른 페이지는 다른 서번트 페이지처럼 수정하기 전까진 제대로 작동하지 않는 경우가 있으니 유의해주세요.

* *cls*
  서번트의 클래스 이름
* *srvn*
  서번트의 이름

```python
out_discord(args)
```

나무위키 페이지에서 데이터를 파싱하여 discord 환경에 맞는 문자열로 반환하는 함수입니다. 대체로 잘 작동하지만 상정한 양식과 다른 서번트 페이지는 의도된 것처럼 출력되지 않는 경우가 있습니다.

* args
  discord.py에서 얻은 인자값을 그대로 넣어주면 됩니다.

  ```python
  ('아처', '에미야', '|보구|스탯|스킬|입력안함|')
  # 입력 예제
  # discord 상에서는 "아처 에미야 스킬"이라고 치기만 하면 위와 같이 넘어갑니다.
  ```

## [view_pickup](#모듈에-대한-설명)

> pip install sqlite3

| 함수 이름                  | 기능                                                         |
| -------------------------- | ------------------------------------------------------------ |
| data_servant_pickup(...)   | 해당 서번트의 픽업에 관한 데이터를 반환하는 함수             |
| data_pickups(...)          | 해당 년도에 있었던 픽업에 관한 데이터를 반환하는 함수        |
| data_pickup(...)           | 특정 픽업에 관한 데이터를 반환하는 함수                      |
| search_pickup_discord(...) | 해당 서번트의 픽업에 관한 데이터를 디스코드에 적합한 문자열로 반환하는 함수 |
| call_discord(...)          | 지정한 옵션에 따른 픽업 정보를 디스코드에 적합한 형식의 문자열로 반환하는 함수 |

```python
data_servant_pickup(sclass, sname)
```

지정 서번트에 대한 픽업 정보를 dict 자료형으로 반환합니다.

* *sclass*
  서번트의 클래스
* *sname*
  서번트의 이름

```python
data_pickups(year)
```

지정 년도에 있었던 모든 픽업을 dict 자료형으로 반환합니다.

* *year*
  년도

```python
data_pickup(id)
```

해당 id의 픽업에 대한 데이터를 dict 자료형으로 반환합니다.

* *id*
  대상 픽업의 id값

```python
search_pickup_discord(args)
```

서번트 픽업에 대한 정보를 디스코드에 적합한 형태로 출력할 수 있게 문자열로 반환하는 함수입니다.

* *args*
  discord.py에서 받아온 tuple을 그대로 넘겨주면 됩니다.

  ```python
  "라이더 메두사"
  # 입력 예제
  ```

```python
call_discord(input_str)
```

지정 옵션에 따른 정보를 디스코드에 적합한 형태의 출력할 수 있게 문자열로 반환하는 함수입니다.

* *input_str*
  입력 문자열입니다. '-<년도 기호> =<페이지> :<픽업 id>'의 양식으로 넣어주면 됩니다. 만약 입력이 없이 함수가 호출된다면 년도 기호가 있는 픽업 리스트의 첫페이지를 반환합니다. 이거만 봐서는 이해가 안 될테니 입력 예제를 참고해주세요.

  ```python
  '-a' # 2015년의 1페이지를 반환
  '-a =2' # 2015년 픽업의 2페이지를 반환
  ':1' # 페그오 사상 첫번째 픽업을 반환
  ```

## [itemsurfer](#모듈에-대한-설명)

> pip install gspread

> pip install --upgrade oauth2client

> pip install PyOpenSSL

| 모듈 정보                    | 기능                                                         |
| ---------------------------- | ------------------------------------------------------------ |
| Pickup_data(...)             | Pickup data 객체를 생성하는 생성자 함수입니다. 생성하면서 옵션에 따라 data 필드가 생성됩니다. |
| Pickup_data.make_json()      | 구글 시트로부터 받아온 정보를 json 파일로 만들고, data 필드에 dict  형태로 저장합니다. |
| Pickup_data.make_keyfile()   | data 필드로부터 번역 이전의 원본 key 파일을 생성합니다.      |
| Pickup_data.search_item(...) | 지정한 재료에 관한 효율 정보를 dict 자료형으로 반환합니다.   |

itemsurfer는 FGO의 재료 효율성에 대한 데이터를 만들고, 그 데이터를 기반으로 자료를 검색하기 위해 만들어진 모듈입니다. [FGO Reddit](https://www.reddit.com/r/grandorder/)의 [Grand Order FGO Drop Rates](https://docs.google.com/spreadsheets/d/1_SlTjrVRTgHgfS7sRqx4CeJMqlz687HdSlYqiW-JvQA) 시트를 원본 데이터로 삼습니다. 데이터는 아래와 같은 형태로 만들어집니다.

```json
{
    "jp": {
        "Proof of Hero": {
            "rank": [
                {
                    "area": "Okeanos",
                    "quest": "Pirate Ship",
                    "takeap": "12",
                    "ap_per_drop": "20.1",
                    "dropchance": "59.7%"
                },
                {
                    "area": "Orleans",
                    "quest": "Marseille",
                    "takeap": "7",
                    "ap_per_drop": "23.8",
                    "dropchance": "29.5%"
                }
            ]
        }
    },
    "kr": {
        ...
    }
```

key 값이 'jp'인 경우 일본 기준으로, 'kr'의 경우 영판 기준으로 데이터를 반환합니다. 영어 시트에서 받아와 영어로 만들어진 `fgo_item.json` 데이터 파일은 `kr2eng_item.json` 파일을 이용하여 한글로 받은 질의를 영어로 변환한 후, 모듈 폴더 안의 `eng2kr_area.json`,  `eng2kr_quest.json`,  `man_eng2kr_quest.json`을 이용하여 데이터를 한글로 출력시킵니다.

```python
Pickup_data(datajson=False, apijson=apijson)
```

Pickup_data 객체를 생성하는 생성자 함수입니다. `pd = Pickup_data(True)` 같은 식으로 생성해주세요.

이 모듈은 Pickup_data 객체를 통해 기능합니다. 외부 구글 시트로부터 크롤링해 `fgo_item.json` 파일을 만들기 위해선 구글 스프레드 시트 관련 API 키가 필요합니다. apijson 속성의 default 변수 apijson은 기본적으로 `scret_credentials.json` 파일을 지정하니 구글 개발자 콘솔에서 만든 json 파일의 이름을 바꿔 패키지 폴더에 해당 이름으로 넣어주세요.

* *datajson*
  `False`: 구글 시트로부터 데이터를 받아와 json 파일을 만듭니다. 파일 생성에 다소 시간이 요구됩니다.
  `True`: 패키지 폴더 내부의 `fgo_item.json`을 참조합니다.

* *apijson*
  구글 스프레드를 다루기 위해 참조할 API key 파일을 입력 받는 변수입니다. 파일 이름 설정을 따로 하지 않는다면 폴더 내부의  `secret_credentials.json` 파일을 참조합니다.

```python
Pickup_data.make_json()
```

이미 생성된 객체의 data 필드 업데이트를 위해 구글 시트로부터 json 파일을 새로 만든 후 해당 파일로 새로이 참조시키는 메소드입니다.

```python
Pickup_data.make_keyfile(option='all', recur_data=[])
```

`raw_.json` 파일로 생성됩니다. 생성된 `raw_.json` 파일들의 value를 채워줌으로서 해석 리소스로 이용이 가능합니다. value를 다 채워주신 후, raw_를 제거시키면 데이터 파일로 이용이 가능합니다. `eng2kr_quest.json`의 경우 `itemsurfer_transmaker.py`를 이용하면 쉽게 생성하실 수 있습니다.

* *option*
  `'item'`: 재료 이름에 대한 raw 파일을 생성합니다.
  `'area'`: 지역 이름에 대한 raw 파일을 생성합니다.
  `'quest'`: 퀘스트 이름에 대한 raw 파일을 생성합니다.

  `'all'`: 재료 이름, 지역 이름, 퀘스트 이름에 대한 raw 파일을 생성합니다.
  `'manquest'`: `eng2kr_quest.json` 파일을 참조하여 퀘스트 이름에 대한, 수동입력해야만 하는 데이터인 `man_eng2kr_quest.json`을 만듭니다. 만약 데이터가 없다면 새로 생성하고, 데이터가 있다면 새로 채워야하는 key 값만 추가됩니다.

* *recur_data*
  재귀 함수로 사용하기 위해 있는 인자값입니다. 값을 넣지 말아주세요.

# 그 외

픽업의 경우 픽업 순서와 실제와 다른 부분이 일부 있습니다. 가령 '클래스별 픽업'의 경우 DB에 존재하지 않아 픽업 순서상으로 표시되지 않습니다. DISCORD 상에서 어떤 식으로 출력되는지는 example 폴더의 [EXAMPLE.MD](../../example/EXAMPLE.MD) 파일을 참고해주세요.
