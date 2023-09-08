import streamlit as st
import pandas as pd
import joblib
import numpy as np
# Load the saved model
model = joblib.load("hotel_rf_model.pkl")

# Read the car data from CSV
hotel = pd.read_csv("hotel_total_final.csv")
# 지역명을 숫자로 매핑하는 딕셔너리를 생성합니다
region_mapping = {
    '도쿄': 0,'삿포로': 1,'오사카': 2,'오키나와': 3,'후쿠오카': 4}
# 지역명을 숫자로 매핑하는 딕셔너리
category_mapping = {'게스트하우스,캡슐호텔,호스텔':0, '리조트,펜션,료칸':1, '호텔':2}
#입실	퇴실	지역	숙박유형	별점	등급	가장 가까운 공항까지 시간

# region_encoded, air_encoded, size_encoded, brand_encoded
# 날짜 선택
start_date = st.date_input("시작 날짜")
end_date = st.date_input("종료 날짜")


# 지역 선택
selected_region = st.radio('원하는 지역을 선택해주세요', hotel['지역'].drop_duplicates().tolist(), label_visibility="collapsed", horizontal=True)
if selected_region:
    filtered_hotels = hotel[hotel['지역'] == selected_region]

    # 숙박 유형 선택
    selected_accommodation_type = st.radio('원하는 숙박유형을 선택해주세요', filtered_hotels['숙박유형'].drop_duplicates().tolist(), label_visibility="collapsed", horizontal=True)
    if selected_accommodation_type:
        filtered_hotels = filtered_hotels[filtered_hotels['숙박유형'] == selected_accommodation_type]

        # 등급 선택
        selected_grade = st.radio('원하는 등급을 선택해주세요', filtered_hotels['등급'].drop_duplicates().tolist(), label_visibility="collapsed", horizontal=True)
        if selected_grade:
            filtered_hotels = filtered_hotels[filtered_hotels['등급'] == selected_grade]
            hotel_name_list = filtered_hotels['호텔명'].drop_duplicates().tolist()

            # 호텔명 출력
            selected_hotel_name = st.radio('호텔명을 선택해주세요', hotel_name_list, label_visibility="collapsed", horizontal=True)
            st.write(f'선택한 호텔명: {selected_hotel_name}')


region = st.radio('지역', list(region_mapping.keys()), label_visibility="collapsed", horizontal=True)

category = st.radio('유형', list(category_mapping.keys()), label_visibility="collapsed", horizontal=True)

star_num = st.number_input("별점 0.0 ~ 10.0", min_value=1, max_value=10, value=8)

grade = st.radio('등급', sorted(hotel['등급'].drop_duplicates().tolist()), index=2, label_visibility="collapsed", horizontal=True)
grade = int(grade[0])

time_num = st.number_input("숙소까지의 시간(분단위) 0 ~ 60", min_value=1, max_value=60, value=20,step=1)

region_encoded = region_mapping[region]
category_encoded = category_mapping[category]
sd = start_date.strftime('%Y%m%d')
ed = end_date.strftime('%Y%m%d')

if st.button("예측하기"):
  input_values=[region_encoded,category_encoded,sd,ed,star_num,grade,time_num]
  # 입력 특성들을 2D 배열 형태로 변환합니다 (예: np.array 사용)
  input_array = np.array([input_values])
  # 예측 결과를 result 변수에 저장한다고 가정합니다. 이 부분은 모델의 예측 방식에 따라 달라집니다.
  result = model.predict(input_array)

  # Show the prediction result to the user
  st.write("예측 결과:", result)