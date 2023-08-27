import streamlit as st
import pandas as pd
import pickle
import io
#from sklearn.ensemble import GradientBoostingRegressor
# import xgboost
# from xgboost import XGBRegressor
from PIL import Image
st.markdown(
    f'<p style="font-size: 36px;color:firebrick;font-weight:bold;background-color:lightskyblue;text-align:center;'
    f'padding:20px;border-radius: 10px">Prediction of Plant PFAS Accumulation</p>',
    unsafe_allow_html=True)
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
    st.markdown(
        f'<p style="font-size: 10px">This web app is developed by Jing Qiu and Shuang Wu,under the guidance of Lei Xiang and Ce-Hui Mo in Jinan University, Guangzhou.</p>',
        unsafe_allow_html=True)
    st.markdown('<hr style="border: 1px solid skyblue;">', unsafe_allow_html=True)
    df = pd.read_excel("Leafy_PFAS.xlsx", index_col=0)
    st.markdown(
        f'<p style="font-size: 14px">Enter the compound you want to search for SMILES,</p>',
        unsafe_allow_html=True
    )

    search_term = st.text_input('you can input abbreviate (e.g.,PFBA) or chemical formula (e.g.,C4HF7O2) to obtain SMILES')

    if search_term:
        result_df = df[df.apply(lambda row: search_term.lower() in row.astype(str).str.lower().values, axis=1)]

        if not result_df.empty:  # 如果找到了就显示出来，否则显示没找到,input_SMILES还是默认值PFOA
            st.dataframe(result_df)
            smiles = result_df.index[0]
            st.markdown('<hr style="border: 1px solid skyblue;">', unsafe_allow_html=True)
            input_SMILES = st.text_input('SMILES', value=smiles)
        else:

            st.markdown(
                f'<p style="font-size: 15px;color:red;text-align: center">This compound is outside the predicted range</p>',
                unsafe_allow_html=True
            )
            st.markdown('<hr style="border: 1px solid skyblue;">', unsafe_allow_html=True)
            input_SMILES = st.text_input('SMILES (you can obtain this indicator according to the above SMILES list)', value='C(=O)(C(C(C(C(C(C(C(F)(F)F)(F)F)(F)F)(F)F)(F)F)(F)F)(F)F)O')

    else:
        st.dataframe(df,height=1)
        st.markdown('<hr style="border: 1px solid skyblue;">', unsafe_allow_html=True)
        input_SMILES = st.text_input('SMILES (you can obtain this indicator according to the above SMILES list)', value='C(=O)(C(C(C(C(C(C(C(F)(F)F)(F)F)(F)F)(F)F)(F)F)(F)F)(F)F)O')
        if input_SMILES.strip() == "":
            st.warning("The input value cannot be empty")
    if input_SMILES not in df.index:
        st.warning("The input value cannot be found")
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
            Eprotein = st.number_input(' Edible protein content (%)', min_value=1.84, max_value=30.0, value=18.3,
                                       step=0.1)
        with col9:
            EproRpro = st.number_input('Edible/Root protein content', value=float(Eprotein / Rprotein))
        col1, col2, col3 = st.columns(3)
        with col2:
            st.button("Predict", type="primary", use_container_width=True)
            st.stop()


    des = df.loc[input_SMILES]
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
    col1, col2, col3 = st.columns(3)
    with col2:
        if st.button("Predict",type="primary",use_container_width=True):
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


