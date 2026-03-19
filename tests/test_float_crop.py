"""
测试浮点数裁剪参数
用于验证 fix: 使用四舍五入处理浮点数裁剪参数

运行: python3 tests/test_float_crop.py
"""
import sys
sys.path.insert(0, 'apps/views/images/handles')

from jpg_handle import ImageProcessor
from PIL import Image
from io import BytesIO


def create_test_image(width=1000, height=1000):
    """创建测试图片"""
    img = Image.new('RGB', (width, height), color='red')
    buf = BytesIO()
    img.save(buf, 'JPEG')
    buf.seek(0)
    return buf.read()


def test_float_crop_params():
    """测试浮点数裁剪参数"""
    content = create_test_image()
    processor = ImageProcessor(content)
    
    test_cases = [
        # (参数, 预期结果说明)
        ('315.7x315.7', '浮点数宽高'),
        ('!315.7xa315.7', '浮点数带偏移'),
        ('x315.7', '仅浮点数高度'),
        ('315.7x', '仅浮点数宽度'),
        ('!200xa1200', '正常整数参数'),
        ('100x100', '标准整数参数'),
    ]
    
    print("=" * 60)
    print("测试浮点数裁剪参数")
    print("=" * 60)
    
    all_passed = True
    for crop_str, desc in test_cases:
        try:
            box = processor.parse_param(crop_str)
            print(f"✅ {crop_str:20s} -> {desc:15s} -> box: {box}")
        except Exception as e:
            print(f"❌ {crop_str:20s} -> {desc:15s} -> 错误: {e}")
            all_passed = False
    
    print("=" * 60)
    if all_passed:
        print("✅ 所有测试通过!")
    else:
        print("❌ 有测试失败!")
    print("=" * 60)
    
    return all_passed


def test_rounding():
    """测试四舍五入具体值"""
    test_values = [
        ('315.7', 316),
        ('315.3', 315),
        ('0.4', 0),
        ('0.5', 0),  # Python round 对 0.5 偶数舍入
        ('0.6', 1),
        ('100.1', 100),
        ('100.9', 101),
    ]
    
    print("\n" + "=" * 60)
    print("测试四舍五入")
    print("=" * 60)
    
    all_passed = True
    for value, expected in test_values:
        result = int(round(float(value)))
        status = "✅" if result == expected else "❌"
        print(f"{status} round({value}) = {result} (expected: {expected})")
        if result != expected:
            all_passed = False
    
    print("=" * 60)
    return all_passed


if __name__ == '__main__':
    test1 = test_float_crop_params()
    test2 = test_rounding()
    
    if test1 and test2:
        print("\n🎉 所有测试验证通过!")
        sys.exit(0)
    else:
        print("\n💥 有测试失败!")
        sys.exit(1)
