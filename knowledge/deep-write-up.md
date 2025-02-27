DeepSearch:
DeepSearch is an application best used for complex questions that require iteratively reasoning, world-knowledge or up-to-date information.

Adding an API Key grants you a Higher Rate Limit: "jina_8465f39295ed481b8a44aeda708f1742rrhsoVYduVNpnEiZTdXcXy81L1kO"
By providing your API key, you can access a higher rate limit, and your key won't be charged.

Model (ID of the model to use.): "jina-deepsearch-v1"

Streaming: If true, returns a stream of events that happen during the Run as server-sent events, terminating when the Run enters a terminal state with a data: [DONE] message. (it is advisable to disable streaming by default as it generates too many messeges)

Reasoning Effort: Constrains effort on reasoning for reasoning models.
Currently supported values are "low", "medium", and "high."

low: Basic reasoning and searching for simple queries (max 500K tokens/req)
medium: Moderate reasoning and searching depth (1M tokens/req)
high: Maximum reasoning and searching for complex queries (2M tokens/req)

Reducing reasoning effort can result in faster responses and fewer tokens used on reasoning in a response (default should be set to "low").

Budget Tokens: This determines the maximum number of tokens is allowed use for DeepSearch process.
Larger budgets can improve response quality by enabling more exhaustive search for complex queries, although DeepSearch may not use the entire budget allocated.
(IMPORTANT)This overrides the reasoning_effort parameter.

Max Attempts: The maximum number of retries for solving a problem (and all sub-problems) in DeepSearch process.
A larger value allows DeepSearch to retry solving the problem by using different reasoning approaches and tackling strategies.
(IMPORTANT) This parameter overrides the reasoning_effort parameter. default "2"

Messages:
A list of messages between the user and the assistant comprising of the conversation so far (this should be an optional parameter considering we may only need the answer to a particular question rather than a whole conversation).

Python Code Example:
import requests
import json

url = "https://deepsearch.jina.ai/v1/chat/completions"
headers = {
"Content-Type": "application/json",
"Authorization": "jina_8465f39295ed481b8a44aeda708f1742rrhsoVYduVNpnEiZTdXcXy81L1kO"
}
data = {
"model": "jina-deepsearch-v1",
"messages": [
{
"role": "user",
"content": "Hi!"
},
{
"role": "assistant",
"content": "Hi, how can I help you?"
},
{
"role": "user",
"content": "what's the latest blog post from jina ai?"
}
],
"stream": False,
"reasoning_effort": "low",
"budget_tokens": "500000",
"max_attempts": 2
}

response = requests.post(url, headers=headers, data=json.dumps(data))

print(response.json())

