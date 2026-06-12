import html
import json
import re
import urllib.error
import urllib.request


# 企业微信机器人配置
WECHAT_WEBHOOK_URL = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=你的key'


def _html_to_text(content):
    """Convert the existing HTML email body into readable WeChat markdown text."""
    text = re.sub(r'<\s*br\s*/?\s*>', '\n', content, flags=re.IGNORECASE)
    text = re.sub(r'</\s*(p|div|h[1-6]|li|ul)\s*>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<[^>]+>', '', text)
    text = html.unescape(text)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return '\n'.join(lines)


def send_wechat_notification(subject, content):
    """
    发送企业微信机器人通知。
    :param subject: 通知标题
    :param content: 通知内容，兼容现有HTML邮件内容
    :return: 发送结果
    """
    message = f"### {subject}\n{_html_to_text(content)}"
    payload = {
        'msgtype': 'markdown',
        'markdown': {
            'content': message[:4096]
        }
    }

    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            WECHAT_WEBHOOK_URL,
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
        if result.get('errcode') != 0:
            print(f"企业微信通知发送失败: {result}")
            return False
        return True
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
        print(f"企业微信通知发送失败: {str(e)}")
        return False
