# Instructor Guide

Instructor materials and preparation scripts live in this folder. The student notebook is a read-only workshop: learners build agents against existing source tables and the ready document-search service. Only instructors use `instructor.scripts.northstar_data`; imports do not create clients or write data. Complete data creation and index synchronization before the session. The student notebook must not contain generator imports, table-write controls or preparation tasks.

## Environment Certification

Candidate baseline: Databricks Runtime 16.4 LTS ML, Python 3.12, with the exact root requirements pins. This has **not** been executed in a Databricks workspace during authoring. Complete and record these checks before teaching; do not describe the pins as tested until then.

Runtime: ___; access mode: ___; cloud/workspace configuration: ___; date: ___; package changes: ___; model endpoint: ___; managed MCP route/schema: ___; tracing: ___. Keep real credentials out of the repository.

- [ ] Import the repository into a Databricks Git folder with the `instructor`, `student` and requirements files together.
- [ ] Verify the repository-root requirements install and a separate Python restart from the nested notebook folders. Reinstall notebook-scoped libraries in new sessions. If needed, supply an absolute `/Workspace/.../<repository>` path, not a Windows path.
- [ ] Test a configured model endpoint, permissions, model connectivity and tool-call round trip.
- [ ] Select an existing catalog and dedicated instructor-owned workshop schema. The instructor identity needs USE CATALOG/SCHEMA, schema/table creation, SELECT and write permissions. Learners need USE CATALOG/SCHEMA and SELECT on the source tables, not creation or modification privileges. Verify permissions using a learner identity; omit write grants and account for inherited grants.
- [ ] Before the session, run [the data-population notebook](populate_data_sources.ipynb), inspect all eight tables and synchronize the search index. Its write step overwrites workshop tables. Do not rerun it while students are querying the shared data.

- [ ] In the AI Search/Vector Search UI, create a Delta Sync index on `document_chunks`, primary key `chunk_id`, embedding source `chunk_text`, **Databricks-managed embeddings**. Choose approved search/embedding endpoints and synchronize `title`, `document_id`, `chunk_index`, `product_id`, `region`, `retailer` and `chunk_text` as retrieval metadata.
- [ ] Complete initial synchronization before class and grant index query access. No notebook cell recreates an index. After any source overwrite, trigger synchronization or wait for continuous synchronization and recheck retrieval before class. New chunk IDs replace the former short-document IDs, so ensure stale chunks have disappeared.
- [ ] Supply the managed AI Search MCP URL supported by the workspace, and test discovery and `call_tool` under learner identity. Never guess a tool name or arguments. Verify title, ID and text are returned, not just scores.
- [ ] Supply catalog, schema, model endpoint, MCP URL and MLflow experiment path for the learner configuration widgets. Test `spark.table(...)` reads on every required table; no learner step should import instructor helpers or initialize source data. Checkpoint/trace storage is separate from source data; allow the necessary experiment permissions.
- [ ] Confirm experiment creation/access, LangChain autolog tracing, writer/tool/MCP spans and checkpoint thread separation.
- [ ] Run all six questions, including the deliberately flawed tool's 800-unit result and the fixed 360-unit result.

References: [notebook libraries](https://docs.databricks.com/aws/en/libraries/notebooks-python-libraries), [working directories](https://docs.databricks.com/aws/en/files/cwd-dbr-14), [managed MCP](https://docs.databricks.com/aws/en/generative-ai/mcp/managed-mcp), [AI Search MCP](https://docs.databricks.com/aws/en/agents/mcp-tools/ai-search), [LangGraph tracing](https://docs.databricks.com/aws/en/mlflow3/genai/tracing/integrations/langgraph).

## Dataset

Deterministic 2025 Sunday-labelled weeks; 24 products across six categories, five regions and four retailers. Eight Delta tables:

| Table | Rows | Purpose |
|---|---:|---|
| products | 24 | Category, variant, pack, price, storage, shelf life |
| retailers | 4 | Account/channel master |
| sales_weekly | 24,648 | Units, price and synthetic sales value |
| availability_weekly | 24,648 | Weekly in-stock proportions |
| shipments_weekly | 24,648 | Ordered/shipped units and fill rate |
| promotions | 1,418 | Recorded planned offers with overlap dates |
| documents | 49 | Full company, account and product documents |
| document_chunks | 294 | Six paragraph chunks per document, with metadata |

The documents are 462-511 words each. Each paragraph is an independent retrieval unit. Product playbooks, regional account plans, a metrics handbook, evidence policy, the original account plan, promotion brief and replenishment note provide varied context. Some plans are deliberately irrelevant to a particular query, providing retrieval/evidence-selection practice. All data is fictional; prices, shipments and wider sales are synthetic, not independently observed evidence validating a narrative.

The controlled OAT-1 Midwest case covers only NorthMart/FreshCo. April totals: 1,000; May: 800. NorthMart: 600 -> 360 (-240, -40%); FreshCo: 400 -> 440 (+40, +10%); overall: -200 (-20%). In-stock averages: 97.75% -> 78% and 97.5% -> 98.25%. The two April promotion records are preserved, with no matching May records. OAT-1 Northeast is intentionally absent so the no-data question remains meaningful. Other products do have Northeast data. Do not validate the expanded dataset using the old global 16/16/2/3 counts: those apply only to the old fixture or the scoped case (chunks are now longer-document paragraph chunks).

## Facilitation

1. Graph/state: ask learners to identify state, node updates, reducer and edges. No tools yet.
2. UC/tools: learners use the supplied query and connect the sales tool to it; the other tools are supplied. They do not write Spark filters from scratch or implement four near-identical tools. Inspect the model's requested arguments before executing them. All source tables are already available and read-only.
3. MCP/writer: show discovery; select a tool by its displayed schema. Review each document citation against the actual chunk. The expanded corpus includes distractors, so keyword matches alone are insufficient. Pre-sync the index.
4. Checkpointing: same-thread follow-up, state/history and new thread. InMemorySaver survives calls, not kernel restarts; it is not long-term memory across threads.
5. Tracing: enable `mlflow.langchain.autolog()` before invocation. Inspect model, local tools, MCP wrapper and writer. Trace only synthetic prompts/data; do not log credentials.
6. Debugging: first prove the direct retailer-filter defect, then fix it. Optional fixes are clarification and causal language. Deterministic defective code keeps the learner exercise independent of model behavior.

Use `scripts/agent_reference.py` as the clean recovery copy; do not import it in learner TODO cells. Show one narrow solution only when necessary rather than replacing the entire learner implementation. Tool and graph behavior needs real Databricks execution.

## Beginner Delivery

Use the notebook's run-unchanged / TODO / checkpoint labels. Learners should run one cell at a time, not Run All: incomplete TODOs and pre-fix assertions intentionally stop execution. After editing a function, rerun its definition; after editing a graph node or tool, rebuild the graph. Introduce the tool description, named inputs, model request, ToolMessage result and graph edge as separate concepts. Keep Spark implementation details as supplied code or optional extensions.

For the sales-wrapper recovery, the learner keeps the `@tool` signature and writes a useful docstring, then returns `query_sales_summary(product_id=product_id, region=region, start_date=start_date, end_date=end_date, retailer=retailer)`. This is the bridge from a query to an agent capability, not another filtering exercise. The reference module remains a clean end-to-end recovery implementation; its internal structure need not mirror the learner's smaller cells.