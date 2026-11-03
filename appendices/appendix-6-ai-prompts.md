# Appendix 6. Use of AI Tools

AI tools used in the thesis: ChatGPT (OpenAI, GPT-5.5 Thinking) and Claude (Anthropic, Claude Opus 5.5). All text and code suggested by the tools was reviewed, revised and approved by the author.

The prompts used to create the figures are given in [figure_prompts.md](figure_prompts.md).

---

ChatGPT (OpenAI)
Prompt 1

Tool: ChatGPT (OpenAI, GPT-5.5 Thinking)
Used for: planning the report structure

I am writing a bachelor thesis at Riga Technical University. The topic is the comparison of answer formatting strategies (no instruction, short paragraph, step-by-step) and source grounding strategies (no instruction, inline citations, source-restricted answering) in a RAG-based question answering system over the Django documentation. The thesis must contain an introduction, an analytical review, a research methodology, an experimental part, results and conclusions, a list of references and appendixes.

This is my planned table of contents:

Introduction

Analytical Review: 1.1 Retrieval-Augmented Generation, 1.2 Domain-Specific Question Answering, 1.3 Software Documentation as a Knowledge Source, 1.4 Answer Formatting, 1.5 Source Grounding and Hallucination, 1.6 Evaluation of Answer Quality, 1.7 Question Types, 1.8 Research Gap
Research Methodology: 2.1 Research Design, 2.2 Experimental Variables, 2.3 Question Set Design, 2.4 Evaluation Criteria and Scoring, 2.5 Experimental Procedure
Experimental Setup: 3.1 Documentation Corpus, 3.2 Corpus Preparation, 3.3 Chunking Configuration, 3.4 Embedding and Retrieval Configuration, 3.5 LLM Configuration, 3.6 Formatting Strategies, 3.7 Grounding Strategies
RAG System Implementation: 4.1 System Architecture, 4.2 Document Processing and Indexing, 4.3 Retrieval Process, 4.4 Answer Generation, 4.5 Answer Evaluation
Experimental Results and Discussion: 5.1 Pilot Experiment, 5.2 Retrieval Verification, 5.3 Formatting Strategy Results, 5.4 Grounding Strategy Results, 5.5 Results by Question Type, 5.6 Discussion, 5.7 Demonstration of Recommendations, 5.8 Limitations Results and Conclusions

Is the order of the chapters and sections logical? Is there a section that is missing, or a section that is in the wrong chapter?

Prompt 2

Tool: ChatGPT (OpenAI, GPT-5.5 Thinking)
Used for: planning the report structure

In my bachelor thesis, Chapter 3 is called "Experimental Setup" and has the sections Documentation Corpus, Corpus Preparation, Chunking Configuration, Embedding and Retrieval Configuration, LLM Configuration, Formatting Strategies and Grounding Strategies. Chapter 4 is called "RAG System Implementation" and has the sections System Architecture, Document Processing and Indexing, Retrieval Process, Answer Generation and Answer Evaluation. I notice that I write about chunking, retrieval and the LLM settings in both chapters. How should I divide the content between the two chapters so that I do not repeat the same information? What should Chapter 3 explain, and what should Chapter 4 explain?

Prompt 3

Tool: ChatGPT (OpenAI, GPT-5.5 Thinking)
Used for: identifying possible information sources

For the analytical review of my bachelor thesis I need academic sources about the following topics: retrieval-augmented generation (RAG) and its components, RAG for domain-specific question answering, software documentation as a knowledge source, how the format of an answer affects its usefulness, hallucinations and source grounding with citations in LLM answers, and how the quality of RAG answers can be evaluated (for example with RAGAS). Which kinds of sources should I look for (survey papers, conference papers, benchmarks, documentation), which keywords should I use in Google Scholar and arXiv, and which well-known papers should I start with for each topic? I will check every source myself.

Prompt 4

Tool: ChatGPT (OpenAI, GPT-5.5 Thinking)
Used for: organising possible information sources

I found the following sources for the analytical review of my thesis. Can you help me group them by the sections of my Chapter 1: 1.1 Retrieval-Augmented Generation, 1.2 Domain-Specific Question Answering, 1.3 Software Documentation as a Knowledge Source, 1.4 Answer Formatting, 1.5 Source Grounding and Hallucination, 1.6 Evaluation of Answer Quality, 1.7 Question Types? A source can belong to more than one section.

