import streamlit as st
import pandas as pd
import joblib
import numpy as np
# Load the saved model
model = joblib.load("car_rf_model.pkl")

# Read the car data from CSV
car = pd.read_csv("car_total.csv")

# 지역명을 숫자로 매핑하는 딕셔너리를 생성합니다
region_mapping = {
    '도쿄': 0,'삿포로': 1,'오사카': 2,'오키나와': 3,'후쿠오카': 4}
# 공항명을 숫자로 매핑하는 딕셔너리
air_mapping = {'CTS': 0,'FUK': 1,'HND': 2,'KIX': 3,'KKJ': 4,'NRT': 5,'OKA': 6}

# 자동차명을 숫자로 매핑하는 딕셔너리
car_mapping = {
   '86': 0,'C-HR': 1,'eK 왜건': 2,'노트 5도어': 3,'노트 E-파워': 4,'데미오': 5,'델리카 8인승': 6,'라이즈': 7,'랜드 크루저 프라도': 8,'레보그': 9,
   '루미': 10,'무브 콘테': 11,'벨파이어 8인승': 12,'복시': 13,'비츠': 14,'스마일': 15,'스텝왜건': 16,'스텝왜건 8인승': 17,'시엔타': 18,'시엔타 6인승': 19,
   '아쿠아': 20,'알파드': 21,'알파드 8인승': 22,'야리스': 23,'엔박스': 24,'왜건 R': 25,'이클립스 크로스': 26,'임프레자': 27,'캠리': 28,'코롤라': 29,
   '코롤라 필더': 30,'큐브': 31,'크라운': 32,'태프트': 33,    '프리우스': 34,'피트': 35,'하이에이스 그랜드 캐빈': 36,'허슬러': 37
}
# 차량 크기를 숫자로 매핑하는 딕셔너리
car_size_mapping = {'RV': 0,'SUV': 1,'경형': 2,'대형': 3,'소형': 4,'왜건': 5,'준중형': 6,'중형': 7}

# 보험을 숫자로 매핑하는 딕셔너리
insurance_mapping = {'면책커버보험 포함': 0,'스탠다드플랜 포함': 1,'프리미엄플랜 포함': 2}

# 브랜드명을 숫자로 매핑하는 딕셔너리
brand_mapping = {'닛산': 0,'다이하쓰': 1,'도요타': 2,'마쯔다': 3,'미쓰비시': 4,'스바루': 5,'스즈키': 6,'혼다': 7}

# region_encoded, air_encoded, size_encoded, brand_encoded
# 날짜 선택
start_date = st.date_input("시작 날짜")
end_date = st.date_input("종료 날짜")

num_passengers = st.number_input("여행 인원수를 입력해주세요.", min_value=1, max_value=10, value=1, step=1)

region = st.radio('지역', list(region_mapping.keys()), label_visibility="collapsed", horizontal=True)
filtered_cars = car[car['지역'] == region]
air = st.radio('공항', filtered_cars['공항'].drop_duplicates().tolist(), label_visibility="collapsed", horizontal=True)


capacity = st.radio('원하는 차종을 선택해주세요', car['크기'].drop_duplicates().tolist(), label_visibility="collapsed", horizontal=True)
if capacity:
    filtered_cars = car[car['크기'] == capacity]
    car_size_list = filtered_cars['브랜드'].drop_duplicates().tolist()
    selected_brand = st.radio('원하는 브랜드를 선택해주세요', car_size_list, label_visibility="collapsed", horizontal=True)

    filtered_cars_by_brand = filtered_cars[filtered_cars['브랜드'] == selected_brand]
    car_name_list = filtered_cars_by_brand['이름'].drop_duplicates().tolist()

insurance = st.radio('원하는 보험을 선택해주세요', car['보험'].drop_duplicates().tolist(), label_visibility="collapsed", horizontal=True)

region_encoded = region_mapping[region]
air_encoded = air_mapping[air]
sd = start_date.strftime('%Y%m%d')
ed = end_date.strftime('%Y%m%d')
size_encoded = car_size_mapping[capacity]
insurance_encoded = insurance_mapping[insurance]
brand_encoded = brand_mapping[selected_brand]

result_list = []
if st.button("예측하기"):
    for name in car_name_list:
      name_encoded = car_mapping[name]
      input_values=[region_encoded,air_encoded,name_encoded,sd,ed,size_encoded,num_passengers,insurance_encoded,brand_encoded]
      input_array = np.array([input_values])
      result_list.append(model.predict(input_array))

    result_array = np.array(result_list)
    min_price = result_array.min()
    max_price = result_array.max()
    st.write(f"{min_price} ~ {max_price}")