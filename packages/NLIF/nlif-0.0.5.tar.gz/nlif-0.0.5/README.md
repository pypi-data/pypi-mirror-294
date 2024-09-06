# NLIF
ChatGPT API를 이용하여 자연어 문장을 조건문으로써 활용할 수 있도록 해주는 프로젝트
(https://pypi.org/project/NLIF/)

# 목차
- [설치](#설치)
- [활용 예시](#활용-예시)
- [Contact](#contact)

# 설치
```
pip install NLIF
```

# 활용 예시
```python
from NLIF import *

ni = NLIF('Your OpenAI API key')

if ni.nlif('Whales are mammals'):
    print('True')
else:
    print('False')
```

# Contact
| Maintainer | e-mail |
|---------|---------|
| marmot8080 | marmot8080@gmail.com |