Lewis et al. (2020), Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks
Yu et al. (2024), Evaluation of Retrieval-Augmented Generation: A Survey
Es et al. (2024), RAGAS: Automated Evaluation of Retrieval Augmented Generation
Sharma et al. (2024), Retrieval Augmented Generation for Domain-specific Question Answering
Wang et al. (2024), Searching for Best Practices in Retrieval-Augmented Generation
Stolfo (2024), Groundedness in Retrieval-augmented Long-form Generation: An Empirical Study
Bohnet et al. (2023), Attributed Question Answering: Evaluation and Modeling for Attributed Large Language Models
Wallat et al. (2025), Correctness is not Faithfulness in Retrieval Augmented Generation Attributions
Perera and Nand (2016), Answer Presentation in Question Answering over Linked Data using Typed Dependency Subtree Patterns
Lin et al. (2003), What Makes a Good Answer? The Role of Context in Question Answering
Saad-Falcon et al. (2024), ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems
Prompt 5

Tool: ChatGPT (OpenAI, GPT-5.5 Thinking)
Used for: grammar correction

English is not my first language. Can you check the grammar and spelling of this paragraph from my bachelor thesis? Please correct only real mistakes and do not rewrite the sentences in your own style. Show me what you changed.

"The formatting strategies also clearly changed the length of the answers. F1 produced the shortest answers (on average 620 characters for ministral-3b-2512 and 745 for ministral-8b-2512), F0 longer answers (1,146 and 1,400 characters), and F2 the longest answers (1,620 and 1,778 characters). The F1 answers that did not follow the instruction had either six sentences or only one or two sentences; three of the short ones was refusals under G2."

Prompt 6

Tool: ChatGPT (OpenAI, GPT-5.5 Thinking)
Used for: minor language improvements

Is the following paragraph from my bachelor thesis written in a formal academic style? Please point out the words or phrases that are too informal and suggest a more formal alternative for each. Do not rewrite the whole paragraph.

"Interestingly, also for answerable questions, seven answers contain the sentence stating that the answer cannot be found in the documentation. In none of these cases, models actually refuse to answer: in two cases, models provide this sentence first and then go on to answer the question using their internalised knowledge. Note that we did not analyse whether these answers are correct."

Claude (Anthropic)
Prompt 7

Tool: Claude (Anthropic, Claude Opus 5.5)
Used for: planning the structure and content of the chapters

These are the goal and the tasks of my bachelor thesis:

Goal: to comparatively evaluate answer formatting and source grounding strategies in a RAG-based question answering system for software documentation, and to formulate recommendations regarding their use with different question types.

Tasks:

To review the literature on RAG-based question answering, software documentation, answer formatting, source grounding, answer quality and hallucination reduction.
To identify and select answer formatting and source grounding strategies suitable for software documentation question answering.
To prepare the evaluation setting, including the software documentation corpus, question set, reference RAG architecture and evaluation criteria.
To apply the selected strategies in the RAG-based question answering setting and to conduct comparative experiments.
To analyse the experimental results and, by formulating practically applicable recommendations, to demonstrate their use in selected question answering scenarios.

My chapters are: 1. Analytical Review, 2. Research Methodology, 3. Experimental Setup, 4. RAG System Implementation, 5. Experimental Results and Discussion (with the sections Pilot Experiment, Retrieval Verification, Formatting Strategy Results, Grounding Strategy Results, Results by Question Type, Discussion, Demonstration of Recommendations and Limitations).

Which chapter or section answers each task? Is there a task that is not clearly answered by any chapter?

Prompt 8

Tool: Claude (Anthropic, Claude Opus 5.5)
Used for: planning the content of a chapter

I am planning Chapter 5 of my bachelor thesis. My research questions are: RQ1 – How do the formatting strategies (F0 no instruction, F1 short paragraph, F2 step-by-step) affect the quality of the answers? RQ2 – How do the grounding strategies (G0 no instruction, G1 inline citations, G2 source-restricted answering) affect the quality of the answers and the behaviour of the LLMs on questions that cannot be answered from the documentation? RQ3 – Which combination of strategies works best for each question type (definition, how-to, troubleshooting, configuration, API usage)?

My results are: mean scores and Friedman and Wilcoxon tests for five criteria (technical correctness, clarity, faithfulness, hallucination control, answer relevance) and an overall score; rule-based checks of whether the instructions were followed; a classification of the answers to the unanswerable questions into correct refusals, partial refusals and unsupported answers; the mean overall score of each strategy combination per question type; and a variability test in which some answers were generated five times. I also have a pilot experiment that I used to choose k and to test the prompts.

In which order should I present these results? Which results should go into the result sections and what should go into the discussion?

Prompt 9

Tool: Claude (Anthropic, Claude Opus 5.5)
Used for: language editing (shortening)

This paragraph from Section 5.3 of my thesis is too long. Please shorten it without changing the meaning or any number. Keep my own sentences as much as possible and change only what is necessary. Show me which parts you removed.

