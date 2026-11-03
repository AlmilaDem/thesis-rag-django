# Appendix 6. Use of AI Tools

AI tools used in the thesis: **ChatGPT** (OpenAI, GPT-5.5 Thinking) and **Claude** (Anthropic, Claude Opus 5.5). All text and code suggested by the tools was reviewed, revised and approved by the author.

The prompts used to create the figures are given in [figure_prompts.md](figure_prompts.md).


---

## ChatGPT (OpenAI)

### Prompt 1

**Tool:** ChatGPT (OpenAI, GPT-5.5 Thinking)  
**Used for:** planning the report structure

> I'm writing my bachelor thesis at RTU about comparing answer formatting (no instruction / short paragraph / step-by-step) and source grounding (no instruction / inline citations / source-restricted answering) in a RAG system over the Django docs. this is my table of contents right now:
>
> - Introduction
> - 1\. Analytical Review: 1.1 Retrieval-Augmented Generation, 1.2 Domain-Specific Question Answering, 1.3 Software Documentation as a Knowledge Source, 1.4 Answer Formatting, 1.5 Source Grounding and Hallucination, 1.6 Evaluation of Answer Quality, 1.7 Question Types, 1.8 Research Gap
> - 2\. Research Methodology: 2.1 Research Design, 2.2 Experimental Variables, 2.3 Question Set Design, 2.4 Evaluation Criteria and Scoring, 2.5 Experimental Procedure
> - 3\. Experimental Setup: 3.1 Documentation Corpus, 3.2 Corpus Preparation, 3.3 Chunking Configuration, 3.4 Embedding and Retrieval Configuration, 3.5 LLM Configuration, 3.6 Formatting Strategies, 3.7 Grounding Strategies
> - 4\. RAG System Implementation: 4.1 System Architecture, 4.2 Document Processing and Indexing, 4.3 Retrieval Process, 4.4 Answer Generation, 4.5 Answer Evaluation
> - 5\. Experimental Results and Discussion: 5.1 Pilot Experiment, 5.2 Retrieval Verification, 5.3 Formatting Strategy Results, 5.4 Grounding Strategy Results, 5.5 Results by Question Type, 5.6 Discussion, 5.7 Demonstration of Recommendations, 5.8 Limitations
> - Results and Conclusions
>
> does this order make sense? is something missing or in the wrong chapter?

---

### Prompt 2

**Tool:** ChatGPT (OpenAI, GPT-5.5 Thinking)  
**Used for:** planning the report structure

> my chapter 3 (Experimental Setup) and chapter 4 (RAG System Implementation) feel like they repeat each other. ch3 has corpus, corpus preparation, chunking, embedding and retrieval, LLM configuration, formatting and grounding strategies. ch4 has architecture, document processing and indexing, retrieval, answer generation and evaluation. I write about chunking, retrieval and the LLM settings in both. what should go in ch3 and what in ch4 so I don't repeat things?

---

### Prompt 3

**Tool:** ChatGPT (OpenAI, GPT-5.5 Thinking)  
**Used for:** organising possible information sources

> can you help me group these sources by my chapter 1 sections (1.1 RAG, 1.2 domain-specific QA, 1.3 software documentation, 1.4 answer formatting, 1.5 grounding and hallucination, 1.6 evaluation, 1.7 question types)? one source can be in more than one section.
>
> - Lewis et al. (2020), Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks  
> - Yu et al. (2024), Evaluation of Retrieval-Augmented Generation: A Survey  
> - Es et al. (2024), RAGAS: Automated Evaluation of Retrieval Augmented Generation  
> - Sharma et al. (2024), Retrieval Augmented Generation for Domain-specific Question Answering  
> - Wang et al. (2024), Searching for Best Practices in Retrieval-Augmented Generation  
> - Stolfo (2024), Groundedness in Retrieval-augmented Long-form Generation: An Empirical Study  
> - Bohnet et al. (2023), Attributed Question Answering: Evaluation and Modeling for Attributed Large Language Models  
> - Wallat et al. (2025), Correctness is not Faithfulness in Retrieval Augmented Generation Attributions  
> - Perera and Nand (2016), Answer Presentation in Question Answering over Linked Data using Typed Dependency Subtree Patterns  
> - Lin et al. (2003), What Makes a Good Answer? The Role of Context in Question Answering  
> - Saad-Falcon et al. (2024), ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems

