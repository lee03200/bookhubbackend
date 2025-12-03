"""
BookHub API 快速测试脚本
用于验证 API 接口是否正常工作
"""

import requests
import json

BASE_URL = "http://localhost:8000/api"


def print_response(title, response):
    """打印响应信息"""
    print(f"\n{'='*60}")
    print(f"测试: {title}")
    print(f"状态码: {response.status_code}")
    try:
        print(f"响应数据: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"响应内容: {response.text}")
    print('='*60)


def test_api():
    """测试主要API接口"""
    
    print("\n" + "="*60)
    print("BookHub API 测试开始")
    print("="*60)
    
    # 1. 测试获取书籍列表
    print("\n[1] 测试获取书籍列表...")
    response = requests.get(f"{BASE_URL}/books/")
    print_response("获取书籍列表", response)
    
    # 2. 测试获取推荐书籍
    print("\n[2] 测试获取推荐书籍...")
    response = requests.get(f"{BASE_URL}/books/recommended/")
    print_response("获取推荐书籍", response)
    
    # 3. 测试搜索书籍
    print("\n[3] 测试搜索书籍...")
    response = requests.get(f"{BASE_URL}/books/?search=三体")
    print_response("搜索书籍", response)
    
    # 4. 测试用户注册
    print("\n[4] 测试用户注册...")
    register_data = {
        "username": "testuser123",
        "email": "test@test.com",
        "password": "password123",
        "password2": "password123"
    }
    response = requests.post(f"{BASE_URL}/register", json=register_data)
    print_response("用户注册", response)
    
    if response.status_code == 201:
        token = response.json().get('token')
        print(f"\n✅ 注册成功！Token: {token}")
        
        # 5. 测试获取用户信息（需要认证）
        print("\n[5] 测试获取用户信息（需要Token）...")
        headers = {"Authorization": f"Token {token}"}
        response = requests.get(f"{BASE_URL}/profile", headers=headers)
        print_response("获取用户信息", response)
        
        # 6. 测试添加书籍到书架（需要认证）
        print("\n[6] 测试添加书籍到书架...")
        shelf_data = {"book_id": 1}
        response = requests.post(f"{BASE_URL}/bookshelf/", json=shelf_data, headers=headers)
        print_response("添加到书架", response)
        
        # 7. 测试查看书架
        print("\n[7] 测试查看书架...")
        response = requests.get(f"{BASE_URL}/bookshelf/", headers=headers)
        print_response("查看书架", response)
        
        # 8. 测试发表评论（需要认证）
        print("\n[8] 测试发表评论...")
        comment_data = {
            "book": 1,
            "content": "这是一本很棒的书！强烈推荐！",
            "rating": 5
        }
        response = requests.post(f"{BASE_URL}/comments/", json=comment_data, headers=headers)
        print_response("发表评论", response)
        
        # 9. 测试获取评论
        print("\n[9] 测试获取书籍评论...")
        response = requests.get(f"{BASE_URL}/comments/?book_id=1")
        print_response("获取评论", response)
        
    else:
        print("\n❌ 注册失败，跳过需要认证的测试")
        print("可能原因：用户名已存在，请尝试更改 register_data 中的用户名")
    
    print("\n" + "="*60)
    print("✅ API 测试完成！")
    print("="*60)


if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("\n❌ 错误：无法连接到服务器")
        print("请确保后端服务器已启动（运行 python manage.py runserver）")
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {str(e)}")
