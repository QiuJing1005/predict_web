import streamlit as st
import pandas as pd
import pickle
import io
# from rdkit import Chem
# from rdkit.Chem import Draw
# import xgboost
# from xgboost import XGBRegressorS
from PIL import Image

def main():

    # 添加左侧选项
    option = st.sidebar.radio("Choose a model", ("Leafy crops model", "Fruit/grain crops model","Root model"))

    if option == "Leafy crops model":
        show_model1_page()
    elif option == "Fruit/grain crops model":
        show_model2_page()
    elif option == "Root model":
        show_model3_page()
    img = Image.open('back_leafy.png')
    st.sidebar.image(img)

def show_model1_page():
    html_temp = """
    <div style="background-color:lightskyblue;padding:10px">
        <h1 style="color:black;text-align:center;">Prediction of Edbile Part PFAS Uptake</h1>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)

    with open('model_leafy.pkl', 'rb') as f:
        model1 = pickle.load(f)
        df = pd.read_excel("Leafy_PFAS.xlsx", index_col=0)  # 如果是xlsx文件，使用 pd.read_excel()，如果是csv文件，使用 pd.read_csv()
        search_term = st.text_input('Enter the compound you want to search for：')

        # 利用Pandas的功能，在DataFrame中查找输入的内容
        if search_term:
            result_df = df[df.apply(lambda row: search_term.lower() in row.astype(str).str.lower().values, axis=1)]

            if not result_df.empty:#如果找到了就显示出来，否则显示没找到
                st.dataframe(result_df)
                smiles = result_df.index[0]
                SMILES = st.text_input('Input SMILES', value=smiles)
            else:
                st.markdown(
                    f'<p style="font-size: 20px;text-align: center">This compound is outside the predicted range</p>',
                    unsafe_allow_html=True
                )
                SMILES = st.text_input('Input SMILES',value='C(=O)(C(C(C(C(C(C(C(F)(F)F)(F)F)(F)F)(F)F)(F)F)(F)F)(F)F)O')

        else:
            st.dataframe(df)
            SMILES = st.text_input('Input SMILES', value='C(=O)(C(C(C(C(C(C(C(F)(F)F)(F)F)(F)F)(F)F)(F)F)(F)F)(F)F)O')

        # mol = Chem.MolFromSmiles(SMILES)
        # img = Draw.MolToImage(mol, size=(400, 300), dpi=500)
        #将图像转换为字节流
        # streamlit_image = io.BytesIO()
        # img.save(streamlit_image, format='PNG')
        #在界面上显示图像
        # st.image(streamlit_image)
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
            OC = st.number_input(' "OC" value', min_value=0.005, max_value=6.34, value=1.32, step=0.1)
        with col3:
            pH = st.number_input(' "pH" value', min_value=5.195, max_value=8.675, value=7.06, step=0.1)

        col4, col5, col6 = st.columns(3)
        with col4:
            PFASs = st.number_input(' "PFASs concentration" value', min_value=0.01, max_value=1000.0, value=5.0,
                                    step=1.0)
        with col5:
            time = st.number_input(' "Exposure time" value', min_value=30.0, max_value=224.0, value=60.0, step=1.0)
        with col6:
            Elipid = st.number_input(' "E-lipid" value', min_value=0.0, max_value=19.14, value=6.45, step=0.1)

        col7, col8, col9 = st.columns(3)
        with col7:
            Rprotein = st.number_input(' "R-protein" value', min_value=0.0, max_value=10.85, value=4.85, step=0.1)
        with col8:
            Eprotein = st.number_input(' "E-protein" value', min_value=1.84, max_value=30.0, value=18.3, step=0.1)
        with col9:
            EproRpro = st.number_input('Eprotein / Rprotein', value=float(Eprotein / Rprotein))

        features = [[SlogP_VSA5, VSA_EState10, VSA_EState9, fr_halogen, HBA, dbonds, LogP, mode, OC, pH, PFASs,
                     time, Rprotein, Eprotein, EproRpro, Elipid]]
        logECF = model1.predict(features)[0]
        ECF = 10 ** logECF
        ECF = str(round(ECF, 2))
        # 居中显示按钮
        st.markdown(
            f'<p style="font-size: 30px;text-align: center">Prediction ECF result</p>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<p style="text-align: center; font-size: 30px;">{ECF}</p>',
            unsafe_allow_html=True
        )
        ECF = float(ECF)
        if 0.076 <= ECF <= 88.1:
            st.markdown(
                f'<p style="font-size: 30px;text-align:center ">good</p>',
                unsafe_allow_html=True
            )

        elif 0.013 < ECF < 0.076 or 88.11 < ECF < 513.79:
            st.markdown(
                f'<p style="font-size: 30px;text-align: center">moderate</p>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<p style="font-size: 30px;text-align: center">bad</p>',
                unsafe_allow_html=True
            )

def show_model2_page():
    html_temp = """
        <div style="background-color:lightskyblue;padding:10px">
            <h1 style="color:black;text-align:center;">Prediction of Edbile Part PFAS Uptake</h1>
        </div>
        """
    st.markdown(html_temp, unsafe_allow_html=True)
    #st.markdown("<h2 style='text-align: center;'>Fruit/grain crops model</h2>", unsafe_allow_html=True)

    with open('model_grain.pkl', 'rb') as f:
        model2= pickle.load(f)

        df = pd.read_excel("Fruit_PFAS.xlsx", index_col=0)  # 如果是xlsx文件，使用 pd.read_excel()，如果是csv文件，使用 pd.read_csv()
        search_term = st.text_input('Enter the compound you want to search for：')

        # 利用Pandas的功能，在DataFrame中查找输入的内容
        if search_term:
            result_df = df[df.apply(lambda row: search_term.lower() in row.astype(str).str.lower().values, axis=1)]

            if not result_df.empty:
                st.dataframe(result_df)
                smiles = result_df.index[0]
                SMILES = st.text_input('Input SMILES', value=smiles)
            else:
                st.markdown(
                    f'<p style="font-size: 20px;text-align: center">该化合物不在预测范围</p>',
                    unsafe_allow_html=True
                )
                SMILES = st.text_input('Input SMILES',
                                       value='C(=O)(C(C(C(C(C(C(C(F)(F)F)(F)F)(F)F)(F)F)(F)F)(F)F)(F)F)O')
        else:
            st.dataframe(df)
            SMILES = st.text_input('Input SMILES', value='C(=O)(C(C(C(C(C(C(C(F)(F)F)(F)F)(F)F)(F)F)(F)F)(F)F)(F)F)O')

        # mol = Chem.MolFromSmiles(SMILES)
        # img = Draw.MolToImage(mol, size=(400, 300), dpi=500)
        # # 将图像转换为字节流
        # streamlit_image = io.BytesIO()
        # img.save(streamlit_image, format='PNG')
        # # 在界面上显示图像
        # st.image(streamlit_image)

        des = df.loc[SMILES]
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
            OC = st.number_input(' "OC" value', min_value=0.0, max_value=3.04, value=1.32, step=0.1)
        with col3:
            pH = st.number_input(' "pH" value', min_value=5.17, max_value=8.54, value=7.59, step=0.1)

        col4, col5 = st.columns(2)
        with col4:
            PFASs = st.number_input(' "PFASs concentration" value', min_value=0.01, max_value=623.0, value=0.7,
                                    step=1.0)
            # PFASs = st.slider(' "PFASs concentration" value', min_value=0.01, max_value=623.0, value=0.7)
        with col5:
            time = st.number_input(' "Exposure time" value', min_value=90.0, max_value=240.0, value=140.0, step=1.0)
            # time =st.slider(' "Exposure time" value', min_value=90.0, max_value=240.0, value=140.0)
        col7, col8, col9 = st.columns(3)
        with col7:
            Rprotein = st.number_input(' "R-protein" value', min_value=3.4, max_value=7.0, value=4.0, step=0.1)
        with col8:
            Eprotein = st.number_input(' "E-protein" value', min_value=1.18, max_value=41.52, value=7.64, step=0.1)
        with col9:
            EproRpro = st.number_input('Eprotein / Rprotein', value=float(Eprotein / Rprotein))

        features = [[HallKierAlpha, Kappa3, MinAbsEStateIndex, MinAbsPartialCharge, MinEStateIndex, MinPartialCharge,
                     PEOE_VSA14,
                     PEOE_VSA2, LogP, mode, OC, pH, PFASs, time, Rprotein, Eprotein, EproRpro]]
        logECF = model2.predict(features)[0]
        ECF = 10 ** logECF
        ECF = str(round(ECF, 2))
        st.markdown(
            f'<p style="font-size: 30px;text-align: center">Prediction ECF result</p>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<p style="text-align: center; font-size: 30px;">{ECF}</p>',
            unsafe_allow_html=True
        )
        ECF = float(ECF)
        if 0.013<=ECF<=97:
            st.markdown(
                f'<p style="font-size: 30px;text-align:center ">good</p>',
                unsafe_allow_html=True
            )

        elif 0.0005<ECF<0.013 or 97<ECF<2763:
            st.markdown(
                f'<p style="font-size: 30px;text-align: center">moderatee</p>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<p style="font-size: 30px;text-align: center">bad</p>',
                unsafe_allow_html=True
            )

def show_model3_page():
    html_temp = """
        <div style="background-color:lightskyblue;padding:10px">
            <h1 style="color:black;text-align:center;">Prediction of Root PFAS Uptake</h1>
        </div>
        """
    st.markdown(html_temp, unsafe_allow_html=True)
    with open('model_root.pkl', 'rb') as f:
        model2= pickle.load(f)

    df = pd.read_excel("Root_PFAS.xlsx", index_col=0)  # 如果是xlsx文件，使用 pd.read_excel()，如果是csv文件，使用 pd.read_csv()
    search_term = st.text_input('Enter the compound you want to search for：')

    # 利用Pandas的功能，在DataFrame中查找输入的内容
    if search_term:
        result_df = df[df.apply(lambda row: search_term.lower() in row.astype(str).str.lower().values, axis=1)]

        if not result_df.empty:
            st.dataframe(result_df)
            smiles = result_df.index[0]
            SMILES = st.text_input('Input SMILES', value=smiles)
        else:
            st.markdown(
                f'<p style="font-size: 20px;text-align: center">该化合物不在预测范围</p>',
                unsafe_allow_html=True
            )
            SMILES = st.text_input('Input SMILES',
                                   value='C(=O)(C(C(C(C(C(C(F)(F)F)(F)F)(F)F)(F)F)(F)F)(F)F)O')
    else:
        st.dataframe(df)
        SMILES = st.text_input('Input SMILES', value='C(=O)(C(C(C(C(C(C(F)(F)F)(F)F)(F)F)(F)F)(F)F)(F)F)O')

    # mol = Chem.MolFromSmiles(SMILES)
    # img = Draw.MolToImage(mol, size=(400, 300), dpi=500)
    # # 将图像转换为字节流
    # streamlit_image = io.BytesIO()
    # img.save(streamlit_image, format='PNG')
    # # 在界面上显示图像
    # st.image(streamlit_image)
    des = df.loc[SMILES]

    TPSA = float(des[2])
    LogP = float(des[3])
    GATSp5 = float(des[4])
    MOMI = float(des[5])
    Weta3 = float(des[6])
    Weta1 = float(des[7])
    QNss = float(des[8])
    EState_VSA8 = float(des[9])
    AATS8i = float(des[10])
    FNSA=float(des[11])
    MATSv6=float(des[12])
    MATSe7=float(des[13])
    WPSA=float(des[13])
    ATSC5s=float(des[14])
    AATSC5p=float(des[15])
    MATSv5=float(des[16])
    ATSC6v=float(des[17])
    AATS2s=float(des[18])
    S7=float(des[19])

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
        ATSC5s= st.number_input('ATSC5s', value=float(ATSC5s))
        AATSC5p=st.number_input('AATSC5p', value=float(AATSC5p))
        MATSv5=st.number_input('MATSv5', value=float(MATSv5))
        ATSC6v=st.number_input('ATSC6v', value=float(ATSC6v))
        AATS2s=st.number_input('AATS2s', value=float(AATS2s))
        S7=st.number_input('S7', value=float(S7))

    col1, col2, col3 = st.columns(3)
    with col1:
        mm = st.selectbox('Cultivation mode', ['pot', 'filed'])
        if mm == 'pot':
            mode = 0
        else:
            mode = 1
    with col2:
        OC = st.number_input(' "OC" value', min_value=0.01, max_value=5.85, value=1.6, step=0.1)
    with col3:
        pH = st.number_input(' "pH" value', min_value=2.6, max_value=11.7, value=7.29, step=0.1)

    col4, col5 = st.columns(2)
    with col4:
        PFASs = st.number_input(' "PFASs concentration" value', min_value=0.01, max_value=1000.0, value=33.3,
                                step=1.0)
    with col5:
        time = st.number_input(' "Exposure time" value', min_value=1.0, max_value=319.0, value=70.0, step=1.0)

    col6, col7 = st.columns(2)
    with col6:
        Rprotein = st.number_input(' "R-protein" value', min_value=0.0, max_value=9.68, value=4.0, step=0.1)
    with col7:
        Rlipid = st.number_input(' "R-lipid" value', min_value=0.17, max_value=5.0, value=3.23, step=0.1)

    features = [[TPSA, LogP, GATSp5, MOMI, Weta3, Weta1, QNss, EState_VSA8, AATS8i, FNSA, MATSv6, MATSe7, WPSA, ATSC5s,
                 AATSC5p, MATSv5, ATSC6v, AATS2s, S7, mode, OC, pH, PFASs, time, Rprotein, Rlipid]]

    logRCF = model2.predict(features)[0]
    RCF = 10 ** logRCF
    RCF = str(round(RCF, 2))

    st.markdown(
        f'<p style="font-size: 30px;text-align: center">Prediction RCF result</p>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<p style="text-align: center; font-size: 30px;">{RCF}</p>',
        unsafe_allow_html=True
    )
    RCF = float(RCF)
    if 0.015<=RCF<=42.32:
        st.markdown(
            f'<p style="font-size: 30px;text-align:center ">good</p>',
            unsafe_allow_html=True
        )

    elif 0.018<RCF<0.015 or 42.32<RCF<347.96:
        st.markdown(
            f'<p style="font-size: 30px;text-align: center">moderate</p>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<p style="font-size: 30px;text-align: center">bad</p>',
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()