"First, we checked whether LLMs actually followed the instructions regarding answer formatting. Answers generated with F1 followed the instruction in 98.1 % of the cases for ministral-3b-2512 and in 92.4 % of the cases for ministral-8b-2512, which means 103 and 97 of 105 answers. Answers generated with F2 followed the instruction in 90.5 % and 89.5 % of the cases, which means 95 and 94 of 105 answers. When F1 answers did not follow the instruction, they either consisted of six sentences or of only one or two sentences, and three of these short answers were refusals under G2. Of the 21 F2 answers that did not contain numbered steps, 19 were answers to unanswerable questions and 14 of them were refusals. Because a refusal is expected to consist of a single sentence, we do not consider this to be a problem."

Prompt 10

Tool: Claude (Anthropic, Claude Opus 5.5)
Used for: suggesting wording

The following sentence from my thesis feels unclear to me. Can you suggest two or three clearer ways to say it, without changing what it means?

"Hence, although F2 combined with G2 leads to the lowest overall scores and F0 combined with G2 to the highest ones, this does not provide evidence for an interaction between formatting and grounding strategies, as the corresponding test was not significant."

Prompt 11

Tool: Claude (Anthropic, Claude Opus 5.5)
Used for: checking a citation against the original source

In my thesis I wrote the following sentence: "Lewis et al. divided Wikipedia articles into passages of 100 words (Lewis, Perez et al., 2020)." The source is: Lewis, P., Perez, E., Piktus, A. et al. Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. Advances in Neural Information Processing Systems 33, 2020. Does the paper really say that the Wikipedia articles were divided into passages of 100 words? In which section of the paper is this described?

Prompt 12

Tool: Claude (Anthropic, Claude Opus 5.5)
Used for: checking a reference entry

Can you check whether this reference from my list of references is correct (authors, title, year and link)? I am not sure whether the author list is complete and in the right order.

"Sharma, S., Yoon, D. S., Dernoncourt, F., Sultania, D., Bagga, K., Zhang, M., Bui, T., and Kotte, V. Retrieval Augmented Generation for Domain-specific Question Answering [online]. arXiv, 2024 [viewed 12 June 2026]. Available from: https://arxiv.org/abs/2404.14760."

Prompt 13

Tool: Claude (Anthropic, Claude Opus 5.5)
Used for: consistency between the text and the source code

In Chapter 3 of my thesis I wrote: "a maximum chunk size of 700 characters was used, and the text was divided at sentence boundaries", "the five most similar chunks are retrieved (k = 5)", "the embedding model all-MiniLM-L6-v2 was used", and "the answers were generated with a temperature of 0, a maximum answer length of 1,200 tokens and a seed of 42". These are the settings in my config.py:

CHUNK_MAX_CHARS = 700 CHUNK_OVERLAP_SENTENCES = 1 EMBEDDING_MODEL = "all-MiniLM-L6-v2" TOP_K = 5 TEMPERATURE = 0 MAX_TOKENS = 1200 SEED = 42

Is the text the same as the code? Is there a setting in the code that I did not mention in the text but should mention?

Prompt 14

Tool: Claude (Anthropic, Claude Opus 5.5)
Used for: checking the calculations based on the result files

This is a result table of my experiment (mean and standard deviation of each criterion for the three formatting strategies, both LLMs together):

formatting, technical_correctness, clarity, faithfulness, hallucination_control, answer_relevance, overall F0, 0.69 (0.21), 4.93 (0.25), 0.87 (0.13), 4.44 (0.94), 0.87 (0.09), 0.86 (0.08) F1, 0.70 (0.20), 4.93 (0.25), 0.91 (0.12), 4.25 (0.91), 0.84 (0.11), 0.85 (0.08) F2, 0.64 (0.21), 4.95 (0.28), 0.85 (0.14), 4.36 (1.03), 0.84 (0.15), 0.83 (0.09)

And this is what I wrote about it: "F1 had the highest faithfulness (0.91) and F2 the lowest (0.85). F2 also had the lowest technical correctness (0.64 compared with 0.69 for F0 and 0.70 for F1) and the lowest overall score (0.83). The clarity scores were almost the same for all strategies."

Are all numbers in my text the same as in the table? Is every statement correct according to the table?

Prompt 15

Tool: Claude (Anthropic, Claude Opus 5.5)
Used for: checking the calculations (counts and percentages)

