def preprocess_text(text):
    """
    Process text as necessary.
    For example:
    Removing any identifiable features of the company or,
    Summarize text to capture the important parts
    """

    return text


def prepare_prompt_messages_verbose(text1, text2):
    summarized_text1 = preprocess_text(text1)
    summarized_text2 = preprocess_text(text2)
    system_prompt = "You are a highly intelligent and precise financial analyst."
    user_prompt = (
        "Below are excerpts from two Japanese companies' quarterly earnings statements. "
        "Please analyze the financial data (e.g., net sales, operating profit, net profit, growth) and determine which company will perform better in the future based only on the information available."
        "Provide a clear explanation of your reasoning, including key metrics compared. If data is incomplete, make reasonable assumptions but note them. "
        "Return the result in a structured JSON format with fields: 'winner' (company A as 0 or company B as 1), 'metrics_compared', and 'reasoning'.\n\n"
        f"Company A Earnings:\n{summarized_text1}\n\n"
        f"Company B Earnings:\n{summarized_text2}"
    )
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


def prepare_prompt_messages(text1, text2):
    summarized_text1 = preprocess_text(text1)
    summarized_text2 = preprocess_text(text2)
    system_prompt = "You are a highly intelligent and precise financial analyst."
    user_prompt = (
        "Below are excerpts from two Japanese companies' quarterly earnings statements. "
        "Please analyze the financial data (e.g., net sales, operating profit, net profit, growth) and determine which company will perform better in the future based only on the information available."
        "If data is incomplete, make reasonable assumptions."
        "Return the result as 0 or 1 only (company A as 0 or company B as 1) (One character only)."
        "Do not provide any extra text! Answer as 0 or 1 only! I will call int(output), that should work!.\n\n"
        f"Company A Earnings:\n{summarized_text1}\n\n"
        f"Company B Earnings:\n{summarized_text2}"
    )
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


def call_grok_mini_api(client, prompt_messages):
    return client.chat.completions.create(model="grok-3-mini", messages=prompt_messages)


def call_grok_api(client, prompt_messages):
    return client.chat.completions.create(model="grok-3", messages=prompt_messages)


def call_deepseek_api(client, prompt_messages):
    return client.chat.completions.create(
        model="deepseek-chat", messages=prompt_messages, temperature=0
    )
