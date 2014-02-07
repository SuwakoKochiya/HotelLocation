import sys
import math
import os
import ogr
import subprocess

#from PIL import Image

#from reportlab.pdfgen import *   
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph   
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet

style = getSampleStyleSheet()

def Exp(a):
    return math.exp(a)

class ModelParam:

    @staticmethod
    def getValue():

        #Hidden values for models
        a1=-58.38081
        a2=-55.07013
        a3=-52.56859

        c1=-53.26554
        c2=-48.70081
        c3=-46.27486

        d1=-49.41376
        d2=-45.95775
        d3=-43.55159

        e1=-79.59153
        e2=-76.4331
        e3=-73.18526

        f1=-59.55085
        f2=-56.36094
        f3=-53.8378

        g1=-84.62192
        g2=-78.51311
        g3=-75.62783

        #Tunable values.
        ##[star,    -beds,      -diver,     -own,       -agglo,     rest,       -road,      subway,     -tour]
        A=[-0.302,  0.119,      0.0165,     0.590,      0.0691,     0.0156,     5.129,      0.2289,     0.571]
        C=[0,       -0.484,     0.00185,    0.788,      0.0436,     0.00544,    5.391,      0.655,      0.969]
        D=[0,       -0.265,     0.00149,    0.333,      0.0842,     0.000131,   4.346,      0.0414,     0.616]
        E=[0,       0.347,      0.0229,     0.329,      0.102,      0.0412,     6.952,      0.187,      0.469]
        F=[-0.425,  0.0251,     0.0169,     0,          0.0718,     0.0227,     5.344,      0.287,      0.517]
        G=[0.555,   0.553,      0.0245,     0,          0.00464,    0.0246,     8.955,      0.0814,     1.623]
        H=[2.621,   0,          0.0956,     7.935,      0,          0.171,      0,          0,          0]
        I=[-0.0217, 0.161,      -0.00115,   0.0795,     0,          0.00168,    -0.0507,    0,          0]
        J=[-0.0768, 0.178,      0,          0.0672,     -0.001,     0,          0,          0,          0]
        K=[119.9585,47.05214,   0,          0,          0,          1.937791,   -19.30494,  4.223994,   0]
        L=[4.2707,  1.134279,   0,          0,          0,          0.0883901,  1.044334,   1.216865,   0]
        M=[1.325925,-1.945994,  0,          0,          0,          0.1289801,  -7.614233,  1.203429,   0]
        return {
            0: [A, [a1, a2, a3]],
            1: {1: [E, [e1, e2, e3]],
                2: [E, [e1, e2, e3]],
                3: [D, [d1, d2, d3]],
                4: [C, [c1, c2, c3]],
                5: [C, [c1, c2, c3]]},
            2: {0: [G, [g1, g2, g3]],
                1: [F, [f1, f2, f3]]},            
            3: [H , [0, 0, 0]],
            4: [I , [0, 0, 0]],
            5: [J , [0, 0, 0]],
            6: [K , [0, 0, 0]],
            7: [L , [0, 0, 0]],
            8: [M , [0, 0, 0]]
        }