def show_model2_page():
    st.markdown(
        f'<p style="font-size: 10px">This web app is developed by Jing Qiu and Shuang Wu,under the guidance of Lei Xiang and Ce-Hui Mo in Jinan University, Guangzhou.</p>',
        unsafe_allow_html=True)
    st.markdown('<hr style="border: 1px solid skyblue;">', unsafe_allow_html=True)
    df = pd.read_excel("Fruit_PFAS.xlsx", index_col=0)
    st.markdown(
        f'<p style="font-size: 14px">Enter the compound you want to search for SMILES,</p>',
        unsafe_allow_html=True
    )
    search_term = st.text_input(
        'you can input abbreviate (e.g.,PFBA) or chemical formula (e.g.,C4HF7O2) to obtain SMILES')
    if search_term:
        result_df = df[df.apply(lambda row: search_term.lower() in row.astype(str).str.lower().values, axis=1)]

        if not result_df.empty:  # 如果找到了就显示出来，否则显示没找到,input_SMILES还是默认值PFOA
            st.dataframe(result_df)
            smiles = result_df.index[0]
            st.markdown('<hr style="border: 1px solid skyblue;">', unsafe_allow_html=True)
            input_SMILES = st.text_input('SMILES', value=smiles)
        else:

            st.markdown(
                f'<p style="font-size: 15px;color:red;text-align: center">This compound is outside the predicted range</p>',
                unsafe_allow_html=True
            )
            st.markdown('<hr style="border: 1px solid skyblue;">', unsafe_allow_html=True)
            input_SMILES = st.text_input('SMILES (you can obtain this indicator according to the above SMILES list)',
                                         value='C(=O)(C(C(C(C(C(C(C(F)(F)F)(F)F)(F)F)(F)F)(F)F)(F)F)(F)F)O')

    else:
        st.dataframe(df, height=1)
        st.markdown('<hr style="border: 1px solid skyblue;">', unsafe_allow_html=True)
        input_SMILES = st.text_input('SMILES (you can obtain this indicator according to the above SMILES list)',
                                     value='C(=O)(C(C(C(C(C(C(C(F)(F)F)(F)F)(F)F)(F)F)(F)F)(F)F)(F)F)O')
        if input_SMILES.strip() == "":
            st.warning("The input value cannot be empty")
    if input_SMILES not in df.index:
        st.warning("The input value cannot be found")
        col1, col2, col3 = st.columns(3)
        with col1:
            mm = st.selectbox('Cultivation mode', ['pot', 'filed'])
            if mm == 'pot':
                mode = 0
            else:
                mode = 1
        with col2:
            OC = st.number_input(' Soil organic carbon (%)', min_value=0.41, max_value=2.58, value=1.32, step=0.1)
        with col3:
            pH = st.number_input('pH', min_value=5.17, max_value=8.54, value=7.59, step=0.1)

        col4, col5 = st.columns(2)
        with col4:
            PFASs = st.number_input('PFASs concentration (μg/kg)', min_value=0.01, max_value=623.0, value=0.7,
                                    step=1.0)
        with col5:
            time = st.number_input('Exposure time (day)', min_value=90.0, max_value=240.0, value=140.0, step=1.0)
            # time =st.slider(' "Exposure time" value', min_value=90.0, max_value=240.0, value=140.0)
        col7, col8, col9 = st.columns(3)
        with col7:
            Rprotein = st.number_input('Root protein content (%)', min_value=3.4, max_value=7.0, value=4.0, step=0.1)
        with col8:
            Eprotein = st.number_input('Edible protein content (%)', min_value=1.18, max_value=41.52, value=7.64,
                                       step=0.1)
        with col9:
            EproRpro = st.number_input('Edible/Root protein content', value=float(Eprotein / Rprotein))
        col1, col2, col3 = st.columns(3)
        with col2:
            st.button("Predict", type="primary", use_container_width=True)
        st.stop()

    des = df.loc[input_SMILES]
    HallKierAlpha = float(des[2])
    Kappa3 = float(des[3])
    MinAbsEStateIndex = float(des[4])
    MinAbsPartialCharge = float(des[5])
    MinEStateIndex = float(des[6])
    MinPartialCharge = float(des[7])
    PEOE_VSA14 = float(des[8])
    PEOE_VSA2 = float(des[9])
    LogP = float(des[10])
    hide_input = True
    if not hide_input:  # 隐藏这些
        HallKierAlpha = st.number_input('HallKierAlpha', value=float(HallKierAlpha))
        Kappa3 = st.number_input('Kappa3', value=float(Kappa3))
        MinAbsEStateIndex = st.number_input('MinAbsEStateIndex', value=float(MinAbsEStateIndex))
        MinAbsPartialCharge = st.number_input('MinAbsPartialCharge', value=float(MinAbsPartialCharge))
        MinEStateIndex = st.number_input('MinEStateIndex', value=float(MinEStateIndex))
        MinPartialCharge = st.number_input('MinPartialCharge', value=float(MinPartialCharge))
        PEOE_VSA14 = st.number_input('PEOE_VSA14', value=float(PEOE_VSA14))
        PEOE_VSA2 = st.number_input('PEOE_VSA2', value=float(PEOE_VSA2))
        LogP = st.number_input('LogP', value=float(LogP))

    col1, col2, col3 = st.columns(3)
    with col1:
        mm = st.selectbox('Cultivation mode', ['pot', 'filed'])
        if mm == 'pot':
            mode = 0
        else:
            mode = 1
    with col2:
        OC = st.number_input(' Soil organic carbon (%)', min_value=0.41, max_value=2.58, value=1.32, step=0.1)
    with col3:
        pH = st.number_input('pH', min_value=5.17, max_value=8.54, value=7.59, step=0.1)

    col4, col5 = st.columns(2)
    with col4:
        PFASs = st.number_input('PFASs concentration (μg/kg)', min_value=0.01, max_value=623.0, value=0.7,
                                step=1.0)
    with col5:
        time = st.number_input('Exposure time (day)', min_value=90.0, max_value=240.0, value=140.0, step=1.0)
        # time =st.slider(' "Exposure time" value', min_value=90.0, max_value=240.0, value=140.0)
    col7, col8, col9 = st.columns(3)
    with col7:
        Rprotein = st.number_input('Root protein content (%)', min_value=3.4, max_value=7.0, value=4.0, step=0.1)
    with col8:
        Eprotein = st.number_input('Edible protein content (%)', min_value=1.18, max_value=41.52, value=7.64, step=0.1)
    with col9:
        EproRpro = st.number_input('Edible/Root protein content', value=float(Eprotein / Rprotein))

    features = [[HallKierAlpha, Kappa3, MinAbsEStateIndex, MinAbsPartialCharge, MinEStateIndex, MinPartialCharge,
                 PEOE_VSA14,PEOE_VSA2, LogP, mode, OC, pH, PFASs, time, Rprotein, Eprotein, EproRpro]]
    with open('model_grain.pkl', 'rb') as f:
        model2 = pickle.load(f)
    logECF = model2.predict(features)[0]
    ECF = 10 ** logECF
    ECF = str(round(ECF, 2))
    col1, col2, col3 = st.columns(3)
    with col2:
        if st.button("Predict", type="primary", use_container_width=True):
            st.success(str(ECF))  # 转换ECF为字符串再显示
            ECF = float(ECF)
            if 0.013<=ECF<=97:
                colA, colB, colC = st.columns(3)
                with colB:
                    st.image(Image.open('good.png'))
            elif 0.0005<ECF<0.013 or 97<ECF<2763:
                colA, colB, colC = st.columns(3)
                with colB:
                    st.image(Image.open('moderate.png'))

            else:
                colA, colB, colC = st.columns(3)
                with colB:
                    st.image(Image.open('bad.png'))
    st.markdown('<hr style="border: 1px solid skyblue;">', unsafe_allow_html=True)


