from langchain_community.llms import Ollama

input = input("Please type what you would like to ask me: ")
llm = Ollama(model="llama3")
res = llm.invoke(input)
print(res)