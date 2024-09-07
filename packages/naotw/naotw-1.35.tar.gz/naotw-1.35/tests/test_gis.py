import unittest

class Test(unittest.TestCase):
    def test(self):
        from naotw.gis import tokml
        from zhongwen.pandas_tools import show_html
        from pathlib import Path
        import geopandas as gpd
        geojson = Path(__file__).parent / '農地光電.geojson'
        gdf = gpd.read_file(geojson)
        tokml(geojson)
        # show_html(gdf)
    def test_plot(self):
        from zhongwen.pandas_tools import show_html
        from pathlib import Path
        import matplotlib.pyplot as plt
        import geopandas as gpd
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei'] 
        gdf = gpd.read_file(Path(__file__).parent / "花蓮路口.gpkg", driver="GPKG")

        # 創建圖形
        fig, ax = plt.subplots()

        # 繪製點
        gdf.plot(ax=ax, color='black', markersize=50)

        # 標註名稱
        for x, y, label in zip(gdf.geometry.x, gdf.geometry.y, gdf['name']):
            ax.annotate(f'{label}路口', xy=(x, y), xytext=(3, 3), textcoords="offset points")

        # 顯示圖形
        plt.show()
 

    def test_osm(self):
        from naotw.交通事故分析 import 載入交通事故案件檔, cache
        from zhongwen.pandas_tools import show_html
        from pathlib import Path
        import geopandas as gpd
        intersections = gpd.read_file(Path(__file__).parent / "花蓮路口.gpkg", driver="GPKG")
        show_html(intersections)
        # cache.clear()
        # gdf_accidents = 載入交通事故案件檔(Path(__file__).parent / '112年A1_A2.xlsx')

        # 將路口資料設為正確的坐標參考系 (與交通事件資料相同)
        # intersections.crs = gdf_accidents.crs

        # 將交通事件與最近的路口進行空間連接
        # gdf_joined = gpd.sjoin_nearest(gdf_accidents, intersections, how='left', distance_col='distance_to_intersection')

        # 計算每個路口的交通事件數量
        # intersection_accident_count = gdf_joined.groupby('index_right').size()

        # 將事件數量合併回路口資料中
        # intersections['accident_count'] = intersections.index.map(intersection_accident_count.get).fillna(0).astype(int)

        # 顯示包含事件數量的路口資料
        # print(intersections[['name', 'accident_count', 'geometry']].head())
        # show_html(gdf_joined)

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    # unittest.main()
    suite = unittest.TestSuite()
    suite.addTest(Test('test_plot'))  # 指定測試
    unittest.TextTestRunner().run(suite)