def show_model3_page():
    st.markdown(
        f'<p style="font-size: 10px;">This web app is developed by Jing Qiu and Shuang Wu,under the guidance of Lei Xiang and Ce-Hui Mo in Jinan University, Guangzhou.</p>',
        unsafe_allow_html=True)
    st.markdown('<hr style="border: 1px solid skyblue;">', unsafe_allow_html=True)

    df = pd.read_excel("Root_PFAS.xlsx", index_col=0)
    st.markdown(
        f'<p style="font-size: 14px">Enter the compound you want to search for SMILES,</p>',
        unsafe_allow_html=True
    )
    search_term = st.text_input(
        'you can input abbreviate (e.g.,PFBA) or chemical formula (e.g.,C4HF7O2) to obtain SMILES')
    if search_term:
        result_df = df[df.apply(lambda row: search_term.lower() in row.astype(str).str.lower().values, axis=1)]

        if not result_df.empty:  # 如果找到了就显示出来，否则显示没找到,input_SMILES还是默认值PFOA
            st.dataframe(result_df)
            smiles = result_df.index[0]
            st.markdown('<hr style="border: 1px solid skyblue;">', unsafe_allow_html=True)
            input_SMILES = st.text_input('SMILES', value=smiles)
        else:

            st.markdown(
                f'<p style="font-size: 15px;color:red;text-align: center">This compound is outside the predicted range</p>',
                unsafe_allow_html=True
            )
            st.markdown('<hr style="border: 1px solid skyblue;">', unsafe_allow_html=True)
            input_SMILES = st.text_input('SMILES (you can obtain this indicator according to the above SMILES list)',
                                         value='C(=O)(C(C(C(C(C(C(F)(F)F)(F)F)(F)F)(F)F)(F)F)(F)F)O')

    else:
        st.dataframe(df, height=1)
        st.markdown('<hr style="border: 1px solid skyblue;">', unsafe_allow_html=True)
        input_SMILES = st.text_input('SMILES (you can obtain this indicator according to the above SMILES list)',
                                     value='C(=O)(C(C(C(C(C(C(C(F)(F)F)(F)F)(F)F)(F)F)(F)F)(F)F)(F)F)O')
        if input_SMILES.strip() == "":
            st.warning("The input value cannot be empty")
    if input_SMILES not in df.index:
        st.warning("The input value cannot be found")
        col1, col2, col3 = st.columns(3)
        with col1:
            mm = st.selectbox('Cultivation mode', ['pot', 'filed'])
            if mm == 'pot':
                mode = 0
            else:
                mode = 1
        with col2:
            OC = st.number_input('Soil organic carbon (%)', min_value=0.01, max_value=5.85, value=1.6, step=0.1)
        with col3:
            pH = st.number_input('pH', min_value=2.6, max_value=11.7, value=7.29, step=0.1)

        col4, col5 = st.columns(2)
        with col4:
            PFASs = st.number_input('PFASs concentration (μg/kg)', min_value=0.01, max_value=1000.0, value=33.3,
                                    step=1.0)
        with col5:
            time = st.number_input('Exposure time (day)', min_value=1.0, max_value=319.0, value=70.0, step=1.0)

        col6, col7 = st.columns(2)
        with col6:
            Rprotein = st.number_input('Root protein content (%)', min_value=0.0, max_value=9.68, value=4.0, step=0.1)
        with col7:
            Rlipid = st.number_input('Root lipid content (%)', min_value=0.17, max_value=5.0, value=3.23, step=0.1)
        col1, col2, col3 = st.columns(3)
        with col2:
            st.button("Predict", type="primary", use_container_width=True)
        st.stop()


    des = df.loc[input_SMILES]
    TPSA = float(des[2])
    LogP = float(des[3])
    GATSp5 = float(des[4])
    MOMI = float(des[5])
    Weta3 = float(des[6])
    Weta1 = float(des[7])
    QNss = float(des[8])
    EState_VSA8 = float(des[9])
    AATS8i = float(des[10])
    FNSA = float(des[11])
    MATSv6 = float(des[12])
    MATSe7 = float(des[13])
    WPSA = float(des[13])
    ATSC5s = float(des[14])
    AATSC5p = float(des[15])
    MATSv5 = float(des[16])
    ATSC6v = float(des[17])
    AATS2s = float(des[18])
    S7 = float(des[19])
    hide_input = True
    if not hide_input:  # 隐藏这些
        TPSA = st.number_input('TPSA', value=float(TPSA))
        LogP = st.number_input('LogP', value=float(LogP))
        GATSp5 = st.number_input('GATSp5', value=float(GATSp5))
        MOMI = st.number_input('MOMI-XZ', value=float(MOMI))
        Weta3 = st.number_input('Weta3.unity', value=float(Weta3))
        Weta1 = st.number_input('Weta1.unity', value=float(Weta1))
        QNss = st.number_input('QNss', value=float(QNss))
        EState_VSA8 = st.number_input('EState_VSA8', value=float(EState_VSA8))
        AATS8i = st.number_input('AATS8i', value=float(AATS8i))
        FNSA = st.number_input('FNSA', value=float(FNSA))
        MATSv6 = st.number_input('MATSv6', value=float(MATSv6))
        MATSe7 = st.number_input('MATSe7', value=float(MATSe7))
        WPSA = st.number_input('WPSA', value=float(WPSA))
        ATSC5s = st.number_input('ATSC5s', value=float(ATSC5s))
        AATSC5p = st.number_input('AATSC5p', value=float(AATSC5p))
        MATSv5 = st.number_input('MATSv5', value=float(MATSv5))
        ATSC6v = st.number_input('ATSC6v', value=float(ATSC6v))
        AATS2s = st.number_input('AATS2s', value=float(AATS2s))
        S7 = st.number_input('S7', value=float(S7))

    col1, col2, col3 = st.columns(3)
    with col1:
        mm = st.selectbox('Cultivation mode', ['pot', 'filed'])
        if mm == 'pot':
            mode = 0
        else:
            mode = 1
    with col2:
        OC = st.number_input('Soil organic carbon (%)', min_value=0.01, max_value=5.85, value=1.6, step=0.1)
    with col3:
        pH = st.number_input('pH', min_value=2.6, max_value=11.7, value=7.29, step=0.1)

    col4, col5 = st.columns(2)
    with col4:
        PFASs = st.number_input('PFASs concentration (μg/kg)', min_value=0.01, max_value=1000.0, value=33.3,
                                step=1.0)
    with col5:
        time = st.number_input('Exposure time (day)', min_value=1.0, max_value=319.0, value=70.0, step=1.0)

    col6, col7 = st.columns(2)
    with col6:
        Rprotein = st.number_input('Root protein content (%)', min_value=0.0, max_value=9.68, value=4.0, step=0.1)
    with col7:
        Rlipid = st.number_input('Root lipid content (%)', min_value=0.17, max_value=5.0, value=3.23, step=0.1)

    features = [[TPSA, LogP, GATSp5, MOMI, Weta3, Weta1, QNss, EState_VSA8, AATS8i, FNSA, MATSv6, MATSe7, WPSA, ATSC5s,
                 AATSC5p, MATSv5, ATSC6v, AATS2s, S7, mode, OC, pH, PFASs, time, Rprotein, Rlipid]]
    with open('model_root.pkl', 'rb') as f:
        model3 = pickle.load(f)
    logRCF = model3.predict(features)[0]
    RCF = 10 ** logRCF
    RCF = str(round(RCF, 2))
    col1, col2, col3 = st.columns(3)
    with col2:
        if st.button("Predict", type="primary", use_container_width=True):
            st.success(str(RCF))  # 转换ECF为字符串再显示
            RCF = float(RCF)
            if 0.015<=RCF<=42.32:
                colA, colB, colC = st.columns(3)
                with colB:
                    st.image(Image.open('good.png'))
            elif 0.018<RCF<0.015 or 42.32<RCF<347.96:
                colA, colB, colC = st.columns(3)
                with colB:
                    st.image(Image.open('moderate.png'))

            else:
                colA, colB, colC = st.columns(3)
                with colB:
                    st.image(Image.open('bad.png'))
    st.markdown('<hr style="border: 1px solid skyblue;">', unsafe_allow_html=True)


if __name__ == "__main__":
    main()