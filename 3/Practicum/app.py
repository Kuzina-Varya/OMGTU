import streamlit as st
import pandas as pd
import joblib
import os
from sklearn.preprocessing import StandardScaler
import numpy as np


st.set_page_config(page_title="Рекомендательная система профиля активности", layout="centered")
st.title(" Рекомендательная система профиля активности")


page = st.sidebar.selectbox("Выберите страницу", ["Прогноз", "О модели"])


if page == "Прогноз":
    st.header("Загрузите данные пользователя")
    
    uploaded_file = st.file_uploader("Выберите CSV-файл с данными", type=["csv"])
    
    if uploaded_file is not None:
        try:
            
            df_input = pd.read_csv(uploaded_file)
            st.write("Загруженные данные:")
            st.dataframe(df_input.head())
            
            
            if 'subj_id' not in df_input.columns:
                st.error(" В файле отсутствует столбец 'subj_id'!")
            else:
                
                cols_to_drop = ['activity', 'time_s']
                for col in cols_to_drop:
                    if col in df_input.columns:
                        df_input = df_input.drop(col, axis=1)
                
                
                subj_ids = df_input['subj_id'].copy()
                X_input = df_input.drop('subj_id', axis=1)
                
               
                categorical_cols = ['gender', 'race']
                if set(categorical_cols).issubset(X_input.columns):
                    X_input = pd.get_dummies(X_input, columns=categorical_cols, drop_first=True)
                
               
                model = joblib.load('best_activity_model.pkl')
                expected_features = model.feature_names_in_ if hasattr(model, 'feature_names_in_') else None
                
                if expected_features is not None:
                    
                    for col in expected_features:
                        if col not in X_input.columns:
                            X_input[col] = 0
                    
                    X_input = X_input[expected_features]
                
              
                y_pred_encoded = model.predict(X_input)
                
                
                le = joblib.load('label_encoder.pkl')  
                y_pred_labels = le.inverse_transform(y_pred_encoded)
                
               
                result_df = pd.DataFrame({
                    'subj_id': subj_ids,
                    'predict': y_pred_labels
                })
                
                st.success(" Прогноз успешно сформирован!")
                st.write("Результат:")
                st.dataframe(result_df)
                
                
                csv = result_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label=" Скачать результат (CSV)",
                    data=csv,
                    file_name="prediction_result.csv",
                    mime="text/csv"
                )
        
        except Exception as e:
            st.error(f" Ошибка при обработке файла: {str(e)}")


else:
    st.header(" О модели и данных")
    
    st.subheader("Исходный набор данных")
    st.markdown("""
    - Данные содержат **сенсорные измерения** с устройств на запястье, бедре и лодыжках.
    - Признаки: ускорение по осям X, Y, Z (в единицах g).
    - Метаданные: возраст, рост, вес, пол, раса, правша/левша.
    - Целевая переменная: тип активности — 
      `walking`, `ascending stairs`, `descending stairs`, `driving`, `non-study activity`.
    - Всего ~4000 наблюдений.
    """)
    
    st.subheader("Механизм работы модели")
    st.markdown("""
    - Используется **Random Forest Classifier** — ансамблевый метод, основанный на множестве решающих деревьев.
    - Модель **не требует масштабирования данных** и устойчива к шуму.
    - На этапе обучения были удалены признаки с утечкой (`time_s`), закодированы категориальные переменные.
    - Точность на тесте: **94.6%**, F1-score: **94.5%**, ROC-AUC: **99.6%**.
    - Модель сохранена в файл `best_activity_model.pkl`.
    """)
    
    st.subheader("Как использовать")
    st.markdown("""
    1. Подготовьте CSV-файл с теми же столбцами, что и в обучающем наборе (без `activity`).
    2. Обязательно включите столбец `subj_id`.
    3. Загрузите файл в приложение.
    4. Получите прогноз и скачайте результат.
    """)