#根据提取数据绘制中国地图
import pandas as pd
from pyecharts.charts import Map
from pyecharts import options as opts 
from pyecharts.globals import ThemeType #引入主题
import time
localtime = time.asctime( time.localtime(time.time()) )
china_data = pd.read_excel('E:/microsoft_edge_downlonds/Sublime Text3/Sublime Text3_PythonCode/china_prov_data.xlsx') #先读取之前保存的数据
data = pd.DataFrame(china_data[['name', 'total_confirm', 'total_dead', 'total_heal']])
present_confirm = pd.DataFrame(data['total_confirm'][i] - data['total_dead'][i] - data['total_heal'][i] for i in range(data.shape[0]))
present_data = pd.concat([pd.DataFrame(china_data['name']), present_confirm], axis = 1) #按列合并
present_information = present_data.values.tolist()
c = (
    Map(init_opts = opts.InitOpts(width = "1000px", height = "600px", theme = ThemeType.DARK)) #可切换主题
    .set_global_opts(
        title_opts = opts.TitleOpts(title = localtime + " confirmed cases"),
        visualmap_opts = opts.VisualMapOpts(
            min_ = 0,
            max_ = 3000,
            range_text = ['现存确诊人数:', ''],  #分区间
            is_piecewise = True,  #定义图例为分段型，默认为连续的图例
            pos_top = "middle",  #分段位置
            pos_left = "left",
            orient = "vertical",
            split_number = 10  #分成10个区间
        )
    )
    .add("present_confirm", present_information, maptype = "china")
    .render("Map.html")
)