In my thesis I classified the 60 answers of each grounding strategy to the unanswerable questions (30 per LLM) into correct refusals (a), partial refusals (b) and unsupported answers (c). The numbers (a, b, c) are: G0 3b: 0, 19, 11; G0 8b: 0, 16, 14; G1 3b: 2, 17, 11; G1 8b: 2, 15, 13; G2 3b: 17, 12, 1; G2 8b: 21, 9, 0.

I wrote: "Under G0 and G1, almost no answer was a correct refusal (0 and 4 of 60 answers), and 25 and 24 of 60 answers were unsupported answers. Under G2, 38 of 60 answers were correct refusals, and only one answer did not state that the information is missing. Under G0 and G1, about 40 % of the answers were unsupported."

Can you check whether the totals and the percentage in my text are calculated correctly from these numbers?

Prompt 16

Tool: ChatGPT (OpenAI, GPT-5.5 Thinking)
Used for: identifying possible information sources

I am writing Section 1.7 (Question Types) of my bachelor thesis. In my experiment, I use five types of questions about software documentation: definition questions (what something is), how-to questions (how to do something), troubleshooting questions (why something does not work and how to fix it), configuration questions (how to set an option or a setting) and API usage questions (how to use a function, class or parameter). I want to justify these types with the literature. Which research areas study the types of questions that developers ask (for example studies of Stack Overflow questions, studies of API documentation, or question classification in question answering), and which search keywords should I use to find papers that describe similar categories? I will read and check every source myself.

Prompt 17

Tool: ChatGPT (OpenAI, GPT-5.5 Thinking)
Used for: organising possible information sources

For Section 1.6 (Evaluation of Answer Quality) of my thesis I want to compare the evaluation approaches that I found. Can you help me organise them in a table with the columns "approach", "what is evaluated", "how it is evaluated (LLM judge, reference answer, human annotation)" and "metrics"? These are the approaches and what I know about them:

RAGAS (Es et al., 2024): reference-free evaluation of RAG; evaluates whether the retrieved context is relevant and focused and whether the LLM uses the context faithfully; the library offers Faithfulness, Response Relevancy, Context Precision, Context Recall, Factual Correctness and Rubrics Based Scoring.
ARES (Saad-Falcon et al., 2024): fine-tunes lightweight LLM judges with synthetic data and about 150 human-annotated examples; evaluates context relevance, answer faithfulness and answer relevance.
Yu et al. (2024): survey of RAG evaluation; describes metrics for retrieval and generation such as relevance, accuracy and faithfulness and gives an overview of benchmarks.
Stolfo (2024): checks whether each sentence of a long-form answer is grounded in the retrieved documents.
Wallat et al. (2025): shows that a citation can be correct without the model having actually used the cited document (correctness is not faithfulness).

Which of these approaches evaluate the same aspects, and which aspect is not covered by any of them?

Prompt 18

Tool: ChatGPT (OpenAI, GPT-5.5 Thinking)
Used for: grammar correction

English is not my first language. Can you check the grammar, spelling and punctuation of the following paragraph from the abstract of my bachelor thesis? Please correct only real mistakes, keep my wording, and list every change you made.

"The formatting strategies had only a small effect on the scores: short paragraph answers had the highest faithfulness, and step-by-step answers the lowest technical correctness and faithfulness. The grounding strategies did not significantly changed the scores of the answers to the answerable questions, but source-restricted answering clearly increased the number of correct refusals to the unanswerable questions (38 of 60 answers, compared with almost none without it). The best combination differed between the question types, but the differences was small."

Prompt 19

Tool: Claude (Anthropic, Claude Opus 5.5)
Used for: planning the structure and content of the chapters

I am writing Section 1.8 (Research Gap) of my bachelor thesis. It should summarise the analytical review and lead to my research questions. These are the main points of my review:

RAG adds information from external sources to the answers of an LLM, which is useful in domain-specific question answering, where the knowledge of the LLM may be incomplete or outdated (Lewis et al., 2020; Es et al., 2024; Sharma et al., 2024).
Software documentation contains technical and frequently changing information, and code examples are the most helpful part of API documentation for LLMs (Wang et al., 2026; Watson et al., 2013; Chen et al., 2025).
RAG systems can give answers that are not grounded in the retrieved texts, and citations do not necessarily show the sources that the model actually used (Elchafei et al., 2026; Stolfo, 2024; Wallat et al., 2025).
The format of an answer matters for its usefulness (Perera and Nand, 2016; Lin et al., 2003), and users of a help system preferred answers with discrete steps (Sharma et al., 2024).
Different question types may need different answers, but I did not find a study that compares formatting and grounding strategies for different types of software documentation questions.

My research questions are: RQ1 – How do the formatting strategies affect the quality of the answers? RQ2 – How do the grounding strategies affect the quality of the answers and the behaviour of the LLMs on questions that cannot be answered from the documentation? RQ3 – Which combination of strategies is most suitable for each question type?

