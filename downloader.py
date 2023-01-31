import json
import urllib.request
import geopandas as gpd
import pandas as pd
from shapely.geometry import shape, Point
import datetime

latlongs = pd.read_csv('PC.csv')

geometry = [Point(xy) for xy in zip(latlongs.Longitude, latlongs.Latitude)]
geoCases = gpd.GeoDataFrame(latlongs, crs = 'epsg:4326', geometry = geometry)
geoCases = geoCases.reset_index(drop=True)

with urllib.request.urlopen("https://services6.arcgis.com/ubm4tcTYICKBpist/ArcGIS/rest/services/Evacuation_Orders_and_Alerts/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=true&returnCentroid=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=0&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pgeojson&token="
                            ) as url:
    js = json.loads(url.read().decode())

df = pd.DataFrame()

for feature in js['features']:
    polygon = shape(feature['geometry'])
    print(feature['properties']['EVENT_NAME'])
    if polygon.geom_type == 'MultiPolygon':
        for geom in polygon.geoms:
            p = gpd.GeoSeries(geom)
            for i in range(0,len(geoCases)):
                if geom.contains(geoCases['geometry'][i]):
                    df = pd.concat([df,pd.DataFrame([geoCases['POSTCD'][i],feature['properties']['ORDER_ALERT_STATUS'],feature['properties']['EVENT_NAME'],feature['properties']['EVENT_TYPE']]).transpose()],ignore_index=True, axis=0)
                    print(df)
    else:
        p = gpd.GeoSeries(polygon)
        for i in range(0,len(geoCases)):
            if polygon.contains(geoCases['geometry'][i]):
                df = pd.concat([df,pd.DataFrame([geoCases['POSTCD'][i],feature['properties']['ORDER_ALERT_STATUS'],feature['properties']['EVENT_NAME'],feature['properties']['EVENT_TYPE']]).transpose()],ignore_index=True, axis=0)
                print(df)

print(df)

df = df.rename(columns={0:"Postal Code",1:"Order Alert Status",2:"Event Name",3:"Event Type"})

df.to_json("matches.csv")

with open("downloadertracker.txt", "w") as file:
    file.write("ran at: "+str(datetime.datetime.today()))
