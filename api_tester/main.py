import json
import os
from .utils.get_res import get_response_data
import time

def test_api(url, token, content, output_dir, filename, **kwargs):
    """
    Test API with given content and save response to file.
    
    Args:
        url (str): API endpoint URL
        token (str): Authentication token
        content (dict): JSON content to send
        output_dir (str): Directory to save response
        filename (str): Output filename
    
    Returns:
        dict: API response data
    """
    response_data = get_response_data(url, token, content, **kwargs)
    if response_data:
        output_filename = f"response_{filename}"
        output_path = os.path.join(output_dir, output_filename)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(response_data, f, ensure_ascii=False, indent=4)
        print(f"响应已保存到: {output_path}", end="")
        return response_data
    else:
        print("No response data received.", end="")
        return None


def batch_test(url, token, test_dir, output_dir, variables_dir=""):
    """
    Batch test all JSON files in a directory.
    
    Args:
        url (str): API endpoint URL
        token (str): Authentication token
        test_dir (str): Directory containing JSON test files
        output_dir (str): Directory to save responses
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    test_count = 0
    success_count = 0
    time_start = time.time()
    for dirpath, dirnames, filenames in os.walk(test_dir):
        for filename in filenames:
            if filename.endswith(".json"):
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = json.load(f)
                        t0 = time.time()
                    print(f"正在测试: {file_path}")
                    if variables_dir and os.path.exists(os.path.join(variables_dir, filename)):
                        with open(os.path.join(variables_dir, filename), "r", encoding="utf-8") as var_file:
                            variables = json.load(var_file)
                    result = test_api(url, token, content, output_dir, filename, variables=variables if variables_dir and os.path.exists(os.path.join(variables_dir, filename)) else {})
                    print(" ，用时",time.time() - t0, "秒")
                    test_count += 1
                    if result:
                        success_count += 1
                except Exception as e:
                    print(f"测试文件 {file_path} 时出错: {str(e)}")
                    test_count += 1
    time_end = time.time()
    print(f"\n测试完成! 总计: {test_count}, 成功: {success_count}, 失败: {test_count - success_count}, 耗时: {time_end - time_start:.2f}秒")