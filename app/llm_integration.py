import re, os, dotenv
from langchain_huggingface import HuggingFaceEndpoint
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from app.db import MYSQL_DB, MYSQL_HOST, MYSQL_PASS, MYSQL_PORT, MYSQL_USER


dotenv.load_dotenv()


sec_key = os.environ.get('HUGGINGFACEHUB_API_KEY')
repo_id = "mistralai/Mistral-7B-Instruct-v0.3"
llm = HuggingFaceEndpoint(repo_id=repo_id, max_length=128, temperature=0.7, token=sec_key)


mysql_uri = f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
db = SQLDatabase.from_uri(mysql_uri)


query_template = """Based on the table schema below, write a SQL query that would answer the user's question:
{schema}

Question: {question}
SQL Query:
"""
query_prompt = ChatPromptTemplate.from_template(query_template)


summary_template = """Convert the SQL response to human readable summary not exceeding 2 lines. The user should not be aware of how it is computed.
Schema: {schema}
Question: {question}
SQL Query: {query}
SQL Response: {response}
Human-Readable Summary:
"""
summary_prompt = ChatPromptTemplate.from_template(summary_template)


def extract_sql_from_response(response):
    sql_code = re.search(r".*(SELECT.*;).*", response, re.DOTALL)
    if sql_code:
        return sql_code.group(1).strip()
    return response.strip()

extract_sql_runnable = RunnableLambda(extract_sql_from_response)

def get_schema(_):
    return "The products table has the following columns: id, which is an integer and the primary key, name, which is a string containing the name of the product, and price, which is a decimal representing the price of the product. The customers table has the following columns: id, which is an integer and the primary key, name, which is a string containing the name of the customer, and email, which is a string containing the email address of the customer. The sales table has the following columns: id, which is an integer and the primary key, product_id, which is a foreign key referring to the id of the product from the products table, customer_id, which is a foreign key referring to the id of the customer from the customers table, quantity, which is an integer representing the number of items sold, and sale_date, which is a date representing when the sale took place. The sales table establishes relationships between the products and customers tables using the product_id and customer_id foreign keys."

def run_query(query):
    return db.run(query)

def get_human_readable_summary(question):
    sql_chain = (
        RunnablePassthrough.assign(schema=get_schema)
        | query_prompt
        | llm.bind(stop=["\nSQLResult:"])
        | StrOutputParser()
        | extract_sql_runnable
    )

    full_chain = (
        RunnablePassthrough.assign(query=sql_chain).assign(
            schema=get_schema,
            response=lambda variables: run_query(variables['query'])
        )
        | summary_prompt
        | llm
    )

    result = full_chain.invoke({"question": question})
    return result
