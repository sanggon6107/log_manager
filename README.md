# CSV 파일 매니저
## Why did I made this?
회사 잡무를 줄여주기 위해 만든 csv파일 처리기이다.  
pandas의 인덱싱이나 데이터 추출 등의 문법도 익힐 수 있는 기회가 될 것이라 판단했고, 현재 업무 뿐만 아니라 광범위하게 필요한 업무임에도 아무도 자동화를 해놓지 않아서 직접 만들게 되었다.

## 기능
현재 회사 로그는 데이터 프레임으로 바로 쓰기 힘들 형태로 되어있어서 정제 과정을 거쳐야 한다. 해당 코드에서는 단순히 "이어붙이기만 한" 로그 파일들을 하나의 로그로 정리해주고, 특정
조건을 만족하는 데이터만을 추출해준다.