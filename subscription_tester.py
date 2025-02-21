#!/usr/bin/env python3
import argparse
import requests
import yaml
from urllib.parse import quote
from pathlib import Path

default_sub_server_url = "http://127.0.0.1:25500"
default_sub_url = "https://dash.pqjc.site/api/v1/client/subscribe?token=1eafe46f445ed95b52586581b12dfafd"
default_config_url = "https://raw.githubusercontent.com/ootonn/clash_rules/refs/heads/main/clash_config.ini"

def validate_yaml(content):
    try:
        yaml.safe_load(content)
        return True
    except yaml.YAMLError as e:
        print(f"YAML格式验证失败: {str(e)}")
        return False

def convert_subscription(base_url, target, url, output, config=None):
    # 编码订阅链接
    encoded_url = quote(url, safe='')
    
    # 构建基础请求URL
    api_url = f"{base_url}/sub?target={quote(target)}&url={encoded_url}"
    
    # 添加模板参数
    if config:
        # 对config参数进行双重编码处理
        encoded_config = quote(config, safe='')
        encoded_config = quote(encoded_config, safe='')
        api_url += f"&config={encoded_config}"
    
    try:
        # 使用curl命令代替requests
        import subprocess
        result = subprocess.run(
            ['curl', '-sS', '-L', '--fail-with-body', api_url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30
        )

        # 手动解码输出
        content = result.stdout.decode('utf-8', errors='ignore')
        error_msg = result.stderr.decode('utf-8', errors='ignore') if result.stderr else ''
        
        # 验证YAML格式
        if not validate_yaml(content):
            return False
        
        # 确保输出目录存在
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 保存文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"转换成功！文件已保存至: {output_path.resolve()}")
        return True
        
    except subprocess.TimeoutExpired as e:
        print(f"请求超时: {str(e)}")
        return False
    except subprocess.CalledProcessError as e:
        print(f"curl命令执行失败: {str(e)}")
        return False
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='订阅转换测试工具')
    parser.add_argument('url', nargs='?', default=default_sub_url, 
                       help='需要转换的订阅链接（可选，默认使用内置订阅）')
    parser.add_argument('-c', '--config', default=default_config_url,
                       help='远程模板文件URL（支持subconverter兼容模板）')
    parser.add_argument('-t', '--target', default='clash', 
                       help='目标格式 (默认: clash)')
    parser.add_argument('-o', '--output', default='./output.yaml',
                       help='输出文件路径 (默认: ./output.yaml)')
    parser.add_argument('-b', '--base', default=default_sub_server_url,
                       help='订阅转换服务地址')
    
    args = parser.parse_args()
    
    success = convert_subscription(
        base_url=args.base.rstrip('/'),
        target=args.target,
        url=args.url,
        output=args.output,
        config=args.config
    )
    
    exit(0 if success else 1) 