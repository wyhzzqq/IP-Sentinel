import random
import os

# ==========================================================
# IP-Sentinel 终极动态指纹工厂 (V4.1.0 - 降维自洽版)
# 战术核心:
# 1. 放弃“假装最新 Chrome”，采用“降维现代化”策略
# 2. 引入老旧 Chromium/WebView (完美掩护缺失的现代 Header)
# 3. 修正 Android Firefox 真实规范 (隐匿具体机型)
# 4. 严控 Safari 比例 (降低 SecureTransport 协议栈冲突)
# 5. 构建 35% Linux + 25% Win 的高权重 Firefox ESR 护城河
# ==========================================================

TOTAL_POOL = 4000

def weighted_choice(weighted_items):
    items = []
    for value, weight in weighted_items:
        items.extend([value] * weight)
    return random.choice(items)

# ----------------------------------------------------------
# 核心组件库
# ----------------------------------------------------------
FIREFOX_ESR_VERSIONS = [
    ("115.0", 50), # 115 ESR (最后支持 Win7/8 的版本，行为古怪很正常)
    ("128.0", 50), # 128 ESR (当前企业/Linux主流)
]

# 降现代化 Chromium 池 (完美掩护 curl 的老旧 TLS 和残缺 Header)
OLD_CHROME_VERSIONS = [
    ("109", 40), # 109 是 Win7/Win8.1 的绝唱版本
    ("114", 30),
    ("120", 30),
]

def generate_ff_ver():
    return weighted_choice(FIREFOX_ESR_VERSIONS)

def generate_old_chrome():
    major = weighted_choice(OLD_CHROME_VERSIONS)
    build = random.randint(5000, 6099)
    patch = random.randint(40, 150)
    return f"{major}.0.{build}.{patch}"

# ----------------------------------------------------------
# 1. Linux Firefox ESR (35% -> 1400条)
# 最匹配 VPS 环境，完美自洽 curl/OpenSSL
# ----------------------------------------------------------
def generate_linux_firefox(count=1400):
    uas = set()
    while len(uas) < count:
        ff_ver = generate_ff_ver()
        distro = random.choice(["X11; Linux x86_64", "X11; Ubuntu; Linux x86_64", "X11; Fedora; Linux x86_64"])
        uas.add(f"Mozilla/5.0 ({distro}; rv:{ff_ver}) Gecko/20100101 Firefox/{ff_ver}")
    return list(uas)

# ----------------------------------------------------------
# 2. Windows Firefox ESR (25% -> 1000条)
# 模拟企业网关、老旧办公电脑
# ----------------------------------------------------------
def generate_windows_firefox(count=1000):
    uas = set()
    while len(uas) < count:
        ff_ver = generate_ff_ver()
        # 混入少量老旧 Windows NT 6.1 (Win7) 以配合 115 ESR
        os_ver = random.choices(["Windows NT 10.0", "Windows NT 6.1"], weights=[80, 20])[0]
        uas.add(f"Mozilla/5.0 ({os_ver}; Win64; x64; rv:{ff_ver}) Gecko/20100101 Firefox/{ff_ver}")
    return list(uas)

# ----------------------------------------------------------
# 3. Android Firefox (15% -> 600条)
# [核心修复] Android Firefox 真实规范，坚决不带手机 Model
# ----------------------------------------------------------
def generate_android_firefox(count=600):
    uas = set()
    while len(uas) < count:
        android_ver = random.choice([11, 12, 13, 14])
        ff_ver = generate_ff_ver()
        # 真实的 Android Firefox 会抹除机型信息防追踪
        uas.add(f"Mozilla/5.0 (Android {android_ver}; Mobile; rv:{ff_ver}) Gecko/{ff_ver} Firefox/{ff_ver}")
    return list(uas)

# ----------------------------------------------------------
# 4. 降现代化 Chromium 池 (15% -> 600条)
# 模拟老旧安卓 WebView、国内套壳浏览器、老旧 Windows 客户端
# ----------------------------------------------------------
def generate_old_chromium(count=600):
    uas = set()
    mid_end_models = [
        "SM-A546B", "SM-A346B", "SM-M146B", "moto g84 5G", "moto g play", 
        "2312DRA50G", "V2318", "CPH2581"
    ]
    while len(uas) < count:
        platform = random.choices(["windows", "android"], weights=[40, 60])[0]
        chrome_ver = generate_old_chrome()
        
        if platform == "windows":
            os_ver = random.choices(["Windows NT 10.0", "Windows NT 6.1"], weights=[70, 30])[0]
            uas.add(f"Mozilla/5.0 ({os_ver}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_ver} Safari/537.36")
        else:
            android_ver = random.choice([10, 11, 12, 13])
            model = random.choice(mid_end_models)
            uas.add(f"Mozilla/5.0 (Linux; Android {android_ver}; {model}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_ver} Mobile Safari/537.36")
    return list(uas)

# ----------------------------------------------------------
# 5. 少量生态噪声 Safari (10% -> 400条)
# 压低比例，防止 SecureTransport 协议栈严重冲突
# ----------------------------------------------------------
def generate_safari_noise(count=400):
    uas = set()
    while len(uas) < count:
        device = random.choices(["mac", "iphone"], weights=[40, 60])[0]
        safari_webkit = random.choice(["605.1.15", "615.1.26"]) # 老版本 WebKit
        
        if device == "mac":
            mac_major = random.choice([12, 13])
            mac_minor = random.randint(0, 6)
            uas.add(f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_{mac_major}_{mac_minor}) AppleWebKit/{safari_webkit} (KHTML, like Gecko) Version/15.6 Safari/{safari_webkit}")
        else:
            ios_major = random.choice([15, 16])
            ios_minor = random.randint(0, 5)
            uas.add(f"Mozilla/5.0 (iPhone; CPU iPhone OS {ios_major}_{ios_minor} like Mac OS X) AppleWebKit/{safari_webkit} (KHTML, like Gecko) Version/{ios_major}.0 Mobile/15E148 Safari/{safari_webkit}")
    return list(uas)

# ----------------------------------------------------------
# 主程序
# ----------------------------------------------------------
if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    pool = []

    # 精确匹配 4000 条定额的混合战术矩阵
    pool.extend(generate_linux_firefox(1400))    # 35%
    pool.extend(generate_windows_firefox(1000))  # 25%
    pool.extend(generate_android_firefox(600))   # 15%
    pool.extend(generate_old_chromium(600))      # 15%
    pool.extend(generate_safari_noise(400))      # 10%

    # 深度洗牌，打破规律
    random.shuffle(pool)

    # 强制截断，确保绝对的 4000 条输出
    final_pool = pool[:TOTAL_POOL]

    output_file = "data/user_agents.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        for ua in final_pool:
            f.write(ua + "\n")

    print(f"✅ 成功生成 {len(final_pool)} 条大智若愚架构指纹库 (V4.1.0 完美降维版)")
    print(f"📦 输出文件: {output_file}")