class Worker:

    def __init__(self, session=None):
        self.session = session
        try:
            self.param = session.param
        except:
            self.param = None

    def Calc(self, Starrate, lbeds, Diver, Ownership, Mode, Shp, f_rd = 1.0, f_subway=1.0):

        M_Constant = [0, 0, 0, 11.24, 0.96, 1.658, -158.2849, 8.775509, -17.11421]
        Stat = [0,0,0,0,0]

        def func1(HuanXian, A, a1, a2, a3):
            if HuanXian <= 1 :
                Presult = Exp(a1 - A) / (1 + Exp(a1- A))
            elif HuanXian > 1 and HuanXian <= 2 :
                Presult = Exp(a2 - A) / (1 + Exp(a2 - A)) - Exp(a1 - A) / (1 + Exp(a1 - A))
            elif HuanXian > 2 and HuanXian <= 3 :
                Presult = Exp(a3 - A) / (1 + Exp(a3 - A)) - Exp(a2 - A) / (1 + Exp(a2- A))
            elif HuanXian > 3 and HuanXian <= 4 :
                Presult = 1 - (Exp(a3 - A) / (1 + Exp(a3 - A)))
            return Presult

        #def func2
        func2 = lambda P: P[0] * Starrate - P[1] * lbeds - P[2] * Diver - P[3] * Ownership - P[4] * Agglomeration + P[5] * restaurant - P[6] * Lnroad * f_rd + P[7] * subway * f_subway - P[8] * Tourism

        #Map variables
        InputFeatureFile = Shp
        featset = ogr.Open(InputFeatureFile, True)
        layer = featset.GetLayer(0)
        defn = layer.GetLayerDefn()
        fdefn = [defn.GetFieldDefn(i) for i in range(defn.GetFieldCount())]
        fnames = [p.GetName() for p in fdefn]
        TourismFieldIndex = fnames.index("C_4K_jd")
        AgglomerationFieldIndex = fnames.index("C_5K_hotel")
        LnroadFieldIndex = fnames.index("road")
        HXFieldIndex = fnames.index("huanxian")
        SubwayFieldIndex = fnames.index("Subway")
        RestaurantFieldIndex = fnames.index("Restaurant")

        temp_result = []

        for p in range(layer.GetFeatureCount()):
            feat = layer.GetFeature(p)

            HuanXian = feat.GetField(HXFieldIndex)
            Agglomeration = feat.GetField(AgglomerationFieldIndex)
            Lnroad = feat.GetField(LnroadFieldIndex)
            Tourism = feat.GetField(TourismFieldIndex)
            restaurant = feat.GetField(RestaurantFieldIndex)
            subway = feat.GetField(SubwayFieldIndex)

            if Mode is None:
                #Test Mode
                Presult = feat.GetField('mymymy')
                sys.stdout.write(str(Presult))
            else:
                #These codes need be totally refactored!
                if self.param and Mode <= 2:
                    Z = self.param[0]
                    z1, z2, z3 = self.param[1];
                    Presult = func1(HuanXian, func2(Z), z1, z2, z3)
                elif self.param and Mode > 2:
                    Z = self.param[0]
                    Presult = func2(Z)
                    Presult += M_Constant[Mode]
                    pass
                else:
                    raise ValueError("Parameters Uninitialized!")
                #elif Mode == 0:
                    #A =[-0.302,0.119,0.0165,0.590,0.0691,0.0156,5.129,0.2289,0.571]
                    #a1=-58.38081
                    #a2=-55.07013
                    #a3=-52.56859
                    #Presult = func1(HuanXian, func2(A), a1, a2, a3)
                #elif Mode == 1:
                    #if Starrate >= 4:
                        #C = 0.484 * lbeds - 0.00185 * Diver  - 0.788 * Ownership - 0.0436 * Agglomeration + 0.00544 * restaurant - 5.391 * Lnroad + 0.655 * subway - 0.969 * Tourism
                        #c1=-53.26554
                        #c2=-48.70081
                        #c3=-46.27486
                        #Presult = func1(HuanXian, C, c1, c2, c3)
                    #elif Starrate == 3:
                        #D = 0.265 * lbeds - 0.00149 * Diver  + 0.333 * Ownership - 0.0842 * Agglomeration + 0.000131 * restaurant - 4.346 * Lnroad + 0.0414 * subway - 0.616 * Tourism
                        #d1=-49.41376
                        #d2=-45.95775
                        #d3=-43.55159
                        #Presult = func1(HuanXian, D, d1, d2, d3)
                    #else:
                        #E = -0.347 * lbeds - 0.0229 * Diver  - 0.329 * Ownership - 0.102 * Agglomeration + 0.0412 * restaurant - 6.952 * Lnroad + 0.187 * subway - 0.469 * Tourism
                        #e1=-79.59153
                        #e2=-76.4331
                        #e3=-73.18526
                        #Presult = func1(HuanXian, E, e1, e2, e3)
                    #pass
                #elif Mode == 2:
                    #if Ownership == 1:
                        #F = -0.425 * Starrate -0.0251 * lbeds - 0.0169 * Diver - 0.0718 * Agglomeration + 0.0227 * restaurant - 5.344 * Lnroad + 0.287 * subway - 0.517 * Tourism
                        #f1=-59.55085
                        #f2=-56.36094
                        #f3=-53.8378
                        #Presult = func1(HuanXian, F, f1, f2, f3)
                    #else:
                        #G = 0.555 * Starrate -0.553 * lbeds - 0.0245 * Diver  - 0.00464 * Agglomeration - 0.0246 * restaurant - 8.955 * Lnroad + 0.0814 * subway - 1.623 * Tourism
                        #g1=-84.62192
                        #g2=-78.51311
                        #g3=-75.62783
                        #Presult = func1(HuanXian, G, g1, g2, g3)
                    #pass
                #elif Mode == 3:
                    #Presult = 11.24 + 2.621 * Starrate - 0.0956 * Diver - 7.935 * Ownership + 0.171 * restaurant
                    #pass
                #elif Mode == 4:
                    #Presult = 0.960 - 0.0217 * Starrate - 0.161 * lbeds + 0.00115 * Diver - 0.0795 * Ownership + 0.00168 * restaurant + 0.0507 * Lnroad
                    #pass
                #elif Mode == 5:
                    #Presult = 1.658 - 0.0768 * Starrate - 0.178 * lbeds - 0.0672 * Ownership + 0.001 * Agglomeration
                    #pass
                #elif Mode == 6:
                    #Presult = 119.9585 * Starrate - 47.05214 * lbeds + 1.937791 * restaurant + 19.30494 * Lnroad + 4.223994 * subway - 158.2849                    
                    #pass
                #elif Mode == 7:
                    #Presult = 4.2707 * Starrate - 1.134279 * lbeds + 0.0883901 * restaurant - 1.044334 * Lnroad + 1.216865 * subway + 8.775509
                    #pass
                #elif Mode == 8:
                    #Presult = 1.325925 * Starrate + 1.945994 * lbeds + 0.1289801 * restaurant + 7.614233 * Lnroad + 1.203429 * subway - 17.11421
                    #pass
                #else:
                    #raise Exception('Invalid Mode!')                    
                temp_result.append(Presult)

        for q in range(layer.GetFeatureCount()):
            feat = layer.GetFeature(q)
            Presult2 = (temp_result[q] - min(temp_result)) / (max(temp_result) - min(temp_result))
            feat.SetField('mymymy', Presult2)
            layer.SetFeature(feat)
            try:
                Stat[int(Presult2 / 0.2)] += 1
            except IndexError:
                Stat[-1] += 1

        featset.Destroy()

        stat = open(os.path.join(os.path.dirname(Shp), 'stat.txt'), 'w')
        stat.write(str(Stat))
        stat.close()

        return Stat

    def Calc2(self, Starrate, lbeds, Diver, Ownership, Mode, Shp):
        return self.Calc(Starrate, lbeds, Diver, Ownership, Mode, Shp, f_rd=1.05)

    def Calc3(self, Starrate, lbeds, Diver, Ownership, Mode, Shp):
        return self.Calc(Starrate, lbeds, Diver, Ownership, Mode, Shp, f_subway=1.05)

    def Report(self, Starrate, lbeds, Diver, Ownership, Mode, Shp):

        def cgi_wrapper(working_dir, img_path):
            pars="QUERY_STRING=MAP=template.map&TRANSPARENT=True&CRS=EPSG:32650&FORMAT=image/png&SRS=EPSG:32650&MODE=map&MAPSIZE=600 600&LAYERS=Road_region_shp grid_final_in4"
            args = ['/usr/bin/mapserv', '-nh', pars]
            proc = subprocess.Popen(args, stdout=subprocess.PIPE, cwd=working_dir)
            out,err = proc.communicate()
            img = open(os.path.join(working_dir, img_path), "wb")
            img.write(out)
            img.close()
            return os.path.join(working_dir, img_path)

        working_dir = os.path.dirname(Shp)
        #Base map
        self.Calc(Starrate, lbeds, Diver, Ownership, Mode, Shp)
        image0 = cgi_wrapper(working_dir, "img0.png")        
        #road + 5%        
        self.Calc2(Starrate, lbeds, Diver, Ownership, Mode, Shp)
        image1 = cgi_wrapper(working_dir, "img1.png")
        #subway + 5%
        self.Calc3(Starrate, lbeds, Diver, Ownership, Mode, Shp)
        image2 = cgi_wrapper(working_dir, "img2.png")
        #Symbol filter        
        symbol = "/var/www/HotelDemo/static/image/legend.png"
        #Create pdf report file
        pdffile = os.path.join(working_dir, 'report.pdf')
        parts = []
        if os.path.exists(pdffile): 
            os.remove(pdffile)
        mydoc = SimpleDocTemplate(pdffile, pagesize=letter)
        parts.append(Paragraph("Oringal model", style["Normal"]))
        parts.append(Image(image0))
        parts.append(Paragraph("Road factor +5%", style["Normal"]))
        parts.append(Image(image1))
        parts.append(Paragraph("Subway station factor +5%", style["Normal"]))
        parts.append(Image(image2))  
        parts.append(Paragraph("Legend", style["Normal"]))
        parts.append(Image(symbol))
        mydoc.build(parts)