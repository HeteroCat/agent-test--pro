import argparse
import sys
from .main import batch_test


def start_web_server():
    """Start the web interface"""
    try:
        from flask import Flask, request, jsonify, render_template
        from .utils.get_res import get_response_data
        
        app = Flask(__name__, template_folder='templates')
        
        @app.route('/')
        def index():
            return render_template('index.html')

        @app.route('/get_response', methods=['POST'])
        def get_response():
            data = request.json
            url = "https://ai-course-fast.huayuntiantu.com/api/v1/chat/completions"
            token = "openapi-v7toprTxmXoTDlgIG6spbAVnGmwsnh9qKGZoEBFnRTaBMWVaSO8o"
            response_data = get_response_data(url, token, data)
            return jsonify(response_data)

        print("启动 Web 界面...")
        print("访问: http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except ImportError:
        print("错误: Flask 未安装。请运行: pip install flask")
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