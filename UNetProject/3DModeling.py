import vtk

# 定义渲染窗口、交互模式
aRender = vtk.vtkRenderer()
Renwin = vtk.vtkRenderWindow()
Renwin.AddRenderer(aRender)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(Renwin)

# 定义个图片读取接口
# 读取PNG图片就换成PNG_Reader = vtk.vtkPNGReader()
PNG_Reader = vtk.vtkPNGReader()
PNG_Reader.SetNumberOfScalarComponents(1)
PNG_Reader.SetFileDimensionality(2)  # 说明图像是三维的

# 定义图像大小，本行表示图像大小为（512*512*240）
# PNG_Reader.SetDataExtent(0, 256, 0, 256, 0, 19)
PNG_Reader.SetDataExtent(0, 695, 0, 695, 1, 198)
# 设置图像的存放位置
# name_prefix = ['mask/mask_']
name_prefix = ['data/masks/']
PNG_Reader.SetFilePrefix(name_prefix[0])

# 设置图像前缀名字
# 表示图像前缀为数字（如：0.jpg）
PNG_Reader.SetFilePattern("%s%d.png")
PNG_Reader.Update()
PNG_Reader.SetDataByteOrderToLittleEndian()
spacing = [1.0, 1.0, 1.0]  # x, y 方向上的间距为 2 像素，z 方向上的间距为 2.5 像素
PNG_Reader.GetOutput().SetSpacing(spacing)

# 高斯平滑
gauss = vtk.vtkImageGaussianSmooth()
gauss.SetInputConnection(PNG_Reader.GetOutputPort())
gauss.SetStandardDeviations(2.0, 2.0, 2.0)
gauss.SetRadiusFactors(2.0, 2.0, 2.0)
gauss.Update()

# 计算轮廓的方法
contour = vtk.vtkMarchingCubes()
gauss.GetOutput().SetSpacing(spacing)
contour.SetInputConnection(gauss.GetOutputPort())
contour.ComputeNormalsOn()
contour.SetValue(0, 100)

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(contour.GetOutputPort())
mapper.ScalarVisibilityOff()

actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(0.7, 0.8, 1.0)

renderer = vtk.vtkRenderer()
renderer.SetBackground([1.0, 1.0, 1.0])
renderer.AddActor(actor)

window = vtk.vtkRenderWindow()
window.SetSize(512, 512)
window.AddRenderer(renderer)

interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(window)

# 保存STL文件
stl_writer = vtk.vtkSTLWriter()
stl_writer.SetFileName("output_model/output.stl")
stl_writer.SetInputConnection(contour.GetOutputPort())
stl_writer.Write()

# 开始显示
if __name__ == '__main__':
    window.Render()
    interactor.Initialize()
    interactor.Start()