---

### Prompt 4

**Tool:** ChatGPT (OpenAI, GPT-5.5 Thinking)  
**Used for:** identifying possible information sources

> I use five question types in my thesis: definition, how-to, troubleshooting, configuration and API usage. I want to support these types with literature. which research areas look at what kind of questions developers ask (stack overflow studies, API documentation studies, question classification...)? and what keywords should I search? I'll read the papers myself.

---

### Prompt 5

**Tool:** ChatGPT (OpenAI, GPT-5.5 Thinking)  
**Used for:** grammar correction

> can you check the grammar in this paragraph? english is not my first language. only fix real mistakes, don't rewrite it in your style, and tell me what you changed.
>
> "The formatting strategies also clearly changed the length of the answers. F1 produced the shortest answers (on average 620 characters for ministral-3b-2512 and 745 for ministral-8b-2512), F0 longer answers (1,146 and 1,400 characters), and F2 the longest answers (1,620 and 1,778 characters). The F1 answers that did not follow the instruction had either six sentences or only one or two sentences; three of the short ones was refusals under G2."

---

### Prompt 6

**Tool:** ChatGPT (OpenAI, GPT-5.5 Thinking)  
**Used for:** minor language improvements

> is this paragraph formal enough for a thesis? which words are too informal? just point them out and suggest other words, don't rewrite the whole thing.
>
> "Interestingly, also for answerable questions, seven answers contain the sentence stating that the answer cannot be found in the documentation. In none of these cases, models actually refuse to answer: in two cases, models provide this sentence first and then go on to answer the question using their internalised knowledge. Note that we did not analyse whether these answers are correct."

---

### Prompt 7

**Tool:** ChatGPT (OpenAI, GPT-5.5 Thinking)  
**Used for:** grammar correction

> can you check grammar and punctuation in this paragraph from my abstract? only real mistakes please, keep my wording and list the changes.
>
> "The formatting strategies had only a small effect on the scores: short paragraph answers had the highest faithfulness, and step-by-step answers the lowest technical correctness and faithfulness. The grounding strategies did not significantly changed the scores of the answers to the answerable questions, but source-restricted answering clearly increased the number of correct refusals to the unanswerable questions (38 of 60 answers, compared with almost none without it). The best combination differed between the question types, but the differences was small."

---

## Claude (Anthropic)

### Prompt 8

**Tool:** Claude (Anthropic, Claude Opus 5.5)  
**Used for:** planning the structure and content of the chapters

> these are the goal and tasks of my thesis. can you check which chapter answers each task and if some task is not covered anywhere?
>
> Goal: to comparatively evaluate answer formatting and source grounding strategies in a RAG-based question answering system for software documentation, and to formulate recommendations regarding their use with different question types.
>
> Tasks:  
> 1. To review the literature on RAG-based question answering, software documentation, answer formatting, source grounding, answer quality and hallucination reduction.  
> 2. To identify and select answer formatting and source grounding strategies suitable for software documentation question answering.  
> 3. To prepare the evaluation setting, including the software documentation corpus, question set, reference RAG architecture and evaluation criteria.  
> 4. To apply the selected strategies in the RAG-based question answering setting and to conduct comparative experiments.  
> 5. To analyse the experimental results and, by formulating practically applicable recommendations, to demonstrate their use in selected question answering scenarios.
>
> my chapters: 1 Analytical Review, 2 Research Methodology, 3 Experimental Setup, 4 RAG System Implementation, 5 Experimental Results and Discussion (pilot, retrieval verification, formatting results, grounding results, results by question type, discussion, demonstration of recommendations, limitations).

---

### Prompt 9

**Tool:** Claude (Anthropic, Claude Opus 5.5)  
**Used for:** planning the content of a chapter

