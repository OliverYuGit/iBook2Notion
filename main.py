import re
import book
import json
import time
from notion import create_note
from config import Config
from typing import Dict

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate, FewShotPromptTemplate

cfg = Config()
llm = OpenAI(temperature=0, openai_api_key=cfg.openai_api_key)


def split_list(eles: list) -> list:
    eles = [str(ele) for ele in eles]
    list_str = '||'.join(eles)
    text_splitter = RecursiveCharacterTextSplitter(separators="||", chunk_size=800, chunk_overlap=0)
    texts = text_splitter.split_text(list_str)
    texts = ['[' + text.replace('||', ',').replace('|', '') + ']' for text in texts]
    return texts


def extract_title(text: str) -> Dict:
    examples = [
        {
            'input': """[{{"id": "i0", "content": "图是更为复杂的数据结构，因为在图中会呈现出多对多的关联关系。"}},
            {{"id": "i1", "content": "计算机科学领域的算法，它的本质是一系列程序指令，用于解决特定的运算和逻辑问题。"}}]""",
            'output': """{{"i0": {{"title": "图的概念"}}, "i1": {{"title": "算法的本质"}}}}"""
        },
        {
            'input': """[{{"id": "i0", "content": "给相关笔记添加链接。"}}]""",
            'output': """{{"i0": {{"title": "笔记链接"}}}}"""
        },
    ]

    example_prompt = PromptTemplate(
        input_variables=['input', 'output'],
        template="Example Input: {input} \nExample Output: {output}"
    )
    
    list_len = text.count("content")

    prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        prefix=f"""
        Given a list (Python) contains {list_len} dict that include the "content".
        List {list_len} dict that contain "title" extracted from "content".
        """,
        suffix="Input: {text} \nOutput:",
        input_variables=["text"]
    )

    prompt_value = prompt.format(text=text)
    # print(prompt_value)
    print(f"""-=-=-=-=-=-=-=-=-= Input for AI =-=-=-=-=-=-=-=-=-\n{text}\n""")
    res = llm(prompt_value)
    print(f"""-=-=-=-=-=-=-=-=-= Output from AI =-=-=-=-=-=-=-=-=-\n{res}\n""")
    try:
        res = res.strip().replace('\'', '\"')
        return json.loads(res)
    except Exception as e:
        print(f"Failed to format title result. Message: {e}")
    


def main():
    notes = book.query()
    
    for i in range(0, len(notes), cfg.max_notes4ai):
        note_list = notes[i:i+cfg.max_notes4ai]
        content_list = [
            {'id': note.get('id'), 'content': note.get('highlight')} for note in note_list
        ]
        # texts = split_list(content_list)

        res = extract_title(str(content_list))
        print("-=-=-=-=-=-=-=-=-= Notion Note =-=-=-=-=-=-=-=-=-")
        for note in note_list:
            idx = note['id']
            title_dict = res.get(idx, None)
            if title_dict is None:
                note['title'] = 'No Title'
            else:
                title = title_dict.get('title', "No Title")
                note['title'] = title
            create_note(note)
            time.sleep(1)
        print("\n")


if __name__ == "__main__":
    main()