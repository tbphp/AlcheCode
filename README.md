# AlcheCode

```mermaid
graph TD
    A((__start__)) --> B[initial]
    B --> C[load_rules]
    C --> D[analyze_node]
    D -- tool avail --> F[execute_tools]
    D -- no tool --> G[format_output]
    F --> G
    G --> H((__end__))
```

## License

This project is built upon [LangChain](https://github.com/langchain-ai/langchain)  
which is licensed under the [MIT License](https://github.com/langchain-ai/langchain/blob/master/LICENSE).