Example Output "low" reasoning effort:
{
"id": "1740645526957",
"object": "chat.completion",
"created": 1740645526,
"model": "jina-deepsearch-v1",
"system*fingerprint": "fp_1740645526957",
"choices": [
{
"index": 0,
"message": {
"role": "assistant",
"content": "The latest blog post from Jina AI is 'A Practical Guide to Implementing DeepSearch/DeepResearch' published on February 25, 2025 [^1]. Another recent post is 'Query Expansion with LLMs: Searching Better by Saying More' published on February 18, 2025 [^2].\n\n[^1]: February 25 2025 16 minutes read A Practical Guide to Implementing DeepSearch DeepResearch QPS out depth in DeepSearch is the new norm Find answers through read search reason loops Learn what it is and how to build it [jina.ai](https://jina.ai/news/a-practical-guide-to-implementing-deepsearch-deepresearch)\n\n[^2]: February 18 2025 9 minutes read Query Expansion with LLMs Searching Better by Saying More Search has changed a lot since embedding models were introduced Is there still a role for lexical techniques like query expansion in AI We think so [jina.ai](https://jina.ai/news/query-expansion-with-llms-searching-better-by-saying-more)"
},
"logprobs": null,
"finish_reason": "stop"
}
],
"usage": {
"prompt_tokens": 56439,
"completion_tokens": 15816,
"total_tokens": 72045
},
"visitedURLs": [
"https://jina.ai/news?tag=tech-blog",
"https://jina.ai/news",
"https://jina.ai/news/a-practical-guide-to-implementing-deepsearch-deepresearch",
"https://jina.ai/news/query-expansion-with-llms-searching-better-by-saying-more",
"https://x.com/jinaai*?lang=en",
"https://jina.ai/",
"https://elastic.co/search-labs/blog/jina-ai-embeddings-rerank-model-open-inference-api",
"https://jina.ai/deepsearch",
"https://medium.com/@kawsarlog/jina-ais-reader-api-a-game-changer-for-developers-be66154b2692",
"https://github.com/jina-ai/node-DeepResearch",
"https://medium.com/@tossy21/trying-out-jina-ais-node-deepresearch-c5b55d630ea6",
"https://jina.ai/news/jina-embeddings-v3-a-frontier-multilingual-embedding-model",
"https://linkedin.com/posts/jinaai_langchain-serve-powering-your-slack-with-activity-7082721087007907841-SUPi",
"https://linkedin.com/posts/jinaai_jina-clip-v2-multilingual-multimodal-embeddings-activity-7265408739002740736-EQfe",
"https://huggingface.co/organizations/FactSet/activity/all",
"https://twitter.com/manisnesan",
"https://x.com/manisnesan?lang=ar-x-fm",
"https://twitter.com/jorgevee7",
"https://quora.com/How-do-I-check-if-a-blog-post-is-indexed-by-Google-or-not?top_ans=229341972",
"https://facebook.com/113348628845304/posts/new-blog-post-taarifa-juu-ya-kanusho-la-watu-wanaotumia-jina-la-flaviana-matata-/137444423102391",
"https://x.com/AkshayGoindani1"
],
"readURLs": [
"https://jina.ai/news?tag=tech-blog",
"https://jina.ai/news",
"https://jina.ai/news/a-practical-guide-to-implementing-deepsearch-deepresearch",
"https://jina.ai/news/query-expansion-with-llms-searching-better-by-saying-more"
]
}

Example Output "high" reasoning effort:
{
"id": "1740646976200",
"object": "chat.completion",
"created": 1740646976,
"model": "jina-deepsearch-v1",
"system_fingerprint": "fp_1740646976200",
"choices": [
{
"index": 0,
"message": {
"role": "assistant",
"content": "The latest blog post from Jina AI is \"A Practical Guide to Implementing DeepSearch/DeepResearch\" published on February 25, 2025[^1]. Other recent posts include \"Query Expansion with LLMs: Searching Better by Saying More\" (February 18, 2025) and \"A Practical Guide to Deploying Search Foundation Models in Production\" (January 31, 2025).[^1]\n\n[^1]: February 25 2025 16 minutes read A Practical Guide to Implementing DeepSearch DeepResearch QPS out depth in DeepSearch is the new norm Find answers through read search reason loops Learn what it is and how to build it [jina.ai](https://jina.ai/news/a-practical-guide-to-implementing-deepsearch-deepresearch)"
},
"logprobs": null,
"finish_reason": "stop"
}
],
"usage": {
"prompt_tokens": 22281,
"completion_tokens": 9513,
"total_tokens": 31662
},
"visitedURLs": [
"https://jina.ai/news",
"https://jina.ai/news?tag=tech-blog",repo:Sheshiyer/jina-ai-mcp-multimodal-search
"https://jina.ai/models",
"https://sacra.com/c/jina-ai",
"https://rivalsense.co/intel/jina-ai",
"https://reddit.com/r/LocalLLaMA/comments/1feiip0/jina_ai_releases_readerlm_05b_and_15b_for",
"https://jina.ai/deepsearch",
"https://elastic.co/search-labs/blog/jina-ai-embeddings-rerank-model-open-inference-api",
"https://medium.com/@kawsarlog/jina-ais-reader-api-a-game-changer-for-developers-be66154b2692",
"https://github.com/jina-ai/node-DeepResearch",
"https://medium.com/@tossy21/trying-out-jina-ais-node-deepresearch-c5b55d630ea6"
],
"readURLs": [
"https://jina.ai/news",
"https://jina.ai/news?tag=tech-blog",
"https://jina.ai/news/a-practical-guide-to-implementing-deepsearch-deepresearch"
]
}

