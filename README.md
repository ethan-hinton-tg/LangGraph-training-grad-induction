# LangGraph-training-grad-induction
Databricks hands-on workshop for graduate induction: six guided exercises.

- [Student exercise notebook](student/langgraph_agent_training.ipynb): read-only table queries, agent-building examples, TODOs, checks and debugging exercises. No source-data preparation steps.
- [Instructor solution notebook](instructor/langgraph_agent_training_solution.ipynb): completed exercise solutions.
- [Instructor data-population notebook](instructor/populate_data_sources.ipynb): previews and writes the workshop source tables.
- [Requirements](requirements.txt): exact candidate package pins, requiring Databricks certification before teaching.
- [Instructor guide](instructor/README.md): pre-work, index setup, facilitation and dataset specification.
- [Data generator](instructor/scripts/northstar_data.py): eight deterministic Spark/Delta tables; no import-time writes.

The fictional Northstar Foods dataset includes 24 products, five regions, four retailers, 24,648 weekly sales rows and 49 long documents split into 294 chunks. The controlled Midwest oat-drink case remains 1,000 April units versus 800 May units. Broader records and retrieval distractors support additional questions without changing the benchmark.

The instructor creates the source tables and synchronizes the AI Search index before the session. Learners receive read-only source-table access and configured model/search services; they do not run the generator. Use a Databricks Git folder and Databricks-managed embeddings. No credentials or real workspace names are stored here. Runtime 16.4 LTS ML is a **candidate**, not locally Databricks-certified. Follow the instructor guide before running the learner notebook.
