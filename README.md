Agentic AI System for Multi-Step Tasks
======================================

Overview
--------

This project implements an **Agentic AI System** capable of handling complex, multi-step user tasks by decomposing them into smaller execution steps and coordinating multiple specialized agents asynchronously. The system is designed to demonstrate strong system design principles such as clear agent boundaries, asynchronous orchestration, fault isolation, and real-time observability.

The project intentionally avoids black-box agent frameworks and instead implements explicit orchestration logic using Redis Streams and independent worker processes. The result is a system that is explainable, debuggable, and suitable for both human evaluation and automated assessment.

Problem Statement
-----------------

Given a high-level user task, the system must:

*   Accept a complex task from the user
    
*   Break the task into multiple execution steps
    
*   Assign each step to a specialized agent
    
*   Execute steps asynchronously
    
*   Stream intermediate execution progress to the user
    
*   Handle failures and retries safely
    

Key Capabilities
----------------

*   Agent-based architecture with single-responsibility agents
    
*   Explicit task planning via a Planner Agent
    
*   Asynchronous execution using Redis Streams
    
*   Manual batching of execution steps
    
*   Real-time progress streaming using Server-Sent Events (SSE)
    
*   Distributed metrics collection (latency and cost)
    
*   Step-level retry and failure handling
    
*   Structured logging for observability
    

High-Level Architecture
-----------------------

The system consists of the following components:

*   Client (Postman or Browser)
    
*   FastAPI API Server
    
*   Planner Agent
    
*   Redis (Streams + Key-Value Store)
    
*   Worker Process hosting specialized agents
    
*   Streaming Layer (Server-Sent Events)
    

The API server handles orchestration and streaming only. All execution logic runs asynchronously inside worker processes, fully decoupled from the API lifecycle.

Architecture Diagram
--------------------

The system architecture diagram is available in the docs/architecture.png file.

The diagram illustrates how user requests flow from the client through the API server, are decomposed by the Planner Agent, queued in Redis Streams, executed asynchronously by worker agents, and streamed back to the client in real time.

Execution Flow
--------------

1.  The client submits a task via the API.
    
2.  The Planner Agent synchronously generates an ordered execution plan.
    
3.  Steps targeting the same agent are manually batched.
    
4.  Batched steps are enqueued into Redis Streams.
    
5.  Worker processes consume steps asynchronously using consumer groups.
    
6.  Each agent executes its assigned step independently.
    
7.  Structured execution events are emitted to Redis.
    
8.  Events are streamed to the client via SSE.
    
9.  Execution metrics are computed and persisted.
    

Agent Roles
-----------

### Planner Agent

*   Interprets user intent
    
*   Generates a structured execution plan
    
*   Assigns steps to specialized agents
    

### Retriever Agent

*   Performs research and data collection tasks
    

### Analyzer Agent

*   Processes raw data and extracts insights
    

### Writer Agent

*   Produces the final human-readable output
    

API Endpoints
-------------

### POST /run-task

Starts a new task execution.

Request body:

*   user\_input (string): High-level task description
    

Response:

*   task\_id (string)
    
*   steps\_created (integer)
    

### GET /stream/{task\_id}

Streams real-time execution events for a specific task using Server-Sent Events.

### GET /metrics/{task\_id}

Returns execution metrics for a completed task, including latency and cost.

Streaming Model
---------------

The system uses **structured event streaming**, not raw text streaming. Each execution update is emitted as a JSON event describing what happened.

Examples include:

*   step\_started
    
*   step\_completed
    
*   task\_completed
    

Server-Sent Events (SSE) were chosen because they are simple, lightweight, natively supported by browsers, and well-suited for one-way progress updates.

Async Execution Model
---------------------

*   The API server never blocks on execution
    
*   Worker processes run independently
    
*   Redis Streams decouple producers and consumers
    
*   At-least-once delivery semantics are enforced
    

This design enables horizontal scaling of workers without changes to the API layer.

Manual Batching Strategy
------------------------

Execution steps targeting the same agent are grouped into batches before being enqueued. This reduces Redis overhead, improves throughput, and demonstrates explicit control over execution behavior.

Failure Handling and Retries
----------------------------

*   Failures are handled at the step level
    
*   Each step has a retry limit
    
*   Retries use exponential backoff
    
*   Agents are designed to be idempotent
    

This approach prevents partial task corruption and allows safe reprocessing.

Metrics and Observability
-------------------------

The system tracks:

*   End-to-end latency per task
    
*   Cost units per step and per task
    

Metrics are computed by worker processes and persisted in Redis, making them accessible across processes.

Structured logs include task ID, agent name, step ID, and execution status.

Tech Stack
----------

*   Python 3.11+
    
*   FastAPI
    
*   Redis (Streams + Key-Value Store)
    
*   Server-Sent Events (SSE)
    
*   Docker (for Redis)
    

Installation and Local Setup
----------------------------

### Prerequisites

*   Python 3.11 or higher
    
*   Docker and Docker Compose
    
*   Git
    

### Step 1: Clone the Repository

Clone the repository and navigate into the project directory.

### Step 2: Start Redis

Start Redis using Docker:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   docker run -d --name redis-agentic -p 6379:6379 redis:7   `

Verify Redis is running:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   docker exec -it redis-agentic redis-cli ping   `

### Step 3: Set Up Python Environment

Create and activate a virtual environment:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python -m venv venv   `

On Windows:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   venv\\Scripts\\activate   `

On macOS/Linux:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   source venv/bin/activate   `

### Step 4: Install Dependencies

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pip install -r requirements.txt   `

### Step 5: Start the API Server

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   uvicorn app.main:app --reload   `

The API will be available at:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   http://127.0.0.1:8000   `

### Step 6: Start the Worker Process

In a separate terminal (with the virtual environment activated):

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python -m worker.agent_worker   `

The worker terminal will display logs for all agents in execution order.

Testing the System
------------------

The system can be tested using Postman or curl.

1.  Submit a task using POST /run-task
    
2.  Stream execution progress using GET /stream/{task\_id}
    
3.  Fetch metrics using GET /metrics/{task\_id}
    

Worker logs and streaming responses together demonstrate end-to-end asynchronous execution.

Project Structure
-----------------

*   app/ : API layer, orchestration, agents, and streaming
    
*   worker/ : Asynchronous worker execution
    
*   docs/ : Architecture diagram, system design, post-mortem
    
*   utils/ : Logging, metrics, retry utilities
    

Trade-offs and Design Decisions
-------------------------------

Key trade-offs include:

*   Redis Streams instead of Kafka
    
*   Server-Sent Events instead of WebSockets
    
*   Manual orchestration instead of agent frameworks
    
*   In-memory state vs persistent state
    

These decisions prioritize simplicity, explainability, and control.

Documentation
-------------

*   System Design Document: docs/system\_design.md
    
*   Post-Mortem Report: docs/post\_mortem.md
    

Conclusion
----------

This project demonstrates a robust agentic architecture with clear agent boundaries, asynchronous execution, real-time streaming, and strong system design principles. The system is designed to be explainable, extensible, and suitable for both technical interviews and automated evaluation.