import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load the saved model
model = joblib.load("air_test.pkl")

# Read the car data from CSV
air = pd.read_csv("air_test_data.csv")

#매핑 데이터
city_to_airport_code_kr = {
    '인천': 'ICN',
    '청주': 'CJJ',
    '대구': 'TAE',
    '광주': 'KWJ',
    '부산': 'PUS'
}

city_to_airport_code_jp = {
    '삿포로': 'CTS',
    '후쿠오카': 'FUK',
    '도쿄(하네다)': 'HND',
    '오사카(간사이)': 'KIX',
    '도쿄(나리타)': 'NRT',
    '오키나와': 'OKA'
}

korea_air = {'CJJ':0, 'ICN':1, 'KWJ':2, 'PUS':3, 'TAE':4}
japan_air = {'CTS':0, 'FUK':1, 'HND':2, 'KIX':3, 'NRT':4, 'OKA':5}

seat_class_mapping = {
    'economy': 0,
    'premium': 1,
    'business': 2,
    'first': 3

}
flight_mapping = {'직항': 0, '1회경유': 1, '그외': 2}

#질문지 작성
air_arr = st.radio('출발 공항', list(city_to_airport_code_kr.keys()), label_visibility="collapsed", horizontal=True)
                                   
air_det = st.radio('도착 공항', list(city_to_airport_code_jp.keys()), label_visibility="collapsed", horizontal=True)

grade=st.radio('클래스',  list(seat_class_mapping.keys()), label_visibility="collapsed", horizontal=True)
   
   
start_date = st.date_input("시작 날짜")
end_date = st.date_input("종료 날짜") 

time_taken=st.radio('항공편',  list(flight_mapping.keys()), label_visibility="collapsed", horizontal=True)

# Get departure and arrival times
depart_hour = st.number_input("출발시간 (시)", min_value=0, max_value=23)
depart_minute = st.number_input("출발시간 (분)", min_value=0, max_value=59)
arrival_hour = st.number_input("도착시간 (시)", min_value=0, max_value=23)
arrival_minute = st.number_input("도착시간 (분)", min_value=0, max_value=59)

# 모델 실행에 필요한 값
selected_airport_value = korea_air[city_to_airport_code_kr[air_arr]]
selected_airport_code_japan = japan_air[city_to_airport_code_jp[air_det]]
seat_grade=seat_class_mapping[grade]
sd = start_date.strftime('%Y%m%d')
ed = end_date.strftime('%Y%m%d')
taken = flight_mapping[time_taken]
# 출발지	도착지	날짜	항공편	가격	좌석등급	출발시간_시	출발시간_분	도착시간_시	도착시간_분

if st.button("예측하기"):
  input_values=[selected_airport_value,selected_airport_code_japan,sd,taken,seat_grade,depart_hour,depart_minute,arrival_hour,arrival_minute]
  # 입력 특성들을 2D 배열 형태로 변환합니다 (예: np.array 사용)
  input_array = np.array([input_values])
  # 예측 결과를 result 변수에 저장한다고 가정합니다. 이 부분은 모델의 예측 방식에 따라 달라집니다.
  result = model.predict(input_array)

  # Show the prediction result to the user
  st.write("예측 결과:", result)