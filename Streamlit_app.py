import streamlit as st
import pandas as pd
import pickle
import io
#from sklearn.ensemble import GradientBoostingRegressor
# import xgboost
# from xgboost import XGBRegressor
from PIL import Image

html_temp = """
<div style="background-color:lightskyblue;padding:10px;border-radius: 10px;">
    <h1 style="color:firebrick;text-align:center;">Prediction of Plant PFAS Uptake</h1>
</div>
"""
st.markdown(html_temp, unsafe_allow_html=True)
# 添加一个空行
st.markdown("&nbsp;")  # 使用HTML的非断空格实现空行

def main():

    colA, colB,colC = st.columns(3)
    with colA:
        option = st.radio("Choose a prediction model:", ("Leafy crops model", "Fruit/grain crops model", "Root model"))
    if option == "Leafy crops model":
        show_model1_page()
    elif option == "Fruit/grain crops model":
        show_model2_page()
    elif option == "Root model":
        show_model3_page()
    with colC:
        st.image(Image.open('back_leafy.png'))


def show_model1_page():

    st.markdown('<hr style="border: 1px solid skyblue;">', unsafe_allow_html=True)
    SMILES = st.text_input("SMILES (you can obtain this indicator according to the blow SMILES list)", value='C(=O)(C(C(C(C(C(C(C(F)(F)F)(F)F)(F)F)(F)F)(F)F)(F)F)(F)F)O')
    df = pd.read_excel("Leafy_PFAS.xlsx", index_col=0)
    des = df.loc[SMILES]
    SlogP_VSA5 = float(des[2])
    VSA_EState10 = float(des[3])
    VSA_EState9 = float(des[4])
    fr_halogen = float(des[5])
    HBA = float(des[6])
    dbonds = float(des[7])
    LogP = float(des[8])
    hide_input = True
    if not hide_input:  # 隐藏这些
        SlogP_VSA5 = st.number_input('SlogP_VSA5', value=float(SlogP_VSA5))
        VSA_EState10 = st.number_input('VSA_EState10', value=float(VSA_EState10))
        VSA_EState9 = st.number_input('VSA_EState9', value=float(VSA_EState9))
        fr_halogen = st.number_input('fr_halogen', value=float(fr_halogen))
        HBA = st.number_input('HBA', value=float(HBA))
        dbonds = st.number_input('dbonds', value=float(dbonds))
        LogP = st.number_input('LogP', value=float(LogP))

    col1, col2, col3 = st.columns(3)
    with col1:
        mm = st.selectbox('Cultivation mode', ['pot', 'filed'])
        if mm == 'pot':
            mode = 0
        else:
            mode = 1
    with col2:
        OC = st.number_input('Soil organic carbon (%)', min_value=0.005, max_value=6.34, value=1.32, step=0.1)
    with col3:
        pH = st.number_input('pH', min_value=6.1, max_value=8.26, value=7.06, step=0.1)

    col4, col5, col6 = st.columns(3)
    with col4:
        PFASs = st.number_input('PFASs concentration (μg/kg)', min_value=0.01, max_value=1000.0, value=5.0,
                                step=1.0)
    with col5:
        time = st.number_input('Exposure time (day)', min_value=30.0, max_value=224.0, value=60.0, step=1.0)
    with col6:
        Elipid = st.number_input('Edible lipid content (%)', min_value=2.14, max_value=12.3, value=6.45, step=0.1)

    col7, col8, col9 = st.columns(3)
    with col7:
        Rprotein = st.number_input('Root protein content (%)', min_value=0.32, max_value=8.23, value=4.85, step=0.1)
    with col8:
        Eprotein = st.number_input(' Edible protein content (%)', min_value=1.84, max_value=30.0, value=18.3, step=0.1)
    with col9:
        EproRpro = st.number_input('Edible/Root protein content', value=float(Eprotein / Rprotein))

    features = [[SlogP_VSA5, VSA_EState10, VSA_EState9, fr_halogen, HBA, dbonds, LogP, mode, OC, pH, PFASs,
                 time, Rprotein, Eprotein, EproRpro, Elipid]]
    with open('model_leafy.pkl', 'rb') as f:
        model1 = pickle.load(f)
    logECF = model1.predict(features)[0]
    ECF = 10 ** logECF
    ECF = str(round(ECF, 2))
    # 居中显示按钮
    col1, col2, col3 = st.columns(3)
    with col2:

        if st.button("          Prediction ECF", key="prediction_button", help="Click to predict"):
            st.success(str(ECF))  # 转换ECF为字符串再显示

            ECF = float(ECF)
            if 0.076 <= ECF <= 88.1:
                colA, colB, colC = st.columns(3)
                with colB:
                    st.image(Image.open('good.png'))
            elif 0.013 < ECF < 0.076 or 88.11 < ECF < 513.79:
                colA, colB, colC = st.columns(3)
                with colB:
                    st.image(Image.open('moderate.png'))

            else:
                colA, colB, colC = st.columns(3)
                with colB:
                    st.image(Image.open('bad.png'))
    st.markdown('<hr style="border: 1px solid skyblue;">', unsafe_allow_html=True)

    st.markdown(
        f'<p style="font-size: 14px">Enter the compound you want to search for,</p>',
        unsafe_allow_html=True
    )
    search_term = st.text_input('you can input abbreviate (e.g.,PFBA) or chemical formula (e.g.,C4HF7O2) to choose SMILES')
    if search_term:
        result_df = df[df.apply(lambda row: search_term.lower() in row.astype(str).str.lower().values, axis=1)]

        if not result_df.empty:  # 如果找到了就显示出来，否则显示没找到
            st.dataframe(result_df)
        else:
            st.markdown(
                f'<p style="font-size: 20px;color: red;text-align: center">This compound is outside the predicted range</p>',
                unsafe_allow_html=True
            )
    else:
        st.dataframe(df)














def show_model2_page():
    html_temp = """
    <div style="background-color:lightskyblue;padding:10px">
        <h1 style="color:black;text-align:center;">Prediction of Edbile Part PFAS Uptake</h1>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)

def show_model3_page():
    html_temp = """
    <div style="background-color:lightskyblue;padding:10px">
        <h1 style="color:black;text-align:center;">Prediction of  Part PFAS Uptake</h1>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)

if __name__ == "__main__":
    main()