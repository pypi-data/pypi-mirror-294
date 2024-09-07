from zhongwen.pandas_tools import show_html, 可顯示
import pandas as pd
from pathlib import Path
from diskcache import Cache
cache = Cache(Path.home() / 'cache' / Path(__file__).stem)

@cache.memoize('載入交通事故案件檔', tag='載入交通事故案件檔')
def 載入交通事故案件檔(xlses=None):
    '傳回座標系TWD97(EPSG:3826：TM2，中央經線121度)之圖資，單位為公尺。'
    from collections.abc import Iterable
    import geopandas as gpd
    if not xlses:
        xlses = [Path(__file__).parent / f'{year}年A1_A2.xlsx' for year in [110, 111, 112]]
    if not isinstance(xlses, Iterable):
        xlses = [xlses]
    df = pd.concat([pd.read_excel(f, header=4 ,dtype={'1.發生時間':str}) for f in xlses])
    df = df.rename(columns=lambda s: s.strip())
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['GPS經度'], df['GPS緯度']), crs='epsg:4326')
    # gdf = gdf.to_crs(epsg=3826)
    return gdf

def 交通事故死亡資料():
    df = 載入交通事故案件檔()
    df['當事者死亡'] = df['22.受傷程度'].str.contains("死亡")
    df['發生年度'] = df.發生年度-1911
    df['當事者事故發生時年齡'] = pd.to_numeric(df.當事者事故發生時年齡, errors='coerce')
    df = df.query('當事者死亡')
    年齡分類 = [0, 13, 18, 25, 30, 45, 65, float('inf')]
    年齡標籤 = ["兒童", "少年", "年輕人", "成年期", "壯年期", "中年期","高齡者"]
    df["年齡層"] = pd.cut(df.當事者事故發生時年齡, bins=年齡分類, labels=年齡標籤, right=False)
    return df

def 交通事故高齡者死亡使用運具統計():
    df = 交通事故死亡資料()
    df = df.rename(columns={"26.當事者區分(類別)":"車種"})
    df = df.query('年齡層=="高齡者"')
    df = df.groupby(["發生年度", '車種'])[["總編號(案件編號)"]].count()
    df = df.unstack(level=-1).fillna(0).astype(int)
    return df

def 交通事故各年度各年齡層死亡人數統計():
    import pandas as pd
    df = 交通事故死亡資料()
    df = df.groupby(['發生年度', '年齡層'])[["總編號(案件編號)"]].count()
    df = df.unstack(level=-1)
    return df


def 交通事故高齡者死亡人數():
    df = 載入交通事故案件檔()
    df['發生年度'] = df.發生年度-1911
    df['死亡人數'] = pd.to_numeric(df['3-1.24小時內死亡人數'], errors='coerce').fillna(0) + pd.to_numeric(df['3-2.2-30日內死亡人數'], errors='coerce').fillna(0)
    df['當事者事故發生時年齡'] = pd.to_numeric(df.當事者事故發生時年齡, errors='coerce')
    df['高齡者'] = df.當事者事故發生時年齡>=65
    df['當事者死亡'] = df['22.受傷程度'].str.contains("死亡")
    # print(df.columns.tolist())
    df = df.query('高齡者 and 當事者死亡')
    df = df.rename(columns={"2-1.發生市區鄉鎮":"發生市區鄉鎮"})
    
    df = df.groupby(['發生市區鄉鎮', '發生年度'])[['當事者順位']].count()
    df = df.rename(columns={"當事者順位":"高齡者死亡人數"})
    df = df.unstack(level=-1).fillna(0).astype(int)
    df = df.sort_values([('高齡者死亡人數', 112)], ascending=False)
    return df


def 高齡者事故防制安全推廣情形():
    df = 載入交通事故案件檔()
    df['當事者事故發生時年齡'] = pd.to_numeric(df.當事者事故發生時年齡, errors='coerce')
    df['高齡者'] = df.當事者事故發生時年齡>=65
    # print(df.columns.tolist())
    df = df.query('高齡者==True')
    df = df.groupby(['2-1.發生市區鄉鎮', '發生年度', '事故類別'])['總編號(案件編號)'].count()
    df = df.unstack(level=-1).unstack(level=-1).fillna(0)
    df = df.sort_values([('A1', 2023), ('A2', 2023)], ascending=[False, False])

    f = Path(__file__).parent.parent / '高齡者交通事故防制措施' / '高齡者宣導情形.xlsx'
    df2 = pd.read_excel(f)
    df2['宣導'] = '宣導次數'
    df2 = df2.groupby(['鄉鎮市', '年度', '宣導']).序號.count().unstack(level=-1).unstack(level=-1)
    df2 = df2.fillna(0)
    df = pd.concat([df, df2], axis=1)
    df = df.fillna(0)
    return df

