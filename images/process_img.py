import os
from PIL import Image

# ===================== 【这里是你需要修改的2个配置项，其他不用动】 =====================
INPUT_FOLDER = "/home/zhangao/hexo/blog/source/images/post_img_raw"  # 待处理的图片文件夹，复制你的文件夹路径粘贴到这里
OUTPUT_FOLDER = "/home/zhangao/hexo/blog/source/images/post_img"  # 处理完的图片保存路径，自动创建该文件夹
# =====================================================================================

# 目标尺寸：Fluid主题最佳封面尺寸
TARGET_WIDTH = 400
TARGET_HEIGHT = 200
# 目标宽高比 2:1
TARGET_RATIO = TARGET_WIDTH / TARGET_HEIGHT

def process_image(img_path, save_path):
    """处理单张图片：先居中裁剪2:1比例 → 再缩放至1200*600"""
    try:
        # 打开图片，忽略图片的EXIF旋转信息（避免部分图片旋转错位）
        with Image.open(img_path) as img:
            # 转为RGB格式，解决png透明背景/通道问题
            img = img.convert("RGB")
            img_width, img_height = img.size
            img_ratio = img_width / img_height

            # ========== 核心步骤1：按2:1比例 裁剪图片正中间的区域 ==========
            if img_ratio > TARGET_RATIO:
                # 图片太宽 → 左右裁剪，高度不变，取中间
                new_width = int(img_height * TARGET_RATIO)
                crop_left = (img_width - new_width) // 2
                crop_box = (crop_left, 0, crop_left + new_width, img_height)
            elif img_ratio < TARGET_RATIO:
                # 图片太高 → 上下裁剪，宽度不变，取中间
                new_height = int(img_width / TARGET_RATIO)
                crop_top = (img_height - new_height) // 2
                crop_box = (0, crop_top, img_width, crop_top + new_height)
            else:
                # 图片刚好是2:1比例，无需裁剪
                crop_box = None

            # 执行裁剪
            if crop_box:
                img_cropped = img.crop(crop_box)
            else:
                img_cropped = img

            # ========== 核心步骤2：将裁剪后的图片缩放至 1200*600 ==========
            img_resized = img_cropped.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)
            
            # 保存图片，质量95%（清晰且体积小，适配博客加载）
            img_resized.save(save_path, quality=95, optimize=True)
            print(f"✅ 处理成功：{os.path.basename(img_path)} → {os.path.basename(save_path)}")
            
    except Exception as e:
        print(f"❌ 处理失败：{os.path.basename(img_path)}，错误信息：{str(e)}")

def batch_process_images():
    """批量处理文件夹内所有图片"""
    # 创建输出文件夹，如果不存在的话
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        print(f"📂 创建输出文件夹：{OUTPUT_FOLDER}")

    # 支持的图片格式
    SUPPORT_FORMATS = ('.jpg', '.jpeg', '.png', '.webp')
    
    # 遍历文件夹内所有文件
    file_list = os.listdir(INPUT_FOLDER)
    img_count = 0
    for file_name in file_list:
        # 过滤非图片文件
        if file_name.lower().endswith(SUPPORT_FORMATS):
            img_count += 1
            img_input_path = os.path.join(INPUT_FOLDER, file_name)
            # 拼接保存路径，文件名不变
            img_output_path = os.path.join(OUTPUT_FOLDER, file_name)
            # 处理单张图片
            process_image(img_input_path, img_output_path)

    print("\n====================================")
    if img_count == 0:
        print("⚠️  文件夹内未找到任何支持的图片文件！")
    else:
        print(f"🎉 全部处理完成！共处理 {img_count} 张图片，保存至：{OUTPUT_FOLDER}")

if __name__ == "__main__":
    batch_process_images()