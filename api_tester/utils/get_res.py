import requests
import json
import re

def handle_streaming_response(url, headers, data):
    """处理流式响应"""
    try:
        response = requests.post(url, headers=headers, json=data, stream=True, timeout=30)
        
        if response.status_code != 200:
            return {"error": f"Request failed with status code {response.status_code}", "details": response.text, "request_data": data}
        
        content_parts = []
        
        for line in response.iter_lines(decode_unicode=True):
            if line.strip():
                # 处理Server-Sent Events格式
                if line.startswith('data: '):
                    data_content = line[6:]  # 移除'data: '前缀
                    
                    if data_content.strip() == '[DONE]':
                        break
                    
                    try:
                        chunk_data = json.loads(data_content)
                        # 提取流式响应中的内容
                        if 'choices' in chunk_data and chunk_data['choices']:
                            delta = chunk_data['choices'][0].get('delta', {})
                            if 'content' in delta and delta['content'] is not None:
                                content_parts.append(delta['content'])
                    except json.JSONDecodeError:
                        continue
        
        # 合并所有内容片段
        full_content = ''.join(content_parts)
        
        if full_content:
            return {"content": full_content}
        else:
            return {"error": "No content received from streaming response"}
            
    except requests.exceptions.Timeout:
        return {"error": "Request timeout after 30 seconds"}
    except requests.exceptions.ConnectionError:
        return {"error": "Connection error - unable to reach the API"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error in streaming: {str(e)}"}

def get_response_data(url, Bearer_token, To_send, **kwargs):
    try:
        headers = {
            "Authorization": f"Bearer {Bearer_token}",
            "Content-Type": "application/json"
        }
        
        # The user provides the full JSON payload in the 'To_send' variable.
        # We should send it directly.
        data = To_send
        # Handle extra variables if provided (future-proofing)
        if 'variables' in kwargs and isinstance(data, dict):
            data['variables'] = kwargs['variables']
        
        # Check if this is a streaming request
        is_streaming = data.get('stream', False)
        
        if is_streaming:
            return handle_streaming_response(url, headers, data)
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code != 200:
            return {"error": f"Request failed with status code {response.status_code}", "details": response.text, "request_data": data}
        
        response_json = response.json()
        
        content = None
        
        # Define a list of places to look for the 'choices' array
        potential_sources = [response_json]
        if isinstance(response_json.get('response'), dict):
            potential_sources.append(response_json['response'])

        # Priority 1: Check for content in 'choices' (OpenAI format) in all potential sources
        for source in potential_sources:
            if isinstance(source.get('choices'), list) and source.get('choices'):
                message = source['choices'][0].get('message', {})
                content = message.get('content')
                if content is not None:
                    break # Found it
        
        # Priority 2: If no content, check for FastGPT's 'responseData' which contains 'textOutput'
        if content is None and isinstance(response_json.get('responseData'), list) and response_json.get('responseData'):
            text_output_str = response_json['responseData'][-1].get('textOutput')
            if text_output_str:
                try:
                    # 'textOutput' can be a JSON string itself containing 'choices'
                    text_output_json = json.loads(text_output_str)
                    if isinstance(text_output_json.get('choices'), list) and text_output_json.get('choices'):
                        message = text_output_json['choices'][0].get('message', {})
                        content = message.get('content')
                    else:
                        # If 'textOutput' is a JSON but not in the expected structure, return it as a string
                        content = json.dumps(text_output_json, ensure_ascii=False)
                except (json.JSONDecodeError, TypeError):
                    # If 'textOutput' is just a plain string
                    content = text_output_str
        
        if content is not None:
            return {"content": content}

        # Fallback: if content is still not found, return an error with the full response
        return {"error": "Could not extract content from the API response.", "response": response_json}
            
    except requests.exceptions.Timeout:
        return {"error": "Request timeout after 30 seconds"}
    except requests.exceptions.ConnectionError:
        return {"error": "Connection error - unable to reach the API"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

