#!/bin/bash
#
# 翰墨精英 (Elite Business) - 华为表盘打包脚本
# 将表盘资源打包为 .hwt 格式文件
#
# 使用方法: ./tools/package.sh
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
WATCHFACE_DIR="$PROJECT_DIR/watchface"
OUTPUT_DIR="$PROJECT_DIR/output"
PACKAGE_NAME="Elite_Business"

echo "============================================"
echo "  翰墨精英 - 华为表盘打包工具"
echo "============================================"

# 检查资源目录
if [ ! -d "$WATCHFACE_DIR/watchface/res" ]; then
    echo "[错误] 资源目录不存在，请先运行 generate_assets.py"
    echo "  python3 tools/generate_assets.py"
    exit 1
fi

if [ ! -f "$WATCHFACE_DIR/description.xml" ]; then
    echo "[错误] description.xml 不存在"
    exit 1
fi

if [ ! -f "$WATCHFACE_DIR/watchface/watch_face_config.xml" ]; then
    echo "[错误] watch_face_config.xml 不存在"
    exit 1
fi

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 清理旧的打包文件
rm -f "$OUTPUT_DIR/${PACKAGE_NAME}.hwt"
rm -f "$OUTPUT_DIR/com.huawei.watchface"

echo ""
echo "[1/4] 检查资源文件..."

# 统计资源文件
TOTAL_FILES=$(find "$WATCHFACE_DIR" -type f | wc -l)
TOTAL_SIZE=$(du -sh "$WATCHFACE_DIR" | cut -f1)
echo "  资源文件数: $TOTAL_FILES"
echo "  总大小: $TOTAL_SIZE"

echo ""
echo "[2/4] 打包为 com.huawei.watchface..."

# 进入 watchface 目录进行打包
cd "$WATCHFACE_DIR"

# 创建 com.huawei.watchface (ZIP格式)
zip -r "$OUTPUT_DIR/com.huawei.watchface" \
    description.xml \
    preview/ \
    watchface/ \
    -x "*.DS_Store" \
    -x "__MACOSX/*" \
    > /dev/null 2>&1

echo "  [OK] com.huawei.watchface 已生成"

echo ""
echo "[3/4] 生成 .hwt 文件..."

# .hwt 本质上就是 zip 文件，改后缀即可
cp "$OUTPUT_DIR/com.huawei.watchface" "$OUTPUT_DIR/${PACKAGE_NAME}.hwt"

echo "  [OK] ${PACKAGE_NAME}.hwt 已生成"

echo ""
echo "[4/4] 验证打包结果..."

# 显示包内容
echo "  包内文件列表:"
unzip -l "$OUTPUT_DIR/${PACKAGE_NAME}.hwt" | head -30

# 检查文件大小
HWT_SIZE=$(stat --format=%s "$OUTPUT_DIR/${PACKAGE_NAME}.hwt" 2>/dev/null || stat -f%z "$OUTPUT_DIR/${PACKAGE_NAME}.hwt" 2>/dev/null)
HWT_SIZE_KB=$((HWT_SIZE / 1024))
HWT_SIZE_MB=$(echo "scale=2; $HWT_SIZE / 1048576" | bc 2>/dev/null || echo "N/A")

echo ""
echo "  文件大小: ${HWT_SIZE_KB} KB (${HWT_SIZE_MB} MB)"

# 华为要求 HWT 包不超过 5MB
if [ "$HWT_SIZE" -gt 5242880 ]; then
    echo "  [警告] HWT文件超过5MB限制！请优化图片资源大小"
else
    echo "  [OK] 文件大小符合华为要求 (< 5MB)"
fi

echo ""
echo "============================================"
echo "  打包完成!"
echo ""
echo "  输出文件:"
echo "    $OUTPUT_DIR/${PACKAGE_NAME}.hwt"
echo "    $OUTPUT_DIR/com.huawei.watchface"
echo ""
echo "  安装方式:"
echo "    1. 将 ${PACKAGE_NAME}.hwt 传输到手机"
echo "    2. 打开华为运动健康 APP"
echo "    3. 进入 设备 > 表盘市场 > 我的"
echo "    4. 选择已下载的表盘文件安装"
echo "============================================"

cd "$PROJECT_DIR"
