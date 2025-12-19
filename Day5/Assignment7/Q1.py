#Create a Streamlit application that allows users to 
#upload a CSV file and view its schema.Use an LLM to 
#convert user questions into SQL queries, execute them 
# on the CSV data using pandasql, and explain the results 
# in simple English

import streamlit as st
import os
import pandas as pd
import pandasql as ps
import openai 
from langchain.chat_models import init_chat_model

openai.api_key = os.getenv("OPENAI_API_KEY")
st.title("CSV uploader")

#upload csv
uploaded_file = st.file_uploader("Upload a CSV file",type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    st.success("CSV uploaded usccessfully")
    
    #show schema
    st.subheader("Dataset Schema")
    schema_df = pd.DataFrame({
        "Column Name": df.columns,
        "Data Type": df.dtypes.astype(str)
    })
    st.table(schema_df)
    
    st.subheader("Ask a question about the data")
    user_question = st.text_input("Example: What is the average salary of employees")
    if st.button("Generate Answer") and user_question:
        with st.spinner("Thinking"):

            # Convert Question → SQL
            
            prompt = f"""
            You are an expert data analyst.
            Convert the following question into an SQL query.
            The table name is df.

            Schema:
            {schema_df.to_string(index=False)}

            Question:
            {user_question}

            Only return the SQL query. No explanation.
            """

            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )

            sql_query = response.choices[0].message.content.strip()

            st.subheader("Generated SQL Query")
            st.code(sql_query, language="sql")

            # STEP 5: Execute SQL on CSV
            
            try:
                result = ps.sqldf(sql_query, {"df": df})

                st.subheader("Query Result")
                st.dataframe(result)

                
                # STEP 6: Explain Result in English
                
                explanation_prompt = f"""
                Explain the following result in simple English.

                Question:
                {user_question}

                SQL Query:
                {sql_query}

                Result:
                {result.to_string(index=False)}
                """

                llm = init_chat_model(
                 model="gpt-3.5-turbo",
                model_provider="openai",
                api_key=os.getenv("OPENAI_API_KEY"))

                sql_query = llm.invoke(prompt).content

                st.subheader("Explanation")
                

            except Exception as e:
                st.error(f"Error executing SQL: {e}")