> I'm planning chapter 5. my RQs: RQ1 – how do the formatting strategies (F0, F1, F2) affect the quality of the answers? RQ2 – how do the grounding strategies (G0, G1, G2) affect the quality and what the LLMs do when the docs don't have the answer? I also compare the five question types descriptively for recommendations.
>
> what I have: mean scores + Friedman and Wilcoxon tests for 5 criteria and an overall score, rule-based checks if the instructions were followed, classification of the answers to the unanswerable questions (correct refusal / partial refusal / unsupported), mean overall score per combination and question type, a variability test, and a pilot that I used to choose k.
>
> in what order should I present these? what goes in the results sections and what in the discussion?

---

### Prompt 10

**Tool:** Claude (Anthropic, Claude Opus 5.5)  
**Used for:** planning the structure and content of the chapters

> I'm writing 1.8 Research Gap. it should sum up the review and lead to my RQs. these are my main points:
>
> 1. RAG adds information from external sources to the answers of an LLM, which is useful in domain-specific question answering, where the knowledge of the LLM may be incomplete or outdated (Lewis et al., 2020; Es et al., 2024; Sharma et al., 2024).  
> 2. Software documentation contains technical and frequently changing information, and code examples are the most helpful part of API documentation for LLMs (Wang et al., 2026; Watson et al., 2013; Chen et al., 2025).  
> 3. RAG systems can give answers that are not grounded in the retrieved texts, and citations do not necessarily show the sources that the model actually used (Elchafei et al., 2026; Stolfo, 2024; Wallat et al., 2025).  
> 4. The format of an answer matters for its usefulness (Perera and Nand, 2016; Lin et al., 2003), and users of a help system preferred answers with discrete steps (Sharma et al., 2024).  
> 5. Different question types may need different answers, but I did not find a study that compares formatting and grounding strategies for different types of software documentation questions.
>
> my RQs: RQ1 – how do the formatting strategies affect the quality of the answers? RQ2 – how do the grounding strategies affect the quality and the behaviour of the LLMs when the docs don't have the answer? I also want to give recommendations for the question types.
>
> in which order should I put these points so the gap and the RQs follow from them? is something missing?

---

### Prompt 11

**Tool:** Claude (Anthropic, Claude Opus 5.5)  
**Used for:** planning the structure and content of the chapters

> these are the limitations I want to write in 5.8. how can I group them so it's easy to read, and what should I say about what each one means for my results?
>
> - the corpus contained only five pages of the Django 5.2 documentation;  
> - the question set had only 25 answerable and 10 unanswerable questions (five and two per question type), so no statistical tests were possible for the question types;  
> - the questions and reference answers were written by me, and the technical correctness scores depend on how complete the reference answers are;  
> - only two formatting and two grounding strategies were tested, each with one fixed wording of the instruction;  
> - only two small LLMs of the same family (ministral-3b-2512 and ministral-8b-2512) were used;  
> - the answers were scored by an LLM (ministral-14b-2512) with RAGAS, and almost all answers received the highest clarity score (424 of 450);  
> - repeated answers to the same prompt were not identical even with a temperature of 0 and a fixed seed;  
> - I did not check whether the cited chunks actually support the claims of the G1 answers;  
> - the manual scoring by an external reviewer was not finished yet.

---

### Prompt 12

**Tool:** Claude (Anthropic, Claude Opus 5.5)  
**Used for:** language editing (shortening)

> this paragraph from 5.3 is too long, can you shorten it? don't change the meaning or any number, keep my sentences as much as you can and show me what you removed.
>
> "First, we checked whether LLMs actually followed the instructions regarding answer formatting. Answers generated with F1 followed the instruction in 98.1 % of the cases for ministral-3b-2512 and in 92.4 % of the cases for ministral-8b-2512, which means 103 and 97 of 105 answers. Answers generated with F2 followed the instruction in 90.5 % and 89.5 % of the cases, which means 95 and 94 of 105 answers. When F1 answers did not follow the instruction, they either consisted of six sentences or of only one or two sentences, and three of these short answers were refusals under G2. Of the 21 F2 answers that did not contain numbered steps, 19 were answers to unanswerable questions and 14 of them were refusals. Because a refusal is expected to consist of a single sentence, we do not consider this to be a problem."

---