def 交通事故類別分析():
    df = 載入交通事故案件檔()
    df = df[['總編號(案件編號)', '發生年度', '事故類別']].drop_duplicates()
    df = df.groupby(['發生年度', '事故類別'])[['總編號(案件編號)']].count()
    df = df.rename(columns={'總編號(案件編號)':'件數'})
    df = df.unstack()
    return df

def 交通事故死亡人數統計():
    df = 載入交通事故案件檔()
    df['死亡人數'] = pd.to_numeric(df['3-1.24小時內死亡人數'], errors='coerce').fillna(0) + pd.to_numeric(df['3-2.2-30日內死亡人數'], errors='coerce').fillna(0)
    df = df[['總編號(案件編號)', '發生年度', '死亡人數']].drop_duplicates()
    df = df.groupby('發生年度').死亡人數.sum().astype(int)
    return df

@可顯示
def 交叉路口案件():
    'crs為epsg:3826'
    import geopandas as gpd
    gdf = 載入交通事故案件檔()
    gdf = gdf.query('地址類型=="交叉路口"')
    def 取路口名(r):
        from zhongwen.text import 是否為空白字串
        n = r['2-1.發生市區鄉鎮']
        rn1 = r['2-1.發生地址_路街']
        postfix = ['段', '巷', '弄']
        for i, cn in enumerate(['2-1.發生地址_段', '2-1.發生地址_巷', '2-1.發生地址_弄']):
            try:
                if 是否為空白字串(r[cn]):
                    continue
            except AttributeError:pass
            rn1 += f'{r[cn]}{postfix[i]}'

        rn2 = r['2-1.發生交叉路口_路街口']
        for i, cn in enumerate(['2-1.發生交叉路口_段', '2-1.發生交叉路口_巷', '2-1.發生交叉路口_弄']):
            try:
                if 是否為空白字串(r[cn]):
                    continue
            except AttributeError:pass
            rn2 += f'{r[cn]}{postfix[i]}'
        n += '與'.join(sorted([rn1, rn2]))
        return n

    gdf['路口名'] = gdf.apply(取路口名, axis=1)
    gdf = gdf[['路口名', '34.初步分析研判子類別-主要', '發生年度'
              ,'總編號(案件編號)'
              ,'3-1.24小時內死亡人數', '3-2.2-30日內死亡人數', '3-2.受傷人數'
              ,'GPS經度', 'GPS緯度'
              ]]
    gdf = gdf.groupby(['路口名', '34.初步分析研判子類別-主要', '發生年度', '總編號(案件編號)','GPS經度', 'GPS緯度']).sum()
    gdf['3-1.24小時內死亡人數'] = pd.to_numeric(gdf['3-1.24小時內死亡人數'], errors='coerce').fillna(0)
    gdf['3-2.2-30日內死亡人數'] = pd.to_numeric(gdf['3-2.2-30日內死亡人數'], errors='coerce').fillna(0)
    gdf['死亡人數'] = gdf['3-1.24小時內死亡人數'] + gdf['3-2.2-30日內死亡人數']
    gdf['3-2.受傷人數'] = pd.to_numeric(gdf['3-2.受傷人數'], errors='coerce').fillna(0)
    gdf = gdf.reset_index().drop_duplicates()
    gdf = gpd.GeoDataFrame(gdf, geometry=gpd.points_from_xy(gdf['GPS經度'], gdf['GPS緯度']), crs='epsg:4326')
    gdf = gdf.to_crs(epsg=3826)
    gdf = gdf.rename(columns={'3-2.受傷人數':'受傷人數', '34.初步分析研判子類別-主要':'主要肇事原因'
        ,'總編號(案件編號)':'案件編號'
        })
    return gdf

def 交通事故各年度各年齡層使用運具死亡人數統計():
    import pandas as pd
    df = 交通事故死亡資料().query('發生年度==112')
    df = df.rename(columns={"26.當事者區分(類別)":"車種"})
    df = df.groupby(['年齡層', '車種'])[["總編號(案件編號)"]].count()
    df = df.unstack(level=-1)
    return df


if __name__ == '__main__':
    from zhongwen.pandas_tools import show_html
    import sys
    df = 交通事故各年度各年齡層使用運具死亡人數統計()
    show_html(df)
    # df = 交叉路口案件(顯示=True)
    # print(df.columns.tolist())
    # show_html(df)
    # sys.exit()
    # df = df.groupby(['路口名', '發生年度']).agg({'總編號(案件編號)':'count'
                                    # ,'死亡人數':sum
                                    # ,'3-2.受傷人數':sum
                                    # }).rename(columns={'總編號(案件編號)':'事故數'})
    # df['路口件數'] = df.groupby('路口名')['事故數'].transform(sum)
    # df = df.sort_values(['路口件數', '發生年度'], ascending=[False, True])
