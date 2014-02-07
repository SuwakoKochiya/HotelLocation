import web
import json, uuid
import os, shutil, sys


sys.path.append(os.path.dirname(__file__))

from string import Template

web.config.debug = True


class index:
    def GET(self):
        title = session.uuid
        #create isolated files in session
        src_path = mapdir
        dst_path = os.path.join(mapdir, session.uuid)
        out_map_path = os.path.join(dst_path, 'template.map')
        if not os.path.exists(os.path.join(mapdir, session.uuid)):
            os.mkdir(os.path.join(mapdir, session.uuid))
            src_files = filter(lambda p: str.startswith(p, 'grid_final_in4') or p == "stat.txt", os.listdir(mapdir))
            src_files_path = map(os.path.join, [src_path]*len(src_files), src_files)
            dst_files_path = map(os.path.join, [dst_path]*len(src_files), src_files)
            map(shutil.copyfile, src_files_path, dst_files_path)
            #Set session based path for mapfile
            tpl_in = open(os.path.join(mapdir, 'template.map.tpl'))
            map_tpl = Template(tpl_in.read())
            out_map = open(out_map_path, 'w')
            out_map.write(map_tpl.safe_substitute(layerpath=os.path.join(dst_path, 'grid_final_in4'), mappath=out_map_path))
            out_map.close()
            tpl_in.close()
        #Render the map
        value_param = json.dumps({'map': out_map_path,
                                'layers': 'grid_final_in4',
                                'crs': "EPSG:32650",
                                #'transparent': "True"
                                })
        road_param = json.dumps({'map': out_map_path,
                                'layers': 'Road_region_shp',
                                'crs': "EPSG:32650",
                                'transparent': "True"
                                })
        subway_param = json.dumps({'map': out_map_path,
                                'layers': 'subwaystation_font_point_shp',
                                'crs': "EPSG:32650",
                                'transparent': "True"
                                })
        restaurant_param = json.dumps({'map': out_map_path,
                                'layers': 'restaurant_point_shp',
                                'crs': "EPSG:32650",
                                'transparent': "True"
                                })
        hotel_param = json.dumps({'map': out_map_path,
                                'layers': 'hotelproj',
                                'crs': "EPSG:32650",
                                'transparent': "True"
                                })
        #create chart
        stat = open(os.path.join(dst_path, 'stat.txt'), 'r')
        line = stat.readline()
        chart_value = json.loads(line)
        stat.close()
        #assert len(chart_value) == 5
        chart_param = json.dumps([['Probilities', 'Value'],
                    ['0.0-0.2', chart_value[0]],
                    ['0.2-0.4', chart_value[1]],
                    ['0.4-0.6', chart_value[2]],
                    ['0.6-0.8', chart_value[3]],
                    ['0.8-1.0', chart_value[4]]])
        #chart_param = chart_value
        import back_logic
        model_param = json.dumps(back_logic.ModelParam.getValue())
        return render.index(title, road_param, value_param, chart_param, subway_param, restaurant_param, hotel_param, model_param)

class calculate:    
    def POST(self):
        import back_logic
        dst_path = os.path.join(mapdir, session.uuid)
        out_report_path = os.path.join(dst_path, 'report.pdf')        
        shp_path = os.path.join(mapdir, session.uuid, 'grid_final_in4.shp')
        i = web.input()
        p = back_logic.Worker(session)
        if i.has_key("report") and int(i.report) == 1:
            p.Report(int(i.starrate), int(i.lbeds), float(i.diver), int(i.ownership), int(i.model), shp_path)
            url = "http://www.hotel-location.net/maps/%s/report.pdf" % session.uuid
            raise web.redirect(url)
        p.Calc(int(i.starrate), int(i.lbeds), float(i.diver), int(i.ownership), int(i.model), shp_path)
        raise web.seeother('/')

class update:
    def POST(self):
        i = web.input()
        import json, decimal
        data_dict = json.loads(i.u)
        p1 = data_dict['0']
        p2 = data_dict['1']
        v1 = []
        v2 = []
        for p in range(9):
            v1.append(float(p1[str(p)]))
        for p in range(3):
            v2.append(float(p2[str(p)]))
        session.param = [v1, v2]
        return [v1, v2]
    def GET(self):
        return "working!"


class test:
    def GET(self):
        import urllib
        i = web.input()
        args = {}
        for p in i:
            args[p] = i[p]
        return urllib.urlencode(args)

class wms:
    def GET(self):
        import urllib
        i = web.input()
        args = {}
        for p in i:
            args[p] = i[p]
        args_url = urllib.urlencode(args)
        #copy map if not exists!
        title = session.uuid
        #create isolated files in session
        src_path = mapdir
        dst_path = os.path.join(mapdir, session.uuid)
        out_map_path = os.path.join(dst_path, 'template.map')
        if not os.path.exists(os.path.join(mapdir, session.uuid)):
            os.mkdir(os.path.join(mapdir, session.uuid))
            src_files = filter(lambda p: str.startswith(p, 'grid_final_in4') or p == "stat.txt", os.listdir(mapdir))
            src_files_path = map(os.path.join, [src_path]*len(src_files), src_files)
            dst_files_path = map(os.path.join, [dst_path]*len(src_files), src_files)
            map(shutil.copyfile, src_files_path, dst_files_path)
            #Set session based path for mapfile
            tpl_in = open(os.path.join(mapdir, 'template.map.tpl'))
            map_tpl = Template(tpl_in.read())
            out_map = open(out_map_path, 'w')
            out_map.write(map_tpl.safe_substitute(layerpath=os.path.join(dst_path, 'grid_final_in4'), mappath=out_map_path))
            out_map.close()
            tpl_in.close()
        #end copy map
        url = "http://www.hotel-location.net/cgi-bin/mapserv.exe?map=%s&%s" % (out_map_path, args_url)
        raise web.seeother(url)
    
class report:
    def POST(self):
        import back_logic

    
#########################  MAIN FUNCTION  ################################
urls = (
    '/', 'index',
    '/calculate', 'calculate',
    '/test', 'test',
    '/wms', 'wms',
    '/update', 'update',
    '/report', 'report'
    )

#Code Base
basedir = os.path.join(os.path.abspath('.'), 'var', 'www', 'HotelDemo')
#Map Base
mapdir = r'/var/www/maps'

#Subject to change
render = web.template.render(os.path.join(basedir, 'templates'))

app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('/tmp/session'), initializer={'uuid': str(uuid.uuid4())})

application = app.wsgifunc()
