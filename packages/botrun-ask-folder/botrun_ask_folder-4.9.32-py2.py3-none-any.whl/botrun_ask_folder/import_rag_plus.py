import concurrent.futures
import json
import re
from typing import List, Dict, Any, Tuple

from .query_qdrant import query_qdrant_knowledge_base, custom_log
from .query_qdrant_keyword import query_qdrant_knowledge_base_keyword


def parse_json_blocks_import_rag_plus(input_str: str) -> Tuple[List[Dict[str, Any]], List[str]]:
    # 匹配包含@begin import_rag_plus到@end的整個段落
    pattern = r"(@begin import_rag_plus\s+.*?\s+@end)"
    matches = re.findall(pattern, input_str, re.DOTALL)
    json_blocks = []
    parsed_original_strings = []
    for match in matches:
        # 直接將匹配到的包含@begin和@end的整個字串添加到列表中
        parsed_original_strings.append(match)
        # 移除@begin import_rag_plus 和 @end標籤來解析JSON
        json_str = match.replace("@begin import_rag_plus", "").replace("@end", "").strip()
        try:
            json_block = json.loads(json_str)
            json_blocks.append(json_block)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    return json_blocks, parsed_original_strings


def has_import_rag_plus_section(input_str: str) -> bool:
    # print(f"has_import_rag_plus_section<==============")
    pattern = r"(@begin import_rag_plus\s+.*?\s+@end)"
    return bool(re.search(pattern, input_str, re.DOTALL))


def replace_system_message_with_knowledge_bases(system_message: str, parsed_original_strings: List[str],
                                                knowledge_bases: List[str]) -> str:
    for original_string, knowledge_base in zip(parsed_original_strings, knowledge_bases):
        system_message = system_message.replace(original_string, knowledge_base, 1)  # 使用 1 確保只替換第一次出現的匹配項
    return system_message


def import_rag_plus(websocket, chat_context, session_memory, websocket_send) -> List[Dict[str, Any]]:
    user_input = chat_context.get_latest_user_input()
    system_message = chat_context.system_message
    system_message = system_message.replace("{user_input}", user_input)  # 替換 user_input
    json_blocks, parsed_original_strings = parse_json_blocks_import_rag_plus(system_message)
    knowledge_bases = []  # 用來儲存每個 json_block 對應的知識庫查詢結果
    botrun_id = session_memory.get_current_botrun_id()

    def query_vector_search(json_block):
        custom_log('INFO', f"import_rag_plus.py, query_vector_search, json_block: {json_block}")
        return query_qdrant_knowledge_base(
            qdrant_host=json_block.get("qdrant_host", "qdrant"),
            qdrant_port=json_block.get("qdrant_port", 6333),
            collection_name=json_block.get("collection_name", ""),
            user_input=user_input,
            embedding_model=json_block.get("embedding_model", "openai/text-embedding-3-large"),
            top_k=json_block.get("top_k", 4),
            hnsw_ef=json_block.get("hnsw_ef", 256)
        )

    def query_keyword_search(json_block):
        custom_log('INFO', f"import_rag_plus.py, query_keyword_search, json_block: {json_block}")
        return query_qdrant_knowledge_base_keyword(
            qdrant_host=json_block.get("qdrant_host", "qdrant"),
            qdrant_port=json_block.get("qdrant_port", 6333),
            collection_name=json_block.get("collection_name", ""),
            user_input=user_input,
            embedding_model=json_block.get("embedding_model", "openai/text-embedding-3-large"),
            chat_model=json_block.get("chat_model", "gpt-4o-2024-08-06"),
            top_k=json_block.get("keyword_top_k", 4),
            is_show_ref_info=json_block.get("is_show_ref_info", True),
            hnsw_ef=json_block.get("hnsw_ef", 256),
            prompt_keyword=json_block.get("prompt_keyword", "auto")
        )

    for json_block in json_blocks:
        str_knowledge_base=""
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                custom_log('INFO', f"import_rag_plus.py, json_block: {json_block}")
                custom_log('INFO', f"submit query_vector_search")
                future_vector = executor.submit(query_vector_search, json_block)
                custom_log('INFO', f"future_vector: {future_vector}")
                custom_log('INFO', f"submit query_keyword_search")
                future_keyword = executor.submit(query_keyword_search, json_block) if json_block.get(
                    "is_keyword_search", False) else None
                custom_log('INFO', f"future_keyword: {future_keyword}")

                str_knowledge_base = future_vector.result()
                if future_keyword:
                    str_knowledge_base_keyword = future_keyword.result()
                    str_knowledge_base += f"{str_knowledge_base_keyword}"

            # 搜尋結果加到知識庫列表 List 物件中，然後回傳
            knowledge_bases.append(str_knowledge_base)
            custom_log('INFO', f"import_rag_plus.py, append knowledge_base: {str_knowledge_base}")
            knowledge_base_display_char_limit = json_block.get("knowledge_base_display_char_limit", 0)
            if knowledge_base_display_char_limit:
                websocket_send(websocket,
                               str_knowledge_base[0:knowledge_base_display_char_limit] + "\n-- AI:\n",
                               botrun_id)
        except Exception as e:
            print(f"import_rag_plus.py, exception: {e}")
            import traceback
            traceback.print_exc()
            knowledge_bases.append(str_knowledge_base)  # 如果查詢失敗，添加一個空字串作為佔位符

    system_message = replace_system_message_with_knowledge_bases(system_message, parsed_original_strings,
                                                                 knowledge_bases)
    chat_context.system_message = system_message
    new_messages = chat_context.get_messages()
    return new_messages
