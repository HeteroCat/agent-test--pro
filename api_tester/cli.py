import argparse
import sys
from .main import batch_test


def start_web_server():
    """Start the web interface"""
    try:
        from flask import Flask, request, jsonify, render_template
        from .utils.get_res import get_response_data
        import os
        import time
        
        # 获取当前文件所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        template_dir = os.path.join(current_dir, 'templates')
        
        app = Flask(__name__, template_folder=template_dir)
        
        @app.route('/')
        def home():
            return render_template('home.html')
        
        @app.route('/test')
        def test():
            return render_template('index.html')
        
        @app.route('/batch')
        def batch():
            return render_template('batch.html')

        @app.route('/get_response', methods=['POST'])
        def get_response():
            try:
                request_data = request.json
                if not request_data:
                    return jsonify({"error": "没有接收到JSON数据"}), 400
                
                # 从请求中提取URL、token和数据
                url = request_data.get('url')
                token = request_data.get('token')
                data = request_data.get('data')
                
                if not url or not token or not data:
                    return jsonify({"error": "缺少必需的参数: url, token, data"}), 400
                
                # 将data转换为标准的OpenAI API格式
                if isinstance(data, str):
                    # 如果是字符串，转换为标准的messages格式
                    formatted_data = {
                        "model": "gpt-3.5-turbo",
                        "messages": [
                            {"role": "user", "content": data}
                        ]
                    }
                else:
                    # 如果已经是字典格式，检查是否包含messages
                    if "messages" not in data:
                        # 如果没有messages字段，尝试从data字段转换
                        content = data.get("data", str(data))
                        formatted_data = {
                            "model": "gpt-3.5-turbo",
                            "messages": [
                                {"role": "user", "content": content}
                            ]
                        }
                    else:
                        # 如果已经有messages字段，直接使用
                        formatted_data = data
                
                # 添加调试信息
                print(f"Debug - URL: {url}")
                print(f"Debug - Token: {token[:20]}..." if token else "Debug - Token: None")
                print(f"Debug - Formatted Data: {formatted_data}")
                
                # 记录开始时间
                start_time = time.time()
                
                response_data = get_response_data(url, token, formatted_data)
                
                # 计算执行时间
                end_time = time.time()
                execution_time = round(end_time - start_time, 2)  # 转换为秒并保留2位小数
                
                # 添加执行时间到响应数据
                if isinstance(response_data, dict):
                    response_data['execution_time_s'] = execution_time
                
                # 添加响应调试信息
                print(f"Debug - Response: {response_data}")
                print(f"Debug - Execution Time: {execution_time}ms")
                
                if response_data is None:
                    return jsonify({"error": "API请求失败，未收到响应"}), 500
                    
                return jsonify(response_data)
                
            except Exception as e:
                return jsonify({"error": f"服务器错误: {str(e)}"}), 500

        print("🚀 启动 Web 界面...")
        print("📱 访问地址: http://localhost:8080")
        print("💡 提示: 按 Ctrl+C 停止服务器")
        
        app.run(debug=True, host='0.0.0.0', port=8080)
        
    except ImportError:
        print("❌ 错误: Flask 未安装。请运行: pip install flask")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 启动Web服务器时出错: {e}")
        sys.exit(1)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="API Tester Tool - Test APIs with JSON files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --test-dir tests --output-dir results
  %(prog)s --test-dir tests --url https://api.example.com --token your-token
  %(prog)s --web
        """
    )
    
    parser.add_argument(
        "--test-dir", 
        type=str, 
        help="Directory containing JSON test files"
    )
    
    parser.add_argument(
        "--output-dir", 
        type=str, 
        default="output",
        help="Directory to save response files (default: output)"
    )
    
    parser.add_argument(
        "--url", 
        type=str, 
        default="https://ai-course-fast.huayuntiantu.com/api/v1/chat/completions",
        help="API endpoint URL"
    )
    
    parser.add_argument(
        "--token", 
        type=str, 
        default="openapi-v7toprTxmXoTDlgIG6spbAVnGmwsnh9qKGZoEBFnRTaBMWVaSO8o",
        help="Authentication token"
    )
    
    parser.add_argument(
        "--variables_dir", 
        type=str, 
        default="", 
        help="Variables to send in the request"
    )

    parser.add_argument(
        "--web", 
        action="store_true",
        help="Start web interface"
    )
    
    parser.add_argument(
        "--version", 
        action="version", 
        version="%(prog)s 1.0.0"
    )
    
    args = parser.parse_args()
    
    if args.web:
        start_web_server()
    elif args.test_dir:
        batch_test(args.url, args.token, args.test_dir, args.output_dir, variables_dir=args.variables_dir)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()