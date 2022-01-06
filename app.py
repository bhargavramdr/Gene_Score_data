from re import X
import streamlit as st
import pandas as pd
import numpy as npac
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
st.set_option('deprecation.showPyplotGlobalUse', False)


def main():
    st.set_option('deprecation.showPyplotGlobalUse', False)
    activities = ["Exploratory Data Analysis", "Individual data source Chats",
                  "Multiple data source Chats"]
    choice = st.sidebar.selectbox("Select Activities", activities)

    # Reading the data
    chronos_data = pd.read_csv('chronos.csv')
    # chronos_data.set_index(["Sample_ID"], inplace=True)

    expression_data = pd.read_csv('expression.csv')
    # expression_data.set_index(["Sample_ID"], inplace=True)

    metadata = pd.read_csv('metadata.csv')
    # metadata.set_index(["Sample_ID"], inplace=True)

    for i in metadata:
        if metadata[i].isnull().sum() < 30:
            metadata[i] = metadata[i].fillna(metadata[i].mode()[0])

    @st.cache
    def convert_df(df):
        return df.to_csv().encode('utf-8')

    if choice == "Exploratory Data Analysis":
        st.subheader("Exploratory Data Analysis")
        select_dataframe = st.selectbox("Select the Data",
                                        ['Chronos Gene', 'Gene Expression', 'Gene Info'])

        if select_dataframe == 'Chronos Gene':
            data = chronos_data
            csv1 = convert_df(chronos_data)
            st.download_button(
                label="Download Chronos data as CSV",
                data=csv1,
                file_name='chronos_data.csv',
                mime='text/csv')
        elif select_dataframe == 'Gene Expression':

            # Reading the data
            data = expression_data
            # Download file
            csv2 = convert_df(expression_data)
            st.download_button(
                label="Download Gene Expression data as CSV",
                data=csv2,
                file_name='expression.csv',
                mime='text/csv')
        elif select_dataframe == 'Gene Info':

            data = metadata
            # Download file
            csv3 = convert_df(metadata)
            st.download_button(
                label="Download Gene info data as CSV",
                data=csv3,
                file_name='metadata.csv',
                mime='text/csv')

        if data is not None:
            df = data
            st.dataframe(df.head())

            if st.checkbox("Show Shape"):
                st.write(df.shape)

            if st.checkbox("Show Columns"):
                all_columns = df.columns.to_list()
                st.write(all_columns)

            if st.checkbox("Summary"):
                st.write(df.describe())

            if st.checkbox("Show Selected Columns"):
                all_columns = df.columns.to_list()
                selected_columns = st.multiselect(
                    "Select Columns", all_columns)
                new_df = df[selected_columns]
                st.dataframe(new_df)

            if st.checkbox("Show Value Counts"):
                st.write(df.iloc[:, -1].value_counts())

            if st.checkbox("Correlation Plot(Seaborn)"):
                all_columns = df.columns.to_list()
                selected_columns = st.multiselect(
                    "Select Columns", all_columns, default=["LIN9", "TCF7"])
                new_df = df[selected_columns]
                st.write(sns.heatmap(new_df.corr(), annot=True))
                st.pyplot()

    # Data visualization for mulitple data------------------
    elif choice == "Multiple data source Chats":
        st.subheader("Multiple data source Data Visualization")
        data1 = pd.read_csv('chronos.csv')
        data1.set_index(["Sample_ID"], inplace=True)
        data2 = pd.read_csv('expression.csv')
        data2.set_index(["Sample_ID"], inplace=True)
        data3 = pd.read_csv('metadata.csv')
        data3.set_index(["Sample_ID"], inplace=True)

        for i in data3:
            if data3[i].isnull().sum() < 30:
                data3[i] = data3[i].fillna(data3[i].mode()[0])

        st.subheader("Gene chronos data")
        st.dataframe(data1.head())
        st.subheader("Gene Expression data")
        st.dataframe(data2.head())
        st.subheader("Gene info data")
        st.dataframe(data3.head())

        # Customizable Plot
        chart_select = st.sidebar.selectbox(
            label="select the chart",
            options=['Scatterplot', 'violin']
        )

        if chart_select == "Scatterplot":
            x_value = st.sidebar.selectbox(
                'Gene Score Data as x-axis', options=list(data1.columns))
            y_value = st.sidebar.selectbox(
                'Gene Expression Data y-axis', options=list(data2.columns))
            label = st.sidebar.selectbox(
                'lable of the points', options=[i for i in data3 if data3[i].isnull().sum() == 0])

            plot = px.scatter(x=data1[x_value],
                              y=data2[y_value], color=data3[label])

            st.plotly_chart(plot)

        elif chart_select == 'violin':
            sel_data = st.sidebar.selectbox(
                "select the data", ["Gene Score Data", "Gene Expression Data"])

            if sel_data == "Gene Score Data":
                value = st.sidebar.selectbox(
                    'chronos value', options=list(data1.columns))
                dar = data1[value]
            elif sel_data == "Gene Expression Data":
                value = st.sidebar.selectbox(
                    'Gene expression value ', options=list(data2.columns))
                dar = data2[value]

            label = st.sidebar.selectbox(
                'lable of the points', options=[i for i in data3 if data3[i].isnull().sum() == 0])

            plot = px.violin(x=dar, color=data3[label])

            st.plotly_chart(plot)

    # Data Visualization for single data-------------------------------------------
    elif choice == "Individual data source Chats":
        st.subheader("Data Visualization on single data")

        select_dataframe = st.selectbox("Select the Data",
                                        ['Chronos Gene', 'Gene Expression', 'Gene Info'])

        if select_dataframe == "Chronos Gene":
            df = chronos_data
        elif select_dataframe == "Gene Expression":
            df = expression_data
        elif select_dataframe == "Gene Info":
            df = metadata

        # Customizable Plot

        all_columns_names = df.columns.tolist()
        type_of_plot = st.selectbox("Select Type of Plot", [
                                    "area", "bar", "line", "hist", "box", "kde"])
        selected_columns_names = st.multiselect(
            "Select Columns To Plot", all_columns_names)

        if st.button("Generate Plot"):
            st.success("Generating Customizable Plot of {} for {}".format(
                type_of_plot, selected_columns_names))

            # Plot By Streamlit
            if type_of_plot == 'area':
                cust_data = df[selected_columns_names]
                st.area_chart(cust_data)

            elif type_of_plot == 'bar':
                cust_data = df[selected_columns_names]
                st.bar_chart(cust_data)

            elif type_of_plot == 'line':
                cust_data = df[selected_columns_names]
                st.line_chart(cust_data)

            # Custom Plot
            elif type_of_plot:
                cust_plot = df[selected_columns_names].plot(kind=type_of_plot)
                st.write(cust_plot)
                st.pyplot()


if __name__ == '__main__':
    main()
