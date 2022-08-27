# AbsDrawer 抽象画生成器

一个生成抽象画的Python脚本。按空格生成下一张图，按s保存大图。Picture文件夹里有一些示例。

A Python script which generates abstract drawings. Press space to generate the next figure, and press s to save a larger picture. There are some pictures in folder 'Picture'.

![](https://raw.githubusercontent.com/Mario-Hero/AbsDrawer/main/Picture/pic-27.jpg)

## 依赖 Depedency

Python 3

opencv, PIL, tkinter (如果未安装，该脚本会自动安装)

## 原理 My way

生成随机数量的圆、线条、长方形，并随机施加阴影。

Generate a random number of circles, lines and rectangles, and apply shadows randomly.

## 简单用法 Usage

按空格生成下一张图，如果觉得喜欢，就可以按s保存大图，图片会保存在当前文件夹。

Press the space to generate the next picture. If you like it, you can press s to save the large picture. The picture will be saved in the current folder.

## 参数 Parameters

canvasWidth: 显示图片宽度

canvasHeight: 显示图片高度

LARGER_FACTOR: 实际导出图片放大倍数



canvasWidth: resolutionX to show

canvasHeight: resolutionY to show

LARGER_FACTOR: resolution to export is [LARGER_FACTOR] times of resolution to show

## License

The project is released under MIT License.