### Prompt 13

**Tool:** Claude (Anthropic, Claude Opus 5.5)  
**Used for:** suggesting wording

> this sentence feels unclear to me, can you give me 2-3 clearer ways to say it without changing the meaning?
>
> "Hence, although F2 combined with G2 leads to the lowest overall scores and F0 combined with G2 to the highest ones, this does not provide evidence for an interaction between formatting and grounding strategies, as the corresponding test was not significant."

---

### Prompt 14

**Tool:** Claude (Anthropic, Claude Opus 5.5)  
**Used for:** language editing

> can you make the flow between the sentences in this paragraph better? keep my sentences and citations, don't add anything new, and show me what you changed.
>
> "The topicality of this bachelor thesis can be explained by the increasing use of Retrieval-Augmented Generation (RAG) systems (Yu, Gan et al., 2024), including technical and domain-specific question answering tasks (Sharma, Yoon et al., 2024). Large language models (LLMs) can generate fluent answers. However, their knowledge may be limited and difficult to update (Lewis, Perez et al., 2020), and they may not be able to answer questions about events that happened after their training (Es, James et al., 2024). In addition, they may generate unsupported information (hallucinations) during question answering (Es, James et al., 2024). On the other hand, RAG combines the LLM with information retrieved from external sources, allowing the system to use relevant sources during answer generation (Lewis, Perez et al., 2020; Es, James et al., 2024)."

---

### Prompt 15

**Tool:** Claude (Anthropic, Claude Opus 5.5)  
**Used for:** checking a citation against the original source

> in my thesis I wrote "Lewis et al. divided Wikipedia articles into passages of 100 words (Lewis, Perez et al., 2020)." is that really what the RAG paper (Lewis et al., NeurIPS 2020) says? which section is it in?

---

### Prompt 16

**Tool:** Claude (Anthropic, Claude Opus 5.5)  
**Used for:** checking the citations against the original sources

> are these two sentences correct according to the RAGAS paper (Es et al., EACL 2024) and the ARES paper (Saad-Falcon et al., NAACL 2024)? especially is "about 150 human-annotated examples" right for ARES, and are the three aspects named correctly?
>
> "Es et al. introduce RAGAS, a framework for evaluating RAG-based systems, which considers both the ability of the retrieval component to find relevant and focused context and the ability of the LLM to use this context faithfully (Es, James et al., 2024)."
>
> "Saad-Falcon et al. introduce ARES, which fine-tunes lightweight LLM judges with synthetic training data and a small set of about 150 human-annotated examples, and evaluates three aspects of RAG systems: context relevance, answer faithfulness and answer relevance (Saad-Falcon, Khattab et al., 2024)."

---

### Prompt 17

**Tool:** Claude (Anthropic, Claude Opus 5.5)  
**Used for:** checking the consistency between the text and the source code

> in table 3.6 I wrote these grounding instructions: G1 – "After each claim, add the number of the chunk that supports it in square brackets, for example [1]." and G2 – "Use only the information in the provided documentation. If the answer is not in the documentation, say: 'The answer cannot be found in the provided documentation.'" and in 4.5 I wrote that auto_checks.py looks for "cannot be found in the provided documentation". this is the code, is it exactly the same?
>
> ```

---

### Prompt 18

**Tool:** Claude (Anthropic, Claude Opus 5.5)  
**Used for:** checking the calculations based on the result files

> I classified the answers to the unanswerable questions into (a) correct refusal, (b) partial refusal, (c) unsupported answer, 30 per LLM for each grounding strategy. numbers (a, b, c): G0 3b: 0, 19, 11; G0 8b: 0, 16, 14; G1 3b: 2, 17, 11; G1 8b: 2, 15, 13; G2 3b: 17, 12, 1; G2 8b: 21, 9, 0.
>
> I wrote: "Under G0 and G1, almost no answer was a correct refusal (0 and 4 of 60 answers), and 25 and 24 of 60 answers were unsupported answers. Under G2, 38 of 60 answers were correct refusals, and only one answer did not state that the information is missing. Under G0 and G1, about 40 % of the answers were unsupported." are the totals and the percentage right?