In which order should I present these points so that the research gap and the research questions follow logically from them? Is there a point that is missing or that does not support the gap?

Prompt 20

Tool: Claude (Anthropic, Claude Opus 5.5)
Used for: planning the structure and content of the chapters

I am writing Section 5.8 (Limitations) of my bachelor thesis. These are the limitations that I want to describe:

the corpus contained only five pages of the Django 5.2 documentation;
the question set had only 25 answerable and 10 unanswerable questions (five and two per question type), so no statistical tests were possible for the question types;
the questions and reference answers were written by me, and the technical correctness scores depend on how complete the reference answers are;
only two formatting and two grounding strategies were tested, each with one fixed wording of the instruction;
only two small LLMs of the same family (ministral-3b-2512 and ministral-8b-2512) were used;
the answers were scored by an LLM (ministral-14b-2512) with RAGAS, and almost all answers received the highest clarity score (424 of 450);
repeated answers to the same prompt were not identical even with a temperature of 0 and a fixed seed;
I did not check whether the cited chunks actually support the claims of the G1 answers;
the manual scoring by an external reviewer was not finished yet.

How can I group these limitations into a few categories so that the section is easy to read? For each category, which consequence for the interpretation of my results should I mention?

Prompt 21

Tool: Claude (Anthropic, Claude Opus 5.5)
Used for: language editing

Here is the first paragraph of the introduction of my bachelor thesis. Can you improve the flow between the sentences? Keep my sentences and all citations, do not add new information or new citations, and change only the connections between the sentences where it is necessary. Show me what you changed.

"The topicality of this bachelor thesis can be explained by the increasing use of Retrieval-Augmented Generation (RAG) systems (Yu, Gan et al., 2024), including technical and domain-specific question answering tasks (Sharma, Yoon et al., 2024). Large language models (LLMs) can generate fluent answers. However, their knowledge may be limited and difficult to update (Lewis, Perez et al., 2020), and they may not be able to answer questions about events that happened after their training (Es, James et al., 2024). In addition, they may generate unsupported information (hallucinations) during question answering (Es, James et al., 2024). On the other hand, RAG combines the LLM with information retrieved from external sources, allowing the system to use relevant sources during answer generation (Lewis, Perez et al., 2020; Es, James et al., 2024)."

Prompt 22

Tool: Claude (Anthropic, Claude Opus 5.5)
Used for: checking the citations against the original sources

In Section 1.6 of my thesis I wrote the following two sentences:

"Es et al. introduce RAGAS, a framework for evaluating RAG-based systems, which considers both the ability of the retrieval component to find relevant and focused context and the ability of the LLM to use this context faithfully (Es, James et al., 2024)."

"Saad-Falcon et al. introduce ARES, which fine-tunes lightweight LLM judges with synthetic training data and a small set of about 150 human-annotated examples, and evaluates three aspects of RAG systems: context relevance, answer faithfulness and answer relevance (Saad-Falcon, Khattab et al., 2024)."

The sources are: Es, S., James, J., Espinosa-Anke, L., and Schockaert, S. RAGAS: Automated Evaluation of Retrieval Augmented Generation. EACL 2024 System Demonstrations, pp. 150–158; and Saad-Falcon, J., Khattab, O., Potts, C., and Zaharia, M. ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems. NAACL 2024. Do the papers really say this? In particular, is "about 150 human-annotated examples" correct for ARES, and are the three aspects named correctly?

Prompt 23

Tool: Claude (Anthropic, Claude Opus 5.5)
Used for: checking the consistency between the text and the source code

In Section 3.7 of my thesis, Table 3.6 gives the instructions of the grounding strategies: G0 – no instruction about sources; G1 – "After each claim, add the number of the chunk that supports it in square brackets, for example [1]."; G2 – "Use only the information in the provided documentation. If the answer is not in the documentation, say: 'The answer cannot be found in the provided documentation.'" In Section 4.5 I wrote that the script auto_checks.py checks whether an answer contains the sentence "cannot be found in the provided documentation".

This is the part of my config.py that defines the instructions:

REFUSAL_SENTENCE = "The answer cannot be found in the provided documentation."
GROUNDING = {
"G0": "",
"G1": "After each claim, add the number of the chunk that supports it in square "
"brackets, for example [1].",
"G2": "Use only the information in the provided documentation. If the answer is "
f"not in the documentation, say: '{REFUSAL_SENTENCE}'",
}

Are the instructions in my table exactly the same as in the code? Does the sentence that the check looks for match the refusal sentence of G2?
