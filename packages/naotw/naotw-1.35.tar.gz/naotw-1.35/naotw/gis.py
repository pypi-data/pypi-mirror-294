'GIS 工具模組'

def 取路口(查詢地點=None):
    '取開放街圖路口'
    import osmnx as ox
    import geopandas as gpd

    # 指定花蓮市的位置名稱
    place_name = "Hualien City, Taiwan"

    # 從 OpenStreetMap 下載花蓮市的道路網絡數據
    G = ox.graph_from_place(place_name, network_type='drive')

    # 提取路口 (交叉點) 的資料
    nodes, edges = ox.graph_to_gdfs(G, nodes=True, edges=True)

    # 篩選出具有多個連接道路的路口 (即交叉點)
    intersections = nodes[nodes['street_count'] > 1]

    def get_intersection_name(node, G):
        "根據路口連接的道路名稱推測路口名稱"
        street_names = set()
        for u, v, key, data in G.edges(node, keys=True, data=True):
            if 'name' in data:
                street_names.add(str(data['name']))
        return "".join(sorted(street_names))

    # 對每個路口推測名稱
    intersections['name'] = intersections.index.map(lambda node: get_intersection_name(node, G))
    return intersections

def tokml(geojson_or_shape):
    '第一個欄位為資料夾(為目的分類)，第二個欄位為識別碼(如地號)，其餘欄位為說明'
    from shapely.geometry.point import Point
    from pathlib import Path
    import geopandas as gpd
    import simplekml
    gdf = gpd.read_file(geojson_or_shape)
    gdf = gdf.to_crs(epsg=4326) # kml crs is epsg 4326
    kml = simplekml.Kml()
    for f in gdf.iloc[:,0].drop_duplicates():
        fol = kml.newfolder(name=f)
        ls = gdf.query(f'{gdf.columns[0]}==@f')
        for i, l in ls.iterrows():
            圖徵說明 = '<br/>'.join(
                f'<h>{c}</h>：{l[c]}' for c in l.index if c != 'geometry') 
            landid = l.iloc[1]
            geometry = l['geometry']
            if isinstance(geometry, Point):
                fol.newpoint(
                     name=landid,
                     coords=[(geometry.x, geometry.y)],
                     description=圖徵說明
                     )
                continue
            try:
                #Polygon
                coords = list(geometry.exterior.coords)
            except:
                #MultiPolygon
                coords = [list(x.exterior.coords) for x in geometry.geoms]
            finally:
                圖徵說明 = '<br/>'.join(
                    f'<h>{c}</h>：{l[c]}' for c in l.index if c != 'geometry')
                fol.newpolygon(
                     name=landid,
                     outerboundaryis=coords, 
                     innerboundaryis=[], 
                     description=圖徵說明
                     )
    geojson_or_shape = Path(geojson_or_shape )
    kml.save(geojson_or_shape.with_suffix('.kml'))

def to_kml(gdf, k, name_column=None, folder_column=None, descs=None, folder_column2=None):
    from shapely.geometry.point import Point
    import simplekml

    gdf = gdf.to_crs(epsg=4326) # kml crs is epsg 4326
    kml = simplekml.Kml()
    if folder_column:
        if folder_column2:
            for f in gdf[folder_column].drop_duplicates():
                fol = kml.newfolder(name=f)
                gdf2 = gdf.query(f'{folder_column}==@f')
                for f2 in gdf2[folder_column2].drop_duplicates():
                    fol2 = fol.newfolder(name=f2)
                    ls = gdf2.query(f'{folder_column2}==@f2')
                    for i, l in ls.iterrows():
                        #print(l)
                        landid = l[name_column]
                        geometry = l['geometry']
                        if isinstance(geometry, Point):
                            fol2.newpoint(
                                 name=landid,
                                 coords=[(geometry.x, geometry.y)]
                                 #description=str(l[descs])
                                 )
                            continue
                        try:
                            #Polygon
                            coords = list(geometry.exterior.coords)
                        except:
                            #MultiPolygon
                            coords = [list(x.exterior.coords) for x in geometry.geoms]
                        finally:
                            fol2.newpolygon(
                                 name=landid,
                                 outerboundaryis=coords, 
                                 innerboundaryis=[], 
                                 description=str(l[descs])
                                 )
    else:
        for f in gdf[folder_column].drop_duplicates():
            fol = kml.newfolder(name=f)
            ls = gdf.query(f'{folder_column}==@f')
            #print(ls)
            for i, l in ls.iterrows():
                #print(l)
                landid = l[name_column]
                geometry = l['geometry']
                if isinstance(geometry, Point):
                    fol.newpoint(
                         name=landid,
                         coords=[(geometry.x, geometry.y)]
                         #description=str(l[descs])
                         )
                    continue
                try:
                    #Polygon
                    coords = list(geometry.exterior.coords)
                except:
                    #MultiPolygon
                    coords = [list(x.exterior.coords) for x in geometry.geoms]
                finally:
                    fol.newpolygon(
                         name=landid,
                         outerboundaryis=coords, 
                         innerboundaryis=[], 
                         description=str(l[descs])
                         )
    kml.save(k)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--file2kml"
                       ,help="地理圖資轉換成KML檔。"
                       ,required=False
                       )
    args = parser.parse_args()
    if args.file2kml:
        tokml(args.file2kml)
