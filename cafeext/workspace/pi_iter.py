#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""逐步计算 π (莱布尼茨级数)，每次迭代输出当前近似值。
用法：
  python3 pi_iter.py [迭代次数] [每次显示多少位小数]
示例：
  python3 pi_iter.py 100 10
"""

import sys
import time


def calculate_pi_leibniz(iterations: int, digits: int = 10):
    """莱布尼茨级数：π/4 = 1 - 1/3 + 1/5 - 1/7 + ...

    每次迭代都打印当前近似值（保留指定小数位）。
    """
    pi_approx = 0.0
    sign = 1
    fmt = f"{{:8d}} | {{:.{digits}f}} | {{:.{digits}f}}"
    header = f"迭代次数 | π 的近似值 (保留{digits}位) | 与真实π的误差"
    print("开始计算 π (莱布尼茨级数)...")
    print(header)
    print("-" * len(header))

    for i in range(iterations):
        term = sign * (4.0 / (2 * i + 1))
        pi_approx += term
        error = abs(pi_approx - 3.141592653589793)
        print(fmt.format(i + 1, pi_approx, error))
        sign = -sign
        # 小延迟，方便观察；可以注释掉以加快速度
        time.sleep(0.05)

    return pi_approx


if __name__ == "__main__":
    iters = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    digs = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    final = calculate_pi_leibniz(iters, digs)
    print()
    print(f"最终结果: π ≈ {final:.{digs}f}")
    print(f"真实π值:   3.141592653589793")
    print(f"最终误差: {abs(final - 3.141592653589793):.{digs}f}")