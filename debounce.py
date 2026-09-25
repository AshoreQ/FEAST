import numpy as np
from util import fixed_length


T_JD = 0.1
T_TAOBAO = 0.12
T_EBAY = 0.1
T_AMAZON = 0.1

def extract_debounce_features(requests,
                                 T       = 0.1,
                                 k       = 20,    # 输出序列固定长度
                                 byte_per_char = 1):
    """
    requests: List[(t:float, size:int)]  已过滤的上行请求
    return: 1D-np.ndarray, shape=(48,)
    """
    if not requests:
        return np.zeros(48, dtype=np.float32)

    # ---------- 1. 相邻请求间隔 ----------
    ts  = [t for t, _ in requests]
    iat = np.diff(ts)                      # shape=(m-1,)
    # 防抖区间：把 > T 的间隔单独拿出来
    debounce_iat = iat[iat > T]
    # 固定长度
    debounce_iat = fixed_length(debounce_iat, k, 0.0)
    # print(debounce_iat)
    # ---------- 2. 防抖次数 / 总间隔比例 ----------
    debounce_cnt = (iat > T).sum()
    debounce_ratio = debounce_cnt / len(iat) if iat.size else 0.0

    # ---------- 3. 每次“合并”字符数 ----------
    sizes = [s for _, s in requests]
    delta = np.diff(sizes)
    chars_per_req = np.round(delta / byte_per_char).astype(int)
    chars_per_req = np.clip(chars_per_req, 0, 15)   # 截断异常值
    chars_per_req = fixed_length(chars_per_req, k, 0)

    # ---------- 4. 合并比例 ----------
    total_chars = chars_per_req.sum()
    req_cnt     = len(requests)
    # 由于防抖，会出现“请求数 < 字符数”
    merge_ratio = max(0.0, 1 - req_cnt / total_chars) if total_chars else 0.0

    # ---------- 5. 防抖间隔的量化误差 ----------
    quant_err = np.mod(debounce_iat, T)
    quant_var = np.var(quant_err) if quant_err.size > 1 else 0.0

    # ---------- 6. 统计特征 ----------
    iat_mean = np.mean(iat) if iat.size else 0.0
    iat_std  = np.std(iat)  if iat.size else 0.0

    # ---------- 7. 拼成 48 维 ----------
    # 0~19: 防抖间隔序列
    # 20~39: 每次合并字符数序列
    # 40~47: 8 个统计量
    stats = np.array([
        quant_var,
        merge_ratio,
        debounce_ratio,
        debounce_cnt,
        iat_mean,
        iat_std,
        np.max(iat)  if iat.size else 0.0,
        np.min(iat)  if iat.size else 0.0
    ], dtype=np.float32)

    return np.hstack([debounce_iat, chars_per_req, stats])


def extract_from_temporal(df, remote_ip, T=0.1, byte_per_char=1, k=20):
    """
    df: temporal_feature.py 返回的 DataFrame
    remote_ip: 搜索引擎 IP 列表（用于过滤上行包）
    return: 1D-array, shape=(48,)
    """
    # 1. 只保留上行请求
    up_df = df[df['dst'].isin(remote_ip)].copy()
    if up_df.empty:
        return np.zeros(48, dtype=np.float32)

    # 2. 构造 (time, size) 列表
    requests = list(zip(up_df['frame_time'], up_df['frame_length']))

    # 3. 复用原逻辑
    return extract_debounce_features(requests, T, k, byte_per_char)