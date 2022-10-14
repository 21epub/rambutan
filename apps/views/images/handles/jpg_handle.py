from io import BytesIO

from PIL import Image, ImageOps

mime_type = {"jpeg": "image/jpeg", "png": "image/png"}


def _get_mime_type(format) -> str:
    return mime_type.get(format.lower())


class ImageProcessor(object):
    def __init__(self, fd, **kwargs):
        _im = Image.open(BytesIO(fd), mode="r")
        self.im = ImageOps.exif_transpose(_im)
        # 原始图片的宽度、长度
        self.origin_width, self.origin_heigth = self.im.size

    def get_format(self):
        return self.im.format

    def resize(self, size=tuple()) -> Image.Image:
        self.im.thumbnail(size)
        return self.im

    @classmethod
    def output(cls, im, format="JPEG", quality=85) -> tuple:
        if not isinstance(im, Image.Image):
            raise
        fd = BytesIO()
        _format = format
        im.save(fd, format=_format, quality=quality)
        content = fd.getvalue()
        fd.close()
        return content, _get_mime_type(_format)

    # 裁剪入口
    def crop_with_param(self, crop_str, ignore_error=False, quality=85):
        box = self.parse_param(crop_str)
        # 裁剪
        im_crop = self.im.crop(box)
        # 保存
        try:
            fd = BytesIO()
            _format = self.im.format
            im_crop.save(fd, format=_format, quality=quality)
            content = fd.getvalue()
            fd.close()
            return content, _get_mime_type(_format)
        except:
            # todo 异常处理
            if ignore_error:
                return
            raise

    def parse_param(self, crop_str):
        """
        :param crop_str: 裁剪表达式(https://developer.qiniu.com/dora/8256/tailoring)
        :return:
        """
        box = [0, 0, self.origin_width, self.origin_heigth]
        if not crop_str:
            return box
        # 裁剪操作参数表(cropsize)
        # 参数名称                      说明
        # /crop/<Width>x               指定目标图片宽度，高度不变。取值范围为0-10000。
        # /crop/x<Height>              指定目标图片高度，宽度不变。取值范围为0-10000。
        # /crop/<Width>x<Height>	   同时指定目标图片宽高。取值范围为0-10000。
        # /ignore-error/<ignoreError>  取值为 1 时，则处理失败时返回原图；取值为 0 时，则处理失败时返回错误信息。默认值为 0。

        # 裁剪偏移参数表 (cropoffset)
        # 参数名称                        说明
        # /crop/!{cropsize}a<dx>a<dy>    相对于偏移锚点，向右偏移dx个像素，同时向下偏移dy个像素。取值范围不限，小于原图宽高即可。
        # /crop/!{cropsize}-<dx>a<dy>    相对于偏移锚点，从指定宽度中减去dx个像素，同时向下偏移dy个像素。取值范围不限，小于原图宽高即可。
        # /crop/!{cropsize}a<dx>-<dy>    相对于偏移锚点，向右偏移dx个像素，同时从指定高度中减去dy个像素。取值范围不限，小于原图宽高即可。
        # /crop/!{cropsize}-<dx>-<dy>    相对于偏移锚点，从指定宽度中减去dx个像素，同时从指定高度中减去dy个像素。取值范围不限，小于原图宽高即可。

        # 偏移处理
        if crop_str.startswith("!"):
            return self.parse_offset_param(crop_str.lstrip("!"), box)
        return self.parse_not_offset_param(crop_str, box)

    def parse_not_offset_param(self, crop_str, box):
        # <Width>x  300x 数值开头，x结尾
        if crop_str.startswith("x"):
            width = int(crop_str.lstrip("x"))
            box[3] = self.get_width(width)
            return box

        if crop_str.endswith("x"):
            height = int(crop_str.rstrip("x"))
            box[2] = self.get_heigth(height)
            return box

        # 坐标
        axis = crop_str.split("x")
        # x<Height>  x300 x开头，数值结尾
        if len(axis) != 2:
            raise Exception(f"裁剪参数错误{crop_str}")
        box[2] = self.get_width(int(axis[0]))
        box[3] = self.get_heigth(int(axis[1]))
        return box

    def parse_offset_param(self, crop_str, box):
        # 裁剪偏移参数表 (cropoffset)
        # 参数名称                        说明
        # /crop/!{cropsize}a<dx>a<dy>    相对于偏移锚点，向右偏移dx个像素，同时向下偏移dy个像素。取值范围不限，小于原图宽高即可。
        # /crop/!{cropsize}-<dx>a<dy>    相对于偏移锚点，从指定宽度中减去dx个像素，同时向下偏移dy个像素。取值范围不限，小于原图宽高即可。
        # /crop/!{cropsize}a<dx>-<dy>    相对于偏移锚点，向右偏移dx个像素，同时从指定高度中减去dy个像素。取值范围不限，小于原图宽高即可。
        # /crop/!{cropsize}-<dx>-<dy>    相对于偏移锚点，从指定宽度中减去dx个像素，同时从指定高度中减去dy个像素。取值范围不限，小于原图宽高即可。

        # /crop/!300x400a10a10 表示从源图坐标为 x:10,y:10 处截取 300x400 的子图片。
        # /crop/!300x400-10a10 表示从源图坐标为 x:0,y:10 处截取 290x400 的子图片。

        # a 出现两次 （第一种情况）
        if crop_str.count("a") == 2:
            cropsize = crop_str.split("a")
            if len(cropsize) != 3:
                raise Exception(f"裁剪参数错误{crop_str}")
            # 调整图片大小
            box = self.parse_not_offset_param(cropsize[0], box)
            # a表示偏移，大小固定
            adx, ady = int(cropsize[1]), int(cropsize[2])
            # 整体移动
            new_box = [box[0] + adx, box[1] + ady, box[2] + adx, box[3] + ady]
            return new_box
        # - 出现两次 （第四种情况）
        if crop_str.count("-") == 2:
            cropsize = crop_str.split("-")
            if len(cropsize) != 3:
                raise Exception(f"裁剪参数错误{crop_str}")
            # 调整图片大小
            box = self.parse_not_offset_param(cropsize[0], box)
            # - 相对于偏移锚点，从指定宽度中减去dx个像素，同时从指定高度中减去dy个像素。取值范围不限，小于原图宽高即可。
            # - 表示减去像素，位置不变
            dx, dy = int(cropsize[1]), int(cropsize[2])
            box[2] = box[2] - dx
            box[3] = box[3] - dy
            return box
        # 只出现一次a
        if crop_str.count("a") == 1 and crop_str.count("-") == 0:
            cropsize = crop_str.split("a")
            if len(cropsize) != 2:
                raise Exception(f"裁剪参数错误{crop_str}")
            # 调整图片大小
            box = self.parse_not_offset_param(cropsize[0], box)
            # a表示偏移，大小固定
            adx = int(cropsize[1])
            # 整体移动
            new_box = [box[0] + adx, box[1], box[2] + adx, box[3]]
            return new_box

        # a、- 各出现一次 （（第二、三种情况））
        if crop_str.count("-") == 1 and crop_str.count("a") == 1:
            # 查看 a出现位置， - 出现位置
            if crop_str.index("a") < crop_str.index("-"):
                # 300x400a10-10
                cropsize = crop_str.split("a")
                # 调整图片大小
                box = self.parse_not_offset_param(cropsize[0], box)

                adx, dy = cropsize[1].split("-")
                box[0] = box[0] + int(adx)
                box[2] = box[2] + int(adx)

                box[1] = box[1] - int(dy)
                box[3] = box[3] - int(dy)
            else:
                # 300x400-10a10
                cropsize = crop_str.split("-")
                # 调整图片大小
                box = self.parse_not_offset_param(cropsize[0], box)

                dx, ady = cropsize[1].split("a")
                box[0] = box[0] - int(dx)
                box[2] = box[2] - int(dx)

                box[1] = box[1] + int(ady)
                box[3] = box[3] + int(ady)

    def crop(self, width=0, height=0, dx=0, dy=0, ignore_error=True, name=0):
        """
        :param width: 裁剪后的宽度
        :param height: 裁剪的高度
        :param dx: 裁剪偏移-向右偏移dx个像素
        :param dy: 向左偏移dx个像素
        :param ignore_error:
        :return:
        """

        box = [0, 0, self.origin_width, self.origin_heigth]  # 650(长)400（高）

        # 向右偏移
        box[0] = self.get_dx(dx)
        # 向下偏移
        box[1] = self.get_dy(dy)

        # 宽度
        box[2] = self.get_width(width)
        # 高度
        box[3] = self.get_heigth(height)

        # 裁剪
        im_crop = self.im.crop(box)
        # 保存
        try:
            if name:
                im_crop.save(f"{name}.png")
            else:
                im_crop.save(f"{box[0]}_{box[1]}_{box[2]}_{box[3]}.png")
        except:
            if ignore_error:
                return
            raise

    def get_width(self, width):
        if width and width < self.origin_width:
            return width
        return self.origin_width

    def get_heigth(self, height):
        if height and height < self.origin_heigth:
            return height
        return self.origin_heigth

    def get_dx(self, dx):
        # todo 偏移量大于最大宽度
        if not dx or dx < 0:
            return 0
        return dx

    def get_dy(self, dy):
        # todo 偏移量大于最大高度
        if not dy or dy < 0:
            return 0
        return dy
